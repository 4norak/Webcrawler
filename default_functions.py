from typing import Any
from bs4 import Tag as _Tag
from re import match as _match, search as _search


def _getitem(tag: Tag, item: str) -> Any:
    """
    Return a tag attribute by name.

    :param tag: The tag the attribute belongs to.
    :param item: The attribute's name.
    """

    return tag[item]


# Select Functions must return bs4.Tag or List of bs4.Tag
SELECT_FUNCTIONS = {
    "select": _Tag.select,
    "find": _Tag.find,
    "find_next": _Tag.find_next,
    "find_previous": _Tag.find_previous,
    "find_next_sibling": _Tag.find_next_sibling,
    "find_previous_sibling": _Tag.find_previous_sibling,
    "find_parent": _Tag.find_parent,
    "find_all": _Tag.find_all,
    "find_all_next": _Tag.find_all_next,
    "find_all_previous": _Tag.find_all_previous,
    "find_next_siblings": _Tag.find_next_siblings,
    "find_previous_siblings": _Tag.find_previous_siblings,
    "find_parents": _Tag.find_parents,
    "children": (lambda tag: tag.children),
    "getitem": _getitem,
    "[]": _getitem
}

# Filter functions must return a boolean
FILTER_FUNCTIONS = {
    "match": (lambda tag,re: _match(re,str(tag)) is not None),
    "match_text": (lambda tag,re: _match(re,tag.text) is not None),
    "match_string": (lambda tag,re: _match(re,tag.string) is not None),
    "search": (lambda tag,re: _search(re,str(tag)) is not None),
    "search_text": (lambda tag,re: _search(re,tag.text) is not None),
    "search_string": (lambda tag,re: _search(re,tag.string) is not None)
}

# Action functions should not return anything
# If they do, the return value will be ignored
ACTION_FUNCTIONS = {
    "print_no_tag": (lambda tag,*args,**kwargs: print(*args, **kwargs)),
    "print_tag": print
}
