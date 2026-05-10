from .base import ElementSchema, base_attributes
from ..schema.attribute_ids import get_attr_id


class Outl(ElementSchema):

    TYPE = "OUTL"

    @classmethod
    def allowed_children(cls):
        return ["VRTX"]

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE)
