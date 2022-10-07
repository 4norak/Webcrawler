from __future__ import annotations

from sys import stderr
from traceback import print_exception
from bs4 import BeautifulSoup, Tag

from .config_parser import BaseParser, SelectFun
from .pages_downloader import BaseDownloader
from .storage_handler import Storage


class Crawler:
    """
    Crawler to check websites for updates.

    Crawler(config_parser: BaseParser, downloader: Downloader,
            storage: Storage)

    :param config_parser: The config parser to get the config from
    :param downloader: The downloader to use for downloading the pages
    :param storage: The storage with the previous page versions
    """

    def __init__(self: Crawler, config_parser: BaseParser,
                 downloader: Downloader, storage: Storage):
        self._config_parser = config_parser
        self._storage = storage
        self._pages_downloader = downloader

    def fetch_pages(self: Crawler, *args, **kwargs) -> None:
        self._pages_downloader.init_download(self._config_parser.get_urls(),
                                             *args, **kwargs)

    def process_pages(self: Crawler):
        config = self._config_parser.get_parsed_config()
        with self._pages_downloader as pd:
            for future in pd:
                try:
                    page = BeautifulSoup(future.result().text, features="lxml")
                except Exception as e:
                    print_exception(None, e, e.__traceback__, file=stderr)
                    continue

                for tfa in config[future.original_url]:
                    try:
                        tag = Crawler.get_tag(page, tfa.select)
                    except Exception as e:
                        print_exception(None, e, e.__traceback__, file=stderr)
                        continue

                    try:
                        old_tag = Crawler.get_tag(self._storage[future.original_url],
                                                  tfa.select)
                    except Exception as e:
                        old_tag = None

                    if old_tag == tag:
                        continue
                    for fa in tfa.filters_actions:
                        if not all(map(lambda f: f(tag), fa.filters)):
                            continue
                        for action in fa.actions:
                            action(tag)

    @staticmethod
    def get_tag(base: Tag, select: list[SelectFun]):
        for f in select:
            if not base:
                return base
            base = f(base)
        return base
