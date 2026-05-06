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
                label="SITE PLANT1",
                attributes={
                    "Type": AttributeValue(1001, "SITE"),
                    "Name": AttributeValue(1002, "PLANT1"),
                },
                children=[
                    TreeNodeModel(
                        node_id=10,
                        label="ZONE ZONE_A",
                        attributes={
                            "Type": AttributeValue(1010, "ZONE"),
                            "Name": AttributeValue(1011, "ZONE_A"),
                        },
                        children=[
                            TreeNodeModel(
                                node_id=100,
                                label="PIPELINE P-100",
                                attributes={
                                    "Type": AttributeValue(1100, "PIPELINE"),
                                    "Name": AttributeValue(1101, "P-100"),
                                    "Fluid": AttributeValue(1102, "STEAM"),
                                    "Spec": AttributeValue(1103, "CS150"),
                                },
                                children=[
                                    TreeNodeModel(
                                        node_id=1001,
                                        label="PIPE 6IN",
                                        attributes={
                                            "Type": AttributeValue(1200, "PIPE"),
                                            "Diameter": AttributeValue(1201, "6"),
                                            "Length": AttributeValue(1202, "1200"),
                                        },
                                        children=[],
                                    ),
                                    TreeNodeModel(
                                        node_id=1002,
                                        label="ELBOW 90DEG",
                                        attributes={
                                            "Type": AttributeValue(1300, "ELBOW"),
                                            "Angle": AttributeValue(1301, "90"),
                                            "Radius": AttributeValue(1302, "LR"),
                                        },
                                        children=[],
                                    ),
                                    TreeNodeModel(
                                        node_id=1003,
                                        label="FLANGE RF",
                                        attributes={
                                            "Type": AttributeValue(1400, "FLANGE"),
                                            "Rating": AttributeValue(1401, "150#"),
                                        },
                                        children=[],
                                    ),
                                ],
                            ),
                            TreeNodeModel(
                                node_id=200,
                                label="STRUCTURE STR-01",
                                attributes={
                                    "Type": AttributeValue(1500, "STRUCTURE"),
                                    "Name": AttributeValue(1501, "STR-01"),
                                },
                                children=[
                                    TreeNodeModel(
                                        node_id=2001,
                                        label="BEAM IPE300",
                                        attributes={
                                            "Type": AttributeValue(1600, "BEAM"),
                                            "Section": AttributeValue(1601, "IPE300"),
                                            "Length": AttributeValue(1602, "6000"),
                                        },
                                        children=[],
                                    )
                                ],
                            ),
                        ],
                    )
                ],
            )
        ]
