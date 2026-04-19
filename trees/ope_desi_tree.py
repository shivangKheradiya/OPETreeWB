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

        root_ref = self.provider.get_element(root_node_id)
        self._build_tree(root_ref)

    # ---------------------------------------------------------
    # Tree construction
    # ---------------------------------------------------------
    def _build_tree(self, root_ref):
        self.clear_tree()
        roots = self._discover_world_roots()

        for root_ref in roots:
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

    def _discover_world_roots(self):
        """
        Discover WORLD root nodes.
        Criteria:
        - Type == "WORLD"
        - No Owner or Owner is null/0
        """
        provider = self.provider
        registry = provider.registry

        type_attr = registry.get_id("Type")
        owner_attr = registry.get_id("Owner")

        # 1️⃣ Find all WORLD-typed nodes
        world_rows = provider.search_by_attribute(
            attribute_id=type_attr,
            value="WORLD",
        )

        world_node_ids = {row["node_id"] for row in world_rows}

        if not world_node_ids:
            return []

        # 2️⃣ Find nodes that HAVE an Owner
        owner_rows = provider.search_by_attribute(
            attribute_id=owner_attr,
            value=None,  # we only want presence check, value filtered below
        )

        owned_nodes = {
            row["node_id"]
            for row in owner_rows
            if row["value"] not in (None, 0)
        }

        # 3️⃣ Roots = WORLD nodes WITHOUT owner
        root_ids = world_node_ids - owned_nodes

        return [ElementRef(provider, nid) for nid in root_ids]
