from ..schema.attribute_ids import get_attr_id
from .base import ElementSchema, base_attributes


class Draw(ElementSchema):
    """
    Drawing container inside a department
    """

    TYPE = "DRAW"

    @classmethod
    def allowed_children(cls):
        return ["SHEE"]

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {
            "Title": {
                "default": "",
                "datatype": "string",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("Title"),
            },
            "Number": {
                "default": "",
                "datatype": "string",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("Number"),
            },
        }
