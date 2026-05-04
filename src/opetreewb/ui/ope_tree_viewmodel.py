from PySide import QtCore
from opetreewb.ui.tree_model import TreeModel, TreeNodeModel
from opetreewb.ui.tree_selection_bus import TREE_SELECTION
from opetreewb.ui.tree_model import AttributeValue


class OPETreeViewModel(QtCore.QObject):

    children_requested = QtCore.Signal(int)  # node_id

    def __init__(self):
        super().__init__()
        self.model = TreeModel()

    def get_roots(self):
        return self.model.roots

    def select_node(self, node: TreeNodeModel):
        TREE_SELECTION.selectionChanged.emit(node)

    def load_children(self, node: TreeNodeModel):
        """
        UI-only lazy loading.
        Later this will call provider / backend.
        """

        node.children = [
            TreeNodeModel(
                node_id=node.node_id * 10 + 1,
                label=f"{node.label}_CHILD_1",
                attributes={
                    "Name": AttributeValue(101, "WORLD_1"),
                    "Type": AttributeValue(102, "WORLD"),
                    "Owner": AttributeValue(103, ""),
                    "Status": AttributeValue(104, "Active"),
                },
                children=[],
            ),
            TreeNodeModel(
                node_id=node.node_id * 10 + 2,
                label=f"{node.label}_CHILD_2",
                attributes={},
                children=[],
            ),
        ]
