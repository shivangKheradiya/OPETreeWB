from .base import ElementSchema


class Zone(ElementSchema):

    TYPE = "ZONE"

    @classmethod
    def allowed_children(cls):
        return ["PIPELINE", "STRUCTURE"]
