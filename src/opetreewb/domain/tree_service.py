from opetreewb.messaging.reporter import Reporter


class TreeService:
    """
    Handles node creation, deletion, and tree structure.
    """

    def create_node(self, parent_id, element_type, name):
        Reporter.info(
            f"[TreeService] create_node called "
            f"(parent_id={parent_id}, type={element_type}, name={name})"
        )
        # TODO: wire to legacy provider.create_node()
        return None

    def delete_node(self, node_id):
        Reporter.info(
            f"[TreeService] delete_node called (node_id={node_id})"
        )
        # TODO: wire to legacy provider.delete_node()