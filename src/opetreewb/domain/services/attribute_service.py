from opetreewb.messaging.reporter import Reporter
from opetreewb.domain.rules.attribute_rules import AttributeRules
from opetreewb.domain.transection.transaction_manager import TransactionManager
from opetreewb.infrastructure.provider_adapter import ProviderAdapter
from opetreewb.infrastructure.dummy_provider_adapter import DummyProviderAdapter
from opetreewb.ui.model.tree_model import AttributeValue
from opetreewb.integration.opedbapi.facade.opedb_client import OpeDBClient


class AttributeService:
    """
    Handles attribute reads and updates.
    """

    def __init__(self, provider_adapter=None, fcadclient:OpeDBClient=None):
        self.provider = provider_adapter or DummyProviderAdapter()
        self.tx = TransactionManager()
        self.fcadclient = fcadclient

    def load_attributes(self, node_id):
        Reporter.info(
            f"[AttributeService] load_attributes called (node_id={node_id})"
        )
        # TODO: return attributes from legacy provider
        return []

    def update_attribute(self, node, attribute_name, data_id, new_value):
    
        result = AttributeRules.can_update(
            attribute_name,
            data_id,
            new_value,
        )
    
        if not result.allowed:
            Reporter.error(
                f"[AttributeService] Update denied: {result.reason}"
            )
            return False
    
        # -------------------------
        # CASE 1: NEW ATTRIBUTE ✅
        # -------------------------
        if data_id is None:
        
            def server_op():
                return self.provider.create_attribute_server(
                    attribute_name, new_value
                )
    
            def local_op():
                new_id = max(
                    [a.data_id for a in node.attributes.values()] + [1000]
                ) + 1
    
                node.attributes[attribute_name] = AttributeValue(
                    data_id=new_id,
                    value=new_value
                )
    
                Reporter.info(
                    f"[LOCAL] attribute created (data_id={new_id})"
                )
    
            result = self.tx.run(server_op, local_op, "Create Attribute")
    
        # -------------------------
        # CASE 2: EXISTING ATTRIBUTE ✅
        # -------------------------
        else:
        
            def server_op():
                return self.provider.update_attribute_server(
                    data_id, new_value
                )
    
            def local_op():
                node.attributes[attribute_name].value = new_value
    
                Reporter.info(
                    f"[LOCAL] attribute updated (data_id={data_id})"
                )
    
            result = self.tx.run(server_op, local_op, "Update Attribute")
    
        # -------------------------
        if not result.success:
            return False
    
        Reporter.success(
            f"[AttributeService] Update allowed "
            f"(data_id={data_id}, value={new_value})"
        )
    
        return True