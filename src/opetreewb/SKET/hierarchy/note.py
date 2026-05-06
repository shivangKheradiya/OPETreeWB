from .base import ElementSchema, base_attributes


class Note(ElementSchema):

    TYPE = "NOTE"

    @classmethod
    def allowed_children(cls):
        return [
            "TEXP",
            "STRA",
            "RECT",
            "CIRC",
            "ARC",
            "HEXA",
            "ELLI",
            "ETRI",
            "OUTL",
        ]

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {
            "Text": {"default": "", "editable": True},
        }