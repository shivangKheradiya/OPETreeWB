from .base import ElementSchema


class Flange(ElementSchema):

    TYPE = "FLANGE"

    @classmethod
    def allowed_children(cls):
        return []