from .base import ElementSchema, base_attributes


class Stra(ElementSchema):

    TYPE = "STRA"

    @classmethod
    def allowed_children(cls):
        return []

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {
            "Start": {"default": "", "editable": True},
            "End": {"default": "", "editable": True},
        }
