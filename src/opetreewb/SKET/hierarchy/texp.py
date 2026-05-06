from .base import ElementSchema, base_attributes


class Texp(ElementSchema):

    TYPE = "TEXP"

    @classmethod
    def allowed_children(cls):
        return []

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {
            "Text": {"default": "", "editable": True},
            "Font": {"default": "Arial", "editable": True},
        }