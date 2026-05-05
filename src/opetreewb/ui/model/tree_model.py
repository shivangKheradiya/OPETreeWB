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
        self.roots = [
            TreeNodeModel(
                node_id=1,
                label="WORLD_1",
                attributes={
                    "Name": AttributeValue(101, "WORLD_1"),
                    "Type": AttributeValue(102, "WORLD"),
                    "Owner": AttributeValue(103, ""),
                    "Status": AttributeValue(104, "Active"),
                },
                children=[
                    TreeNodeModel(
                        node_id=2,
                        label="PART_A",
                        attributes={
                            "Name": AttributeValue(201, "PART_A"),
                            "Type": AttributeValue(202, "PART"),
                            "Owner": AttributeValue(203, "WORLD_1"),
                            "Weight": AttributeValue(204, "12.5"),
                        },
                        children=[],
                    ),
                    TreeNodeModel(
                        node_id=3,
                        label="PART_B",
                        attributes={
                            "Name": AttributeValue(301, "PART_B"),
                            "Type": AttributeValue(302, "PART"),
                            "Owner": AttributeValue(303, "WORLD_1"),
                            "Color": AttributeValue(304, "Red"),
                        },
                        children=[],
                    ),
                ],
            )
        ]