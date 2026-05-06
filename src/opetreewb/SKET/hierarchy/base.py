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