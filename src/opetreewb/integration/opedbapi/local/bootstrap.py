from pathlib import Path
from OPE_DB_API.config.loader import set_client_config_file


def initialize_opedb_config():
    """
    Initialize OPE_DB_API configuration.
    Must be called before any DB operation.
    """

    # ✅ move up until we find project root (contains /config)
    current = Path(__file__).resolve()

    while current != current.parent:
        if (current / "config").exists():
            base_path = current
            break
        current = current.parent
    else:
        raise RuntimeError("Project root not found")

    client_config = base_path / "config" / "config_client.toml"

    if not client_config.exists():
        raise FileNotFoundError(f"Config not found: {client_config}")

    set_client_config_file(client_config)