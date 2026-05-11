# domain/services/tree_service.py
from opetreewb.messaging.reporter import Reporter
from opetreewb.domain.rules.tree_rules import TreeRules
from opetreewb.domain.transection.transaction_manager import TransactionManager
from opetreewb.domain.transection.transaction_result import TransactionResult
from opetreewb.integration.opedbapi.facade.opedb_client import OpeDBClient
from opetreewb.ui.model.tree_model import TreeModel


class TreeService:
    """
    Tree structure contract.
    """

    def __init__(self, provider_adapter=None, fcadclient:OpeDBClient=None):
        self.tx = TransactionManager()
        self.model = TreeModel()
        self.fcadclient = fcadclient

    def get_children(self, parent_node_id):
        Reporter.info(
            f"[TreeService] get_children(parent_node_id={parent_node_id})"
        )
        return []

    def create_node(self, parent_node, element_type, name=None):
        result = TreeRules.can_create_node(parent_node, element_type)

        if not result.allowed:
            Reporter.info(
                f"[TreeService] create_node("
                f"parent_id={parent_node.node_id}, type={element_type}, name={name})"
            )
            return False
        
        def server_op():
            node_id = self.fcadclient.create_node_api( 
                parent_node_id=parent_node.node_id, 
                element_type=element_type, 
                name=name,
            )
            return TransactionResult(success=True, message=node_id)

        def local_op():
            Reporter.info(
                f"[LOCAL] create_node applied under {parent_node.node_id}"
            )

            self.fcadclient.create_node_local(
                parent_node_id=parent_node.node_id, 
                element_type=element_type, 
                name=name,
            )

            return TransactionResult(success=True, message="200 OK")

        result = self.tx.run(server_op, local_op, "Create Node")

        if not result.success:
            Reporter.error(
                f"[TreeService] Create Failed "
                f"(parent={parent_node.node_id}, type={element_type}, name={name})"
            )
            return False
        
        Reporter.success(
            f"[TreeService] Create allowed "
            f"(parent={parent_node}, type={element_type}, name={name})"
        )

        return True
    
    def create_node_root(self, element_type, name=None):
        result = TreeRules.can_create_root_node(element_type)

        if not result.allowed:
            Reporter.info(
                f"[TreeService] create_node_root("
                f"(type={element_type}, name={name})"
            )
            return False
        
        def server_op():
            node_id = self.fcadclient.create_node_api( 
                parent_node_id=0,
                element_type=element_type,
                name=name,
            )
            return TransactionResult(success=True, message=node_id)

        def local_op():
            Reporter.info(
                f"[LOCAL] create_node_root applied under root"
            )

            self.fcadclient.create_node_local(
                parent_node_id=0,
                element_type=element_type,
                name=name,
            )
            
            return TransactionResult(success=True, message="200 OK")

        result = self.tx.run(server_op, local_op, "Create Node")

        if not result.success:
            Reporter.error(
                f"[TreeService] Create Failed "
                f"type={element_type}, name={name})"
            )
            return False
        
        Reporter.success(
            f"[TreeService] Create allowed "
            f"(type={element_type}, name={name})"
        )

        return True

    def delete_node(self, node, element_type):
        result = TreeRules.can_delete_node(node)

        if not result.allowed:
            Reporter.error(
                f"[TreeService] Delete denied: {result.reason}"
            )
            return

        def server_op():
            self.fcadclient.delete_node_api(node.node_id, element_type)
            return TransactionResult(success=True, message="200 OK")

        def local_op():
            Reporter.info(
                f"[LOCAL] delete_node applied (node_id={node.node_id})"
            )
            self.fcadclient.delete_node_local(node.node_id)
            return TransactionResult(success=True, message="200 OK")

        result = self.tx.run(server_op, local_op, "Delete Node")

        if not result.success:
            Reporter.error(
                f"[TreeService] Delete Failed (node_id={node.node_id})"
            )
            return TransactionResult(success=True, message="200 OK")

        Reporter.success(
            f"[TreeService] Delete allowed (node_id={node.node_id})"
        )

        return True

    def _find_parent(self, target_node):
        def search(node):
            for child in node.children:
                if child is target_node:
                    return node
                result = search(child)
                if result:
                    return result
            return None

        for root in self.model.roots:
            if root is target_node:
                return None
            parent = search(root)
            if parent:
                return parent

        return None
    
    def get_roots(self):
        Reporter.info("[TreeService] get_roots() called")
        return self.model.roots
