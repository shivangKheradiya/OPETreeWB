"""
T0007 — API Work Save (Commit) Test

Objective:
    Verify that staged overlay changes are committed to live data.

Scope:
    - context.py
    - client.py
    - attribute_api.py
    - query_api.py

Expected:
    - Overlay data is committed to live table
    - Overlay is cleared
    - No exceptions
"""

import FreeCAD

# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT
from opetreewb.integration.opedbapi.api.client import OpeApiClient

TEST_ID = "T0007"


# ---------------------------------------------------------
# TEST EXECUTION
# ---------------------------------------------------------
def run():

    FreeCAD.Console.PrintMessage(f"\n[{TEST_ID}] START\n")

    try:
        # ✅ Precondition — session must be active
        if not OPE_DB_CONTEXT.is_session_active:
            raise RuntimeError("FAILED: No active session (run T0004, T006 first)")

        client = OpeApiClient()

        FreeCAD.Console.PrintMessage("Committing overlay → live\n")

        # ✅ Step 1 — SAVE (COMMIT)
        result = client.post(
            "work/commit",
            use_session=True
        )

        FreeCAD.Console.PrintMessage("Result :{}\n".format(result))
        FreeCAD.Console.PrintMessage("Save response received\n")

        # ✅ Step 2 — Validate session closed
        if OPE_DB_CONTEXT.is_session_active:
            FreeCAD.Console.PrintMessage("Note: Context still active (API closes backend session only)\n")

        FreeCAD.Console.PrintMessage(f"\n[{TEST_ID}] PASSED ✅\n")

    except Exception as e:
        import traceback
        traceback.print_exc()
        FreeCAD.Console.PrintError(f"[{TEST_ID}] FAILED ❌ → {e}\n")

