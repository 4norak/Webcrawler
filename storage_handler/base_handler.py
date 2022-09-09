from __future__ import annotations

from abc import ABC, abstractmethod

from .storage import Storage


class BaseHandler(ABC):
    """
    Base class for all storage loader classes.
    """

    @staticmethod
    @abstractmethod
    def save_storage(storage_path: str, storage: Storage) -> None:
        """
        Save storage to file.

        :param storage_path: The path to the storage file.
        :param storage: The storage to save.
        """

        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def load_storage(storage_path: str) -> Storage:
        """
        Load storage from file and return the storage object.

        :param storage_path: The path to the storage file.

        :return: The storage object.
        """

        raise NotImplementedError()
