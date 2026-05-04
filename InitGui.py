import sys
from pathlib import Path
import FreeCADGui
import FreeCAD

# -------------------------------------------------
# Add src/ to Python path (FreeCAD-safe way)
# -------------------------------------------------
WB_ROOT = Path(FreeCAD.getHomePath()) / "Mod" / "OPETreeWB"
SRC_PATH = WB_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

# -------------------------------------------------
# Register the workbench
# -------------------------------------------------
from opetreewb.app.workbench import OPETreeWorkbench

FreeCADGui.addWorkbench(OPETreeWorkbench())