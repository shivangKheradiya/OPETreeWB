from sqlalchemy.orm import Session

from opetreewb.integration.opedbapi.api.session_api import SessionAPI
from opetreewb.integration.opedbapi.api.node_api import NodeAPI
from opetreewb.integration.opedbapi.api.attribute_api import AttributeAPI
from opetreewb.integration.opedbapi.api.query_api import QueryAPI
from opetreewb.integration.opedbapi.api.client import OpeApiClient

from opetreewb.integration.opedbapi.local.session_local import SessionLocal
from opetreewb.integration.opedbapi.local.attribute_local import AttributeLocal
from opetreewb.integration.opedbapi.local.query_local import QueryLocal
from opetreewb.integration.opedbapi.local.client import LocalClient

from opetreewb.domain.stores.stores import OPE_DB_CONTEXT
from opetreewb.messaging.reporter import Reporter

from OPE_DB_API.crud.commit.commit import commit_session
from OPE_DB_API.crud.session.abort import abort_session

class OpeDBClient:
    """
    Hybrid client with explicit API / LOCAL separation.
    """

    def __init__(self, id_generator = None):
        id_gen = id_generator

        Reporter.info("[OpeDBClient] Initializing")

        # ✅ API
        self.api_session = SessionAPI()
        self.api_node = NodeAPI(id_generator=id_gen)
        self.api_attr = AttributeAPI(id_generator=id_gen)
        self.api_query = QueryAPI()
        self.api_client = OpeApiClient()

        # ✅ LOCAL
        self.local_session = SessionLocal()
        self.local_attr = AttributeLocal(id_gen)
        self.local_query = QueryLocal()
        self.local_client = LocalClient()

        Reporter.success("[OpeDBClient] Ready")

    # =========================================================
    # SESSION (EXPLICIT)
    # =========================================================

    # ---------- START ----------
    def start_session_api(self):
        Reporter.info("[OpeDBClient][API] start_session_api")
        try:
            session_id = self.api_session.start()
            Reporter.success(f"[OpeDBClient][API] session started → {session_id}")
            return session_id
        except Exception as e:
            Reporter.error(f"[OpeDBClient][API] start_session failed → {e}")
            raise

    def start_session_local(self):
        Reporter.info("[OpeDBClient][LOCAL] start_session_local")
        try:
            self.local_session.start()
            Reporter.success("[OpeDBClient][LOCAL] session created")
        except Exception as e:
            Reporter.error(f"[OpeDBClient][LOCAL] start_session failed → {e}")
            raise

    # ---------- CLOSE ----------
    def close_session_api(self):
        Reporter.info("[OpeDBClient][API] close_session_api")
        try:
            session_id = self.api_session.close()
            Reporter.success("[OpeDBClient][API] session closed")
            return session_id
        except Exception as e:
            Reporter.error(f"[OpeDBClient][API] close_session failed → {e}")
            raise

    def close_session_local(self):
        Reporter.info("[OpeDBClient][LOCAL] close_session_local")
        try:
            self.local_session.close()
            Reporter.success("[OpeDBClient][LOCAL] session closed")
        except Exception as e:
            Reporter.error(f"[OpeDBClient][LOCAL] close_session failed → {e}")
            raise

    # ---------- COMMIT ----------
    def commit_session_api(self):
        Reporter.info("[OpeDBClient][API] commit_session_api")
        try:
            result = self.api_client.post(
                "work/commit",
                use_session=True
            )
            Reporter.success("[OpeDBClient][API] commit applied")
        except Exception as e:
            Reporter.error(f"[OpeDBClient][API] commit failed → {e}")
            raise

    def commit_session_local(self):
        Reporter.info("[OpeDBClient][LOCAL] commit_session_local")
        db: Session = self.local_client.get_session()
        try:
            commit_session(
                db,
                domain=OPE_DB_CONTEXT.domain.upper(),
                session_id=OPE_DB_CONTEXT.session_id,
            )
            db.commit()
            Reporter.success("[OpeDBClient][LOCAL] commit applied")
        except Exception as e:
            Reporter.error(f"[OpeDBClient][LOCAL] commit failed → {e}")
            raise
        finally:
            db.close()

    # ---------- ABORT ----------
    def abort_session_api(self):
        Reporter.info("[OpeDBClient][API] abort_session_api")
        try:
            result = self.api_client.post(
                "work/discard",
                use_session=True
            )
            Reporter.success("[OpeDBClient][API] abort applied")
        except Exception as e:
            Reporter.error(f"[OpeDBClient][API] abort failed → {e}")
            raise

    def abort_session_local(self):
        Reporter.info("[OpeDBClient][LOCAL] abort_session_local")

        db: Session = self.local_client.get_session()

        try:
            abort_session(
                db,
                session_id=OPE_DB_CONTEXT.session_id,
                domain=OPE_DB_CONTEXT.domain.upper(),
            )
            db.commit()
            Reporter.success("[OpeDBClient][LOCAL] abort applied")
        except Exception as e:
            Reporter.error(f"[OpeDBClient][LOCAL] abort failed → {e}")
            raise
        finally:
            db.close()

    # =========================================================
    # ATTRIBUTE (EXPLICIT)
    # =========================================================

    def push_attribute_api(self, **kwargs):
        Reporter.info("[OpeDBClient][API] push_attribute_api")
        try:
            data_id = self.api_attr.push(**kwargs)
            Reporter.success(f"[OpeDBClient][API] attribute pushed → {data_id}")
            return data_id
        except Exception as e:
            Reporter.error(f"[OpeDBClient][API] push_attribute failed → {e}")
            raise

    def push_attribute_local(self, *, node_id, attribute_id, value, data_id):
        Reporter.info("[OpeDBClient][LOCAL] push_attribute_local")
        try:
            self.local_attr.push(
                node_id=node_id,
                attribute_id=attribute_id,
                value=value,
                data_id=data_id,
            )
            Reporter.success("[OpeDBClient][LOCAL] attribute stored")
        except Exception as e:
            Reporter.error(f"[OpeDBClient][LOCAL] push_attribute failed → {e}")
            raise

    def delete_attribute_api(self, **kwargs):
        Reporter.info("[OpeDBClient][API] delete_attribute_api")
        try:
            self.api_attr.delete(**kwargs)
            Reporter.success("[OpeDBClient][API] attribute deleted")
        except Exception as e:
            Reporter.error(f"[OpeDBClient][API] delete failed → {e}")
            raise

    def delete_attribute_local(self, **kwargs):
        Reporter.info("[OpeDBClient][LOCAL] delete_attribute_local")
        try:
            self.local_attr.delete(**kwargs)
            Reporter.success("[OpeDBClient][LOCAL] attribute removed")
        except Exception as e:
            Reporter.error(f"[OpeDBClient][LOCAL] delete failed → {e}")
            raise

    # =========================================================
    # QUERY
    # =========================================================

    def search(self, **kwargs):

        Reporter.info("[OpeDBClient] SEARCH")

        try:
            Reporter.info("[OpeDBClient][LOCAL] search")
            result = self.local_query.search(**kwargs)

            if result and result.get("items"):
                Reporter.success("[OpeDBClient][LOCAL] result found")
                return result

            Reporter.info("[OpeDBClient][LOCAL] empty → fallback API")

        except Exception as e:
            Reporter.warning(f"[OpeDBClient][LOCAL] search failed → {e}")

        Reporter.info("[OpeDBClient][API] search fallback")

        try:
            result = self.api_query.search(**kwargs)
            Reporter.success("[OpeDBClient][API] result returned")
            return result
        except Exception as e:
            Reporter.error(f"[OpeDBClient][API] search failed → {e}")
            raise

    def load_node(self, node_id):

        Reporter.info(f"[OpeDBClient] LOAD NODE → {node_id}")

        return self.search(
            filter_dict={
                "field": "node_id",
                "op": "=",
                "value": node_id,
            }
        )