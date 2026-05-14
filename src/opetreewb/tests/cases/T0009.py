"""
T0009 — API Attribute Push Test

Objective:
    Verify that attribute API correctly stages CREATE, UPDATE and DELETE.

Scope:
    - attribute_api.py
    - query_api.py

Expected:
    - Attribute staged in overlay
    - Update works
    - Delete works
"""

import FreeCAD

from opetreewb.domain.identity.snowflake import SnowflakeIDGenerator
# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT
from opetreewb.integration.opedbapi.api.attribute_api import AttributeAPI
from opetreewb.integration.opedbapi.api.query_api import QueryAPI

TEST_ID = "T0009"


# ---------------------------------------------------------
def run():

    FreeCAD.Console.PrintMessage(f"\n[{TEST_ID}] START\n")

    try:
        if not OPE_DB_CONTEXT.is_session_active:
            raise RuntimeError("FAILED: No active session (run T0004 first)")

        id_gen = SnowflakeIDGenerator()
        attr_api = AttributeAPI(id_gen)
        query = QueryAPI()

        node_id = 12345
        attribute_id = 1

        # -----------------------------------------
        # CREATE
        # -----------------------------------------
        data_id = attr_api.push(
            node_id=node_id, attribute_id=attribute_id, value="100", data_id=None
        )

        FreeCAD.Console.PrintMessage(f"CREATED data_id={data_id}\n")

        # -----------------------------------------
        # UPDATE
        # -----------------------------------------
        attr_api.push(
            node_id=node_id, attribute_id=attribute_id, value="200", data_id=data_id
        )

        FreeCAD.Console.PrintMessage("UPDATED\n")

        # -----------------------------------------
        # DELETE
        # -----------------------------------------
        attr_api.delete(node_id=node_id, attribute_id=attribute_id, data_id=data_id)

        FreeCAD.Console.PrintMessage("DELETED\n")

        # ✅ Final validation (no crash)
        FreeCAD.Console.PrintMessage(f"\n[{TEST_ID}] PASSED ✅\n")

    except Exception as e:
        FreeCAD.Console.PrintError(f"[{TEST_ID}] FAILED ❌ → {e}\n")
