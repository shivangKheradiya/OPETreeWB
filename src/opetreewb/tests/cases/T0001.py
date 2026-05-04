import FreeCAD
from opetreewb.domain.domain_rules import DOMAIN_RULES


def run():
    FreeCAD.Console.PrintMessage("[T001] START\n")

    assert "DESI" in DOMAIN_RULES
    assert "DICT" in DOMAIN_RULES

    assert DOMAIN_RULES["DESI"]["RootType"] == "DESIWLD"
    assert DOMAIN_RULES["DICT"]["RootType"] == "DICTWLD"

    FreeCAD.Console.PrintMessage("[T0001] PASSED ✅\n")