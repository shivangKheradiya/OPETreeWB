from .base import ElementSchema, base_attributes
from ..schema.attribute_ids import get_attr_id


class Rect(ElementSchema):

    TYPE = "RECT"

    @classmethod
    def allowed_children(cls):
        return []

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {

            "Width": {
                "default": "0",
                "datatype": "float",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("Width"),
            },

            "Height": {
                "default": "0",
                "datatype": "float",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("Height"),
            },
        }