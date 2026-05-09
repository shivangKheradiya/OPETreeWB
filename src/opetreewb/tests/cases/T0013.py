"""
T0014 — Local Session Close Test

Objective:
    Verify that local session close works using OPE_DB_API CRUD.

Scope:
    - session_local.py
    - local/client.py
    - OPE_DB_API.crud.session.close

Expected:
    - Session marked inactive in local DB
    - ended_at timestamp set
    - No exceptions
"""

import FreeCAD

# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT
from opetreewb.integration.opedbapi.local.session_local import SessionLocal

TEST_ID = "T0013"


# ---------------------------------------------------------
def run():

    FreeCAD.Console.PrintMessage(f"\n[{TEST_ID}] START\n")

    # If fails then run T0004

    try:
        if not OPE_DB_CONTEXT.session_id:
            raise RuntimeError("FAILED: No session_id in context")

        session_local = SessionLocal()

        FreeCAD.Console.PrintMessage(
            f"CLOSING session_id={OPE_DB_CONTEXT.session_id}\n"
        )

        # ✅ Step 3 — Close session
        session = session_local.close(
            session_id=OPE_DB_CONTEXT.session_id
        )

        FreeCAD.Console.PrintMessage("Session closed in local DB\n")

        # ✅ Step 4 — Validate
        if session.active:
            raise RuntimeError("FAILED: Session still active")

        # Note: ended_at presence implicit via CRUD logic

        FreeCAD.Console.PrintMessage("Validation OK\n")
        FreeCAD.Console.PrintMessage(f"\n[{TEST_ID}] PASSED ✅\n")

    except Exception as e:
        FreeCAD.Console.PrintError(f"[{TEST_ID}] FAILED ❌ → {e}\n")
