# core/provider_factory.py
"""
Factory for creating PyDBML providers from the AppContext.
"""

import socket
import os
from pathlib import Path
from types import MethodType
from OPETreeWB.core.app_context import APP_CONTEXT
from OPE_DB_API.cache.engine import CacheEngine
from OPE_DB_API.db.session import get_client_db_session
from OPE_DB_API.config import set_client_config_file
from OPE_DB_API.db.engine import get_client_engine
from OPE_DB_API.db.init_db import init_database

def create_provider():
    """
    Create and return a PyDBML provider using current AppContext.
    """
    if not APP_CONTEXT.is_configured():
        raise RuntimeError("OPE connection is not configured")
    
    from PyDBML.providers import OpeApiProvider
    from PyDBML.identity import SnowflakeIDGenerator
    from PyDBML.metadata import AttributeRegistry
    here = Path(__file__).resolve()
    wb_root = here.parents[1]  # OPETreeWB/

    registry_path = wb_root / "PyDBML" / "PyDBML" / "metadata" / "attributes.json"

    if not registry_path.exists():
        raise RuntimeError(f"Attribute registry not found: {registry_path}")

    registry = AttributeRegistry(registry_path)

    provider = OpeApiProvider(
        base_url=APP_CONTEXT.api_url,
        code=APP_CONTEXT.project_code,
        domain=APP_CONTEXT.domain,
        username=APP_CONTEXT.username or os.getlogin(),
        hostname=APP_CONTEXT.hostname or socket.gethostname(),
        attribute_registry=registry,
        snowflake=SnowflakeIDGenerator(),
    )

    # -------------------------------------------------
    # Ensure local cache DB exists
    # -------------------------------------------------
    set_client_config_file(r"C:\SKRepo\OPETreeWB\OPE_DB_API\defaults\config_client.toml")
    engine = get_client_engine(APP_CONTEXT.project_code)
    init_database(engine)

    # -------------------------------------------------
    # Local-cache presence helpers (NO behavior change yet)
    # -------------------------------------------------

    def has_children_cached(self, node_id: int) -> bool:
        """
        Placeholder: return False until local cache is wired.
        """
        return False

    def has_attributes_cached(self, node_id: int) -> bool:
        """
        Placeholder: return False until local cache is wired.
        """
        return False
    
    provider.has_children_cached = MethodType(has_children_cached, provider)
    provider.has_attributes_cached = MethodType(has_attributes_cached, provider)
    
    def ensure_node_loaded(self, node_id: int):
        """
        Ensure node data is loaded.
        Current implementation: server-backed.
        Future: local-cache-first.
        """
        if not provider.has_attributes_cached(node_id):
            provider.load_node(node_id)

    provider.ensure_node_loaded = MethodType(ensure_node_loaded, provider)

    return provider