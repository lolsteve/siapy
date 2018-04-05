"""
Provide functionality for Sia decentrilized storage.
"""
from sia.constants import (
    daemon as daemon_constants,
    consensus as consensus_constants,
    gateway as gateway_constants,
    host as host_constants,
    hostdb as hostdb_constants,
    miner as miner_constants,
    renter as renter_constants,
    wallet as wallet_constants,
    file as file_constants,
)

from sia.endpoints import (
    daemon,
    consensus,
    gateway,
    host,
    hostdb,
    miner,
    renter,
    wallet,
    file,
)
from sia.mixins.http import HttpMixinToDeprecate


class SiaToDeprecate(HttpMixinToDeprecate):  # pylint: disable=too-many-public-methods
    """
    Deprecated API for Sia storage.
    """

    # Daemon API

    def get_constants(self):
        """
        Returns set of constants in use.
        """
        return self.http_get(daemon_constants.CONSTANTS_URL)

    def stop(self):
        """
        Cleanly shuts down the daemon.
        """
        return self.http_get(daemon_constants.STOP_URL)

    def get_version(self):
        """
        Returns the version of siad running.
        """
        version = self.http_get(daemon_constants.VERSION_URL)
        return version.get('version')

    # Consensus API

    def get_consensus(self):
        """
        Returns information about the consensus set.
        """
        return self.http_get(consensus_constants.CONSENSUS_URL)

    def validate_transactionset(self, transactionset):
        """
        Validates a set of transactions using the current utxo set.
        """
        return self.http_post(
            consensus_constants.VALIDATE_URL,
            transactionset,
        )

    # Gateway API

    def get_gateway(self):
        """
        Returns information about the gateway.
        """
        return self.http_get(gateway_constants.INFO_URL)

    def gateway_connect(self, netaddress):
        """
        Connects the gateway to a peer.
        """
        self.http_post(gateway_constants.CONNECT_URL + netaddress)

    def gateway_disconnect(self, netaddress):
        """
        Disconnects the gateway from a peer.
        """
        self.http_post(gateway_constants.DISCONNECT_URL + netaddress)

    # Host API

    def get_host(self):
        """
        Returns information about the host.
        """
        return self.http_get(host_constants.HOST_URL)

    def set_host(self, host_settings):
        """
        Configures hosting parameters.
        """
        return self.http_post(host_constants.HOST_URL, host_settings)

    def host_announce(self, netaddress=None):
        """
        Announces the host to the network as a source of storage.
        """
        payload = None
        if netaddress is not None:
            payload = {
                'netaddress': netaddress,
            }
        return self.http_post(host_constants.ANNOUNCE_URL, payload)

    def host_storage(self):
        """
        Returns a list of folders tracked by the storage manager.
        """
        return self.http_get(host_constants.STORAGE_URL).get('folders')

    def host_storage_add(self, path, size):
        """
        Adds a storage folder to the manager.
        """
        payload = {
            'path': path,
            'size': size,
        }
        return self.http_post(host_constants.STORAGE_ADD_URL, payload)

    def host_storage_remove(self, path, force=False):
        """
        Removes a folder from the storage manager.
        """
        payload = {
            'path': path,
            'force': force,
        }
        return self.http_post(host_constants.STORAGE_REMOVE_URL, payload)

    def host_storage_resize(self, path, size):
        """
        Resizes a folder in the manager.
        """
        payload = {
            'path': path,
            'size': size,
        }
        return self.http_post(host_constants.RESIZE_STORAGE_URL, payload)

    def host_storage_sector_delete(self, merkleroot):
        """
        Deletes a sector from the manager.
        """
        return self.http_post(host_constants.STORAGE_SECTOR_URL + merkleroot)

    def host_estimatescore(self, host_settings=None):
        """
        Returns the estimated HostDB score of the host using its current settings, combined with the provided settings.
        """
        return self.http_get(host_constants.ESTIMATE_SCORE_URL, host_settings)

    # HostDB API

    def get_hostdb(self):
        """
        Returns list of all known hosts.
        """
        return self.http_get(hostdb_constants.ALL_URL).get('hosts')

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
        return self.http_get(hostdb_constants.ACTIVE_URL, payload).get('hosts')

    def get_hostdb_host(self, pubkey):
        """
        Fetches detailed information about a particular host, including
        metrics regarding the score of the host within the database
        """
        return self.http_get(hostdb_constants.HOSTS_URL + pubkey)

    # Miner API

    def get_miner(self):
        """
        Returns status of the miner.
        """
        return self.http_get(miner_constants.STATUS_URL)

    def start_miner(self):
        """
        Starts a single threaded CPU miner.
        """
        return self.http_get(miner_constants.START_URL)

    def stop_miner(self):
        """
        Stops the CPU miner.
        """
        return self.http_get(miner_constants.STOP_URL)

    def get_block_header(self):
        """
        Returns a block header for mining.
        Returned as bytes.
        Byte formatting: https://github.com/NebulousLabs/Sia/blob/master/doc/api/Miner.md#byte-response
        """
        return self.http_get_bytes(miner_constants.HEADER_URL).content

    def post_block_header(self, header):
        """
        Submits a header that has passed the POW.
        Must be sent as bytes.
        Byte formatting: https://github.com/NebulousLabs/Sia/blob/master/doc/api/Miner.md#byte-response
        """
        return self.http_post(miner_constants.HEADER_URL, header)

    # Renter API

    def get_renter(self):
        """
        Returns current renter settings.
        """
        return self.http_get(renter_constants.SETTINGS_URL)

    def get_renter_prices(self):
        """
        Returns current renter settings.
        """
        return self.http_get(renter_constants.PRICES_URL)

    def get_renter_contracts(self):
        """
        Returns a list of active contracts.
        """
        return self.http_get(renter_constants.CONTRACTS_URL).get('contracts')

    # File API

    def list_files(self):
        """
        Returns a list of all files.
        """
        files = self.http_get(file_constants.LIST_URL)
        return files.get('files')

    def delete_file(self, siapath):
        """
        Deletes a renter file.
        """
        self.http_post(file_constants.DELETE_URL + siapath)

    def download_file(self, path, siapath):
        """
        Downloads a file from sia.
        """
        payload = {
            'destination': (None, path),
        }
        self.http_get(file_constants.DOWNLOAD_URL + siapath, payload)

    def rename_file(self, siapath, newsiapath):
        """
        Renames a file.
        """
        payload = {
            'newsiapath': newsiapath,
        }
        self.http_post(file_constants.RENAME_URL + siapath, payload)

    def upload_file(self, path, siapath):
        """
        Uploads a file to sia.
        """
        payload = {
            'source': path,
        }
        self.http_post(file_constants.UPLOAD_URL + siapath, payload)

    def get_downloads(self):
        """
        Returns a list of files in the download queue.
        """
        return self.http_get(renter_constants.DOWNLOADS_URL).get('downloads')

    # Wallet API

    def get_wallet(self):
        """
        Returns information aout the wallet.
        """
        return self.http_get(wallet_constants.INFO_URL)

    def load_033x(self, source, encryptionpassword):
        """
        Loads a v0.3.3.x wallet into the current wallet.
        """
        payload = {
            'source': source,
            'encryptionpassword': encryptionpassword,
        }
        self.http_post(wallet_constants.V_033X_URL, payload)

    def get_address(self):
        """
        Returns a single address from the wallet.
        """
        return self.http_get(wallet_constants.ADDRESS_URL).get('address')

    def get_addresses(self):
        """
        Returns a list of addresses from the wallet.
        """
        return self.http_get(wallet_constants.ADDRESS_LIST_URL).get('addresses')

    def backup_wallet(self, destination):
        """
        Creates a backup of the wallet settings.
        """
        payload = {
            'destination': destination,
        }
        return self.http_get(wallet_constants.BACKUP_URL, payload)

    def wallet_init(self, encryptionpassword=None):
        """
        Initializes a new wallet.
        Returns the wallet seed.
        """
        payload = None
        if encryptionpassword is not None:
            payload = {
                'encryptionpassword': encryptionpassword,
            }
        return self.http_post(wallet_constants.INIT_URL, payload).get('primaryseed')

    def wallet_load_seed(self, encryptionpassword, seed, dictionary='english'):
        """
        Gives the wallet a seed to track when looking for incoming transactions
        """
        payload = {
            'encryptionpassword': encryptionpassword,
            'dictionary': dictionary,
            'seed': seed,
        }
        return self.http_post(wallet_constants.SEED_URL, payload)

    def wallet_seeds(self, dictionary='english'):
        """
        Returns the list of seeds in use by the wallet
        """
        payload = {
            'dictionary': dictionary,
        }
        return self.http_get(wallet_constants.SEEDS_URL, payload)

    def send_siacoins(self, amount, address):
        """
        Sends siacoins to an address or set of addresses
        Returns list of transaction IDs
        """
        payload = {
            'amount': amount,
            'destination': address,
        }
        return self.http_post(wallet_constants.SIACOINS_URL, payload).get('transactionids')

    def send_siafunds(self, amount, address):
        """
        Sends siafunds to an address.
        Returns a list of transaction IDs.
        """
        payload = {
            'amount': amount,
            'destination': address,
        }
        return self.http_post(wallet_constants.SIAFUNDS_URL, payload).get('transactionids')

    def load_siagkey(self, encryptionpassword, keyfiles):
        """
        Loads a key into the wallet that was generated by siag.
        """
        payload = {
            'encryptionpassword': encryptionpassword,
            'keyfiles': keyfiles,
        }
        return self.http_post(wallet_constants.SIAGKEY_URL, payload)

    def lock_wallet(self):
        """
        Locks the wallet.
        """
        return self.http_post(wallet_constants.LOCK_URL)

    def get_transaction(self, transaction_id):
        """
        Gets the transaction associated with a specific transaction id.
        """
        return self.http_get(wallet_constants.TRANSACTION_URL + transaction_id).get('transaction')

    def get_transactions(self, startheight, endheight):
        """
        Returns a list of transactions related to the wallet in chronological order.
        """
        return self.http_get(
            wallet_constants.TRANSACTIONS_URL + '?startheight=%d&endheight=%d' % (startheight, endheight),
        )

    def get_transactions_related(self, address):
        """
        Returns a list of transactions related to the given address.
        """
        return self.http_get(wallet_constants.TRANSACTIONS_URL + address).get('transactions')

    def unlock_wallet(self, encryptionpassword):
        """
        Unlocks the wallet.
        """
        payload = {'encryptionpassword': encryptionpassword}
        return self.http_post(wallet_constants.UNLOCK_URL, payload)

    def verify_address(self, address):
        """
        Returns if the given address is valid
        """
        return self.http_get(wallet_constants.VERIFY_URL + address).get('Valid')

    def change_password(self, encryptionpassword, newpassword):
        """
        Changes the wallet's encryption key.
        """
        payload = {
            'encryptionpassword': encryptionpassword,
            'newpassword': newpassword,
        }
        return self.http_post(wallet_constants.CHANGE_PASSWORD_URL, payload)


class Sia(SiaToDeprecate):
    """
    Implements API for Sia storage. Provide support for deprecated Sia API.
    """

    @property
    def file(self):  # pylint: disable=missing-docstring
        return file.File()

    @property
    def consensus(self):  # pylint: disable=missing-docstring
        return consensus.Consensus()

    @property
    def daemon(self):  # pylint: disable=missing-docstring
        return daemon.Daemon()

    @property
    def gateway(self):  # pylint: disable=missing-docstring
        return gateway.Gateway()

    @property
    def host(self):  # pylint: disable=missing-docstring
        return host.Host()

    @property
    def hostdb(self):  # pylint: disable=missing-docstring
        return hostdb.HostDb()

    @property
    def miner(self):  # pylint: disable=missing-docstring
        return miner.Miner()

    @property
    def renter(self):  # pylint: disable=missing-docstring
        return renter.Renter()

    @property
    def wallet(self):  # pylint: disable=missing-docstring
        return wallet.Wallet()
