from .base import ElementSchema, base_attributes
from ..schema.attribute_ids import get_attr_id


class Vrtx(ElementSchema):

    TYPE = "VRTX"

    @classmethod
    def allowed_children(cls):
        return []

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {

            "X": {
                "default": "0",
                "datatype": "float",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("X"),
            },

            "Y": {
                "default": "0",
                "datatype": "float",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("Y"),
            },
        }