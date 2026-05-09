import time
from typing import Optional

from opetreewb.integration.opedbapi.api.client import OpeApiClient
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT, ID_GENERATOR

class SessionAPI:
    """
    Handles session lifecycle via API.
    """

    def __init__(self):
        self.client = OpeApiClient()

    # -------------------------------------------------
    # START SESSION
    # -------------------------------------------------
    def start(
        self
    ) -> int:
        """
        Start a new session via API.
        """

        if OPE_DB_CONTEXT.is_session_active:
            return OPE_DB_CONTEXT.session_id

        # ✅ Generate session_id (as required by API)
        session_id = ID_GENERATOR.next_id()

        params = {
            "session_id": session_id,
        }

        if OPE_DB_CONTEXT.username:
            params["username"] = OPE_DB_CONTEXT.username

        if OPE_DB_CONTEXT.hostname:
            params["hostname"] = OPE_DB_CONTEXT.hostname

        # ✅ API call
        self.client.post(
            "session/start",
            params=params,
            use_session=False,  # session not yet created
        )

        # ✅ Store in context
        OPE_DB_CONTEXT.start_session(session_id)

        return session_id

    # -------------------------------------------------
    # CLOSE SESSION
    # -------------------------------------------------
    def close(self):
        """
        Close current session via API.
        """

        if not OPE_DB_CONTEXT.is_session_active:
            return

        session_id = OPE_DB_CONTEXT.session_id

        # ✅ API call
        self.client.post(
            f"session/{session_id}/close",
            use_session=False,
        )

        # ✅ Clear context
        OPE_DB_CONTEXT.close_session()

    # -------------------------------------------------
    # GET ACTIVE SESSION (OPTIONAL)
    # -------------------------------------------------
    def get_active(self):
        """
        Fetch active session from API.
        """

        return self.client.get(
            "session/active",
            params={
                "username": OPE_DB_CONTEXT.username,
                "hostname": OPE_DB_CONTEXT.hostname,
            },
            use_session=False,
        )
