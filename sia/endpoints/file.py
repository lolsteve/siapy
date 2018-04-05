"""
File API.
"""
from sia.constants import file as file_constants
from sia.mixins.http import Http


class File:
    """
    Implement file-API for Sia storage.
    """
    def __init__(self):
        self.http = Http()

    def list(self):
        """
        Returns a list of all files.
        """
        files = self.http.get(file_constants.LIST_URL)
        return files.get('files')

    def delete(self, siapath):
        """
        Deletes a renter file.
        """
        self.http.post(file_constants.DELETE_URL + siapath)

    def download(self, path, siapath):
        """
        Downloads a file from sia.
        """
        payload = {
            'destination': (None, path),
        }
        self.http.get(file_constants.DOWNLOAD_URL + siapath, payload)

    def rename(self, siapath, newsiapath):
        """
        Renames a file.
        """
        payload = {
            'newsiapath': newsiapath,
        }
        self.http.post(file_constants.RENAME_URL + siapath, payload)

    def upload(self, source_path, siapath):
        """
        Uploads a file to sia.
        """
        payload = {
            'source': source_path,
        }
        self.http.post(file_constants.UPLOAD_URL + siapath, payload)
