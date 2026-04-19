# core/provider_factory.py
"""
Factory for creating PyDBML providers from the AppContext.
"""

import socket
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
        username=APP_CONTEXT.username,
        hostname=APP_CONTEXT.hostname or socket.gethostname(),
        attribute_registry=registry,
        snowflake=SnowflakeIDGenerator(),
    )

    return provider