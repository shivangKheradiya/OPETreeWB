from .base import ElementSchema, base_attributes


class Shee(ElementSchema):
    """
    Sheet inside a drawing
    """

    TYPE = "SHEE"

    @classmethod
    def allowed_children(cls):
        return ["NOTE"]   # leaf node (for now)

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {
            "SheetNumber": {
                "default": "",
                "datatype": "int",
                "editable": True,
                "kind": "user",
            },
            "Scale": {
                "default": "",
                "datatype": "string",
                "editable": False,
                "kind": "system",
            },
        }
