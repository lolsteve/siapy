"""
Daemon API.
"""
from sia.constants import daemon as daemon_constants
from sia.mixins.http import Http


class Daemon:
    """
    Implement daemon-API for Sia storage.
    """
    def __init__(self):
        self.http = Http()

    def get_constants(self):
        """
        Returns set of constants in use.
        """
        return self.http.get(daemon_constants.CONSTANTS_URL)

    def stop(self):
        """
        Cleanly shuts down the daemon.
        """
        return self.http.get(daemon_constants.STOP_URL)

    def get_version(self):
        """
        Returns the version of siad running.
        """
        version = self.http.get(daemon_constants.VERSION_URL)
        return version.get('version')
