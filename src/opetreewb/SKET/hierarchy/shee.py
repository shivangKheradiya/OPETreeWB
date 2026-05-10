from .base import ElementSchema, base_attributes
from ..schema.attribute_ids import get_attr_id


class Shee(ElementSchema):
    """
    Sheet inside a drawing
    """

    TYPE = "SHEE"

    @classmethod
    def allowed_children(cls):
        return ["NOTE"]   # leaf node (for now)

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {

            "SheetNumber": {
                "default": "0",                 # ✅ FIXED (was "")
                "datatype": "int",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("SheetNumber"),   # ✅ ADDED
            },

            "Scale": {
                "default": "",
                "datatype": "string",
                "editable": False,
                "kind": "system",
                "id": get_attr_id("Scale"),         # ✅ ADDED
            },
        }