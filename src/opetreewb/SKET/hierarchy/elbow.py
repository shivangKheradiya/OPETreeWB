from .base import ElementSchema


class Elbow(ElementSchema):

    TYPE = "ELBOW"

    @classmethod
    def allowed_children(cls):
        return []