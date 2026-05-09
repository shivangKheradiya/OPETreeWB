from sqlalchemy import select
from typing import Dict, Any, List

from opetreewb.integration.opedbapi.local.client import LocalClient
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT
from OPE_DB_API.schemas.search import SearchRequest
from OPE_DB_API.crud.search.executor import execute_search

from sqlalchemy.inspection import inspect




class QueryLocal:
    """
    Local DB query layer.

    Provides:
    - working state (overlay ⊕ live)
    - search by node_id
    """

    def __init__(self):
        self.client = LocalClient()

    # -------------------------------------------------
    # SEARCH (WORKING MODE ONLY FOR NOW)
    # -------------------------------------------------
    def search(
        self,
        *,
        filter_dict: Dict[str, Any],
        mode: str = "working",
        limit: int = 1000,
        offset: int = 0,
    )-> Dict:
        db = self.client.get_session()

        try:
            session_id = OPE_DB_CONTEXT.session_id
            domain = OPE_DB_CONTEXT.domain.upper()

            # ✅ Create SearchRequest object
            search_request = SearchRequest(
                mode=mode,
                filter=filter_dict,
                limit=limit,
                offset=offset,
            )

            result = execute_search(
                db,
                domain=domain,
                session_id=session_id,
                search=search_request,
            )

            result["items"] = [self._serialize_row(row) for row in result["items"]]

            return result
        
        finally:
            db.close()

    def _serialize_row(self, row):
        return {
            c.key: getattr(row, c.key)
            for c in inspect(row).mapper.column_attrs
        }
