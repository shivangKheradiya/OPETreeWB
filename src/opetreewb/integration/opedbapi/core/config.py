from typing import Optional


class OpeDBConfig:
    """
    Static configuration for OPE DB integration.

    Stores:
    - API base URL
    - operation mode (api / local)
    - optional settings (timeout, etc.)
    """

    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        mode: str = "api",
        timeout: int = 60,
    ):
        self._base_url = base_url
        self._mode = mode.lower()
        self._timeout = timeout

    # -------------------------------------------------
    # GETTERS
    # -------------------------------------------------
    @property
    def base_url(self) -> str:
        if not self._base_url:
            raise RuntimeError("Base URL is not configured")
        return self._base_url

    @property
    def mode(self) -> str:
        return self._mode

    @property
    def timeout(self) -> int:
        return self._timeout

    # -------------------------------------------------
    # MODE CHECKS
    # -------------------------------------------------
    @property
    def is_api_mode(self) -> bool:
        return self._mode == "api"

    @property
    def is_local_mode(self) -> bool:
        return self._mode == "local"


# ✅ GLOBAL CONFIG INSTANCE
OPE_DB_CONFIG = OpeDBConfig()