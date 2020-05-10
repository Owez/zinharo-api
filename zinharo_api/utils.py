import os


class Config:
    """
    Config class for getting enviroment variables and crucial setup constants
    """

    def _get_var(self, name):
        """
        Frontend to slot in var-getting
        """

        return os.environ[name]

    def _get_var_flag(self, text):
        """
        Gets an environment variable and converts it into a bool.

        If env var doesn't exist or can't convert to a bool, returns False
        If env var is found, returns the value.
        """

        try:
            return bool(self._get_var("DEBUG"))
        except:
            return False

    def _get_api_prefix(self):
        """
        Gets the api prefix from optinoal environment variables,
        defaulting to `/api` (@ API_PREFIX_DEFAULT) if not found.
        """

        API_PREFIX_DEFAULT = "" # none for production with `api.` subdomain

        try:
            return self._get_var("API_PREFIX")
        except:
            return API_PREFIX_DEFAULT

    def __init__(self):
        self.MIN_API_VERSION = "0.0.1"
        self.DEBUG = self._get_var_flag("DEBUG")
        self.API_PREFIX = self._get_api_prefix()
        self.SECRET_KEY = self._get_var("SECRET_KEY")
