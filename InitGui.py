import sys
from pathlib import Path
import FreeCADGui
import FreeCAD

# -------------------------------------------------
# Add src/ to Python path (FreeCAD-safe way)
# -------------------------------------------------
WB_ROOT = Path(FreeCAD.getHomePath()) / "Mod" / "OPETreeWB"
SRC_PATH = WB_ROOT / "src"
VENDOR_PATH = WB_ROOT / "vendor"
OPE_DB_API_PATH = VENDOR_PATH / "OPE_DB_API"
PYDBML_PARENT = VENDOR_PATH / "PyDBML"

paths = [
    SRC_PATH,
    OPE_DB_API_PATH,
    PYDBML_PARENT,
]

for p in paths:
    if p.exists() and str(p) not in sys.path:
        sys.path.insert(0, str(p))

# -------------------------------------------------
# Register the workbench
# -------------------------------------------------
from opetreewb.app.workbench import OPETreeWorkbench

FreeCADGui.addWorkbench(OPETreeWorkbench())