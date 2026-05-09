import requests
from typing import Optional, Dict, Any

from opetreewb.integration.opedbapi.core.config import OPE_DB_CONFIG
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT


class OpeApiClient:
    """
    Low-level HTTP client for OPE_DB_API.

    Responsibilities:
    - Build URLs
    - Send HTTP requests
    - Attach session_id automatically
    - Handle errors consistently
    """

    # -------------------------------------------------
    # INTERNAL: URL BUILDING
    # -------------------------------------------------
    def _base_url(self) -> str:
        return OPE_DB_CONFIG.base_url.rstrip("/")

    def _prefix(self) -> str:
        return f"{self._base_url()}/{OPE_DB_CONTEXT.code}/{OPE_DB_CONTEXT.domain}"

    def _session_prefix(self) -> str:
        return f"{self._prefix()}/{OPE_DB_CONTEXT.session_id}"

    # -------------------------------------------------
    # HTTP METHODS
    # -------------------------------------------------
    def get(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        use_session: bool = False,
    ):
        url = self._build_url(path, use_session)

        response = requests.get(
            url,
            params=params,
            timeout=OPE_DB_CONFIG.timeout,
        )

        self._handle_response(response)

        return response.json()

    def post(
        self,
        path: str,
        *,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        use_session: bool = False,
    ):
        url = self._build_url(path, use_session)

        response = requests.post(
            url,
            json=json,
            params=params,
            timeout=OPE_DB_CONFIG.timeout,
        )

        self._handle_response(response)

        if response.content:
            return response.json()

        return None

    # -------------------------------------------------
    # URL BUILDER
    # -------------------------------------------------
    def _build_url(self, path: str, use_session: bool) -> str:

        if use_session:
            base = self._session_prefix()
        else:
            base = self._prefix()

        # normalize path
        path = path.lstrip("/")

        return f"{base}/{path}"

    # -------------------------------------------------
    # ERROR HANDLING
    # -------------------------------------------------
    def _handle_response(self, response):

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise RuntimeError(
                f"OPE_API_ERROR: {response.status_code} → {response.text}"
            ) from e
