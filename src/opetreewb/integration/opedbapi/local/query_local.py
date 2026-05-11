from sqlalchemy import select
from typing import Dict, Any, List

from opetreewb.integration.opedbapi.local.client import LocalClient
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT
from OPE_DB_API.schemas.search import SearchRequest
from OPE_DB_API.crud.search.executor import execute_search

from sqlalchemy.inspection import inspect
from opetreewb.SKET.schema.attribute_ids import get_attr_id

from collections import defaultdict
from opetreewb.ui.utils.node_mapper import node_dict_to_model


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

    def get_root_nodes(self):
        result = self.search(
            filter_dict={
                    "and": [
                        {"field": "attribute_id", "op": "=", "value": get_attr_id("Owner")},  # Owner
                        {"field": "value", "op": "=", "value": "0"},      # ROOT
                    ]
                },
            mode="live",
        )
        
        items = result.get("items", [])
        if not items:
            return []

        node_ids = list({row["node_id"] for row in items})

        # ✅ Step 2: fetch all rows for nodes
        result = self.search(
            filter_dict={
                "field": "node_id",
                "op": "in",
                "value": node_ids,
            },
            mode="working",
        )

        rows = result.get("items", [])

        # ✅ Step 3: convert to TreeNodeModel
        return self._rows_to_nodes(rows)

    def _rows_to_nodes(self, rows):

        grouped = defaultdict(list)

        for r in rows:
            grouped[r["node_id"]].append(r)

        nodes = []
        for node_id, node_rows in grouped.items():
            node_dict = {
                "node_id": node_id,
                "attributes": {
                    r["attribute_id"]: {
                        "data_id": r["data_id"],
                        "value": r["value"],
                    }
                    for r in node_rows
                }
            }

            node = node_dict_to_model(node_dict)
            nodes.append(node)

        return nodes
    
    def get_children(self, parent_node_id):
        # ✅ Step 1 → find children (Owner = parent_node_id)
        result = self.search(
            filter_dict={
                "and": [
                    {
                        "field": "attribute_id",
                        "op": "=",
                        "value": get_attr_id("Owner"),
                    },
                    {
                        "field": "value",
                        "op": "=",
                        "value": parent_node_id,
                    },
                ]
            },
            mode="working",
        )

        items = result.get("items", [])

        if not items:
            return []

        # ✅ Step 2 → extract child node_ids
        node_ids = list({row["node_id"] for row in items})

        # ✅ Step 3 → fetch all attributes for those nodes
        result = self.search(
            filter_dict={
                "field": "node_id",
                "op": "in",
                "value": node_ids,
            },
            mode="working",
        )

        rows = result.get("items", [])

        return self._rows_to_nodes(rows)