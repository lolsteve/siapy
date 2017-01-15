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
        """
        url = self.address + ':' + str(self.port) + path
        resp = requests.get(url, headers=self.headers, files=data)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise SiaError(resp.status_code, resp.json().get('message')) from e
        return resp.json()

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

    def get_version(self):
        """Returns the version of siad running."""
        version = self.http_get('/daemon/version')
        return version.get('version')

    def get_consensus(self):
        """Returns information about the consensus set."""
        return self.http_get('/consensus')

    def get_gateway(self):
        """Returns information aout the gateway."""
        return self.http_get('/gateway')

    def get_host(self):
        """Returns information about the host."""
        return self.http_get('/host')

    def get_files(self):
        """Returns a list of all files."""
        files = self.http_get('/renter/files')
        return files.get('files')

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

    def get_renter(self):
        """Returns information about the renter."""
        return self.http_get('/renter')

    def download_file(self, path, siapath):
        """Downloads a file from sia.
        """
        payload = { 'destination': (None, path) }
        self.http_get('/renter/download/'+ siapath, payload)

    def upload_file(self, path, siapath):
        """Uploads a file to sia.
        """
        payload = { 'source': path }
        self.http_post('/renter/upload/' + siapath, payload)

    def get_wallet(self):
        """Returns information aout the wallet."""
        return self.http_get('/wallet')

    def get_address(self):
        """Returns a single address from the wallet."""
        return self.http_get('/wallet/address').get('address')

    def get_addresses(self):
        """Returns a list of addresses from the wallet."""
        return self.http_get('/wallet/addresses').get('addresses')

    def lock_wallet(self):
        """Locks the wallet."""
        self.http_post('/wallet/lock')

    def unlock_wallet(self, encryptionpassword):
        """Unlocks the wallet."""
        payload = { 'encryptionpassword' : encryptionpassword }
        self.http_post('/wallet/unlock', payload)

class SiaError(Exception):

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

