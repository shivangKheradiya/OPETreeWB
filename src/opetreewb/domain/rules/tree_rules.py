from opetreewb.domain.rules.rules import RuleResult


class TreeRules:
    """
    Declarative rules for tree operations.
    Backend integration will enforce these later.
    """

    @staticmethod
    def can_create_node(parent_node, element_type) -> RuleResult:
        if parent_node is None:
            return RuleResult.deny("Parent node does not exist")

        if not element_type:
            return RuleResult.deny("Element type is required")

        # Future rules (placeholder)
        # - schema hierarchy
        # - session state
        # - permissions

        return RuleResult.ok()

    @staticmethod
    def can_delete_node(node) -> RuleResult:
        if node is None:
            return RuleResult.deny("Node does not exist")

        # Example future rule:
        # if node.is_root:
        #     return RuleResult.deny("Root nodes cannot be deleted")

        return RuleResult.ok()