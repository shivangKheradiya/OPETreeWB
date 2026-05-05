from opetreewb.messaging.reporter import Reporter


class AttributeService:
    """
    Handles attribute reads and updates.
    """

    def load_attributes(self, node_id):
        Reporter.info(
            f"[AttributeService] load_attributes called (node_id={node_id})"
        )
        # TODO: return attributes from legacy provider
        return []

    def update_attribute(self, data_id, value):
        Reporter.info(
            f"[AttributeService] update_attribute "
            f"(data_id={data_id}, value={value})"
        )
        # TODO: wire to attribute update logic