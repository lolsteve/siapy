"""
Host API.
"""

from sia.constants import host as host_constants
from sia.mixins.http import Http


class Host:
    """
    Implement host-API for Sia storage.
    """
    def __init__(self):
        self.http = Http()

    def get_host(self):
        """
        Returns information about the host.
        """
        return self.http.get(host_constants.HOST_URL)

    def set_host(self, host_settings):
        """
        Configures hosting parameters.
        """
        return self.http.post(host_constants.HOST_URL, host_settings)

    def host_announce(self, netaddress=None):
        """
        Announces the host to the network as a source of storage.
        """
        payload = None
        if netaddress is not None:
            payload = {
                'netaddress': netaddress,
            }
        return self.http.post(host_constants.ANNOUNCE_URL, payload)

    def host_storage(self):
        """
        Returns a list of folders tracked by the storage manager.
        """
        return self.http.get(host_constants.STORAGE_URL).get('folders')

    def host_storage_add(self, path, size):
        """
        Adds a storage folder to the manager.
        """
        payload = {
            'path': path,
            'size': size,
        }
        return self.http.post(host_constants.STORAGE_ADD_URL, payload)

    def host_storage_remove(self, path, force=False):
        """
        Removes a folder from the storage manager.
        """
        payload = {
            'path': path,
            'force': force,
        }
        return self.http.post(host_constants.STORAGE_REMOVE_URL, payload)

    def host_storage_resize(self, path, size):
        """
        Resizes a folder in the manager.
        """
        payload = {
            'path': path,
            'size': size,
        }
        return self.http.post(host_constants.RESIZE_STORAGE_URL, payload)

    def host_storage_sector_delete(self, merkleroot):
        """
        Deletes a sector from the manager.
        """
        return self.http.post(host_constants.STORAGE_SECTOR_URL + merkleroot)

    def host_estimatescore(self, host_settings=None):
        """
        Returns the estimated HostDB score of the host using its current settings, combined with the provided settings.
        """
        return self.http.get(host_constants.ESTIMATE_SCORE_URL, host_settings)
