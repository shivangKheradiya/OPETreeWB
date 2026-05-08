class ElementSchema:
    """
    Base class for all hierarchy elements.
    """

    TYPE = "BASE"

    @classmethod
    def attributes(cls):
        return {}

    @classmethod
    def allowed_children(cls):
        return []
    

# ✅ Common helper
def base_attributes(type_name):
    return {
        "Name": {
            "default": "",
            "datatype": "string",
            "editable": True,
            "kind": "user",
            "id": 1,
        },        
        "Type": {
            "default": "SHEE",
            "datatype": "string",
            "editable": False,
            "kind": "system",
            "id": 2,
        },
        "Owner": {
            "default": "",
            "datatype": "string",
            "editable": False,
            "kind": "system",
            "id": 3,
        },
    }
