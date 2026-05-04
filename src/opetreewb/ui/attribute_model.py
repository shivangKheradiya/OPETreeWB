"""
AttributeTableModel

Model representing attribute rows.
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
        self.rows: List[AttributeRow] = []

    def clear(self):
        self.rows.clear()