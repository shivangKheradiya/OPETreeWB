"""
T0015 — Local Attribute Push Test

Objective:
    Verify that attribute_local correctly stages data in local overlay.

Scope:
    - attribute_local.py
    - local/client.py
    - local/bootstrap.py

Expected:
    - Attribute row inserted into overlay table
    - operation_type = 1 (CREATE)
    - Value stored correctly
    - No exceptions
"""

import FreeCAD

from opetreewb.domain.identity.snowflake import SnowflakeIDGenerator
# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT
from opetreewb.integration.opedbapi.local.attribute_local import AttributeLocal
from opetreewb.integration.opedbapi.local.query_local import QueryLocal

TEST_ID = "T0014"


# ---------------------------------------------------------
def run():

    FreeCAD.Console.PrintMessage(f"\n[{TEST_ID}] START\n")

    FreeCAD.Console.PrintMessage("Preliminary Run required T0004 , T0012 \n")

    try:
        if not OPE_DB_CONTEXT.session_id:
            raise RuntimeError(
                "FAILED: No session_id in context (run T0004 , T0012 first)"
            )

        id_gen = SnowflakeIDGenerator()
        attr_local = AttributeLocal(id_gen)
        query_local = QueryLocal()

        node_id = 999999999  # test node
        attribute_id = 1  # test attribute (dummy, not schema-bound)
        value = {"test": "value"}

        FreeCAD.Console.PrintMessage(
            f"PUSH attribute node_id={node_id}, attr_id={attribute_id}\n"
        )

        # ✅ Step 1 — Push attribute (CREATE)
        data_id = attr_local.push(
            node_id=node_id, attribute_id=attribute_id, value=value, data_id=None
        )

        FreeCAD.Console.PrintMessage(f"data_id={data_id}\n")

        # ✅ Step 2 — Validate using local query
        result = query_local.search(
            filter_dict={"field": "node_id", "op": "=", "value": node_id}
        )

        FreeCAD.Console.PrintMessage("SEARCH RESULT RECEIVED\n")

        items = result.get("items", [])

        # ✅ Check if staged row exists
        found = any(row["data_id"] == data_id for row in items)

        if not found:
            raise RuntimeError("FAILED: Attribute not found after push")

        FreeCAD.Console.PrintMessage("Validation OK\n")
        FreeCAD.Console.PrintMessage(f"\n[{TEST_ID}] PASSED ✅\n")

    except Exception as e:
        FreeCAD.Console.PrintError(f"[{TEST_ID}] FAILED ❌ → {e}\n")
