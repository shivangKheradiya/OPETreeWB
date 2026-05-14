from ..schema.attribute_ids import get_attr_id
from .base import ElementSchema, base_attributes


class Arc(ElementSchema):
    TYPE = "ARC"

    @classmethod
    def allowed_children(cls):
        return []

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {
            "CenterX": {
                "default": "0",
                "datatype": "float",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("CenterX"),
            },
            "CenterY": {
                "default": "0",
                "datatype": "float",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("CenterY"),
            },
            "Radius": {
                "default": "0",
                "datatype": "float",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("Radius"),
            },
            "StartAngle": {
                "default": "0",
                "datatype": "float",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("StartAngle"),
            },
            "EndAngle": {
                "default": "90",
                "datatype": "float",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("EndAngle"),
            },
            "LineStyle": {
                "default": "Solid",
                "datatype": "string",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("LineStyle"),
            },
            "LineWidth": {
                "default": 2.0,
                "datatype": "float",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("LineWidth"),
            },
            "LineColor": {
                "default": [0, 0, 0],
                "datatype": "list",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("LineColor"),
            },
        }
