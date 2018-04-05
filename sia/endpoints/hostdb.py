"""
HostDB API.
"""
from sia.constants import hostdb as hostdb_constants
from sia.mixins.http import Http


class HostDb:
    """
    Implement hostdb-API for Sia storage.
    """

    def __init__(self):
        self.http = Http()

    def get_hostdb(self):
        """
        Returns list of all known hosts.
        """
        return self.http.get(hostdb_constants.ALL_URL).get('hosts')

    def get_hostdb_active(self, numhosts=None):
        """
        Returns list of active hosts.
        Optional parameter numhosts for maximum number of hosts returned.
        """
        payload = None
        if numhosts is not None:
            payload = {
                'numhosts': (None, str(numhosts)),
            }
        return self.http.get(hostdb_constants.ACTIVE_URL, payload).get('hosts')

    def get_hostdb_host(self, pubkey):
        """
        Fetches detailed information about a particular host, including
        metrics regarding the score of the host within the database
        """
        return self.http.get(hostdb_constants.HOSTS_URL + pubkey)
