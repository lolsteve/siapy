"""
Provide functionality for most common HTTP-methods.
"""
import requests

from sia.constants import http as http_constants
from sia.errors.http import SiaError


class HttpMixinToDeprecate:
    """
    Implements functionality of most common HTTP-methods.
    """

    def __init__(self, address=http_constants.DEFAULT_ADDRESS, port=http_constants.DEFAULT_PORT):
        self.address = address
        self.port = port
        self.headers = http_constants.DEFAULT_HEADERS

    def http_get(self, path, data=None):
        """
        Helper HTTP GET request function that returns a decoded json dict.
        """
        url = self.address + ':' + str(self.port) + path
        resp = requests.get(url, headers=self.headers, files=data)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            raise SiaError(resp.status_code, resp.json().get('message'))
        return resp.json()

    def http_get_bytes(self, path, data=None):
        """
        Helper HTTP GET request function that returns a byte array.
        """
        url = self.address + ':' + str(self.port) + path
        resp = requests.get(url, headers=self.headers, files=data)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            raise SiaError(resp.status_code, resp.json().get('message'))
        return resp

    def http_post(self, path, data=None):
        """
        Helper HTTP POST request function.
        Sends HTTP POST request to given path with given payload.
        """
        url = self.address + ':' + str(self.port) + path
        resp = requests.post(url, headers=self.headers, data=data)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            raise SiaError(resp.status_code, resp.json().get('message'))
        try:
            return resp.json()
        except ValueError:
            return resp


class Http:
    """
    Implements functionality of most common HTTP-methods.
    """

    @staticmethod
    def get(path, data=None):  # pylint: disable=missing-docstring
        return HttpMixinToDeprecate().http_get(path, data)

    @staticmethod
    def post(path, data=None):  # pylint: disable=missing-docstring
        return HttpMixinToDeprecate.http_post(path, data)

    @staticmethod
    def get_bytes(path, data=None):  # pylint: disable=missing-docstring
        return HttpMixinToDeprecate.http_get_bytes(path, data)
