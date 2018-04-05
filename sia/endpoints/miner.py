"""
Miner API.
"""
from sia.constants import miner as miner_constants
from sia.mixins.http import Http


class Miner:
    """
    Miner API.
    """
    def __init__(self):
        self.http = Http()

    def get_miner(self):
        """
        Returns status of the miner.
        """
        return self.http.get(miner_constants.STATUS_URL)

    def start_miner(self):
        """
        Starts a single threaded CPU miner.
        """
        return self.http.get(miner_constants.START_URL)

    def stop_miner(self):
        """
        Stops the CPU miner.
        """
        return self.http.get(miner_constants.STOP_URL)

    def get_block_header(self):
        """
        Returns a block header for mining.
        Returned as bytes.
        Byte formatting: https://github.com/NebulousLabs/Sia/blob/master/doc/api/Miner.md#byte-response
        """
        return self.http.get_bytes(miner_constants.HEADER_URL).content

    def post_block_header(self, header):
        """
        Submits a header that has passed the POW.
        Must be sent as bytes.
        Byte formatting: https://github.com/NebulousLabs/Sia/blob/master/doc/api/Miner.md#byte-response
        """
        return self.http.post(miner_constants.HEADER_URL, header)
