"""
Renter API.
"""
from sia.constants import renter as renter_constants
from sia.mixins.http import Http


class Renter:
    """
    Renter API.
    """

    def __init__(self):
        self.http = Http()

    def get_renter(self):
        """
        Returns current renter settings.
        """
        return self.http.get(renter_constants.SETTINGS_URL)

    def get_renter_prices(self):
        """
        Returns current renter settings.
        """
        return self.http.get(renter_constants.PRICES_URL)

    def get_renter_contracts(self):
        """
        Returns a list of active contracts.
        """
        return self.http.get(renter_constants.CONTRACTS_URL).get('contracts')
