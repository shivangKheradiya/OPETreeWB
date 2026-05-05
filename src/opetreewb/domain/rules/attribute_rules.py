from opetreewb.domain.rules.rules import RuleResult


class AttributeRules:
    """
    Declarative rules for attribute operations.
    """

    READ_ONLY_ATTRIBUTES = {
        "Type",
        "Owner",
    }

    @staticmethod
    def can_update(attribute_name, data_id, new_value) -> RuleResult:
        if not data_id:
            return RuleResult.deny("Missing data_id")

        if attribute_name in AttributeRules.READ_ONLY_ATTRIBUTES:
            return RuleResult.deny(
                f"Attribute '{attribute_name}' is read-only"
            )

        # Future rules (placeholders):
        # - session state
        # - type coercion
        # - value range
        # - permissions

        return RuleResult.ok()