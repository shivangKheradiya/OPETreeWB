from .base import ElementSchema, base_attributes
from ..schema.attribute_ids import get_attr_id


class Texp(ElementSchema):

    TYPE = "TEXP"

    @classmethod
    def allowed_children(cls):
        return []

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {

            "Text": {
                "default": "Text",
                "datatype": "string",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("Text"),
            },
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
            "FontSize": {
                "default": "12",
                "datatype": "float",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("FontSize"),
            },
            "LineColor": {
                "default": [0, 0, 0],
                "datatype": "list",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("LineColor"),
            },
        }