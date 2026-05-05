from opetreewb.messaging.reporter import Reporter
from opetreewb.domain.attribute_rules import AttributeRules

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

    def update_attribute(self, attribute_name, data_id, new_value):
        result = AttributeRules.can_update(
            attribute_name,
            data_id,
            new_value,
        )

        if not result.allowed:
            Reporter.error(
                f"[AttributeService] Update denied: {result.reason}"
            )
            return

        Reporter.success(
            f"[AttributeService] Update allowed "
            f"(data_id={data_id}, value={new_value})"
        )

        # TODO: backend integration here