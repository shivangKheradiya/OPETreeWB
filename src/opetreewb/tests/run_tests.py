import FreeCAD

from opetreewb.tests.T0001 import run as T0001


def run_all():
    FreeCAD.Console.PrintMessage(
        "\n==== OPETreeWB TESTS START ====\n"
    )

    T0001()

    FreeCAD.Console.PrintMessage(
        "==== OPETreeWB TESTS END ✅ ====\n"
    )
