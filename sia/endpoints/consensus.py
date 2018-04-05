"""
Consensus API.
"""
from sia.constants import consensus as consensus_constants
from sia.mixins.http import Http


class Consensus:
    """
    Implement consensus-API for Sia storage.
    """

    def __init__(self):
        self.http = Http()

    def get_consensus(self):
        """
        Returns information about the consensus set.
        """
        return self.http.get(consensus_constants.CONSENSUS_URL)

    def validate_transactionset(self, transactionset):
        """
        Validates a set of transactions using the current utxo set.
        """
        return self.http.post(consensus_constants.VALIDATE_URL, transactionset)
