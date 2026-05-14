from ..schema.attribute_ids import get_attr_id
from .base import ElementSchema, base_attributes


class Dept(ElementSchema):
    """
    Department (top-level container for drawings)
    """

    TYPE = "DEPT"

    @classmethod
    def allowed_children(cls):
        return ["REGI"]

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {
            "Description": {
                "default": "",
                "datatype": "string",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("Description"),
            },
        }
