#OPETreeWB\src\opetreewb\domain\plugin\plugin_loader.py

import sys
from pathlib import Path

_OPE_PATHS = []
_OPE_PLUGIN_PATHS = []

def register_sys_path(path: str):
    p = Path(path)

    if not p.exists():
        return

    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

    if path not in _OPE_PATHS:
        _OPE_PATHS.append(path)


def get_ope_paths():
    return list(_OPE_PATHS)

def register_plugin_path(path: str):
    if path not in _OPE_PLUGIN_PATHS:
        _OPE_PLUGIN_PATHS.append(path)
    register_sys_path(path=path)

def get_plugin_paths():
    return list(_OPE_PLUGIN_PATHS)