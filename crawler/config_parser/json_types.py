from typing import TypeVar, Union


JsonElement = TypeVar("JsonElement", str, int, bool, list["JsonElement"],
                   dict[str,"JsonElement"])
JsonConfFun = dict[str,Union[str,list[JsonElement],dict[str,JsonElement]]]
JsonConfFA = dict[str,list[JsonConfFun]]
JsonConfTFA = dict[str,Union[list[JsonConfFun],list[JsonConfFA]]]
JsonConf = dict[str,list[JsonConfTFA]]
