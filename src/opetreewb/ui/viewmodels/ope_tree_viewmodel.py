from PySide import QtCore
from opetreewb.ui.model.tree_model import TreeModel, TreeNodeModel
from opetreewb.ui.store.tree_store import TREE_STORE
from opetreewb.ui.model.tree_model import AttributeValue
from opetreewb.domain.services.service_locator import (
    get_tree_service,
)

class OPETreeViewModel(QtCore.QObject):

    children_requested = QtCore.Signal(int)  # node_id

    def __init__(self):
        super().__init__()
        self.model = TREE_STORE

    def get_roots(self):
        return self.model.roots

    def load_children(self, node: TreeNodeModel):
        """
        UI-only lazy loading.
        Later this will call provider / backend.
        """
        node.children = get_tree_service().get_children(node.node_id)
        
    def create_child_node(self, parent_node, element_type, name):
        new_node_id = max(
            [n.node_id for n in parent_node.children] + [parent_node.node_id]
        ) + 1

        attrs = {
            "Type": AttributeValue(new_node_id * 10, element_type),
        }

        if name:
            attrs["Name"] = AttributeValue(new_node_id * 10 + 1, name)

        new_node = TreeNodeModel(
            node_id=new_node_id,
            label="",
            attributes=attrs,
            children=[],
        )

        parent_node.children.append(new_node)
        return new_node


    def delete_node(self, parent_node, node):
        if parent_node:
            parent_node.children = [
                c for c in parent_node.children if c is not node
            ]
        else:
            self.model.roots = [
                r for r in self.model.roots if r is not node
            ]

    def get_roots(self):
        return get_tree_service().get_roots()
