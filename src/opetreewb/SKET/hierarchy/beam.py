from .base import ElementSchema


class Beam(ElementSchema):

    TYPE = "BEAM"

    @classmethod
    def allowed_children(cls):
        return []