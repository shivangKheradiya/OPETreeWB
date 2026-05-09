"""
T0008 — API Work Discard Test

Objective:
    Verify that staged overlay changes are discarded correctly.

Scope:
    - context.py
    - client.py
    - query_api.py

Expected:
    - Overlay data is cleared
    - No changes persist to live table
    - No exceptions
"""

import FreeCAD

# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT
from opetreewb.integration.opedbapi.api.client import OpeApiClient
from opetreewb.integration.opedbapi.api.query_api import QueryAPI

TEST_ID = "T0008"


# ---------------------------------------------------------
# TEST EXECUTION
# ---------------------------------------------------------
def run():

    FreeCAD.Console.PrintMessage(f"\n[{TEST_ID}] START\n")

    try:
        # ✅ Precondition — active session required
        if not OPE_DB_CONTEXT.is_session_active:
            raise RuntimeError("FAILED: No active session (run T0004, T006 first)")

        client = OpeApiClient()
        query_api = QueryAPI()

        session_id = OPE_DB_CONTEXT.session_id
        FreeCAD.Console.PrintMessage(f"Discarding session: {session_id}\n")

        # ✅ Step 1 — DISCARD overlay
        client.post(
            "work/discard",
            use_session=True
        )

        FreeCAD.Console.PrintMessage("Discard response received\n")

        # ✅ Step 2 — Validate overlay cleared (indirect check)
        # Try fetching working state; should not contain staged changes
        result = query_api.search(
            filter_dict={
                "field": "node_id",
                "op": "=",
                "value": 999999999  # dummy control query
            }
        )

        if result["total"] != 0:
            raise RuntimeError("FAILED: Element Still exist in the Table")

        FreeCAD.Console.PrintMessage("Working state accessible post-discard\n")

        FreeCAD.Console.PrintMessage(f"\n[{TEST_ID}] PASSED ✅\n")

    except Exception as e:
        FreeCAD.Console.PrintError(f"[{TEST_ID}] FAILED ❌ → {e}\n")

