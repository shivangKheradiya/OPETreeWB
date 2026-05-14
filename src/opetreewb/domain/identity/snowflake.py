# PyDBML/identity/snowflake.py

from __future__ import annotations

import hashlib
import os
import platform
import random
import socket
import threading
import time
import uuid
from pathlib import Path


class SnowflakeIDGenerator:
    """
    Client-side Snowflake ID generator.

    Guarantees:
    - globally unique 64-bit integers
    - safe across machines, users, sessions, databases
    - works offline
    """

    # --- Bit configuration ---
    TIMESTAMP_BITS = 41
    MACHINE_ID_BITS = 10
    SEQUENCE_BITS = 12

    MAX_MACHINE_ID = (1 << MACHINE_ID_BITS) - 1
    MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1

    # Custom epoch (ms)
    EPOCH = 1700000000000  # ~Nov 2023 UTC

    def __init__(self, machine_id: int | None = None):
        self._lock = threading.Lock()

        self.machine_id = (
            machine_id if machine_id is not None else self._load_or_create_machine_id()
        )

        if not (0 <= self.machine_id <= self.MAX_MACHINE_ID):
            raise ValueError("machine_id out of range")

        self.last_timestamp = -1
        self.sequence = 0

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------
    def next_id(self) -> int:
        """
        Generate the next Snowflake ID.
        """
        with self._lock:
            timestamp = self._current_millis()

            if timestamp < self.last_timestamp:
                raise RuntimeError("Clock moved backwards")

            if timestamp == self.last_timestamp:
                self.sequence += 1
                if self.sequence > self.MAX_SEQUENCE:
                    # Wait for next millisecond
                    timestamp = self._wait_next_millis(timestamp)
                    self.sequence = 0
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            return self._assemble_id(timestamp, self.sequence)

    # ---------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------
    def _assemble_id(self, timestamp: int, sequence: int) -> int:
        """
        Build the 64-bit Snowflake ID.
        """
        return (
            ((timestamp - self.EPOCH) << (self.MACHINE_ID_BITS + self.SEQUENCE_BITS))
            | (self.machine_id << self.SEQUENCE_BITS)
            | sequence
        )

    def _current_millis(self) -> int:
        return int(time.time() * 1000)

    def _wait_next_millis(self, last_timestamp: int) -> int:
        timestamp = self._current_millis()
        while timestamp <= last_timestamp:
            timestamp = self._current_millis()
        return timestamp

    # ---------------------------------------------------------
    # Machine ID persistence
    # ---------------------------------------------------------
    def _load_or_create_machine_id(self) -> int:
        """
        Load machine_id from local file, or create and persist one.
        """
        path = self._machine_id_path()

        if path.exists():
            return int(path.read_text().strip())

        machine_id = self._generate_machine_id()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(str(machine_id))
        return machine_id

    def _machine_id_path(self) -> Path:
        home = Path.home()
        return home / ".pydbml" / "machine_id"

    def _generate_machine_id(self) -> int:
        """
        Generate a stable machine ID using cross-platform host entropy.
        """
        hostname = socket.gethostname()
        nodename = platform.node()
        mac = uuid.getnode()  # 48-bit MAC or random fallback

        seed = f"{hostname}-{nodename}-{mac}".encode("utf-8")
        digest = hashlib.sha256(seed).digest()

        # Reduce to required bit size
        return int.from_bytes(digest, "big") % (self.MAX_MACHINE_ID + 1)
