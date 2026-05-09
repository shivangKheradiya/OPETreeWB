from opetreewb.integration.opedbapi.api.client import OpeApiClient
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT
from opetreewb.integration.opedbapi.utils.schema_helper import load_element_schema

class NodeAPI:

    def __init__(self, registry=None, id_generator=None):
        self.client = OpeApiClient()
        self.id_gen = id_generator

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

            self._push(
                data_id=data_id,
                node_id=node_id,
                attribute_id=attr_id,
                value=value,
            )

        return node_id

    # -------------------------------------------------
    # DELETE NODE
    # -------------------------------------------------
    def delete(self, node_id):

        result = self.client.post(
            "search",
            json={
                "mode": "working",
                "filter": {
                    "field": "node_id",
                    "op": "=",
                    "value": node_id,
                },
                "limit": 1000,
                "offset": 0,
            },
            use_session=True,
        )

        items = result.get("items", [])

        for row in items:
            self._delete_attribute(
                node_id=row["node_id"],
                attribute_id=row["attribute_id"],
                data_id=row["data_id"],
            )

    # -------------------------------------------------
    # INTERNAL
    # -------------------------------------------------
    def _push(self, *, data_id, node_id, attribute_id, value):

        self.client.post(
            "work/push",
            json={
                "data_id": data_id,
                "node_id": node_id,
                "attribute_id": attribute_id,
                "operation_type": 1,
                "value": value,
            },
            use_session=True,
        )

    def _delete_attribute(self, *, node_id, attribute_id, data_id):

        self.client.post(
            "work/push",
            json={
                "data_id": data_id,
                "node_id": node_id,
                "attribute_id": attribute_id,
                "operation_type": 3,
                "value": None,
            },
            use_session=True,
        )
