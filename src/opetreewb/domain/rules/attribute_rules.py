from opetreewb.domain.rules.rules import RuleResult
from opetreewb.domain.schema.schema_loader import get_schema

class AttributeRules:
    """
    Declarative rules for attribute operations.
    """

    @staticmethod
    def can_update(node, attribute_name, data_id, new_value) -> RuleResult:

        # ✅ 1. Get node type
        type_attr = node.attributes.get("Type")
        if not type_attr:
            return RuleResult.deny("Missing Type")

        schema = get_schema(type_attr.value)
        if not schema:
            return RuleResult.deny("Schema not found")

        attr_meta = schema.attributes().get(attribute_name)
        if not attr_meta:
            return RuleResult.deny(f"Unknown attribute '{attribute_name}'")

        # ✅ 2. Check editable flag
        if not attr_meta.get("editable", True):
            return RuleResult.deny(
                f"Attribute '{attribute_name}' is read-only"
            )

        return RuleResult.ok()