"""
Utility functions for formatting tree node labels.
Pure domain logic.
"""


def format_node_label(
    *,
    type_name: str | None,
    name: str | None = None,
    node_id: str | int | None = None,
) -> str:
    """
    Return a tree node label in the unified format:

        <Type> <Name or ID>

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
