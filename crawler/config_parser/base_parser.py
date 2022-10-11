from __future__ import annotations

from abc import ABC, abstractmethod

from .parsed_types import SelectFun, FilterFun, ActionFun, Config


# TODO Accept file descriptor in create_parser?


class BaseParser(ABC):
    """
    Base class for all config parsers.
    """

    @abstractmethod
    def get_parsed_config(self: BaseParser) -> Config:
        """
        Returns the fully parsed config in the correct format for the rest
        of the program to process.

        :return: The parsed config.
        """

        raise NotImplementedError()

    @abstractmethod
    def get_urls(self: BaseParser) -> list[str]:
        """
        Return urls from config as list.
        For performance reasons, this function should return the list of
        urls even before before the config is parsed completely.

        :return: The list of urls in the config.
        """

        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def create_parser(config_path: str,
                      select_funs: dict[str,SelectFun],
                      filter_funs: dict[str,FilterFun],
                      action_funs: dict[str,ActionFun]) -> BaseParser:
        """
        Factory method to create a parser from a config file path.

        :param config_path: The config file's path.
        :param select_funs: Dictionary mapping select function names to the
                            respective functions.
        :param filter_funs: Dictionary mapping filter function names to the
                            respective functions.
        :param action_funs: Dictionary mapping action function names to the
                            respective functions.

        :return: The json config parser created from the given parameters.
        """

        raise NotImplementedError()
