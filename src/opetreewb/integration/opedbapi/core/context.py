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
        self._api_url: Optional[str] = None
        self._mode = "api"
        self._timeout = 60

    # -------------------------------------------------
    # SESSION CONTROL
    # -------------------------------------------------
    def start_session(self, session_id: int):
        self._session_id = session_id

    def close_session(self):
        self._session_id = None

    # -------------------------------------------------
    # GETTERS / SETTERS
    # -------------------------------------------------
    @property
    def code(self) -> str:
        if not self._code:
            raise RuntimeError("Context not configured (code missing)")
        return self._code

    @code.setter
    def code(self, value: str):
        self._code = value

    @property
    def domain(self) -> str:
        if not self._domain:
            raise RuntimeError("Context not configured (domain missing)")
        return self._domain

    @domain.setter
    def domain(self, value: str):
        self._domain = value

    @property
    def session_id(self) -> int:
        if self._session_id is None:
            raise RuntimeError("No active session")
        return self._session_id

    @session_id.setter
    def session_id(self, value: int):
        self._session_id = value

    @property
    def username(self) -> Optional[str]:
        return self._username

    @username.setter
    def username(self, value: str):
        self._username = value

    @property
    def hostname(self) -> str:
        return self._hostname

    @hostname.setter
    def hostname(self, value: str):
        self._hostname = value

    @property
    def is_session_active(self) -> bool:
        return self._session_id is not None

    @property
    def api_url(self) -> str:
        if not self._api_url:
            raise RuntimeError("Base URL is not configured")
        return self._api_url

    @api_url.setter
    def api_url(self, value: str):
        self._api_url = value

    @property
    def mode(self) -> str:
        return self._mode

    @mode.setter
    def mode(self, value: str):
        self._mode = value

    @property
    def timeout(self) -> int:
        return self._timeout

    @timeout.setter
    def timeout(self, value: int):
        self._timeout = value

    # -------------------------------------------------
    # MODE CHECKS
    # -------------------------------------------------
    @property
    def is_api_mode(self) -> bool:
        return self._mode == "api"

    @property
    def is_local_mode(self) -> bool:
        return self._mode == "local"