from .base import ElementSchema


class Pipeline(ElementSchema):

    TYPE = "PIPELINE"

    @classmethod
    def allowed_children(cls):
        return ["PIPE"]