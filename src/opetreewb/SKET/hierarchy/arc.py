from .base import ElementSchema, base_attributes
from ..schema.attribute_ids import get_attr_id

class Arc(ElementSchema):

    TYPE = "ARC"

    @classmethod
    def allowed_children(cls):
        return []

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {
            "Radius": {
                "default": "0",
                "datatype": "float",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("Radius"),
            },

            "Angle": {
                "default": "0",
                "datatype": "float",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("Angle"),
            },
        }