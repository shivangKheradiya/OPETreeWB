import FreeCAD

from opetreewb.domain.label_utils import format_node_label

TEST_ID = "T0002"


def run():
    FreeCAD.Console.PrintMessage(f"[{TEST_ID}] START\n")

    # Type + Name
    assert (
        format_node_label(
            type_name="Part",
            name="Wheel",
            node_id=10,
        )
        == "Part Wheel"
    )

    # Type + ID fallback
    assert (
        format_node_label(
            type_name="Part",
            name=None,
            node_id=20,
        )
        == "Part 20"
    )

    # Type default fallback
    assert (
        format_node_label(
            type_name=None,
            name=None,
            node_id=30,
        )
        == "Node 30"
    )

    # Only type
    assert (
        format_node_label(
            type_name="Assembly",
            name=None,
            node_id=None,
        )
        == "Assembly"
    )

    FreeCAD.Console.PrintMessage(f"[{TEST_ID}] PASSED ✅\n")
