from opetreewb.domain.services.service_container import ServiceContainer

class AppContext:
    """
    Global application state (safe and explicit).
    """

    container:ServiceContainer = None