from opetreewb.integration.opedbapi.core.operation_context import OperationContext
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT
from OPE_DB_API.schemas.work import WorkPushRequest
from OPE_DB_API.crud.work.push import push_work
from opetreewb.integration.opedbapi.local.client import LocalClient

class NodeLocal:

    def __init__(self, op_context:OperationContext=None,localclient:LocalClient=None):
        self.op_context = op_context
        self.client = localclient

    def apply_operations(self):
        session_id = OPE_DB_CONTEXT.session_id
        domain = OPE_DB_CONTEXT.domain.upper()
        db = self.client.get_session()

        try:
            for op in self.op_context.get_all():
                payload = WorkPushRequest(
                    node_id=op["node_id"],
                    attribute_id=op["attribute_id"],
                    data_id=op["data_id"],
                    operation_type=op["operation_type"],
                    value=None if op["operation_type"] == 3 else op["value"],
                )

                row = push_work(
                    db,
                    domain=domain,
                    session_id=session_id,
                    payload=payload,
                )

                db.commit()
                db.refresh(row)
        finally:
            db.close()

        self.op_context.clear()
        
