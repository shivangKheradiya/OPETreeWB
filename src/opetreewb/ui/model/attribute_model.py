"""
AttributeTableModel

Model representing attribute rows.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class AttributeRow:
    def __init__(self, attribute, value, data_id, meta):
        self.attribute = attribute
        self.value = value
        self.data_id = data_id
        self.meta = meta


class AttributeTableModel:
    """
    Holds attribute data for UI rendering.
    """

    def __init__(self):
        self.rows: List[AttributeRow] = []

    def clear(self):
        self.rows.clear()