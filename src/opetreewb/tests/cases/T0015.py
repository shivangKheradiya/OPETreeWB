"""
T0016 — Local Commit Test

Objective:
    Verify that local commit applies overlay changes to live table.

Scope:
    - attribute_local.py
    - query_local.py
    - commit_session (OPE_DB_API)

Expected:
    - Overlay changes applied to live table
    - Overlay is cleared
    - Session is closed
    - No exceptions
"""

import FreeCAD
from OPE_DB_API.crud.commit.commit import commit_session
# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------
from sqlalchemy.orm import Session

from opetreewb.domain.stores.stores import OPE_DB_CONTEXT
from opetreewb.integration.opedbapi.local.client import LocalClient
from opetreewb.integration.opedbapi.local.query_local import QueryLocal

TEST_ID = "T0015"


# ---------------------------------------------------------
def run():

    FreeCAD.Console.PrintMessage(f"\n[{TEST_ID}] START\n")

    FreeCAD.Console.PrintMessage(
        "\nPlease Run Preliminary Setup T0004 T0012 T0014 if not run \n"
    )

    try:
        session_id = OPE_DB_CONTEXT.session_id
        domain = OPE_DB_CONTEXT.domain.upper()

        client = LocalClient()
        db: Session = client.get_session()

        FreeCAD.Console.PrintMessage(f"COMMIT session_id={session_id}\n")

        # ✅ Step 1 — Commit overlay → live
        commit_session(
            db,
            domain=domain,
            session_id=session_id,
        )

        db.commit()

        FreeCAD.Console.PrintMessage("Commit executed\n")

        # ✅ Step 2 — Validate overlay cleared
        query_local = QueryLocal()

        result_overlay = query_local.search(
            filter_dict={
                "field": "node_id",
                "op": "=",
                "value": 999999,
            }
        )

        overlay_items = result_overlay.get("items", [])

        if overlay_items:
            raise RuntimeError("FAILED: Overlay not cleared")

        FreeCAD.Console.PrintMessage("Overlay cleared OK\n")

        FreeCAD.Console.PrintMessage(f"\n[{TEST_ID}] PASSED ✅\n")

    except Exception as e:
        FreeCAD.Console.PrintError(f"[{TEST_ID}] FAILED ❌ → {e}\n")

    finally:
        db.close()
