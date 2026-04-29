# OPETreeWB/trees/ope_dict_tree.py

"""
OPEDictTree

Dictionary / lookup tree backed by PyDBML.
This tree is FLAT (non-hierarchical).
"""

from OPETreeWB.trees.ope_tree_base import OPETree
from OPETreeWB.adapters.pydbml_adapter import PyDBMLTreeAdapter
from PyDBML.core import ElementRef


class OPEDictTree(OPETree):
    """
    OPE Dictionary Tree implementation.

    Displays all dictionary nodes (Type == 'DICT') in a flat list.
    """

    def __init__(self, provider, parent=None):
        super().__init__(provider,parent)