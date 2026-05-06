from .base import ElementSchema, base_attributes


class Elli(ElementSchema):

    TYPE = "ELLI"

    @classmethod
    def allowed_children(cls):
        return []

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {
            "MajorRadius": {"default": "", "editable": True},
            "MinorRadius": {"default": "", "editable": True},
        }
