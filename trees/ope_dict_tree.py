# OPETreeWB/trees/ope_dict_tree.py

"""
OPEDictTree

Dictionary / lookup tree backed by PyDBML.
This tree is FLAT (non-hierarchical).
"""

from OPETreeWB.trees.ope_tree_base import OPETree
from OPETreeWB.adapters.pydbml_adapter import PyDBMLTreeAdapter
from PyDBML import ElementRef


class OPEDictTree(OPETree):
    """
    OPE Dictionary Tree implementation.

    Displays all dictionary nodes (Type == 'DICT') in a flat list.
    """

    def __init__(self, provider, parent=None):
        super().__init__(parent)

        self.provider = provider
        self.adapter = PyDBMLTreeAdapter(provider)

        self._build_tree()

    # ---------------------------------------------------------
    # Tree construction
    # ---------------------------------------------------------
    def _build_tree(self):
        """
        Builds a flat dictionary tree.
        """
        self.clear_tree()

        type_attr_id = self.provider.registry.get_id("Type")

        # Find all dictionary nodes
        rows = self.provider.search_by_attribute(
            attribute_id=type_attr_id,
            value="DICT",
        )

        # Collect unique node IDs
        node_ids = sorted({row["node_id"] for row in rows})

        for node_id in node_ids:
            element_ref = ElementRef(self.provider, node_id)
            label = self.adapter.get_label(element_ref)

            item = self.create_item(label, element_ref)
            self.addTopLevelItem(item)
