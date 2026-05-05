# domain/tree_service.py
from opetreewb.messaging.reporter import Reporter
from opetreewb.domain.tree_rules import TreeRules


class TreeService:
    """
    Tree structure contract.
    """

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

        Reporter.success(
            f"[TreeService] Delete allowed (node_id={node_id.node_id})"
        )

        # TODO: backend integration here
