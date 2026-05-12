from opetreewb.messaging.reporter import Reporter
from opetreewb.domain.rules.attribute_rules import AttributeRules
from opetreewb.domain.transection.transaction_manager import TransactionManager
from opetreewb.ui.model.tree_model import AttributeValue
from opetreewb.integration.opedbapi.facade.opedb_client import OpeDBClient
from opetreewb.SKET.schema.attribute_ids import get_attr_id
from opetreewb.domain.transection.transaction_result import TransactionResult
from opetreewb.domain.stores.stores import ID_GENERATOR

class AttributeService:
    """
    Handles attribute reads and updates.
    """

    def __init__(self, fcadclient:OpeDBClient=None):
        self.tx = TransactionManager()
        self.fcadclient = fcadclient

    def update_attribute(self, node, attribute_name, data_id, new_value):
    
        result = AttributeRules.can_update(
            node,
            attribute_name,
            data_id,
            new_value,
        )
    
        if not result.allowed:
            Reporter.error(
                f"[AttributeService] Update denied: {result.reason}"
            )
            return False
    
        attribute_id = get_attr_id(attribute_name)
        # -------------------------
        # CASE 1: NEW ATTRIBUTE ✅
        # -------------------------
        if data_id is None:

            new_data_id = ID_GENERATOR.next_id()

            def server_op():
                self.fcadclient.api_attr.push(
                    node_id=node.node_id,
                    attribute_id=attribute_id, 
                    value=new_value,
                    data_id=new_data_id,
                    operation_type=1,
                )
                return TransactionResult(success=True, message="200 OK")
    
            def local_op():
                self.fcadclient.local_attr.push(
                    attribute_id=attribute_id,
                    data_id=new_data_id,
                    node_id=node.node_id,
                    value=new_value,
                    operation_type=1
                )
                
                node.attributes[attribute_name] = AttributeValue(
                    data_id=new_data_id,
                    value=new_value
                )

                Reporter.info(
                    f"[LOCAL] attribute created (data_id={new_data_id})"
                )

                return TransactionResult(success=True, message="200 OK")
    
            result = self.tx.run(server_op, local_op, "Create Attribute")
    
        # -------------------------
        # CASE 2: EXISTING ATTRIBUTE ✅
        # -------------------------
        else:
        
            def server_op():
                self.fcadclient.api_attr.push(
                    node_id=node.node_id,
                    attribute_id=attribute_id, 
                    value=new_value,
                    data_id=data_id,
                    operation_type=2,
                )
                return TransactionResult(success=True, message="200 OK")
    
            def local_op():
                self.fcadclient.local_attr.push(
                    node_id=node.node_id,
                    attribute_id=attribute_id, 
                    value=new_value,
                    data_id=data_id,
                    operation_type=2,
                )

                node.attributes[attribute_name].value = new_value

                Reporter.info(
                    f"[LOCAL] attribute updated (data_id={data_id})"
                )

                return TransactionResult(success=True, message="200 OK")
    
            result = self.tx.run(server_op, local_op, "Update Attribute")
    
        # -------------------------
        if not result.success:
            return False
    
        Reporter.success(
            f"[AttributeService] Update allowed "
            f"(data_id={data_id}, value={new_value})"
        )
    
        return True