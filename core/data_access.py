# core/data_access.py

from OPE_DB_API.db.session import get_client_db_session
from OPE_DB_API.registry.tables import LIVE_TABLE_REGISTRY
from OPETreeWB.core.domain_rules import DOMAIN_RULES
from OPE_DB_API.crud.work.read import read_current_work
from sqlalchemy import cast
from sqlalchemy.types import BigInteger

class OPEDataAccess:
    """
    Local-first data access layer.

    Responsibilities (ONLY):
    - Read local DB first
    - Hydrate local DB using Search API (minimum calls)
    - Interpret node/root/child relationships locally

    DOES NOT:
    - Compare with server state
    - Perform sync (history/snapshot)
    """

    def __init__(self, provider):
        self.provider = provider
        self.code = provider.code
        self.domain = provider.domain
        self.registry = provider.registry

    # =========================================================
    # ROOT LEVEL
    # =========================================================

    def ensure_root_nodes_loaded(self) -> None:
        """
        Ensure root nodes are available locally.

        Server calls:
        - 1× search(Type == RootType)
        - 1× search(Owner == ANY)

        No per-node server calls.
        """
        if self._has_root_nodes_local():
            return

        root_type = DOMAIN_RULES[self.domain]["RootType"]
        type_attr = self.registry.get_id("Type")
        owner_attr = self.registry.get_id("Owner")
    
        # 1️⃣ Discover nodes of root type
        type_rows = self.provider.search_by_attribute(
            attribute_id=type_attr,
            value=root_type,
        )
    
        # 2️⃣ Discover all owned nodes
        owner_rows = self.provider.search_by_attribute(
            attribute_id=owner_attr,
            value=None,  # fetch all Owner attributes
        )

        # --- Local interpretation ---

        owned_nodes = {
            r["node_id"]
            for r in owner_rows
            if r["value"] not in (None, 0)
        }
    
        # 3️⃣ Root node IDs
        root_node_ids = {
            r["node_id"]
            for r in type_rows
            if r["node_id"] not in owned_nodes
        }
    
        # ✅ 4️⃣ FULL hydration of root nodes
        self._hydrate_nodes(root_node_ids)

    def _has_root_nodes_local(self) -> bool:
        """
        Return True if at least one root node exists locally.

        Root node = node_id with NO Owner attribute row.
        """
        owner_attr = self.registry.get_id("Owner")

        with get_client_db_session(self.code) as db:
            model = LIVE_TABLE_REGISTRY[self.domain]

            exists = (
                db.query(model.node_id)
                .filter(
                    ~db.query(model)
                    .filter(
                        model.attribute_id == owner_attr,
                        model.node_id == model.node_id,
                    )
                    .exists()
                )
                .limit(1)
                .first()
            )

            return exists is not None

    def get_root_nodes_local(self):
        """
        Fetch root nodes from local DB.
        """
        owner_attr = self.registry.get_id("Owner")

        with get_client_db_session(self.code) as db:
            model = LIVE_TABLE_REGISTRY[self.domain]

            root_ids = [
                r[0]
                for r in db.query(model.node_id)
                .filter(
                    ~db.query(model)
                    .filter(
                        model.attribute_id == owner_attr,
                        model.node_id == model.node_id,
                    )
                    .exists()
                )
                .distinct()
                .all()
            ]

            return db.query(model).filter(
                model.node_id.in_(root_ids)
                ).all()

    # -----------------------------
    # CHILD LEVEL
    # -----------------------------
    def ensure_children_loaded(self, parent_node_id: int) -> None:
        """
        Ensure immediate children of parent_node_id are available locally.

        Server calls:
        - 1× search(Owner == parent_node_id)

        No loops, no extra calls.
        """
        if self._has_children_local(parent_node_id):
            return

        # 1️⃣ Discover child node IDs
        owner_rows = self._fetch_children_from_server(parent_node_id)
        child_node_ids = {row["node_id"] for row in owner_rows}

        # ✅ 2️⃣ FULL hydration of child nodes
        self._hydrate_nodes(child_node_ids)

    def _has_children_local(self, parent_node_id: int) -> bool:
        owner_attr = self.registry.get_id("Owner")

        with get_client_db_session(self.code) as db:
            model = LIVE_TABLE_REGISTRY[self.domain]

            return (
                db.query(model)
                .filter(
                    model.attribute_id == owner_attr,
                    cast(model.value, BigInteger) == parent_node_id,
                )
                .limit(1)
                .count()
                > 0
            )

    def _fetch_children_from_server(self, parent_node_id: int):
        """
        Fetch child nodes from server using ONE search call.
        """
        owner_attr = self.registry.get_id("Owner")

        return self.provider.search_by_attribute(
            attribute_id=owner_attr,
            value=parent_node_id,
        )

    # =========================================================
    # COMMON
    # =========================================================

    def _persist_rows(self, rows) -> None:
        """
        Persist Search API rows into local DB (upsert-safe).
        """
        if not rows:
            return

        with get_client_db_session(self.code) as db:
            model = LIVE_TABLE_REGISTRY[self.domain]
            for row in rows:
                db.merge(model(**row))
            db.commit()

    def _hydrate_nodes(self, node_ids: set[int]) -> None:
        """
        Fully hydrate nodes using load_node(), which is the only
        API that returns complete node data (Type, Name, Owner, etc.).
        """
        if not node_ids:
            return
    
        rows = []
    
        for node_id in node_ids:
            element = self.provider.load_node(node_id)
    
            cached_attrs = self.provider._cache.get(node_id, {})
            for attr_id, (data_id, value) in cached_attrs.items():
                rows.append({
                    "data_id": data_id,
                    "node_id": node_id,
                    "attribute_id": attr_id,
                    "value": value,
                })
    
        self._persist_rows(rows)

    def get_children_local(self, parent_node_id: int):
        owner_attr = self.registry.get_id("Owner")
    
        with get_client_db_session(self.code) as db:
            model = LIVE_TABLE_REGISTRY[self.domain]
    
            return (
                db.query(model)
                .filter(
                    model.attribute_id == owner_attr,
                    cast(model.value, BigInteger) == parent_node_id,
                )
                .all()
            )
        
    def ensure_node_loaded(self, node_id: int) -> None:
        """
        Ensure full attributes for a single node are present locally.
        Local-first:
        - If cached locally → no-op
        - Else → hydrate via provider.load_node()
        """
        if self._has_node_local(node_id):
            return

        self._hydrate_nodes({node_id})


    def _has_node_local(self, node_id: int) -> bool:
        """
        True if at least one attribute row for node_id exists locally.
        """
        with get_client_db_session(self.code) as db:
            model = LIVE_TABLE_REGISTRY[self.domain]
            return (
                db.query(model)
                .filter(model.node_id == node_id)
                .limit(1)
                .count()
                > 0
            )
        
    def get_node_attributes_local(self, node_id: int):
        """
        Return ALL attributes for node_id from local DB.
        """
        with get_client_db_session(self.code) as db:
            model = LIVE_TABLE_REGISTRY[self.domain]
            return (
                db.query(model)
                .filter(model.node_id == node_id)
                .all()
            )

    def get_node_attributes_working(self, node_id: int):
        """
        Return merged LIVE ⊕ OVERLAY attributes for a node.
        """
        with get_client_db_session(self.code) as db:
            rows = read_current_work(
                db,
                domain=self.domain,
                session_id=self.provider._session_id,
            )

        return [r for r in rows if r.node_id == node_id]