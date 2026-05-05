class InfrastructureError(Exception):
    """Base infrastructure error."""


class ProviderUnavailableError(InfrastructureError):
    pass


class BackendOperationError(InfrastructureError):
    pass
