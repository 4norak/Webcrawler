from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from json import load
from requests.utils import requote_uri
from bs4 import Tag
from typing import Callable, Any, Type
from .base_config_parser import BaseConfigParser
from .parsed_config_types import (SelectBaseFun, FilterBaseFun, ActionBaseFun,
                                  FiltersActions, TagFiltersActions, Config)
from .json_config_types import JsonConf, JsonConfFA, JsonConfTFA, JsonConfFun
from .json_config_errors import JSONConfigErrors


# TODO Strings in different file
# TODO Maybe add option to load config in background?


class JSONConfigParser(BaseConfigParser):
    """
    Class for parsing json config file in "default" format.

    :param json_config: Config loaded from json file with json.load.
    :param select_funs: Dictionary mapping select function names to the
                        respective functions.
    :param filter_funs: Dictionary mapping filter function names to the
                        respective functions.
    :param action_funs: Dictionary mapping action function names to the
                        respective functions.
    """

    __slots__ = ["_json_config", "_select_funs", "_filter_funs",
                 "_action_funs", "_executor", "_parsed_config_future"]

    def __init__(self: JSONConfigParser, json_config: JsonConf,
                 select_funs: dict[str,SelectBaseFun],
                 filter_funs: dict[str,FilterBaseFun],
                 action_funs: dict[str,ActionBaseFun]) -> None:

        if (errors := JSONConfigParser.check_json_config(json_config)):
            raise ValueError("\n".join(errors))

        # Save values needed for config parsing and returning values needed
        # in rest of program
        self._json_config = JSONConfigParser.merge_duplicate_urls(json_config)
        self._select_funs = select_funs
        self._filter_funs = filter_funs
        self._action_funs = action_funs

        # ThreadPoolExecutor used to parse config in background
        self._executor = ThreadPoolExecutor()
        # Start parsing config in background
        self._parsed_config_future = self._executor.submit(self.parse_config)

    def parse_config(self: JSONConfigParser) -> None:
        """
        Parse loaded config and return result.

        :return: The parsed config.
        """

        parsed_config: JsonConf = {}
        for url,tfa_list in self._json_config.items():
            # Parse each select-filter-action triple for url
            parsed_config[url] = [JSONConfigParser.get_tfa(tfa,
                                                           self._select_funs,
                                                           self._filter_funs,
                                                           self._action_funs)
                                  for tfa in tfa_list]
        return parsed_config

    def get_urls(self: JSONConfigParser) -> list[str]:
        """
        Return urls from config as list. Used to start fetching pages even
        before the config is parsed completely.

        :return: The list of urls in the config.
        """

        return list(self._json_config.keys())

    def get_parsed_config(self: JSONConfigParser) -> Config:
        """
        Return the fully parsed config in a format expected by the rest
        of the program.

        :return: The parsed config.
        """

        return self._parsed_config_future.result()

    @staticmethod
    def check_json_fun(fun: JsonConfFun, path: str) -> list[str]:
        """
        Check if json config function specification is syntactically valid
        and return all errors.

        :param fun: The JSON function specification.
        :param path: The path to the function specification.

        :return: A list of errors in the function specification.
        """

        if not isinstance(fun, dict):
            return [f"{path}: {JSONConfigErrors.NO_DICT.value}"]

        errors = []

        if "function" in fun.keys():
            if not isinstance(fun["function"], str):
                errors.append(
                        f"{path} -> function: {JSONConfigErrors.NO_STR.value}")
        else:
            errors.append(f"{path}: {JSONConfigErrors.NO_KEY.value} `function`")
        if "args" in fun.keys():
            if not isinstance(fun["args"], list):
                errors.append(
                        f"{path} -> args: {JSONConfigErrors.NO_LIST.value}")
        else:
            errors.append(f"{path}: {JSONConfigErrors.NO_KEY.value} `args`")
        if "kwargs" in fun.keys():
            if not isinstance(fun["kwargs"], dict):
                errors.append(
                        f"{path} -> kwargs: {JSONConfigErrors.NO_DICT.value}")
        else:
            errors.append(f"{path}: {JSONConfigErrors.NO_KEY.value} `kwargs`")

        for k in fun.keys():
            if k not in ["function", "args", "kwargs"]:
                errors.append(
                        f"{path}: {JSONConfigErrors.INV_KEY.value} `{k}`")

        return errors

    @staticmethod
    def check_json_fa(fa: JsonConfFA, path: str) -> list[str]:
        """
        Check if json config functions actions pair is syntactically valid
        and return all errors.

        :param fa: The functions actions pair.
        :param path: The pair's path.

        :return: A list of errors in the pair.
        """

        if not isinstance(fa, dict):
            return [f"{path}: {JSONConfigErrors.NO_DICT}"]

        errors = []

        for k in ["filters", "actions"]:
            if k in fa.keys():
                if isinstance(fa[k], list):
                    for i,f in enumerate(fa[k]):
                        errors += JSONConfigParser.check_json_fun(f,
                                f"{path} -> [k] -> {i}")
                else:
                    errors.append(
                            f"{path} -> {k}: {JSONConfigErrors.NO_LIST.value}")
            else:
                errors.append(f"{path}: {JSONConfigErrors.NO_KEY.value} `{k}`")

        for k in fa.keys():
            if k not in ["filters", "actions"]:
                errors.append(
                        f"{path}: {JSONConfigErrors.INV_KEY.value} `{k}`")

        return errors

    @staticmethod
    def check_json_tfa(tfa: JsonConfTFA, path: str) -> list[str]:
        """
        Check if a json config select functions actions triple is
        syntactically valid and return all errors.

        :param tfa: The select functions actions triple.
        :param path: The triple's path.

        :return: A list of errors in the triple.
        """

        if not isinstance(tfa, dict):
            return [f"{path}: {JSONConfigErrors.NO_DICT.value}"]

        errors = []

        if "select-chain" in tfa.keys():
            if isinstance(tfa["select-chain"], list):
                for i,f in enumerate(tfa["select-chain"]):
                    errors += JSONConfigParser.check_json_fun(f,
                            f"{path} -> select-chain -> {i}")
            else:
                errors.append(f"{path} -> select-chain: {JSONConfigErrors.NO_LIST.value}")
        else:
            errors.append(f"{path}: {JSONConfigErrors.NO_KEY.value} `select-chain`")
        if "filters-actions-pairs" in tfa.keys():
            if isinstance(tfa["filters-actions-pairs"], list):
                for i,fa in enumerate(tfa["filters-actions-pairs"]):
                    errors += JSONConfigParser.check_json_fa(fa,
                        f"{path} -> filters-actions-pairs -> {i}")
            else:
                errors.append(f"{path} -> filters-actions-pairs: {JSONConfigErrors.NO_LIST.value}")
        else:
            errors.append(f"{path}: {JSONConfigErrors.NO_KEY.value} `filters-actions-pairs`")

        for k in tfa.keys():
            if k not in ["select-chain", "filters-actions-pairs"]:
                errors.append(f"{path}: {JSONConfigErrors.INV_KEY.value} `{k}`")

        return errors

    @staticmethod
    def check_json_config(json_config: JsonConf) -> list[str]:
        """
        Check if json config is syntactically valid and return errors.

        :param json_config: The json config.

        :return: A list of errors in the config.
        """

        # TODO Check by config scheme

        if not isinstance(json_config, dict):
            return [f"toplevel: {JSONConfigErrors.NO_DICT}"]

        errors = []

        for url,tfas in json_config.items():
            if not isinstance(url, str):
                errors.append(f"toplevel: {JSONConfigErrors.NO_STR}")
            if not isinstance(tfas, list):
                errors.append(f"toplevel -> {url}: {JSONConfigErrors.NO_LIST}")
                continue

            for i,tfa in enumerate(tfas):
                errors += JSONConfigParser.check_json_tfa(tfa, f"toplevel -> {url} -> {i}")

        return errors

    @staticmethod
    def create_parser(config_path: str,
                      select_funs: dict[str,SelectBaseFun],
                      filter_funs: dict[str,FilterBaseFun],
                      action_funs: dict[str,ActionBaseFun]
                      ) -> JSONConfigParser:
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

        with open(config_path, "r") as file:
            return JSONConfigParser(load(file), select_funs, filter_funs,
                              action_funs)

    @staticmethod
    def normalize_url(url: str) -> str:
        """
        Return URL in normalized format to recognize duplicates.

        :param url: The url to normalize.

        :return: The normalized url.
        """

        return requote_uri(url)

    @staticmethod
    def merge_duplicate_urls(json_config: JsonConf) -> JsonConf:
        """
        Merge entries for duplicate URLs in the config and return the
        resulting config.

        :param json_config: The json config loaded from the json file.

        :return: The json config with duplicate entries merged.
        """

        new_config = {}
        for url,tag_list in json_config.items():
            n_url = JSONConfigParser.normalize_url(url)
            if n_url != url:
                # Duplicate found, save all under normalized url
                # TODO Prevent duplicate tfas
                new_config[n_url] = new_config.get(n_url, []) + tag_list

        return new_config

    @staticmethod
    def create_single_arg_fun(base_fun: Callable, *args: Any,
                              **kwargs: Any) -> Callable[[Any],Any]:
        """
        Create single arg function from arbitrary function by preparing
        function with all arguments except for the first and returning the
        prepared function.

        :param base_fun: Base function to prepare.
        :param args: Variable arguments to prepare function with.
        :param kwargs: Keyword arguments to prepare function with.

        :return: Prepared function that takes single argument.
        """

        # TODO Add Cache
        # Avoid mistake from last time: List and dict are not hashable
        return (lambda x: base_fun(x, *args, **kwargs))

    @staticmethod
    def parse_funs(fun_specs: list[JsonConfFunType],
                   fun_dict: dict[str,Callable]) -> list[Callable[[Any],Any]]:
        """
        Parse and return functions specified in json config.

        :param fun_specs: List of function specifications from json config.
        :param fun_dict: Dictionary mapping function names used in
                         fun_specs to the respective functions.

        :return: The list of parsed functions.
        """

        return [JSONConfigParser.create_single_arg_fun(fun_dict[fun_spec["function"]],
            *fun_spec["args"], **fun_spec["kwargs"])
            for fun_spec in fun_specs]

    @staticmethod
    def get_fa(config_entry: JsonConfFA,
               filter_funs: dict[str,FilterBaseFun],
               action_funs: dict[str,ActionBaseFun]) -> FiltersActions:
        """
        Parse and return a filter-action pair from a config entry.

        :param config_entry: The config entry specifying the pair.
        :param filter_funs: Dictionary mapping filter function names to the
                            respective functions.
        :param action_funs: Dictionary mapping action function names to the
                            respective functions.

        :return: The filter-action pair.
        """

        try:
            filters = JSONConfigParser.parse_funs(config_entry["filters"],
                                                  filter_funs)
        except KeyError as e:
            raise ValueError(f"{e.args[0]}: {JSONConfigErrors.INV_FUN} in filter functions")
        try:
            actions = JSONConfigParser.parse_funs(config_entry["actions"],
                                                  action_funs)
        except KeyError as e:
            raise ValueError(f"{e.args[0]}: {JSONConfigErrors.INV_FUN} in action functions")

        return FiltersActions(filters=filters, actions=actions)

    @staticmethod
    def get_tfa(config_entry: JsonConfTFA,
                select_funs: dict[str,SelectBaseFun],
                filter_funs: dict[str,FilterBaseFun],
                action_funs: dict[str,ActionBaseFun]) -> TagFiltersActions:
        """
        Parse and return a tag-filter-action triple from a config entry.

        :param config_entry: The config entry specifying the triple.
        :param select_funs: Dictionary mapping select function names to the
                            respective functions.
        :param filter_funs: Dictionary mapping filter function names to the
                            respective functions.
        :param action_funs: Dictionary mapping action function names to the
                            respective functions.

        :return: The tag-filter-action triple.
        """

        try:
            selects = JSONConfigParser.parse_funs(config_entry["select-chain"],
                                                  select_funs)
        except KeyError as e:
            raise ValueError(f"{e.args[0]}: {JSONConfigErrors.INV_FUN} in select functions")
        filters_actions = [JSONConfigParser.get_fa(ce, filter_funs,
                                                   action_funs)
                           for ce in config_entry["filters-actions-pairs"]]
        return TagFiltersActions(select=selects,
                                 filters_actions=filters_actions)
