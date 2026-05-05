# domain/tree_service.py
from opetreewb.messaging.reporter import Reporter


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
        Reporter.info(
            f"[TreeService] create_node("
            f"parent_id={parent_node_id}, type={element_type}, name={name})"
        )

    def delete_node(self, node_id):
        Reporter.info(
            f"[TreeService] delete_node(node_id={node_id})"
        )