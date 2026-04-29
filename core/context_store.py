import json
import tempfile
from pathlib import Path

from OPETreeWB.core.app_context import APP_CONTEXT


_CONTEXT_DIR = Path(tempfile.gettempdir()) / "ope_treewb"
_CONTEXT_FILE = _CONTEXT_DIR / "context.json"


def save_context():
    """
    Persist AppContext to temp storage.
    """
    _CONTEXT_DIR.mkdir(parents=True, exist_ok=True)

    data = {
        # Server / API
        "api_url": APP_CONTEXT.api_url,
        "project_code": APP_CONTEXT.project_code,
        "domain": APP_CONTEXT.domain,
        "username": APP_CONTEXT.username,
        "hostname": APP_CONTEXT.hostname,

        # Tree
        "root_node_id": APP_CONTEXT.root_node_id,

        # Local cache DB
        "local_db_host": APP_CONTEXT.local_db_host,
        "local_db_port": APP_CONTEXT.local_db_port,
        "local_db_name": APP_CONTEXT.local_db_name,
        "local_db_user": APP_CONTEXT.local_db_user,
        # ❗ password stored intentionally (temp scope)
        "local_db_password": APP_CONTEXT.local_db_password,
    }

    with _CONTEXT_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_context():
    """
    Load AppContext from temp storage (if exists).
    """
    if not _CONTEXT_FILE.exists():
        return

    try:
        with _CONTEXT_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return  # silently ignore corrupt file

    for key, value in data.items():
        setattr(APP_CONTEXT, key, value)
