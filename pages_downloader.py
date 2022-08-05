from __future__ import annotations
from concurrent.futures import as_completed
from concurrent.futures._base import Future
from requests_futures.sessions import FuturesSession
from typing import Iterator, Generator


# TODO Maybe remove cookies by passing custom subclass of Session to FuturesSessions


class PagesDownloader:
    """
    Downloads web pages concurrently and acts as an iterator over them
    The download starts as soon as the object is created. The iterator
    blocks and returns the next result as soon as it is available.

    PagesDownloader(urls: list[str], futures_session_kwargs: dict = {})

    :param urls: The list of urls to download the web pages from.
    :param futures_session_kwargs: Passed to
    requests_futures.sessions.FuturesSession.__init__ as kwargs.
    FuturesSession is used internally to download the web pages.
    """

    def __init__(self, urls: list[str], futures_session_kwargs: dict = {},
                 get_kwargs: dict = {}) -> None:
        # Session used to fetch web pages. Only stored to gracefully close it later
        self._session: FuturesSession = FuturesSession(*futures_session_kwargs)
        # Iterator over all Futures containing fully downloaded web pages
        self._complete_futures: Iterator[Future] = as_completed(
            [self._session.get(u, **get_kwargs) for u in urls]
        )

    def close(self) -> None:
        """
        Closes all open connections.
        """

        # Close used session with all open connections
        self._session.close()

    def _create_generator(self) -> Generator[Future,None,None]:
        yield from self._complete_futures

    def __enter__(self) -> PagesDownloader:
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def __iter__(self) -> Generator[Future,None,None]:
        yield from self._complete_futures

    def __next__(self) -> Future:
        return next(iter(self))
