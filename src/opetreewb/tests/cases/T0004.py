"""
T0004 — API Session Start Test

Objective:
    Verify that API-based session start works and updates runtime context.

Scope:
    - context.py
    - config.py
    - client.py
    - session_api.py

Expected:
    - Session ID generated
    - Session active in context
    - No exceptions
"""

import FreeCAD

# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------
from opetreewb.integration.opedbapi.core.config import OPE_DB_CONFIG
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT
from opetreewb.integration.opedbapi.api.session_api import SessionAPI


TEST_ID = "T0004"
# ---------------------------------------------------------
# TEST EXECUTION
# ---------------------------------------------------------
def run():

    FreeCAD.Console.PrintMessage(f"[{TEST_ID}] START\n")

    # ✅ Step 1 — Configure API
    OPE_DB_CONFIG._base_url = "http://127.0.0.1:8000"

    # ✅ Step 2 — Configure context
    OPE_DB_CONTEXT.configure(
        code="XYZ",
        domain="SKET",
        username="Shivang",
        hostname="PCS",
    )

    FreeCAD.Console.PrintMessage("Context configured:\n")
    FreeCAD.Console.PrintMessage("  Code:{}\n".format(OPE_DB_CONTEXT.code))
    FreeCAD.Console.PrintMessage("  Domain:{}\n".format(OPE_DB_CONTEXT.domain))
    FreeCAD.Console.PrintMessage("  Username:{}\n".format(OPE_DB_CONTEXT.username))
    FreeCAD.Console.PrintMessage("  Hostname:{}\n".format(OPE_DB_CONTEXT.hostname))

    # ✅ Step 3 — Start session
    api = SessionAPI()

    session_id = api.start()

    # ✅ Step 4 — Validate
    FreeCAD.Console.PrintMessage("\n--- RESULT ---\n")
    FreeCAD.Console.PrintMessage("Session ID:{}\n".format(session_id))
    FreeCAD.Console.PrintMessage("Context Active:{}\n".format(OPE_DB_CONTEXT.is_session_active))
    FreeCAD.Console.PrintMessage("Context Session ID:{}\n".format(OPE_DB_CONTEXT.session_id))

    # ✅ Assertion-style checks (manual)
    if not session_id:
        raise RuntimeError("❌ FAILED: session_id not generated")

    if not OPE_DB_CONTEXT.is_session_active:
        raise RuntimeError("❌ FAILED: context not active")

    if OPE_DB_CONTEXT.session_id != session_id:
        raise RuntimeError("❌ FAILED: session_id mismatch")

    FreeCAD.Console.PrintMessage(f"[{TEST_ID}] PASSED ✅\n")
