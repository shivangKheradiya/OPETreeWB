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
        },        
        "Type": {
            "default": "SHEE",
            "datatype": "string",
            "editable": False,
            "kind": "system",
        },
        "Owner": {
            "default": "",
            "datatype": "string",
            "editable": False,
            "kind": "system",
        },
    }
