"""
T0006 — API Work Push Test

Objective:
    Verify that attribute changes are correctly staged
    into the session overlay using work/push.

Scope:
    - context.py
    - client.py
    - attribute_api.py

Expected:
    - Attribute is staged in overlay
    - No commit happens
    - No exceptions
"""

import FreeCAD

# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT
from opetreewb.integration.opedbapi.api.attribute_api import AttributeAPI
from opetreewb.integration.opedbapi.api.query_api import QueryAPI
from opetreewb.domain.identity.snowflake import SnowflakeIDGenerator

TEST_ID = "T0006"


# ---------------------------------------------------------
# TEST EXECUTION
# ---------------------------------------------------------
def run():

    FreeCAD.Console.PrintMessage(f"\n[{TEST_ID}] START\n")

    try:
        # ✅ Precondition — active session required
        if not OPE_DB_CONTEXT.is_session_active:
            raise RuntimeError("FAILED: No active session (run T0004 first)")

        # ✅ Setup
        node_id = 999999999   # test node (can be dummy)
        attribute_id = 1     # example attribute (must exist in DB config)
        value = {"test": "value"}

        id_gen = SnowflakeIDGenerator()
        attr_api = AttributeAPI(id_gen)
        query_api = QueryAPI()

        FreeCAD.Console.PrintMessage(f"Staging attribute on node: {node_id}\n")

        # ✅ Step 1 — PUSH (CREATE)
        data_id = attr_api.push(
            node_id=node_id,
            attribute_id=attribute_id,
            value=value,
            data_id=None
        )

        FreeCAD.Console.PrintMessage(f"Data ID: {data_id}\n")

        # ✅ Step 2 — Validate via WORKING STATE
        result = query_api.search(
            filter_dict={
                "field": "node_id",
                "op": "=",
                "value": node_id
            }
        )

        FreeCAD.Console.PrintMessage("SEARCH RESULT RECEIVED\n")

        items = result.get("items", [])

        # ✅ Check if staged row exists
        found = any(row["data_id"] == data_id for row in items)

        if not found:
            raise RuntimeError("FAILED: pushed attribute not found in working state")

        FreeCAD.Console.PrintMessage(f"\n[{TEST_ID}] PASSED ✅\n")

    except Exception as e:
        FreeCAD.Console.PrintError(f"[{TEST_ID}] FAILED ❌ → {e}\n")
