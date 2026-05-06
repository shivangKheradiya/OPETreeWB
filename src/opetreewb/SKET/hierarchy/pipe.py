from .base import ElementSchema


class Pipe(ElementSchema):

    TYPE = "PIPE"

    @classmethod
    def allowed_children(cls):
        return ["ELBOW", "FLANGE"]
