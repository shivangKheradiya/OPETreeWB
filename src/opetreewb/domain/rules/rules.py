from dataclasses import dataclass


@dataclass
class RuleResult:
    allowed: bool
    reason: str = ""

    @staticmethod
    def ok():
        return RuleResult(True, "")

    @staticmethod
    def deny(reason: str):
        return RuleResult(False, reason)