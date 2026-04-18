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


from OPETreeWB.core.label_utils import format_node_label


class MockElementRef:
    def __init__(self, *, type_name, name=None, node_id=None, attributes=None):
        self._type = type_name
        self._name = name
        self._id = node_id
        self._attrs = attributes or {}

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._name

    def keys(self):
        return ["Type", "Name", "NodeID"] + list(self._attrs.keys())

    def __getitem__(self, key):
        if key == "Type":
            return self._type
        if key == "Name":
            return self._name
        if key == "NodeID":
            return self._id
        return self._attrs[key]

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def label(self):
        """
        Unified label used by all trees.
        """
        return format_node_label(
            type_name=self._type,
            name=self._name,
            node_id=self._id,
        )


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
        root_ref = MockElementRef(
            type_name="Assembly",
            name="RootAssembly",
            node_id=1,
        )

        root_item = self.create_item(
            root_ref.label(),
            root_ref,
        )
        self.addTopLevelItem(root_item)

        part1_ref = MockElementRef(
            type_name="Part",
            name="Part001",
            node_id=2,
        )

        part1_item = self.create_item(
            part1_ref.label(),
            part1_ref,
        )
        root_item.addChild(part1_item)

        # Child 2
        part2_ref = MockElementRef(
            type_name="Part",
            name="Part002",
            node_id=3,
        )

        part2_item = self.create_item(
            part2_ref.label(),
            part2_ref,
        )

        root_item.addChild(part2_item)

        root_item.setExpanded(True)