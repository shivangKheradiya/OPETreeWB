import FreeCAD
from opetreewb.domain.rules.domain_rules import DOMAIN_RULES

TEST_ID = "T0003"

def run():
    FreeCAD.Console.PrintMessage(f"[{TEST_ID}] START\n")

    try:
        DOMAIN_RULES["DESI"]["RootType"] = "INVALID"
        assert False, "DOMAIN_RULES should not be mutable in practice"
    except Exception:
        pass

    FreeCAD.Console.PrintMessage(f"[{TEST_ID}] PASSED ✅\n")