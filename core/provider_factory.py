# core/provider_factory.py
"""
Factory for creating PyDBML providers from the AppContext.
"""

import socket
import os
from pathlib import Path
from OPETreeWB.core.app_context import APP_CONTEXT


def create_provider():
    """
    Create and return a PyDBML provider using current AppContext.
    """
    if not APP_CONTEXT.is_configured():
        raise RuntimeError("OPE connection is not configured")
    
    from PyDBML import OpeApiProvider, SnowflakeIDGenerator, AttributeRegistry
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
    # Local-cache presence helpers (NO behavior change yet)
    # -------------------------------------------------

    def has_children_cached(node_id: int) -> bool:
        """
        Placeholder: return False until local cache is wired.
        """
        return False

    def has_attributes_cached(node_id: int) -> bool:
        """
        Placeholder: return False until local cache is wired.
        """
        return False
    
    provider.has_children_cached = has_children_cached
    provider.has_attributes_cached = has_attributes_cached
    
    def ensure_node_loaded(node_id: int):
        """
        Ensure node data is loaded.
        Current implementation: server-backed.
        Future: local-cache-first.
        """
        if not provider.has_attributes_cached(node_id):
            provider.load_node(node_id)
    
    provider.ensure_node_loaded = ensure_node_loaded
    
    return provider