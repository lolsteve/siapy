"""
Provide custom exception to use inside Sia package.
"""
class SiaError(Exception):
    """
    Exception raised when errors returned from sia daemon.
    """
    def __init__(self, status_code, message):
        super(SiaError, self).__init__(message)
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return 'HTTP code: ' + repr(self.status_code) + ' With message: ' + repr(self.message)
