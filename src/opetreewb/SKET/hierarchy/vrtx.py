from .base import ElementSchema, base_attributes


class Vrtx(ElementSchema):

    TYPE = "VRTX"

    @classmethod
    def allowed_children(cls):
        return []

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {
            "X": {"default": "", "editable": True},
            "Y": {"default": "", "editable": True},
        }