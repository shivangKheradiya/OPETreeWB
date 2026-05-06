from .base import ElementSchema, base_attributes


class Outl(ElementSchema):

    TYPE = "OUTL"

    @classmethod
    def allowed_children(cls):
        return ["VRTX"]

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE)
