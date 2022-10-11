from typing import NamedTuple, Callable, Union, Any
from bs4 import Tag


SelectFun = Callable[[Any],Any]
FilterFun = Callable[[tuple[Tag,Tag]],bool]
ActionFun = Callable[[tuple[Tag,Tag]],None]

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
