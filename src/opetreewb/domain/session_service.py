from opetreewb.messaging.reporter import Reporter


class SessionService:
    """
    Manages OPE session lifecycle.
    """

    def start(self):
        Reporter.success("[SessionService] session start requested")
        # TODO: legacy provider.start_session()

    def commit(self):
        Reporter.success("[SessionService] session commit requested")
        # TODO: legacy provider.commit_session()

    def abort(self):
        Reporter.warning("[SessionService] session abort requested")
        # TODO: legacy provider.abort_session()