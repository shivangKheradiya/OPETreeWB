from .base import ElementSchema, base_attributes


class Etri(ElementSchema):

    TYPE = "ETRI"

    @classmethod
    def allowed_children(cls):
        return []

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE)