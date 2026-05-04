"""
FreeCAD GUI entry point for the OPETree workbench.

This module is responsible for:
- creating the OPETreeWorkbench instance
- registering it with FreeCADGui

IMPORTANT:
- This module contains NO business logic
- It must remain side-effect safe except for registration
"""

import FreeCADGui
from opetreewb.app.workbench import OPETreeWorkbench


def register_workbench():
    """
    Register OPETreeWorkbench with FreeCAD.

    This function exists to:
    - isolate side effects
    - make the entry-point importable
    """
    FreeCADGui.addWorkbench(OPETreeWorkbench())


# FreeCAD expects registration at import time
register_workbench()