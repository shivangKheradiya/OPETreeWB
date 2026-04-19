# adapters/pydbml_adapter.py
"""
PyDBML → OPETree adapter.

This module translates PyDBML ElementRef objects into
tree-ready representations (labels and child nodes).

UI code MUST NOT directly inspect PyDBML internals.
"""

from typing import List

try:
    from PyDBML.datatypes import RefTarget
    from PyDBML import ElementRef
except ImportError:
    RefTarget = None

from OPETreeWB.core.label_utils import format_node_label

class PyDBMLTreeAdapter:
    """
    Adapter for representing PyDBML ElementRef objects in OPETree.
    """

    def __init__(self, provider):
        """
        provider:
            PyDBML provider instance (e.g. OpeApiProvider)
        """
        self.provider = provider

    # ---------------------------------------------------------
    # Tree label
    # ---------------------------------------------------------
    def get_label(self, element_ref) -> str:
        # ✅ Load element explicitly (never use element_ref.element)
        element = self.provider.load_node(element_ref.id)

        # Resolve Type
        type_name = "Node"
        try:
            type_attr_id = self.provider.registry.get_id("Type")
            if type_attr_id in element.attributes:
                type_name = element.attributes[type_attr_id].value
        except Exception:
            pass

        # Resolve Name
        name = None
        try:
            if element_ref.exists("Name"):
                name = element_ref["Name"]
        except Exception:
            pass

        return format_node_label(
            type_name=type_name,
            name=name,
            node_id=element_ref.id,
        )

    # ---------------------------------------------------------
    # Child traversal
    # ---------------------------------------------------------
    def get_children(self, element_ref) -> List:
        provider = self.provider
        owner_attr_id = provider.registry.get_id("Owner")

        children = []

        rows = provider.search_by_attribute(
            attribute_id=owner_attr_id,
            value=element_ref.id,
        )

        for row in rows:
            child_node_id = row["node_id"]
            children.append(ElementRef(provider, child_node_id))

        return children

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------
    def _is_ref(self, value) -> bool:
        return RefTarget is not None and isinstance(value, RefTarget)

    def _resolve_ref(self, ref_target):
        """
        Resolve RefTarget → ElementRef using provider.
        """
        try:
            return self.provider.get_element(
                int(ref_target.element_id)
            )
        except Exception:
            return None