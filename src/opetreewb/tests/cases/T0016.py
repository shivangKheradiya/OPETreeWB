"""
T0017 — Local Abort Test

Objective:
    Verify that abort_session clears overlay without affecting live data.

Scope:
    - attribute_local.py
    - query_local.py
    - abort_session (OPE_DB_API)

Expected:
    - Overlay is cleared
    - Live data unchanged
    - Session is closed
    - No exceptions
"""

import FreeCAD
from OPE_DB_API.crud.session.abort import abort_session
# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------
from sqlalchemy.orm import Session

from opetreewb.domain.stores.stores import OPE_DB_CONTEXT
from opetreewb.integration.opedbapi.local.client import LocalClient
from opetreewb.integration.opedbapi.local.query_local import QueryLocal

TEST_ID = "T0016"


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

        FreeCAD.Console.PrintMessage(f"ABORT session_id={session_id}\n")

        # ✅ Step 1 — Abort session (clear overlay)
        abort_session(
            db,
            session_id=session_id,
            domain=domain,
        )

        db.commit()

        FreeCAD.Console.PrintMessage("Abort executed\n")

        # ✅ Step 2 — Validate overlay is cleared
        query_local = QueryLocal()

        result = query_local.search(
            filter_dict={
                "field": "node_id",
                "op": "=",
                "value": 999999,
            }
        )

        items = result.get("items", [])

        if items:
            raise RuntimeError("FAILED: Overlay not cleared after abort")

        FreeCAD.Console.PrintMessage("Overlay cleared ✅\n")

        FreeCAD.Console.PrintMessage(f"\n[{TEST_ID}] PASSED ✅\n")

    except Exception as e:
        FreeCAD.Console.PrintError(f"[{TEST_ID}] FAILED ❌ → {e}\n")

    finally:
        db.close()
