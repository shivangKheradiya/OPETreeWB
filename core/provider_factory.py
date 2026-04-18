# core/provider_factory.py
"""
Factory for creating PyDBML providers from the AppContext.
"""

import socket

from OPETreeWB.core.app_context import APP_CONTEXT


def create_provider():
    """
    Create and return a PyDBML provider using current AppContext.
    """
    if not APP_CONTEXT.is_configured():
        raise RuntimeError("OPE connection is not configured")
    
    from PyDBML import (
        OpeApiProvider,
        SnowflakeIDGenerator,
        AttributeRegistry,
    )
    registry = AttributeRegistry(
        registry_path="PATH_TO_ATTRIBUTE_REGISTRY.json"
    )

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