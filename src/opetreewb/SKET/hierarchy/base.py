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
        "Name": {"default": "", "editable": True},
        "Type": {"default": type_name, "editable": False},
        "Owner": {"default": "", "editable": False},
    }
