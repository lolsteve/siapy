"""
Gateway API.
"""
from sia.constants import gateway as gateway_constants
from sia.mixins.http import Http


class Gateway:
    """
    Implement gateway-API for Sia storage.
    """

    def __init__(self):
        self.http = Http()

    def get_gateway(self):
        """
        Returns information about the gateway.
        """
        return self.http.get(gateway_constants.INFO_URL)

    def gateway_connect(self, netaddress):
        """
        Connects the gateway to a peer.
        """
        self.http.post(gateway_constants.CONNECT_URL + netaddress)

    def gateway_disconnect(self, netaddress):
        """
        Disconnects the gateway from a peer.
        """
        self.http.post(gateway_constants.DISCONNECT_URL + netaddress)
