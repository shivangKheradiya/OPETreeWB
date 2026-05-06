from .base import ElementSchema, base_attributes


class Circ(ElementSchema):

    TYPE = "CIRC"

    @classmethod
    def allowed_children(cls):
        return []

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {
            "Radius": {"default": "", "editable": True},
        }
