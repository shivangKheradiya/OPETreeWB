# trees/ope_desi_tree.py
"""
OPEDesiTree

DESI domain tree backed by PyDBML.
"""
from PyDBML import ElementRef
from OPETreeWB.trees.ope_tree_base import OPETree
from OPETreeWB.adapters.pydbml_adapter import PyDBMLTreeAdapter


class OPEDesiTree(OPETree):
    """
    OPE DESI Tree implementation.
    """

    def __init__(self, provider, root_node_id: int, parent=None):
        """
        provider:
            PyDBML provider instance (e.g. OpeApiProvider)

        root_node_id:
            Node ID that acts as the root of the DESI tree
        """
        super().__init__(parent)

        self.provider = provider
        self.adapter = PyDBMLTreeAdapter(provider)

        root_ref = ElementRef(self.provider, root_node_id)
        self._build_tree(root_ref)

    # ---------------------------------------------------------
    # Tree construction
    # ---------------------------------------------------------
    def _build_tree(self, root_ref):
        self.clear_tree()

        root_item = self._build_item_recursive(root_ref)
        self.addTopLevelItem(root_item)
        root_item.setExpanded(True)

    def _build_item_recursive(self, element_ref):
        """
        Build a tree item recursively from an ElementRef.
        """
        label = self.adapter.get_label(element_ref)
        item = self.create_item(label, element_ref)

        for child_ref in self.adapter.get_children(element_ref):
            if child_ref is None:
                continue
            child_item = self._build_item_recursive(child_ref)
            item.addChild(child_item)

        return item