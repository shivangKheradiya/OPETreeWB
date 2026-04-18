# core/label_utils.py
"""
Common tree label formatting utilities.

All OPETree implementations must use the same label format:
    <Type> <Name or ID>
"""


def format_node_label(
    *,
    type_name: str | None,
    name: str | None = None,
    node_id: str | int | None = None,
) -> str:
    """
    Return a tree node label in the unified format.

    Priority:
      - Type: required (fallback = 'Node')
      - Name: preferred
      - ID: fallback if name is missing
    """
    type_part = type_name or "Node"

    if name:
        value_part = str(name)
    elif node_id is not None:
        value_part = str(node_id)
    else:
        value_part = ""

    return f"{type_part} {value_part}".strip()