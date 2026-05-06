#OPETreeWB\src\opetreewb\domain\rules\tree_rules.py

from opetreewb.domain.rules.rules import RuleResult
from opetreewb.domain.schema.schema_loader import get_schema
from opetreewb.messaging.reporter import Reporter

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

        schema = get_schema(parent_node.type)
        
        if not schema:
            Reporter.error(
                f"[TreeRules] No schema found for {parent_node.type}"
            )

            return RuleResult.deny(
                f"No schema found for {parent_node.type}"
            )

        allowed = schema.allowed_children()

        if element_type not in allowed:
            Reporter.error(
                f"[TreeRules] {element_type} not allowed under {parent_node.type}"
            )
            return RuleResult.deny(
                f"{element_type} not allowed under {parent_node.type}"
            )
        
        Reporter.info(
            f"[TreeRules] {element_type} allowed under {parent_node.type}"
        )
        return RuleResult.ok()

    @staticmethod
    def can_delete_node(node) -> RuleResult:
        if node is None:
            return RuleResult.deny("Node does not exist")

        # Example future rule:
        # if node.is_root:
        #     return RuleResult.deny("Root nodes cannot be deleted")

        return RuleResult.ok()