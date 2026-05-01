# OPETreeWB/facades/attribute_facade.py
USE_WORKING_VIEW = True

class AttributeFacade:
    """
    Facade for attribute-related operations.

    IMPORTANT:
    - NO new logic here yet
    - This just centralizes existing behavior
    """

    def __init__(self, provider, data_access, *, debug=False):
        self.provider = provider
        self.data_access = data_access
        self.debug = debug

    # -----------------------------
    # READ (existing behavior)
    # -----------------------------
    def get_attributes(self, node_id):
        self._log(f"get_attributes(node_id={node_id})")

        if USE_WORKING_VIEW:
            self._log("using WORKING VIEW (LIVE ⊕ OVERLAY)")
            from OPE_DB_API.crud.work.read import read_current_work
            from OPE_DB_API.db.session import get_client_db_session
            
            with get_client_db_session(self.provider.code) as db:
                raw_rows = read_current_work(
                    db,
                    domain=self.provider.domain,
                    session_id=self.provider._session_id,
                )
        else:
            self._log("using LIVE ONLY view")
            raw_rows = self.data_access.get_node_attributes_local(node_id)

        rows = [self._normalize_row(r) for r in raw_rows]
        rows = [r for r in rows if r["node_id"] == node_id]

        self._log(f"returned {len(rows)} rows")
        return rows

    # -----------------------------
    # WRITE (existing behavior)
    # -----------------------------
    def update_attribute(self, element_ref, attr_name, value):
        """
        Update attribute value in WORKING mode.

        - Server update (authoritative)
        - Local LIVE ensure
        - Local OVERLAY write
        """
        self._log(
            f"update_attribute(node={element_ref.id}, attr={attr_name}, value={value})"
        )

        # -------------------------------------------------
        # 1️⃣ Server-side update (existing, keep it)
        # -------------------------------------------------
        element_ref[attr_name] = value

        # -------------------------------------------------
        # 2️⃣ Ensure local LIVE row exists
        # -------------------------------------------------
        node_id = int(element_ref.id)
        self.data_access.ensure_node_loaded(node_id)

        # -------------------------------------------------
        # 3️⃣ Write LOCAL overlay row
        # -------------------------------------------------
        from types import SimpleNamespace
        from OPE_DB_API.crud.work.push import push_work
        from OPE_DB_API.db.session import get_client_db_session

        attr_id = self.provider.registry.get_id(attr_name)

        # data_id comes from provider cache populated by load_node
        data_id, _ = self.provider._cache[node_id][attr_id]

        payload = SimpleNamespace(
            data_id=data_id,
            node_id=node_id,
            attribute_id=attr_id,
            operation_type=2,   # UPDATE
            value=value,
        )

        with get_client_db_session(self.provider.code) as db:
            push_work(
                db,
                domain=self.provider.domain,
                session_id=self.provider._session_id,
                payload=payload,
            )
            db.commit()

    # -----------------------------
    # META
    # -----------------------------
    def is_editable(self):
        editable = self.provider._session_id is not None
        self._log(f"is_editable -> {editable}")
        return editable
    
    
    def _log(self, msg):
        if self.debug:
            print(f"[AttributeFacade] {msg}")

    def _normalize_row(self, r):
            """
            Convert any row (ORM object or dict) into a clean dict.
            This is the ONLY place that knows about row shapes.
            """
            # Case 1: dict (from read_current_work)
            if isinstance(r, dict):
                return {
                    "data_id": r["data_id"],
                    "node_id": r["node_id"],
                    "attribute_id": r["attribute_id"],
                    "value": r["value"],
                }

            # Case 2: ORM row (from LIVE table)
            return {
                "data_id": r.data_id,
                "node_id": r.node_id,
                "attribute_id": r.attribute_id,
                "value": r.value,
            }