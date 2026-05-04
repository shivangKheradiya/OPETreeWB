"""
TreeSelectionBus

UI-only replacement for global CN.
Used to broadcast selected tree node to other UI panels.
"""

from PySide import QtCore


class TreeSelectionBus(QtCore.QObject):
    selectionChanged = QtCore.Signal(object)


TREE_SELECTION = TreeSelectionBus()