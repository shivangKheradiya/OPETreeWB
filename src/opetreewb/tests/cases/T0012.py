"""
T0013 — Local Session Start Test

Objective:
    Verify that local session start works using OPE_DB_API CRUD.

Scope:
    - session_local.py
    - local/client.py
    - OPE_DB_API.crud.session.start

Expected:
    - Session created in local DB
    - Session row active = True
    - No exceptions
"""

import FreeCAD

# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------
from opetreewb.integration.opedbapi.core.context import OPE_DB_CONTEXT
from opetreewb.integration.opedbapi.local.session_local import SessionLocal
from opetreewb.domain.identity.snowflake import SnowflakeIDGenerator

TEST_ID = "T0012"


# ---------------------------------------------------------
def run():

    FreeCAD.Console.PrintMessage(f"\n[{TEST_ID}] START\n")

    # If fails then run T0004

    try:
        # ✅ Configure context (if not already)
        if not OPE_DB_CONTEXT.code:
            OPE_DB_CONTEXT.configure(
                code="XYZ",
                domain="SKET",
                username="Shivang",
                hostname="PCS",
            )

        id_gen = SnowflakeIDGenerator()

        session_local = SessionLocal()

        FreeCAD.Console.PrintMessage(f"STARTING session_id={OPE_DB_CONTEXT.session_id}\n")

        # ✅ Start session
        session = session_local.start(
            session_id=OPE_DB_CONTEXT.session_id,
            username=OPE_DB_CONTEXT.username,
        )

        FreeCAD.Console.PrintMessage("Session created in local DB\n")

        # ✅ Basic validation
        if not session:
            raise RuntimeError("FAILED: No session returned")

        if not session.active:
            raise RuntimeError("FAILED: Session not active")

        if session.session_id != OPE_DB_CONTEXT.session_id:
            raise RuntimeError("FAILED: Session ID mismatch")

        FreeCAD.Console.PrintMessage("Validation OK\n")
        FreeCAD.Console.PrintMessage(f"\n[{TEST_ID}] PASSED ✅\n")

    except Exception as e:
        FreeCAD.Console.PrintError(f"[{TEST_ID}] FAILED ❌ → {e}\n")
