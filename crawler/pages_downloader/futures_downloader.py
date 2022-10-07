from __future__ import annotations

from concurrent.futures import as_completed
from concurrent.futures._base import Future
from requests_futures.sessions import FuturesSession
from typing import Iterator, Generator, Any

from .base_downloader import BaseDownloader


# TODO Maybe remove cookies by passing custom subclass of Session to FuturesSessions
# TODO Use __slots__


class FuturesDownloader(BaseDownloader):
    """
    Downloads web pages concurrently and acts as an iterator over them
    The download starts as soon as init_download is called. The iterator
    blocks and returns the next result as soon as it is available.
    """

    def init_download(self: FuturesDownloader, urls: list[str],
                      futures_session_kwargs: dict = {}, get_kwargs: dict = {}
                     ) -> None:
        """
        Initialize and start the downloader with the respective URLs and
        arguments.

        :param urls: The list of urls to download the web pages from.
        :param futures_session_kwargs: Passed to
        requests_futures.sessions.FuturesSession.__init__ as kwargs.
        FuturesSession is used internally to download the web pages.
        """

        # Session used to fetch web pages. Only stored to gracefully close it later
        self._session: FuturesSession = FuturesSession(*futures_session_kwargs)
        # Iterator over all Futures containing fully downloaded web pages
        futures = []
        for u in urls:
            futures.append(self._session.get(u, **get_kwargs))
            futures[-1].original_url = u
        self._complete_futures: Iterator[Future] = as_completed(futures)

    def close(self: FuturesDownloader) -> None:
        """
        Closes all open connections.
        """

        # Close used session with all open connections
        self._session.close()

    def __enter__(self: FuturesDownloader) -> FuturesDownloader:
        """
        Enable use in contexts.
        """

        return self

    def __exit__(self: FuturesDownloader, *args: Any) -> None:
        """
        Enable use in contexts.
        """

        self.close()

    def __iter__(self: FuturesDownloader) -> Generator[Future,None,None]:
        """
        Enable conversion to iterator.
        """

        yield from self._complete_futures

    def __next__(self: FuturesDownloader) -> Future:
        """
        Enable use as iterable.
        """

        return next(iter(self))
