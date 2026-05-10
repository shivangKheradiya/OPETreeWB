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
                "default": "",
                "datatype": "string",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("Text"),   # ✅ reuse same as NOTE
            },

            "Font": {
                "default": "Arial",
                "datatype": "string",
                "editable": True,
                "kind": "user",
                "id": get_attr_id("Font"),
            },
        }