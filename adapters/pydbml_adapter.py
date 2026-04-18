# adapters/pydbml_adapter.py
"""
PyDBML → OPETree adapter.

This module translates PyDBML ElementRef objects into
tree-ready representations (labels and child nodes).

UI code MUST NOT directly inspect PyDBML internals.
"""

from typing import List

try:
    from PyDBML.core import ElementRef
    from PyDBML.datatypes import RefTarget
except ImportError:
    ElementRef = None
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
        """
        Return a unified tree label:
            <Type> <Name or ID>
        """
        element = element_ref.element
    
        type_name = element.type or "Node"
    
        try:
            if element_ref.exists("Name"):
                name = element_ref["Name"]
            else:
                name = None
        except Exception:
            name = None
    
        return format_node_label(
            type_name=type_name,
            name=name,
            node_id=element_ref.id,
        )

        """
        Return display label for a tree node.
        """
        if element_ref is None:
            return "<None>"

        # Prefer Name attribute if available
        try:
            if element_ref.exists("Name"):
                return str(element_ref["Name"])
        except Exception:
            pass

        return f"Node {element_ref.id}"

    # ---------------------------------------------------------
    # Child traversal
    # ---------------------------------------------------------
    def get_children(self, element_ref) -> List:
        """
        Return child ElementRefs discovered via REFERENCE attributes.
        """
        children = []

        element = element_ref.element

        for attr in element.attributes.values():
            if attr.type == "REFERENCE":
                children.append(
                    self._resolve_ref(attr.value)
                )

            elif attr.type == "ARRAY":
                for item in attr.value:
                    if self._is_ref(item):
                        children.append(
                            self._resolve_ref(item)
                        )

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