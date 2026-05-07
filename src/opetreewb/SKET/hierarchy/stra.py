from .base import ElementSchema, base_attributes


class Stra(ElementSchema):

    TYPE = "STRA"

    @classmethod
    def allowed_children(cls):
        return []

    @classmethod
    def attributes(cls):
        return base_attributes(cls.TYPE) | {
            # ✅ GEOMETRY ATTRIBUTES
            "StartX": {
                "default": "0",
                "datatype": "float",
                "editable": True,
                "kind": "user",
            },
            "StartY": {
                "default": "0",
                "datatype": "float",
                "editable": True,
                "kind": "user",
            },
            "EndX": {
                "default": "10",
                "datatype": "float",
                "editable": True,
                "kind": "user",
            },
            "EndY": {
                "default": "0",
                "datatype": "float",
                "editable": True,
                "kind": "user",
            },
        }
