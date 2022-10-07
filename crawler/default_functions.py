from typing import Any as Any
from bs4 import Tag as Tag
from re import match as match, search as search


def getitem(tag: Tag, item: str) -> Any:
    """
    Return a tag attribute by name.

    :param tag: The tag the attribute belongs to.
    :param item: The attribute's name.
    """

    return tag[item]


# Select Functions must return bs4.Tag or List of bs4.Tag
SELECT_FUNCTIONS = {
    "select": Tag.select,
    "find": Tag.find,
    "find_next": Tag.find_next,
    "find_previous": Tag.find_previous,
    "find_next_sibling": Tag.find_next_sibling,
    "find_previous_sibling": Tag.find_previous_sibling,
    "find_parent": Tag.find_parent,
    "find_all": Tag.find_all,
    "find_all_next": Tag.find_all_next,
    "find_all_previous": Tag.find_all_previous,
    "find_next_siblings": Tag.find_next_siblings,
    "find_previous_siblings": Tag.find_previous_siblings,
    "find_parents": Tag.find_parents,
    "children": (lambda tag: tag.children),
    "getitem": getitem,
    "[]": getitem
}

# Filter functions must return a boolean
FILTER_FUNCTIONS = {
    "re_match": (lambda tag,re: match(re,str(tag)) is not None),
    "re_match_text": (lambda tag,re: match(re,tag.text) is not None),
    "re_match_string": (lambda tag,re: match(re,tag.string) is not None),
    "re_search": (lambda tag,re: search(re,str(tag)) is not None),
    "re_search_text": (lambda tag,re: search(re,tag.text) is not None),
    "re_search_string": (lambda tag,re: search(re,tag.string) is not None)
}

# Action functions should not return anything
# If they do, the return value will be ignored
ACTION_FUNCTIONS = {
    "print_no_tag": (lambda tag,*args,**kwargs: print(*args, **kwargs)),
    "print_tag": print
}
