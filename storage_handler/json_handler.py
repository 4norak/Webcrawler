from __future__ import annotations

from json import load, dump

from .base_handler import BaseHandler
from .storage import Storage

class JSONHandler(BaseHandler):
    """
    Class for loading json storages.
    """

    @staticmethod
    def save_storage(storage_path: str, storage: Storage) -> None:
        """
        Save storage to file.

        :param storage_path: The path to the storage file.
        :param storage: The storage to save.
        """

        if not storage_path:
            path = self._path

        assert storage_path, "Invalid path"

        with open(storage_path, "w") as file:
            dump(storage_path, dict((url, soup.prettify()) for url, soup in self._pages.items()))

    @staticmethod
    def load_storage(storage_path: str) -> Storage:
        """
        Load storage from file and return the storage object.

        :param storage_path: The path to the storage file.

        :return: The storage object.
        """

        with open(storage_path, "r") as file:
            return Storage(load(file))
