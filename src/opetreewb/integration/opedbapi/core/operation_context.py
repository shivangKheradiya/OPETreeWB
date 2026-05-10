class OperationContext:
    """
    Captures operations generated during API execution.

    Allows same operations to be replayed in LOCAL layer
    without regenerating node_id or data_id.
    """

    def __init__(self):
        self._operations = []

    # -------------------------------------------------
    # ADD OPERATION
    # -------------------------------------------------
    def add(self, op: dict):
        self._operations.append(op)

    # -------------------------------------------------
    # GET OPERATIONS
    # -------------------------------------------------
    def get_all(self):
        return list(self._operations)

    # -------------------------------------------------
    # CLEAR (optional)
    # -------------------------------------------------
    def clear(self):
        self._operations.clear()