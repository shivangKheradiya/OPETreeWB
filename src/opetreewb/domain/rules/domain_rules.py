"""
Domain-level rules for OPETree.

This module defines invariant rules per domain.
No FreeCAD, no database, no side effects.
"""

DOMAIN_RULES = {
    "DESI": {
        "RootType": "DESIWLD",
        "MaxRoots": None,
    },
    "DICT": {
        "RootType": "DICTWLD",
        "MaxRoots": None,
    },
}
