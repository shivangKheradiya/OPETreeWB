from collections import defaultdict

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

    # -------------------------------------------------
    # ✅ NEW: Group operations by node
    # -------------------------------------------------
    def group_by_node(self):

        grouped = defaultdict(list)

        for op in self._operations:
            grouped[op["node_id"]].append(op)

        return grouped

    # -------------------------------------------------
    # ✅ NEW: Extract node attribute map
    # -------------------------------------------------
    def build_node_dicts(self):

        grouped = self.group_by_node()

        nodes = []

        for node_id, ops in grouped.items():

            attr_map = {}

            for op in ops:
                attr_map[op["attribute_id"]] = {
                    "data_id": op["data_id"],
                    "value": op["value"]
                }

            nodes.append({
                "node_id": node_id,
                "attributes": attr_map
            })

        return nodes
