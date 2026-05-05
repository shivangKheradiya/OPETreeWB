from opetreewb.messaging.reporter import Reporter
from opetreewb.domain.rules.attribute_rules import AttributeRules
from opetreewb.domain.transection.transaction_manager import TransactionManager
from opetreewb.infrastructure.provider_adapter import ProviderAdapter
from opetreewb.infrastructure.dummy_provider_adapter import DummyProviderAdapter


class AttributeService:
    """
    Handles attribute reads and updates.
    """

    def __init__(self, provider_adapter=None):
        self.provider = provider_adapter or DummyProviderAdapter()
        self.tx = TransactionManager()

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

        def server_op():
            return self.provider.update_attribute_server(
                data_id, new_value
            )

        def local_op():
            Reporter.info(
                f"[LOCAL] attribute updated (data_id={data_id})"
            )

        result = self.tx.run(server_op, local_op, "Update Attribute")
        
        if not result.success:
            # IMPORTANT: stop here
            return False

        Reporter.success(
            f"[AttributeService] Update allowed "
            f"(data_id={data_id}, value={new_value})"
        )