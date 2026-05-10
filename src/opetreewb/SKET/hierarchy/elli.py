from .base import ElementSchema, base_attributes
from ..schema.attribute_ids import get_attr_id


class Elli(ElementSchema):

    TYPE = "ELLI"

    @classmethod
    def allowed_children(cls):
        return []

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {

            "MajorRadius": {
                "default": "0",
                "datatype": "float",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("MajorRadius"),
            },

            "MinorRadius": {
                "default": "0",
                "datatype": "float",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("MinorRadius"),
            },
        }