# core/data_access.py

from OPE_DB_API.db.session import get_client_db_session
from OPE_DB_API.registry.tables import LIVE_TABLE_REGISTRY
from OPETreeWB.core.domain_rules import DOMAIN_RULES


class OPEDataAccess:
    """
    Local-first data access layer.

    Rules:
    - Read local DB first
    - If missing, fetch via PyDBML Search API
    - Persist results locally
    """

    def __init__(self, provider):
        self.provider = provider
        self.code = provider.code
        self.domain = provider.domain
        self.registry = provider.registry

    # -----------------------------
    # ROOT LEVEL
    # -----------------------------

    def ensure_root_nodes_loaded(self):
        if self._has_root_nodes_local():
            return

        root_type = DOMAIN_RULES[self.domain]["RootType"]
        type_attr = self.registry.get_id("Type")
        owner_attr = self.registry.get_id("Owner")

        # 1️⃣ Fetch ALL nodes with this root type
        type_rows = self.provider.search_by_attribute(
            attribute_id=type_attr,
            value=root_type,
        )

        # 2️⃣ Fetch ALL owner attribute rows ONCE
        owner_rows = self.provider.search_by_attribute(
            attribute_id=owner_attr,
            value=None,  # fetch all Owner attrs (value filtered locally)
        )

        # 3️⃣ Compute ownership locally
        owned_nodes = {
            r["node_id"]
            for r in owner_rows
            if r["value"] not in (None, 0)
        }

        # 4️⃣ Roots = type nodes without Owner attribute
        root_node_ids = [
            r["node_id"]
            for r in type_rows
            if r["node_id"] not in owned_nodes
        ]

        self._persist_root_nodes(type_rows, root_node_ids)


    def _has_root_nodes_local(self) -> bool:
        owner_attr = self.registry.get_id("Owner")

        with get_client_db_session(self.code) as db:
            model = LIVE_TABLE_REGISTRY[self.domain]

            all_nodes = {
                r[0] for r in db.query(model.node_id).distinct().all()
            }
            if not all_nodes:
                return False

            owned_nodes = {
                r.node_id
                for r in db.query(model)
                .filter(model.attribute_id == owner_attr)
                .all()
                if r.value not in (None, 0)
            }

            roots = all_nodes - owned_nodes
            return bool(roots)

    def _persist_root_nodes(self, rows, root_node_ids):
        with get_client_db_session(self.code) as db:
            model = LIVE_TABLE_REGISTRY[self.domain]
            for row in rows:
                if row["node_id"] in root_node_ids:
                    db.merge(model(**row))
            db.commit()

    def get_root_nodes_local(self):
        owner_attr = self.registry.get_id("Owner")

        with get_client_db_session(self.code) as db:
            model = LIVE_TABLE_REGISTRY[self.domain]

            all_nodes = {
                r[0] for r in db.query(model.node_id).distinct().all()
            }

            owned_nodes = {
                r.node_id
                for r in db.query(model)
                .filter(model.attribute_id == owner_attr)
                .all()
                if r.value not in (None, 0)
            }

            root_ids = all_nodes - owned_nodes

            return db.query(model).filter(
                model.node_id.in_(root_ids)
            ).all()

        
    # -----------------------------
    # CHILD LEVEL
    # -----------------------------
    def _has_children_local(self, parent_node_id: int) -> bool:
        owner_attr = self.registry.get_id("Owner")
    
        with get_client_db_session(self.code) as db:
            model = LIVE_TABLE_REGISTRY[self.domain]
    
            return (
                db.query(model)
                .filter(
                    model.attribute_id == owner_attr,
                    model.value == parent_node_id,
                )
                .limit(1)
                .count()
                > 0
            )

    def _fetch_children_from_server(self, parent_node_id: int):
            """
            Fetch immediate children of a node using Search API.
            """
            owner_attr = self.registry.get_id("Owner")

            return self.provider.search_by_attribute(
                attribute_id=owner_attr,
                value=parent_node_id,
            )
    
    def _persist_child_rows(self, rows):
        """
        Persist child rows into local DB.
        """
        with get_client_db_session(self.code) as db:
            model = LIVE_TABLE_REGISTRY[self.domain]
            for row in rows:
                db.merge(model(**row))
            db.commit()

    def ensure_children_loaded(self, parent_node_id: int):
            """
            Ensure immediate children of parent_node_id are present locally.
            """
            if self._has_children_local(parent_node_id):
                return

            rows = self._fetch_children_from_server(parent_node_id)
            self._persist_child_rows(rows)