from opetreewb.integration.opedbapi.api.session_api import SessionAPI
from opetreewb.integration.opedbapi.api.node_api import NodeAPI
from opetreewb.integration.opedbapi.api.attribute_api import AttributeAPI
from opetreewb.integration.opedbapi.api.query_api import QueryAPI

from opetreewb.integration.opedbapi.local.session_local import SessionLocal
from opetreewb.integration.opedbapi.local.attribute_local import AttributeLocal
from opetreewb.integration.opedbapi.local.query_local import QueryLocal

from opetreewb.domain.stores.stores import ID_GENERATOR


class OpeDBClient:
    """
    Hybrid client (API + Local) orchestrator.

    Principles:
    - WRITE → API first, then local
    - READ  → local first, fallback API
    """

    def __init__(self):

        id_gen = ID_GENERATOR

        # ✅ API
        self.api_session = SessionAPI()
        self.api_node = NodeAPI(id_generator=id_gen)
        self.api_attr = AttributeAPI(id_generator=id_gen)
        self.api_query = QueryAPI()

        # ✅ LOCAL
        self.local_session = SessionLocal()
        self.local_attr = AttributeLocal(id_gen)
        self.local_query = QueryLocal()

    # =========================================================
    # SESSION
    # =========================================================
    def start_session(self, username=None):

        # ✅ API first
        session_id = self.api_session.start(username=username)

        # ✅ then local (same session_id)
        self.local_session.start(
            session_id=session_id,
            username=username,
        )

        return session_id

    def close_session(self):

        session_id = self.api_session.close()

        # ✅ ensure local also closed
        if session_id:
            self.local_session.close(session_id)

    # =========================================================
    # NODE
    # =========================================================
    def create_node(self, **kwargs):

        # ✅ API first
        node_id = self.api_node.create(**kwargs)

        # ✅ OPTIONAL: replicate locally via attribute push (future)
        return node_id

    def delete_node(self, node_id):

        # ✅ API first
        self.api_node.delete(node_id)

        # local cleanup happens automatically via sync/overlay later

    # =========================================================
    # ATTRIBUTE (WRITE)
    # =========================================================
    def push_attribute(self, **kwargs):

        # ✅ Step 1 — API
        data_id = self.api_attr.push(**kwargs)

        # ✅ Step 2 — LOCAL
        self.local_attr.push(
            node_id=kwargs["node_id"],
            attribute_id=kwargs["attribute_id"],
            value=kwargs["value"],
            data_id=data_id,
        )

        return data_id

    def delete_attribute(self, **kwargs):

        # ✅ API
        self.api_attr.delete(**kwargs)

        # ✅ LOCAL
        self.local_attr.delete(**kwargs)

    # =========================================================
    # QUERY (READ)
    # =========================================================
    def search(self, **kwargs):

        # ✅ Step 1 — LOCAL
        try:
            result = self.local_query.search(**kwargs)

            if result and result.get("items"):
                return result

        except Exception:
            # fallback to API safely
            pass

        # ✅ Step 2 — API fallback
        return self.api_query.search(**kwargs)

    def load_node(self, node_id):

        result = self.search(
            filter_dict={
                "field": "node_id",
                "op": "=",
                "value": node_id,
            }
        )

        return result