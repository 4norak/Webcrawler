from __future__ import annotations

from abc import ABC, abstractmethod
from concurrent.futures._base import Future
from typing import Iterator, Generator


# Remove requirement for page to be returned as Future


class BaseDownloader(ABC):
    """
    Base class for all downloader classes.
    """

    @abstractmethod
    def __enter__(self: BaseDownloader) -> BaseDownloader:
        """
        Enable use in contexts.
        """

        raise NotImplementedError()

    @abstractmethod
    def __exit__(self: BaseDownloader, *args: Any) -> None:
        """
        Enable use in contexts.
        """

        raise NotImplementedError()

    @abstractmethod
    def __iter__(self: BaseDownloader) -> Iterator[Future]:
        """
        Enable conversion to iterator.
        """

        raise NotImplementedError()

    @abstractmethod
    def __next__(self: BaseDownloader) -> Future:
        """
        Enable use as iterable.
        """

        raise NotImplementedError()
