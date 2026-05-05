from opetreewb.domain.transection.transaction_result import TransactionResult
from opetreewb.messaging.reporter import Reporter


class DummyProviderAdapter:
    """
    Dummy provider adapter used during UI / skeleton phase.
    Always simulates successful server operations.
    """

    def create_node_server(self, parent_node_id, element_type, name):
        Reporter.info(
            f"[DUMMY SERVER] create_node(parent={parent_node_id.node_id}, type={element_type})"
        )
        return TransactionResult(True, "200 OK")

    def delete_node_server(self, node_id):
        Reporter.info(
            f"[DUMMY SERVER] delete_node(node_id={node_id})"
        )
        return TransactionResult(True, "200 OK")

    def update_attribute_server(self, data_id, value):
        Reporter.info(
            f"[DUMMY SERVER] update_attribute(data_id={data_id}, value={value})"
        )
        return TransactionResult(True, "200 OK")
