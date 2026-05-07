"""
T0005 — API Session Close Test

Objective:
    Verify that API-based session close correctly deactivates the session
    and updates runtime context.

Scope:
    - context.py
    - client.py
    - session_api.py

Expected:
    - Session is closed in backend
    - Context session cleared
    - No exceptions
"""

import FreeCAD

# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------
from opetreewb.integration.opedbapi.core.context import OPE_DB_CONTEXT
from opetreewb.integration.opedbapi.api.session_api import SessionAPI

TEST_ID = "T0005"


# ---------------------------------------------------------
# TEST EXECUTION
# ---------------------------------------------------------
def run():

    FreeCAD.Console.PrintMessage(f"\n[{TEST_ID}] START\n")

    try:
        # ✅ Precondition — session must exist
        if not OPE_DB_CONTEXT.is_session_active:
            raise RuntimeError("FAILED: No active session (run T0004 first)")

        session_id = OPE_DB_CONTEXT.session_id
        FreeCAD.Console.PrintMessage(f"Closing Session: {session_id}\n")

        api = SessionAPI()

        # ✅ Step 1 — Close session
        api.close()

        # ✅ Step 2 — Validate context
        FreeCAD.Console.PrintMessage("\nRESULT:\n")
        FreeCAD.Console.PrintMessage(f"  Context Active: {OPE_DB_CONTEXT.is_session_active}\n")

        # ✅ Assertions
        if OPE_DB_CONTEXT.is_session_active:
            raise RuntimeError("FAILED: session still active")

        FreeCAD.Console.PrintMessage(f"\n[{TEST_ID}] PASSED ✅\n")

    except Exception as e:
        FreeCAD.Console.PrintError(f"[{TEST_ID}] FAILED ❌ → {e}\n")
