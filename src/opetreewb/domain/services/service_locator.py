from opetreewb.app.app_context import AppContext


def get_container():
    """
    Returns active service container.
    """
    if not AppContext.container:
        raise RuntimeError("No active connection (ServiceContainer not initialized)")
    return AppContext.container


# -------------------------------------------------
# Services
# -------------------------------------------------


def get_tree_service():
    return get_container().tree_service


def get_attribute_service():
    return get_container().attribute_service


def get_session_service():
    return get_container().session_service


def get_client():
    return get_container().fcadclient


def get_geometry_service():
    return get_container().geometry_service


def get_sync_service():
    return get_container().sync_service
