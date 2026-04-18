# trees/ope_mock_tree.py
"""
Mock OPETree for development and testing.

Used to validate:
- Tree selection
- CN behavior
- AttributeViewer updates

No PyDBML dependency.
"""

from OPETreeWB.trees.ope_tree_base import OPETree


class MockElementRef:
    """
    Minimal stand-in for PyDBML ElementRef.
    """

    def __init__(self, attributes: dict):
        self._attrs = attributes

    def keys(self):
        return list(self._attrs.keys())

    def __getitem__(self, key):
        return self._attrs[key]

    def __getattr__(self, name):
        try:
            return self._attrs[name]
        except KeyError:
            raise AttributeError(name)

    def __repr__(self):
        return f"<MockElementRef {self._attrs}>"


class OPEMockTree(OPETree):
    """
    Mock tree with hard-coded data.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._populate()

    def _populate(self):
        self.clear_tree()

        # Root node
        root_ref = MockElementRef({
            "Name": "RootAssembly",
            "Type": "Assembly",
            "Owner": "OPE",
        })

        root_item = self.create_item("RootAssembly", root_ref)
        self.addTopLevelItem(root_item)

        # Child 1
        part1_ref = MockElementRef({
            "Name": "Part001",
            "Material": "Steel",
            "Weight": 12.5,
        })
        part1_item = self.create_item("Part001", part1_ref)
        root_item.addChild(part1_item)

        # Child 2
        part2_ref = MockElementRef({
            "Name": "Part002",
            "Material": "Aluminium",
            "Weight": 4.2,
        })
        part2_item = self.create_item("Part002", part2_ref)
        root_item.addChild(part2_item)

        root_item.setExpanded(True)