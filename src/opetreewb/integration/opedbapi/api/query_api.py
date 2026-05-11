from datetime import datetime
from typing import Dict, Any, List

from opetreewb.integration.opedbapi.api.client import OpeApiClient
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT
from opetreewb.SKET.schema.attribute_ids import get_attr_id

class QueryAPI:
    """
    Handles read operations via API:
    - search
    - load node
    - snapshot
    - history
    """

    def __init__(self):
        self.client = OpeApiClient()

    # -------------------------------------------------
    # GENERIC SEARCH
    # -------------------------------------------------
    def search(
        self,
        *,
        filter_dict: Dict[str, Any],
        mode: str = "working",
        limit: int = 1000,
        offset: int = 0,
    ) -> Dict:
        """
        Generic search API.
        """

        if not OPE_DB_CONTEXT.is_session_active:
            raise RuntimeError("No active session")

        response = self.client.post(
            "search",
            json={
                "mode": mode,
                "filter": filter_dict,
                "limit": limit,
                "offset": offset,
            },
            use_session=True,
        )

        return response

    # -------------------------------------------------
    # LOAD NODE (FULL ATTRIBUTES)
    # -------------------------------------------------
    def load_node(self, node_id: int) -> Dict:
        """
        Fetch all attributes of a node.
        """

        response = self.search(
            filter_dict={
                "field": "node_id",
                "op": "=",
                "value": node_id,
            }
        )

        return response

    # -------------------------------------------------
    # LOAD NODE METADATA (LIGHTWEIGHT)
    # -------------------------------------------------
    def load_node_meta(self, node_id: int) -> Dict:
        """
        Fetch minimal data for tree display:
        - name
        - type
        """

        response = self.load_node(node_id)

        items = response.get("items", [])

        name = None
        type_value = None

        # NOTE: attribute IDs resolved externally (later via registry)
        for row in items:
            attr_id = row.get("attribute_id")

            # temporary fallback — will be replaced by registry mapping
            if attr_id == 1:  # Name (placeholder)
                name = row.get("value")
            elif attr_id == 2:  # Type (placeholder)
                type_value = row.get("value")

        return {
            "id": node_id,
            "name": name,
            "type": type_value,
        }

    # -------------------------------------------------
    # FIND CHILDREN (OWNER RELATION)
    # -------------------------------------------------
    def find_children(
        self,
        *,
        owner_attribute_id: int,
        parent_node_id: int,
    ) -> List[int]:
        """
        Find children nodes using OWNER relationship.
        """

        response = self.search(
            filter_dict={
                "field": "attribute_id",
                "op": "=",
                "value": owner_attribute_id,
            }
        )

        items = response.get("items", [])

        return [
            row["node_id"]
            for row in items
            if row["value"] == parent_node_id
        ]

    # -------------------------------------------------
    # SNAPSHOT (TREE RECONSTRUCTION)
    # -------------------------------------------------
    def fetch_snapshot(
        self,
        *,
        root_node_id: int,
        owner_attribute_id: int,
    ) -> List[Dict]:
        """
        Fetch full subtree snapshot from server.
        """

        response = self.client.get(
            "sync/snapshot",
            params={
                "root_node_id": root_node_id,
                "owner_attribute_id": owner_attribute_id,
            },
            use_session=True,
        )

        return response

    # -------------------------------------------------
    # HISTORY (SYNC LATER)
    # -------------------------------------------------
    def fetch_history(
        self,
        *,
        after_ts: datetime,
        limit: int = 5000,
    ) -> List[Dict]:
        """
        Fetch committed history rows.
        """

        response = self.client.get(
            "sync/history",
            params={
                "after_ts": after_ts.isoformat(),
                "limit": limit,
            },
            use_session=True,
        )

        return response

    def fetch_root_node_ids(self):
        result = self.client.post(
            "search",
            json={
                "mode": "live",
                "filter": {
                    "and": [
                        {"field": "attribute_id", "op": "=", "value": get_attr_id("Owner")},  # Owner
                        {"field": "value", "op": "=", "value": "0"},      # ROOT
                    ]
                },
                "limit": 10000,
                "offset": 0,
            },
            use_session=True,
        )
    
        return list({row["node_id"] for row in result.get("items", [])})
    
    def fetch_nodes_by_ids(self, node_ids):
        return self.client.post(
            "search",
            json={
                "mode": "live",
                "filter": {
                    "field": "node_id",
                    "op": "in",
                    "value": node_ids,
                },
                "limit": 10000,
                "offset": 0,
            },
            use_session=True,
        )
    
    def fetch_root_nodes(self):
        node_ids = self.fetch_root_node_ids()
        if not node_ids:
            return {"items": []}

        return self.fetch_nodes_by_ids(node_ids)
    