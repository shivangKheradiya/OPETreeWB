from .base import ElementSchema, base_attributes


class Arc(ElementSchema):

    TYPE = "ARC"

    @classmethod
    def allowed_children(cls):
        return []

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {
            "Radius": {"default": "", "editable": True},
            "Angle": {"default": "", "editable": True},
        }