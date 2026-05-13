from .base import ElementSchema, base_attributes
from ..schema.attribute_ids import get_attr_id

class Stra(ElementSchema):

    TYPE = "STRA"

    @classmethod
    def allowed_children(cls):
        return []

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {
            # ✅ GEOMETRY ATTRIBUTES
            "StartX": {
                "default": "0",
                "datatype": "float",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("StartX"),
            },
            "StartY": {
                "default": "0",
                "datatype": "float",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("StartY"),
            },
            "EndX": {
                "default": "10",
                "datatype": "float",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("EndX"),
            },
            "EndY": {
                "default": "0",
                "datatype": "float",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("EndY"),
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
                "default": [0.0, 0.0, 0.0],  # black
                "datatype": "list",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("LineColor"),
            },
        }
