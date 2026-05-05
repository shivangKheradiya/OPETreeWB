from opetreewb.messaging.reporter import Reporter
from opetreewb.infrastructure.infra_errors import (
    ProviderUnavailableError,
    BackendOperationError,
)


class ProviderAdapter:
    """
    Thin adapter around the legacy provider.

    This class is the ONLY place allowed to:
    - reference legacy provider objects
    - call DB / HTTP / API code
    - translate backend errors
    """

    def __init__(self, provider):
        if provider is None:
            raise ProviderUnavailableError("Provider is not available")

        self._provider = provider
        Reporter.info("[ProviderAdapter] Initialized")

    # -------------------------------------------------
    # Session operations
    # -------------------------------------------------

    def start_session(self):
        Reporter.info("[ProviderAdapter] start_session()")
        # TODO: self._provider.start_session()

    def commit_session(self):
        Reporter.info("[ProviderAdapter] commit_session()")
        # TODO: self._provider.commit_session()

    def abort_session(self):
        Reporter.info("[ProviderAdapter] abort_session()")
        # TODO: self._provider.abort_session()

    # -------------------------------------------------
    # Tree operations
    # -------------------------------------------------

    def create_node(self, parent_node_id, element_type, name):
        Reporter.info(
            f"[ProviderAdapter] create_node("
            f"parent_id={parent_node_id}, type={element_type}, name={name})"
        )
        # TODO: self._provider.create_node(...)
        return None

    def delete_node(self, node_id):
        Reporter.info(
            f"[ProviderAdapter] delete_node(node_id={node_id})"
        )
        # TODO: self._provider.delete_node(node_id)

    def load_children(self, parent_node_id):
        Reporter.info(
            f"[ProviderAdapter] load_children(parent_node_id={parent_node_id})"
        )
        # TODO: return self._provider.get_children(...)
        return []

    # -------------------------------------------------
    # Attribute operations
    # -------------------------------------------------

    def load_attributes(self, node_id):
        Reporter.info(
            f"[ProviderAdapter] load_attributes(node_id={node_id})"
        )
        # TODO: return self._provider.load_attributes(...)
        return []

    def update_attribute(self, data_id, value):
        Reporter.info(
            f"[ProviderAdapter] update_attribute("
            f"data_id={data_id}, value={value})"
        )
        # TODO: self._provider.update_attribute(...)