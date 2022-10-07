from __future__ import annotations
from bs4 import BeautifulSoup


class Storage:
    """
    Storage class for stored pages.

    :param pages_dict: Dictionary mapping utls to html contents
    """

    def __init__(self: Storage, pages_dict: dict[str,str]) -> None:
        self._pages = dict((url, BeautifulSoup(html, features="lxml"))
                           for url, html in pages_dict.items())

    def export(self: Storage) -> dict[str,str]:
        """
        Export storage as dictionary (e.g. to use in storage handler class).
        """

        return dict((url, soup.prettify())
                    for url, soup in self._pages.items())

    def __getitem__(self: JSONStorage, url: str) -> BeautifulSoup:
        """
        Return a saved web page by url or none if the page is not saved.

        :param url: The page's url.

        :return: The page's BeautifulSoup object.
        """

        return self._pages.get(url, None)

    def __setitem__(self: JSONStorage, url: str, page: BeautifulSoup) -> None:
        """
        Save a web page for a specific url.

        :param url: The page's url.
        :param page: The page's BeautifulSoup object
        """

        assert isinstance(url, str), "The url has to be a string"
        assert isinstance(page, BeautifulSoup), "The page has to be a BeautifulSoup object"

        self._pages[url] = page

    def __iter__(self):
        """
        Enable conversion to iterator.
        """

        return iter(self._pages.items())

    def __next__(self):
        """
        Enable use as iterable.
        """

        if not hasattr(self.__next__, "it"):
            self.__next__.it = iter(self._pages.items())

        try:
            return next(self.__next__.it)
        except StopIteration as e:
            del self.__next__.it
            raise e
