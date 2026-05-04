import FreeCAD
import importlib
import pkgutil

import opetreewb.tests.cases as cases_pkg


def run_all():
    FreeCAD.Console.PrintMessage(
        "\n==== OPETreeWB TESTS START ====\n"
    )

    # Discover all test modules under cases/
    test_modules = []

    for module_info in pkgutil.iter_modules(cases_pkg.__path__):
        name = module_info.name

        # Only accept files like T0001, T0123, etc.
        if name.startswith("T") and name[1:].isdigit():
            test_modules.append(name)

    # Sort by numeric test ID
    test_modules.sort()

    # Run tests one by one
    for test_name in test_modules:
        module = importlib.import_module(
            f"opetreewb.tests.cases.{test_name}"
        )

        if hasattr(module, "run"):
            module.run()
        else:
            FreeCAD.Console.PrintError(
                f"[{test_name}] ERROR: no run() function\n"
            )

    FreeCAD.Console.PrintMessage(
        "==== OPETreeWB TESTS END ✅ ====\n"
    )
