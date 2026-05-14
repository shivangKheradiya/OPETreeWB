def load_element_schema(element_type):
    """
    Load merged schema for a given element:
    base + specific type
    """

    from opetreewb.SKET.hierarchy.base import ElementSchema

    try:
        module = __import__(
            f"opetreewb.SKET.hierarchy.{element_type.lower()}", fromlist=["*"]
        )

        class_name = element_type.capitalize()
        element_class = getattr(module, class_name)

    except Exception:
        element_class = ElementSchema

    # ✅ Merge base + specific
    base_attrs = ElementSchema.attributes()
    type_attrs = element_class.attributes()

    merged = {**base_attrs, **type_attrs}

    return merged
