from PySide import QtCore
from opetreewb.ui.tree_model import TreeModel, TreeNodeModel
from opetreewb.ui.tree_selection_bus import TREE_SELECTION


class OPETreeViewModel(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.model = TreeModel()

    def get_roots(self):
        return self.model.roots

    def select_node(self, node: TreeNodeModel):
        TREE_SELECTION.selectionChanged.emit(node)