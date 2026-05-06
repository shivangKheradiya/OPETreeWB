from .base import ElementSchema


class Structure(ElementSchema):

    TYPE = "STRUCTURE"

    @classmethod
    def allowed_children(cls):
        return ["BEAM"]