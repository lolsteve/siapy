import requests

class Sia:

    address = 'http://localhost'
    port = 9980
    headers = {
        'User-Agent': 'Sia-Agent',
    }

    def __init__(self, address='http://localhost', port=9980):
        self.set_address(address)
        self.set_port(port)

    def set_address(self, address='http://localhost'):
        """Sets address of Sia object to send requests to.
        If no address is set, resets to localhost.
        """
        self.address = address

    def set_port(self, port=9980):
        """Sets port of Sia object to send requests to.
        If no port is set, resets to 9980.
        """
        self.port = port

    def http_get(self, path, data=None):
        """Helper HTTP GET request function.
        Sends HTTP GET request to given path.
        Attempts to return json decoded dict.
        Returns whole response if response is not json encoded.
        """
        url = self.address + ':' + str(self.port) + path
        resp = requests.get(url, headers=self.headers, files=data)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise SiaError(resp.status_code, resp.json().get('message')) from e
        try:
            return resp.json()
        except ValueError as e:
            return resp

    def http_post(self, path, data=None):
        """Helper HTTP POST request function.
        Sends HTTP POST request to given path with given payload.
        """
        url = self.address + ':' + str(self.port) + path
        resp = requests.post(url, headers=self.headers, data=data)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise SiaError(resp.status_code, resp.json().get('message')) from e
        try:
            return resp.json()
        except ValueError as e:
            return resp

    """Daemon API"""

    def get_constants(self):
        """Returns set of constants in use."""
        return self.http_get('/daemon/constants')

    def stop(self):
        """Cleanly shuts down the daemon."""
        return self.http_get('daemon/stop')

    def get_version(self):
        """Returns the version of siad running."""
        version = self.http_get('/daemon/version')
        return version.get('version')

    """Consensus API"""

    def get_consensus(self):
        """Returns information about the consensus set."""
        return self.http_get('/consensus')

    """Gateway API"""

    def get_gateway(self):
        """Returns information aout the gateway."""
        return self.http_get('/gateway')

    def gateway_connect(self, netaddress):
        """Connects the gateway to a peer."""
        self.http_post('/gateway/connect/' + netaddress)

    def gateway_disconnect(self, netaddress):
        """Disconnects the gateway from a peer."""
        self.http_post('/gateway/disconnect/' + netaddress)

    """Host API"""

    def get_host(self):
        """Returns information about the host."""
        return self.http_get('/host')

    def host_announce(self, netaddress=None):
        """Announces the host to the network as a source of storage."""
        payload = None
        if netaddress is not None:
            payload = { 'netaddress' : netaddress }
        self.http_post('/host/announce', payload)

    def host_storage(self):
        """Returns a list of folders tracked by the storage manager."""
        return self.http_get('/host/storage').get('folders')

    def host_storage_add(self, path, size):
        """Adds a storage folder to the manager."""
        payload = { 'path' : path, 'size' : size }
        self.http_post('/host/storage/folders/add', payload)

    def host_storage_remove(self, path, force=False):
        """Removes a folder from the storage manager."""
        payload = { 'path' : path, 'force' : force }
        self.http_post('/host/storage/folders/remove', payload)

    def host_storage_resize(self, path, size):
        """Resizes a folder in the manager."""
        payload = { 'path' : path, 'size' : size }
        self.http_post('/host/storage/folder/resize', payload)

    def host_storage_sector_delete(self, merkleroot):
        """Deletes a sector from the manager."""
        self.http_post('/host/storage/sector/' + merkleroot)

    """HostDB API"""

    def get_hostdb(self):
        """Returns list of all known hosts."""
        return self.http_get('/hostdb/all').get('hosts')

    def get_hostdb_active(self, numhosts=None):
        """Returns list of active hosts.
        Optional parameter numhosts for maximum number of hosts returned.
        """
        payload = None
        if numhosts is not None:
            payload = { 'numhosts' : (None, str(numhosts)) }
        return self.http_get('/hostdb/active', payload).get('hosts')

    """Miner API"""

    def get_miner(self):
        """Returns status of the miner."""
        return self.http_get('/miner')

    def start_miner(self):
        """Starts a single threaded CPU miner."""
        return self.http_get('/miner/start')

    def stop_miner(self):
        """Stops the CPU miner."""
        return self.http_get('/miner/stop')

    def get_block_header(self):
        """Returns a block header for mining.
        Returned as bytes.
        """
        return self.http_get('/miner/header').content

    """Renter API"""

    def get_renter(self):
        """Returns current renter settings."""
        return self.http_get('/renter')

    def get_renter_contracts(self):
        """Returns a list of active contracts."""
        return self.http_get('/renter/contracts').get('contracts')

    def get_downloads(self):
        """Returns a list of files in the download queue."""
        return self.http_get('renter/downloads').get('downloads')

    def get_files(self):
        """Returns a list of all files."""
        files = self.http_get('/renter/files')
        return files.get('files')

    def delete_file(self, siapath):
        """Deletes a renter file."""
        self.http_post('/renter/delete/' + siapath)

    def download_file(self, path, siapath):
        """Downloads a file from sia.
        """
        payload = { 'destination': (None, path) }
        self.http_get('/renter/download/'+ siapath, payload)

    def rename_file(self, siapath, newsiapath):
        """Renames a file."""
        payload = { 'newsiapath' : newsiapath }
        self.http_post('/renter/rename/' + siapath, payload)

    def upload_file(self, path, siapath):
        """Uploads a file to sia.
        """
        payload = { 'source': path }
        self.http_post('/renter/upload/' + siapath, payload)

    """Wallet API"""

    def get_wallet(self):
        """Returns information aout the wallet."""
        return self.http_get('/wallet')

    def load_033x(self, source, encryptionpassword):
        payload = { 'source' : source, 'encryptionpassword' : encryptionpassword }
        self.http_post('/wallet/033x', payload)

    def get_address(self):
        """Returns a single address from the wallet."""
        return self.http_get('/wallet/address').get('address')

    def get_addresses(self):
        """Returns a list of addresses from the wallet."""
        return self.http_get('/wallet/addresses').get('addresses')

    def backup_wallet(self, destination):
        """Creates a backup of the wallet settings."""
        payload = { 'destination' : destination }
        return self.http_get('/wallet/backup', payload)

    def wallet_init(self, encryptionpassword=None):
        """Initializes a new wallet.
        Returns the wallet seed.
        """
        payload = None
        if encryptionpassword is not None:
            payload = { 'encryptionpassword' : encryptionpassword }
        return self.http_post('/wallet/init', payload).get('primaryseed')

    def wallet_load_seed(self, encryptionpassword, seed, dictionary='english'):
        payload = { 'encryptionpassword' : encryptionpassword,
                   'dictionary' : dictionary,
                   'seed' :  seed }
        self.http_post('/wallet/seed', payload)

    def wallet_seeds(self, dictionary='english'):
        payload = { 'dictionary' : dictionary }
        return self.http_get('/wallet/seeds', payload)

    def send_siacoins(self, amount, address):
        payload = { 'amount' : amount, 'destination' : address }
        return self.http_post('/wallet/siacoins', payload).get('transactionids')

    def send_siafunds(self, amount, address):
        payload = { 'amount' : amount, 'destination' : address }
        return self.http_post('/wallet/siacfunds', payload).get('transactionids')

    def load_siagkey(self, encryptionpassword, keyfiles):
        payload = { 'encryptionpassword' : encryptionpassword,
                   'keyfiles' : keyfiles }
        self.http_post('/wallet/siagkey', payload)

    def lock_wallet(self):
        """Locks the wallet."""
        self.http_post('/wallet/lock')

    def get_transaction(self, transaction_id):
        return self.http_get('/wallet/transaction/' + transaction_id, payload).get('transaction')

    def get_transactions(self, startheight, endheight):
        payload = { 'startheight' : startheight, 'endheight' : endheight }
        return self.http_get('/wallet/transactions', payload)

    def get_transactions_related(self, address):
        """Returns a list of transactions related to the given address."""
        return self.http_get('/wallet/transactions/' + address).get('transactions')

    def unlock_wallet(self, encryptionpassword):
        """Unlocks the wallet."""
        payload = { 'encryptionpassword' : encryptionpassword }
        self.http_post('/wallet/unlock', payload)

class SiaError(Exception):

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

