# domain/services/tree_service.py
from opetreewb.messaging.reporter import Reporter
from opetreewb.domain.rules.tree_rules import TreeRules
from opetreewb.domain.transection.transaction_manager import TransactionManager
from opetreewb.infrastructure.dummy_provider_adapter import DummyProviderAdapter
from opetreewb.ui.store.tree_store import TREE_STORE
from opetreewb.ui.model.tree_model import TreeNodeModel, AttributeValue

class TreeService:
    """
    Tree structure contract.
    """

    def __init__(self, provider_adapter=None):
        self.provider = provider_adapter or DummyProviderAdapter()
        self.tx = TransactionManager()
        self.model = TREE_STORE

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
                f"[LOCAL] create_node applied under {parent_node_id.node_id}"
            )

            new_id = max(
                [c.node_id for c in parent_node_id.children] + [parent_node_id.node_id]
            ) + 1

            attrs = {
                "Type": AttributeValue(new_id * 10, element_type),
            }

            if name:
                attrs["Name"] = AttributeValue(new_id * 10 + 1, name)

            new_node = TreeNodeModel(
                node_id=new_id,
                label="",
                attributes=attrs,
                children=[]
            )

            parent_node_id.children.append(new_node)

        result = self.tx.run(server_op, local_op, "Create Node")

        if not result.success:
            Reporter.error(
                f"[TreeService] Create Failed "
                f"(parent={parent_node_id.node_id}, type={element_type}, name={name})"
            )
            return False
        
        Reporter.success(
            f"[TreeService] Create allowed "
            f"(parent={parent_node_id.node_id}, type={element_type}, name={name})"
        )

        return True

    def delete_node(self, node_id):
        result = TreeRules.can_delete_node(node_id)

        if not result.allowed:
            Reporter.error(
                f"[TreeService] Delete denied: {result.reason}"
            )
            return

        def server_op():
            return self.provider.delete_node_server(node_id.node_id)

        def local_op():
            Reporter.info(
                f"[LOCAL] delete_node applied (node_id={node_id.node_id})"
            )
            parent = self._find_parent(node_id)

            if parent:
                parent.children = [
                    c for c in parent.children if c is not node_id
                ]
            else:
                # root-level delete
                self.model.roots = [
                    r for r in self.model.roots if r is not node_id
                ]


        result = self.tx.run(server_op, local_op, "Delete Node")

        if not result.success:
            Reporter.error(
                f"[TreeService] Delete Failed (node_id={node_id.node_id})"
            )
            return False

        Reporter.success(
            f"[TreeService] Delete allowed (node_id={node_id.node_id})"
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