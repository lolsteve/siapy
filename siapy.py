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

    def http_get(self, path):
        """Helper HTTP GET request function.
        Sends HTTP GET request to given path.
        """
        url = self.address + ':' + str(self.port) + path
        resp = requests.get(url, headers=self.headers)
        if resp.status_code != 200:
            raise SiaError(resp.status_code, resp.json().get('message'))
        return resp.json()

    def http_post(self, path, data):
        """Helper HTTP POST request function.
        Sends HTTP POST request to given path with given payload.
        Returns True on success.
        """
        url = self.address + ':' + str(self.port) + path
        resp = requests.post(url, headers=self.headers, data=data)
        if resp.status_code not in (200, 204):
            raise SiaError(resp.status_code, resp.json().get('message'))
        return True

    def get_version(self):
        """Returns the version of siad running."""
        version = self.http_get('/daemon/version')
        return version.get('version')

    def get_files(self):
        """Returns a list of all files."""
        files = self.http_get('/renter/files')
        return files.get('files')

    def upload_file(self, path, siapath):
        """Uploads a file to sia."""
        payload = { 'source': path }
        resp = self.http_post('/renter/upload/' + siapath, payload)
        return resp

class SiaError(Exception):

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

