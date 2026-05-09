"""
T0010 — API Node Creation Structure Test (Schema + Sparse Model)

Objective:
    Verify that node creation:
    - uses schema-defined attribute IDs
    - follows sparse storage model
    - satisfies identity rule (data_id == node_id for Name)

Scope:
    - node_api.py
    - query_api.py
    - hierarchy schema

Expected:
    - Only Name, Type, Owner are stored
    - Correct attribute_id mapping
    - Identity rule satisfied
"""

import FreeCAD

# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT
from opetreewb.integration.opedbapi.api.node_api import NodeAPI
from opetreewb.integration.opedbapi.api.query_api import QueryAPI
from opetreewb.domain.identity.snowflake import SnowflakeIDGenerator

TEST_ID = "T0010"


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
        # CREATE NODE
        # -----------------------------------------
        node_id = node_api.create(
            parent_node_id=parent_id,
            type_value=element_type,
            name=""
        )

        FreeCAD.Console.PrintMessage(f"CREATED node_id={node_id}\n")

        # -----------------------------------------
        # FETCH NODE DATA
        # -----------------------------------------
        result = query.search(
            filter_dict={
                "field": "node_id",
                "op": "=",
                "value": node_id
            }
        )

        items = result.get("items", [])

        if not items:
            raise RuntimeError("FAILED: Node not found")

        FreeCAD.Console.PrintMessage(f"Retrieved {len(items)} attributes\n")

        # -----------------------------------------
        # ✅ EXPECT EXACTLY 3 ATTRIBUTES (SPARSE MODEL)
        # -----------------------------------------
        if len(items) != 3:
            raise RuntimeError("FAILED: Expected exactly 3 base attributes")

        FreeCAD.Console.PrintMessage("Sparse model OK\n")

        # -----------------------------------------
        # ✅ VALIDATE ATTRIBUTES
        # -------------------------------------------------
        # Schema IDs:
        # 1 → Name
        # 2 → Type
        # 3 → Owner
        # -------------------------------------------------
        for row in items:

            attr_id = row["attribute_id"]
            value = row["value"]
            data_id = row["data_id"]

            # -------------------------
            # NAME (ID = 1)
            # -------------------------
            if attr_id == 1:
                if data_id != node_id:
                    raise RuntimeError("FAILED: Identity rule violated (Name)")
                if value != "":
                    raise RuntimeError("FAILED: Name default incorrect")

            # -------------------------
            # TYPE (ID = 2)
            # -------------------------
            elif attr_id == 2:
                if value != element_type:
                    raise RuntimeError("FAILED: Type incorrect")

            # -------------------------
            # OWNER (ID = 3)
            # -------------------------
            elif attr_id == 3:
                if value != parent_id:
                    raise RuntimeError("FAILED: Owner incorrect")

            else:
                raise RuntimeError(f"FAILED: Unexpected attribute_id {attr_id}")

        FreeCAD.Console.PrintMessage("Attribute validation OK\n")

        FreeCAD.Console.PrintMessage(f"\n[{TEST_ID}] PASSED ✅\n")

    except Exception as e:
        FreeCAD.Console.PrintError(f"[{TEST_ID}] FAILED ❌ → {e}\n")
