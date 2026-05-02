# OPETreeWB/core/sync/history_replay.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from OPE_DB_API.registry import LIVE_TABLE_REGISTRY


def replay_history_rows(
    *,
    db: Session,
    domain: str,
    history_rows: list,
) -> None:
    """
    Apply history rows to LIVE tables (CREATE / UPDATE / DELETE).

    Assumptions:
    - history_rows are ordered correctly
    - executed inside a DB transaction
    """

    live_model = LIVE_TABLE_REGISTRY[domain]

    for row in history_rows:
        op = row["operation_type"]
        data_id = row["data_id"]

        live_row = (
            db.query(live_model)
            .filter(live_model.data_id == data_id)
            .one_or_none()
        )

        if live_row is None:
            if op == 1:  # CREATE
                db.add(
                    live_model(
                        data_id=data_id,
                        node_id=row["node_id"],
                        attribute_id=row["attribute_id"],
                        value=row["new_value"],
                    )
                )
        elif live_row is not None:
            if op == 2:  # UPDATE
                live_row.value = row["new_value"]
            elif op == 3:  # DELETE
                db.delete(live_row)

        else:
            raise RuntimeError(f"Unknown operation_type: {op}")