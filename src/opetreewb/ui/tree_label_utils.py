"""
UI-only helpers for tree node labels.
"""

from opetreewb.ui.tree_model import AttributeValue


def build_node_label(node) -> str:
    """
    Label format:
    <ElementType> <name | data_id>
    """
    attrs = node.attributes

    type_attr = attrs.get("Type")
    name_attr = attrs.get("Name")

    element_type = type_attr.value if type_attr else "UNKNOWN"

    if name_attr and name_attr.value:
        suffix = name_attr.value
    else:
        # Fallback to data_id if Name is missing
        suffix = str(type_attr.data_id if type_attr else node.node_id)

    return f"{element_type} {suffix}"