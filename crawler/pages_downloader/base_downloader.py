from __future__ import annotations

from abc import ABC, abstractmethod
from concurrent.futures._base import Future
from typing import Iterator, Generator


# Remove requirement for page to be returned as Future


class BaseDownloader(ABC):
    """
    Base class for all downloader classes.
    """


    # TODO Avoid collisions in args and kwargs
    @abstractmethod
    def init_download(self: BaseDownloader, urls: list[str], *args: Any,
                      **kwargs: Any) -> None:
        """
        Initialize the downloader with the respective URLs and arguments.

        :param urls: The list of urls to download the web pages from
        :param args: Arbitrary arguments accepted by the child class
        :param kwargs: Arbitrary keyword arguments accepted by the child class
        """

        raise NotImplementedError()

    def __enter__(self: BaseDownloader) -> BaseDownloader:
        """
        Enable use in contexts.
        """

        return self

    def __exit__(self: BaseDownloader, *args: Any) -> None:
        """
        Enable use in contexts.
        """

        pass

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
