from PySide import QtCore

from opetreewb.domain.services.service_locator import get_tree_service
from opetreewb.ui.model.tree_model import (AttributeValue, TreeModel,
                                           TreeNodeModel)


class OPETreeViewModel(QtCore.QObject):
    children_requested = QtCore.Signal(int)  # node_id

    def __init__(self):
        super().__init__()
        self.model = TreeModel()

    def load_children(self, node: TreeNodeModel):
        """
        UI-only lazy loading.
        Later this will call provider / backend.
        """
        node.children = get_tree_service().get_children(node.node_id)

    def get_roots(self):
        return get_tree_service().get_roots()
