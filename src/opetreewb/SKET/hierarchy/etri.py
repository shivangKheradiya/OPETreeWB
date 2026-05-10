from .base import ElementSchema, base_attributes
from ..schema.attribute_ids import get_attr_id


class Etri(ElementSchema):

    TYPE = "ETRI"

    @classmethod
    def allowed_children(cls):
        return []

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE)