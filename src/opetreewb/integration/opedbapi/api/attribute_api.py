from typing import Any

from opetreewb.integration.opedbapi.api.client import OpeApiClient
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT


class AttributeAPI:
    """
    Handles attribute CRUD via API.

    Uses work/push model:
    - CREATE → operation_type = 1
    - UPDATE → operation_type = 2
    - DELETE → operation_type = 3
    """

    def __init__(self, id_generator):
        self.client = OpeApiClient()
        self.id_gen = id_generator

    # -------------------------------------------------
    # CREATE OR UPDATE ATTRIBUTE
    # -------------------------------------------------
    def push(
        self,
        *,
        node_id: int,
        attribute_id: int,
        value: Any,
        data_id,
        operation_type:int = 2
    ):
        """
        Create or update attribute row.

        - If data_id exists → UPDATE
        - If data_id None → CREATE
        """

        if not OPE_DB_CONTEXT.is_session_active:
            raise RuntimeError("No active session")

        self.client.post(
            "work/push",
            json={
                "data_id": data_id,
                "node_id": node_id,
                "attribute_id": attribute_id,
                "operation_type": operation_type,
                "value": value,
            },
            use_session=True,
        )

        return data_id

    # -------------------------------------------------
    # DELETE ATTRIBUTE
    # -------------------------------------------------
    def delete(
        self,
        *,
        node_id: int,
        attribute_id: int,
        data_id: int,
    ):
        """
        Delete attribute row.
        """

        if not OPE_DB_CONTEXT.is_session_active:
            raise RuntimeError("No active session")

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