from dataclasses import dataclass
from typing import List, Dict


@dataclass
class AttributeValue:
    data_id: int
    value: str

@dataclass
class TreeNodeModel:
    node_id: int
    label: str
    attributes: Dict[str, AttributeValue]
    children: List["TreeNodeModel"]

class TreeModel:
    """
    Dummy hierarchical tree model with realistic attribute data_ids.
    """

    def __init__(self):
        self.roots = []