from opetreewb.integration.opedbapi.api.client import OpeApiClient
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT
from opetreewb.integration.opedbapi.utils.schema_helper import load_element_schema
from opetreewb.integration.opedbapi.core.operation_context import OperationContext

class NodeAPI:

    def __init__(self, id_generator=None, op_context:OperationContext=None,opeapiclient:OpeApiClient=None):
        self.client = opeapiclient
        self.id_gen = id_generator
        self.op_context = op_context

    # -------------------------------------------------
    # CREATE NODE (SPARSE MODEL ✅)
    # -------------------------------------------------
    def create(self, *, parent_node_id, type_value, name=None):

        if not OPE_DB_CONTEXT.is_session_active:
            raise RuntimeError("No active session")

        node_id = self.id_gen.next_id()

        schema = load_element_schema(type_value)

        for attr_name, meta in schema.items():

            attr_id = meta["id"]

            # -------------------------
            # VALUE RULES
            # -------------------------
            if attr_name == "Name":
                value = name if name is not None else ""
                data_id = node_id  # ✅ identity rule

            elif attr_name == "Type":
                value = type_value
                data_id = self.id_gen.next_id()

            elif attr_name == "Owner":
                value = parent_node_id
                data_id = self.id_gen.next_id()

            else:
                # ✅ SPARSE MODEL → skip defaults
                continue

            self._create_attribute(
                data_id=data_id,
                node_id=node_id,
                attribute_id=attr_id,
                value=value,
            )

        return node_id

    # -------------------------------------------------
    # DELETE NODE
    # -------------------------------------------------
    def delete(self, node_id, type_value):
        schema = load_element_schema(type_value)
        self._delete_attribute(
            node_id=node_id,
            attribute_id=schema["Name"]["id"],
            data_id=node_id,
        )

    # -------------------------------------------------
    # INTERNAL
    # -------------------------------------------------
    def _create_attribute(self, *, data_id, node_id, attribute_id, value):
        
        op = {
            "data_id": data_id,
            "node_id": node_id,
            "attribute_id": attribute_id,
            "operation_type": 1,
            "value": value,
        }

        self.log_submit_operation(op)

    def _delete_attribute(self, *, node_id, attribute_id, data_id):

        op = {
            "data_id": data_id,
            "node_id": node_id,
            "attribute_id": attribute_id,
            "operation_type": 3,
            "value": None,
        }

        self.log_submit_operation(op)

    def log_submit_operation(self, op):
        if self.op_context:
            self.op_context.add(op)

        self.client.post(
            "work/push",
            json=op,
            use_session=True,
        )