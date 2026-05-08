"""
T0012 — API Node Delete Test (Cascade + Sparse Model)

Objective:
    Verify that node deletion removes all associated attribute rows.

Scope:
    - node_api.py
    - query_api.py

Expected:
    - All attributes of node are deleted
    - Node is no longer retrievable
    - No exceptions occur
"""

import FreeCAD

# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------
from opetreewb.integration.opedbapi.core.context import OPE_DB_CONTEXT
from opetreewb.integration.opedbapi.api.node_api import NodeAPI
from opetreewb.integration.opedbapi.api.query_api import QueryAPI
from opetreewb.domain.identity.snowflake import SnowflakeIDGenerator

TEST_ID = "T0011"


# ---------------------------------------------------------
# TEST EXECUTION
# ---------------------------------------------------------
def run():

    FreeCAD.Console.PrintMessage(f"\n[{TEST_ID}] START\n")

    try:
        # ✅ Precondition
        if not OPE_DB_CONTEXT.is_session_active:
            raise RuntimeError("FAILED: No active session")

        id_gen = SnowflakeIDGenerator()
        node_api = NodeAPI(id_generator=id_gen)
        query = QueryAPI()

        parent_id = 1000
        element_type = "STRA"

        # -----------------------------------------
        # CREATE NODE (for deletion test)
        # -----------------------------------------
        node_id = node_api.create(
            parent_node_id=parent_id,
            type_value=element_type,
        )

        FreeCAD.Console.PrintMessage(f"CREATED node_id={node_id}\n")

        # -----------------------------------------
        # DELETE NODE
        # -----------------------------------------
        node_api.delete(node_id)

        FreeCAD.Console.PrintMessage("NODE DELETE CALLED\n")

        # -----------------------------------------
        # VALIDATE REMOVAL
        # -----------------------------------------
        result = query.search(
            filter_dict={
                "field": "node_id",
                "op": "=",
                "value": node_id
            }
        )

        if result["total"] != 0:
            raise RuntimeError("FAILED: Element Still exist in the Table")

        FreeCAD.Console.PrintMessage("Deletion validation OK\n")

        FreeCAD.Console.PrintMessage(f"\n[{TEST_ID}] PASSED ✅\n")

    except Exception as e:
        FreeCAD.Console.PrintError(f"[{TEST_ID}] FAILED ❌ → {e}\n")
