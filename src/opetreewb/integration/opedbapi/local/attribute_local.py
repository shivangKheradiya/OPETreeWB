from dataclasses import dataclass

from opetreewb.integration.opedbapi.local.client import LocalClient
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT
from OPE_DB_API.schemas.work import WorkPushRequest
from OPE_DB_API.crud.work.push import push_work


class AttributeLocal:
    """
    Local attribute layer using OPE_DB_API CRUD.

    Mirrors API work/push behavior exactly.
    """

    def __init__(self, id_generator):
        self.client = LocalClient()
        self.id_gen = id_generator

    # -------------------------------------------------
    # CREATE / UPDATE
    # -------------------------------------------------
    def push(
        self,
        *,
        node_id,
        attribute_id,
        value,
        data_id,
        operation_type:int = 2
    ):
        db = self.client.get_session()

        try:
            session_id = OPE_DB_CONTEXT.session_id
            domain = OPE_DB_CONTEXT.domain.upper()

            payload = WorkPushRequest(
                data_id=data_id,
                node_id=node_id,
                attribute_id=attribute_id,
                operation_type=operation_type,
                value=value,
            )

            row = push_work(
                db,
                domain=domain,
                session_id=session_id,
                payload=payload,
            )

            db.commit()
            db.refresh(row)

            return row.data_id

        finally:
            db.close()

    # -------------------------------------------------
    # DELETE
    # -------------------------------------------------
    def delete(
        self,
        *,
        node_id,
        attribute_id,
        data_id,
    ):
        db = self.client.get_session()

        try:
            session_id = OPE_DB_CONTEXT.session_id
            domain = OPE_DB_CONTEXT.domain.upper()

            payload = WorkPushRequest(
                data_id=data_id,
                node_id=node_id,
                attribute_id=attribute_id,
                operation_type=3,  # DELETE
                value=None,
            )

            row = push_work(
                db,
                domain=domain,
                session_id=session_id,
                payload=payload,
            )

            db.commit()
            db.refresh(row)

        finally:
            db.close()
