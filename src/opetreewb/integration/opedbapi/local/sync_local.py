from opetreewb.integration.opedbapi.local.client import LocalClient


class SyncLocal:
    def __init__(self,localclient:LocalClient=None):
        self.client = localclient
        pass