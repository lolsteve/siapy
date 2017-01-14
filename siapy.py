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
        self.address = address

    def set_port(self, port=9980):
        self.port = port

    def http_get(self, path):
        url = self.address + ':' + str(self.port) + path
        resp = requests.get(url, headers=self.headers)
        if resp.status_code != 200:
            raise SiaError(resp.status_code, resp.json().get('message'))
        return resp.json()

    def get_version(self):
        version = self.http_get('/daemon/version')
        return version.get('version')

    def get_files(self):
        files = self.http_get('/renter/files')
        return files.get('files')

class SiaError(Exception):

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

