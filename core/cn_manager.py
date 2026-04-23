# core/cn_manager.py
"""
Global Current Node (CN).

CN represents the single Current Node across the entire OPETree workbench.

Usage:
    CN(element_ref)   -> set current node
    CN(node_id)       -> set current node by ref no / id
    CN(None)          -> clear current node
    CN()              -> get current node

Consumers (trees, attribute viewer, commands) subscribe to CN.changed.
"""

from PySide import QtCore


# Sentinel object for distinguishing getter vs setter call
_NOT_SET = object()


class _CurrentNode(QtCore.QObject):
    """
    Global Current Node holder.

    Behaves like a callable state variable with change notification.
    """

    changed = QtCore.Signal(object)  # ElementRef | int | None
    attributeChanged = QtCore.Signal(object, str)  # (ElementRef, attr_name)
    
    def __init__(self):
        super().__init__()
        self._cn = None

    # ---------------------------------------------------------
    # Callable interface
    # ---------------------------------------------------------
    def __call__(self, value=_NOT_SET):
        """
        Getter / Setter for Current Node.

        CN()          -> return current node
        CN(x)         -> set current node to x
        CN(None)      -> clear current node
        """
        # Getter
        if value is _NOT_SET:
            return self._cn

        # Setter (no-op if unchanged)
        if value is self._cn:
            return

        self._cn = value
        self.changed.emit(self._cn)

    # ---------------------------------------------------------
    # Convenience helpers
    # ---------------------------------------------------------
    def clear(self):
        """Clear the current node."""
        self(None)

    def is_set(self) -> bool:
        """Return True if a current node is set."""
        return self._cn is not None


# -------------------------------------------------------------
# Singleton instance: this IS the Current Node (CN)
# -------------------------------------------------------------
CN = _CurrentNode()