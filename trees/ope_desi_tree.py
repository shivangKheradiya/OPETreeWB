# trees/ope_desi_tree.py
"""
OPEDesiTree

DESI domain tree backed by PyDBML.
"""
from PyDBML.core import ElementRef
from OPETreeWB.trees.ope_tree_base import OPETree
from OPETreeWB.adapters.pydbml_adapter import PyDBMLTreeAdapter


class OPEDesiTree(OPETree):
    """
    OPE DESI Tree implementation.
    """

    def __init__(self, provider, parent=None):
        super().__init__(provider,parent)
