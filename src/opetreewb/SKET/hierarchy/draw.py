from .base import ElementSchema, base_attributes


class Draw(ElementSchema):
    """
    Drawing container inside a department
    """

    TYPE = "DRAW"

    @classmethod
    def allowed_children(cls):
        return ["SHEE"]

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {
            "Title": {"default": "", "editable": True},
            "Number": {"default": "", "editable": True},
        }

