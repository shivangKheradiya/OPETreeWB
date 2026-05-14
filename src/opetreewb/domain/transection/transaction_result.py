from dataclasses import dataclass


@dataclass
class TransactionResult:
    success: bool
    message: str = ""
