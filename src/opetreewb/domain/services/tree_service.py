# domain/tree_service.py
from opetreewb.messaging.reporter import Reporter
from opetreewb.domain.rules.tree_rules import TreeRules
from opetreewb.domain.transection.transaction_manager import TransactionManager
from opetreewb.infrastructure.dummy_provider_adapter import DummyProviderAdapter

class TreeService:
    """
    Tree structure contract.
    """

    def __init__(self, provider_adapter=None):
        self.provider = provider_adapter or DummyProviderAdapter()
        self.tx = TransactionManager()

    def load_children(self, parent_node_id):
        Reporter.info(
            f"[TreeService] load_children(parent_node_id={parent_node_id})"
        )
        return []

    def create_node(self, parent_node_id, element_type, name):
        result = TreeRules.can_create_node(parent_node_id, element_type)

        if not result.allowed:
            Reporter.info(
                f"[TreeService] create_node("
                f"parent_id={parent_node_id}, type={element_type}, name={name})"
            )
            return None
        
        def server_op():
            return self.provider.create_node_server(
                parent_node_id, element_type, name
            )

        def local_op():
            Reporter.info(
                f"[LOCAL] create_node applied under {parent_node_id}"
            )
            # UI / in-memory model already updated

        self.tx.run(server_op, local_op, "Create Node")

        Reporter.success(
            f"[TreeService] Create allowed "
            f"(parent={parent_node_id.node_id}, type={element_type}, name={name})"
        )

        # TODO: backend integration here
        return None

    def delete_node(self, node_id):
        result = TreeRules.can_delete_node(node_id)

        if not result.allowed:
            Reporter.error(
                f"[TreeService] Delete denied: {result.reason}"
            )
            return

        def server_op():
            return self.provider.delete_node_server(node_id)

        def local_op():
            Reporter.info(
                f"[LOCAL] delete_node applied (node_id={node_id})"
            )

        self.tx.run(server_op, local_op, "Delete Node")

        Reporter.success(
            f"[TreeService] Delete allowed (node_id={node_id.node_id})"
        )

        # TODO: backend integration here
