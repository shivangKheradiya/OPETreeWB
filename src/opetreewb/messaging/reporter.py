import FreeCAD


class Reporter:
    @staticmethod
    def info(msg: str):
        FreeCAD.Console.PrintMessage(f"ℹ️ {msg}\n")

    @staticmethod
    def success(msg: str):
        FreeCAD.Console.PrintMessage(f"✅ {msg}\n")

    @staticmethod
    def warning(msg: str):
        FreeCAD.Console.PrintWarning(f"⚠️ {msg}\n")

    @staticmethod
    def error(msg: str):
        FreeCAD.Console.PrintError(f"❌ {msg}\n")