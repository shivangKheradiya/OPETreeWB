import FreeCAD
from OPETreeWB.commands.session_commands import get_active_provider
from OPETreeWB.core.root_node_creator import create_root_node
from OPETreeWB.core.cn_manager import CN


class CreateRootNodeCommand:
    def GetResources(self):
        return {
            "MenuText": "Create Root Node",
            "ToolTip": "Create a domain root node",
        }

    def IsActive(self):
        return get_active_provider() is not None

    def Activated(self):
        provider = get_active_provider()
        if not provider:
            return

        try:
            ref = create_root_node(provider)
            # ✅ notify all tree views
            CN.structureChanged.emit()
            FreeCAD.Console.PrintMessage(
                f"Root node created: {ref.id}\n"
            )
        except Exception as exc:
            FreeCAD.Console.PrintError(str(exc) + "\n")