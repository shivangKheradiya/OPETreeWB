from .base import ElementSchema, base_attributes


class Regi(ElementSchema):

    TYPE = "REGI"

    @classmethod
    def allowed_children(cls):
        return ["DRAW"]

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {
            "RegionName": {"default": "", "editable": True},
        }