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
        }
