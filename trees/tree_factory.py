# OPETreeWB/trees/tree_factory.py

from OPETreeWB.trees.ope_desi_tree import OPEDesiTree
from OPETreeWB.trees.ope_dict_tree import OPEDictTree


TREE_BY_DOMAIN = {
    "DESI": OPEDesiTree,
    "DICT": OPEDictTree,
}


def create_tree(domain: str, provider, parent=None):
    """
    Factory to create the correct tree for the selected domain.
    """
    try:
        tree_cls = TREE_BY_DOMAIN[domain.upper()]
    except KeyError:
        raise RuntimeError(f"Unsupported domain: {domain}")

    return tree_cls(provider, parent)