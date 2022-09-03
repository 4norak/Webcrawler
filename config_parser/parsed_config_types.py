from typing import NamedTuple, Callable, Union
from bs4 import Tag


SelectBaseFun = Callable[...,Union[Tag,list[Tag]]]
FilterBaseFun = Callable[...,bool]
ActionBaseFun = Callable[...,None]

SelectFun = Callable[[Tag],Union[Tag,list[Tag]]]
FilterFun = Callable[[Tag],bool]
ActionFun = Callable[[Tag],None]

FiltersActions = NamedTuple( # TODO Find better name
    "FiltersActions",
    [
        ("filters", list[FilterFun]),
        ("actions", list[ActionFun])
    ]
)
TagFiltersActions = NamedTuple( # TODO Find better name
    "TagFiltersActions",
    [
        ("select", list[SelectFun]),
        ("filters_actions", list[FiltersActions])
    ]
)

Config = dict[str,list[TagFiltersActions]]
