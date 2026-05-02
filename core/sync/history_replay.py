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

        if op == 1:  # CREATE
            exists = (
                db.query(live_model)
                .filter(live_model.data_id == data_id)
                .one_or_none()
            )
            if exists is None:
                db.add(live_model(**row["new_value"]))

        elif op == 2:  # UPDATE
            exists = (
                db.query(live_model)
                .filter(live_model.data_id == data_id)
                .one_or_none()
            )
            if exists:
                for k, v in row["new_value"].items():
                    setattr(exists, k, v)

        elif op == 3:  # DELETE
            (
                db.query(live_model)
                .filter(live_model.data_id == data_id)
                .delete(synchronize_session=False)
            )

        else:
            raise RuntimeError(f"Unknown operation_type: {op}")