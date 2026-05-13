from .base import ElementSchema, base_attributes
from ..schema.attribute_ids import get_attr_id


class Note(ElementSchema):

    TYPE = "NOTE"

    @classmethod
    def allowed_children(cls):
        return [
            "TEXP",
            "STRA",
            "RECT",
            "CIRC",
            "ARC",
            "HEXA",
            "ELLI",
        ]

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {

            "Text": {
                "default": "",
                "datatype": "string",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("Text"),
            },
        }