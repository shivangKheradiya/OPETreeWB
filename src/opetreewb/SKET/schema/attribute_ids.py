"""
SKET Attribute ID Registry
"""

ATTR_ID = {
    # Base
    "Name": 1,
    "Type": 2,
    "Owner": 3,

    # Geometry
    "StartX": 4,
    "StartY": 5,
    "EndX": 6,
    "EndY": 7,

    "Radius": 8,
    "Angle": 9,

    "Description": 10,
    "Title": 11,
    "Number": 12,
    "MajorRadius": 13,
    "MinorRadius": 14,
    "Text": 15,
    "Width": 16,
    "Height": 17,
    "RegionName": 18,
    "SheetNumber": 19,
    "Scale": 20,
    "Font": 21,
    "X": 22,
    "Y": 23,
}

def get_attr_id(name):
    if name not in ATTR_ID:
        raise KeyError(f"{name} not registered in ATTR_ID")
    return ATTR_ID[name]


ATTR_NAME_BY_ID = {v: k for k, v in ATTR_ID.items()}

def get_attr_name(attr_id):
    return ATTR_NAME_BY_ID.get(attr_id, f"ATTR_{attr_id}")
