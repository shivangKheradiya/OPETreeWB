from .base import ElementSchema, base_attributes


class Rect(ElementSchema):

    TYPE = "RECT"

    @classmethod
    def allowed_children(cls):
        return []

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {
            "Width": {"default": "", "editable": True},
            "Height": {"default": "", "editable": True},
        }
