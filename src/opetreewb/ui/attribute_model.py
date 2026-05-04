"""
AttributeTableModel

UI-only model representing attribute rows.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class AttributeRow:
    attribute: str
    value: str
    data_id: str


class AttributeTableModel:
    """
    Holds attribute data for UI rendering.
    """

    def __init__(self):
        # Dummy attribute data
        self.rows: List[AttributeRow] = [
            AttributeRow("Name", "Demo Node", "101"),
            AttributeRow("Type", "SKET", "102"),
            AttributeRow("Owner", "System", "103"),
            AttributeRow("Status", "Active", "104"),
        ]

    def clear(self):
        self.rows.clear()