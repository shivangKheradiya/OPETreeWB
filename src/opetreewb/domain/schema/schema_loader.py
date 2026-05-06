#OPETreeWB\src\opetreewb\domain\schema\schema_loader.py

import importlib, sys
from opetreewb.domain.plugin.plugin_loader import get_plugin_paths

_SCHEMA_CACHE = {}
DEV_MODE = True

def get_schema(type_name: str):

    if not type_name:
        return None

    if not DEV_MODE and type_name in _SCHEMA_CACHE:
        return _SCHEMA_CACHE[type_name]

    module_name = type_name.lower()

    # ✅ search all plugin paths
    for base in get_plugin_paths():
        try:
            full_module = f"{base}.hierarchy.{module_name}"
            if DEV_MODE and full_module in sys.modules:
                module = importlib.reload(sys.modules[full_module])
            else:
                module = importlib.import_module(full_module)
        except ModuleNotFoundError:
            continue

        for attr in dir(module):
            obj = getattr(module, attr)
            if hasattr(obj, "TYPE") and obj.TYPE == type_name:
                _SCHEMA_CACHE[type_name] = obj
                return obj

    return None
