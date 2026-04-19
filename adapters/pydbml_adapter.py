# OPETreeWB/adapters/pydbml_adapter.py

"""
PyDBML → OPETree adapter.

Converts PyDBML ElementRef objects into
tree-ready labels and child ElementRefs.

IMPORTANT:
- Adapters NEVER import ElementRef
- Adapters NEVER import RefTarget
- Adapters NEVER touch ElementRef.element
"""

from typing import List
from OPETreeWB.core.label_utils import format_node_label


class PyDBMLTreeAdapter:
    def __init__(self, provider):
        self.provider = provider

    # ---------------------------------------------------------
    # Tree label
    # ---------------------------------------------------------
    def get_label(self, element_ref) -> str:
        # Load raw Element via provider (SAFE)
        element = self.provider.load_node(element_ref.id)

        # Type
        type_name = "Node"
        try:
            type_id = self.provider.registry.get_id("Type")
            if type_id in element.attributes:
                type_name = element.attributes[type_id].value
        except Exception:
            pass

        # Name
        name = None
        try:
            name_id = self.provider.registry.get_id("Name")
            if name_id in element.attributes:
                name = element.attributes[name_id].value
        except Exception:
            pass

        return format_node_label(
            type_name=type_name,
            name=name,
            node_id=element_ref.id,
        )

    # ---------------------------------------------------------
    # Child traversal (Owner-based hierarchy)
    # ---------------------------------------------------------
    def get_children(self, element_ref) -> List:
        provider = self.provider
        owner_attr_id = provider.registry.get_id("Owner")

        rows = provider.search_by_attribute(
            attribute_id=owner_attr_id,
            value=element_ref.id,
        )

        # Ask provider to give ElementRef (NEVER construct directly)
        return [
            provider.get_element(row["node_id"])
            for row in rows
        ]