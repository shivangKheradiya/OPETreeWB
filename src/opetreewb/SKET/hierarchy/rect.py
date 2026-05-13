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