from ..schema.attribute_ids import get_attr_id
from .base import ElementSchema, base_attributes


class Regi(ElementSchema):
    TYPE = "REGI"

    @classmethod
    def allowed_children(cls):
        return ["DRAW"]

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {
            "RegionName": {
                "default": "",
                "datatype": "string",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("RegionName"),
            },
        }
