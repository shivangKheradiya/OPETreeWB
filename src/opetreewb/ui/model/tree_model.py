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
                label="DEPT ENG",
                attributes={
                    "Type": AttributeValue(1001, "DEPT"),
                    "Name": AttributeValue(1002, "ENG"),
                },
                children=[
                
                    TreeNodeModel(
                        node_id=10,
                        label="REGI REGION-01",
                        attributes={
                            "Type": AttributeValue(1010, "REGI"),
                            "Name": AttributeValue(1011, "REGION-01"),
                        },
                        children=[
                        
                            TreeNodeModel(
                                node_id=100,
                                label="DRAW GA-001",
                                attributes={
                                    "Type": AttributeValue(1100, "DRAW"),
                                    "Name": AttributeValue(1101, "GA-001"),
                                },
                                children=[
                                
                                    TreeNodeModel(
                                        node_id=1000,
                                        label="SHEE 001",
                                        attributes={
                                            "Type": AttributeValue(1200, "SHEE"),
                                            "Name": AttributeValue(1201, "001"),
                                        },
                                        children=[
                                        
                                            TreeNodeModel(
                                                node_id=2000,
                                                label="NOTE N-1",
                                                attributes={
                                                    "Type": AttributeValue(1300, "NOTE"),
                                                    "Name": AttributeValue(1301, "N-1"),
                                                },
                                                children=[
                                                
                                                    TreeNodeModel(
                                                        node_id=2100,
                                                        label="TEXP TEXT",
                                                        attributes={
                                                            "Type": AttributeValue(1310, "TEXP"),
                                                        },
                                                        children=[]
                                                    ),
        
                                                    TreeNodeModel(
                                                        node_id=2101,
                                                        label="STRA",
                                                        attributes={
                                                            "Type": AttributeValue(1320, "STRA"),
                                                            "StartX": AttributeValue(1321, "0"),
                                                            "StartY": AttributeValue(1322, "0"),
                                                            "EndX": AttributeValue(1323, "10"),
                                                            "EndY": AttributeValue(1324, "0"),
                                                        },
                                                        children=[]
                                                    ),
        
                                                    TreeNodeModel(
                                                        node_id=2102,
                                                        label="RECT BOX",
                                                        attributes={
                                                            "Type": AttributeValue(1330, "RECT"),
                                                        },
                                                        children=[]
                                                    ),
        
                                                    TreeNodeModel(
                                                        node_id=2103,
                                                        label="CIRC",
                                                        attributes={
                                                            "Type": AttributeValue(1340, "CIRC"),
                                                        },
                                                        children=[]
                                                    ),
        
                                                    TreeNodeModel(
                                                        node_id=2104,
                                                        label="ARC",
                                                        attributes={
                                                            "Type": AttributeValue(1350, "ARC"),
                                                        },
                                                        children=[]
                                                    ),
        
                                                    TreeNodeModel(
                                                        node_id=2105,
                                                        label="OUTL BORDER",
                                                        attributes={
                                                            "Type": AttributeValue(1360, "OUTL"),
                                                        },
                                                        children=[
                                                        
                                                            TreeNodeModel(
                                                                node_id=2106,
                                                                label="VRTX 1",
                                                                attributes={
                                                                    "Type": AttributeValue(1370, "VRTX"),
                                                                    "X": AttributeValue(1371, "0"),
                                                                    "Y": AttributeValue(1372, "0"),
                                                                },
                                                                children=[]
                                                            ),
        
                                                            TreeNodeModel(
                                                                node_id=2107,
                                                                label="VRTX 2",
                                                                attributes={
                                                                    "Type": AttributeValue(1380, "VRTX"),
                                                                    "X": AttributeValue(1381, "100"),
                                                                    "Y": AttributeValue(1382, "0"),
                                                                },
                                                                children=[]
                                                            ),
        
                                                        ]
                                                    ),
        
                                                ],
                                            )
        
                                        ],
                                    )
        
                                ],
                            )
        
                        ],
                    )
        
                ],
            )
        
        ]