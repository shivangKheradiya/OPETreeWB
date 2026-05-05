from opetreewb.messaging.reporter import Reporter


class ProviderAdapter:
    """
    Thin wrapper around legacy provider.
    """

    def __init__(self, provider):
        self._provider = provider
        Reporter.info("[ProviderAdapter] initialized")

    # Future: implement methods that call legacy code safely
