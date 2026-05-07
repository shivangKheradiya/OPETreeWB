from typing import Optional
import socket


class OpeDBContext:
    """
    Shared runtime context for OPE DB integration.

    This holds:
    - active session_id
    - project code
    - domain (SKET, DRAW, etc.)
    - user identity

    This is used by both:
    - API provider
    - Local DB provider
    """

    def __init__(self):
        self._code: Optional[str] = None
        self._domain: Optional[str] = None
        self._session_id: Optional[int] = None

        self._username: Optional[str] = None
        self._hostname: Optional[str] = socket.gethostname()

    # -------------------------------------------------
    # SETUP
    # -------------------------------------------------
    def configure(self, *, code: str, domain: str, username: Optional[str] = None, hostname:str):

        self._code = code.upper()
        self._domain = domain
        self._username = username
        self._hostname = hostname

    # -------------------------------------------------
    # SESSION CONTROL
    # -------------------------------------------------
    def start_session(self, session_id: int):
        self._session_id = session_id

    def close_session(self):
        self._session_id = None

    # -------------------------------------------------
    # GETTERS
    # -------------------------------------------------
    @property
    def code(self) -> str:
        if not self._code:
            raise RuntimeError("Context not configured (code missing)")
        return self._code

    @property
    def domain(self) -> str:
        if not self._domain:
            raise RuntimeError("Context not configured (domain missing)")
        return self._domain

    @property
    def session_id(self) -> int:
        if self._session_id is None:
            raise RuntimeError("No active session")
        return self._session_id

    @property
    def username(self) -> Optional[str]:
        return self._username

    @property
    def hostname(self) -> str:
        return self._hostname

    @property
    def is_session_active(self) -> bool:
        return self._session_id is not None


# ✅ GLOBAL INSTANCE (VERY IMPORTANT)
OPE_DB_CONTEXT = OpeDBContext()
