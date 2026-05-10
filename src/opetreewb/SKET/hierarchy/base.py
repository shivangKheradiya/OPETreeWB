from ..schema.attribute_ids import get_attr_id

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
            "id": get_attr_id("Name"),
        },        
        "Type": {
            "default": type_name,
            "datatype": "string",
            "editable": False,
            "kind": "system",
            "id": get_attr_id("Type"),
        },
        "Owner": {
            "default": "",
            "datatype": "string",
            "editable": False,
            "kind": "system",
            "id": get_attr_id("Owner"),
        },
    }
