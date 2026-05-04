import FreeCAD
from opetreewb.domain.domain_rules import DOMAIN_RULES

TEST_ID = "T0001"

def run():
    FreeCAD.Console.PrintMessage("[{TEST_ID}] START\n")

    assert "DESI" in DOMAIN_RULES
    assert "DICT" in DOMAIN_RULES

    assert DOMAIN_RULES["DESI"]["RootType"] == "DESIWLD"
    assert DOMAIN_RULES["DICT"]["RootType"] == "DICTWLD"

    FreeCAD.Console.PrintMessage("[{TEST_ID}] PASSED ✅\n")