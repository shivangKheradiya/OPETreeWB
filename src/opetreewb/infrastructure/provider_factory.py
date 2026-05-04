"""
ProviderFactory

Responsible for creating a provider instance
from application configuration.

Does NOT:
- start sessions
- touch UI
- mutate SessionContext
"""

from opetreewb.infrastructure import SESSION_CONTEXT


def create_provider(provider_cls, **kwargs):
    """
    Create a provider instance and register it
    as the active provider in SessionContext.

    Parameters:
    - provider_cls: class of the provider to construct
    - kwargs: passed directly to provider constructor

    Returns:
    - provider instance
    """
    provider = provider_cls(**kwargs)

    # ✅ authoritative provider registration
    SESSION_CONTEXT.set_provider(provider)

    return provider