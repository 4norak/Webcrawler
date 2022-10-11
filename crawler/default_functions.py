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


# Select functions can return anything but will be chained, so the next
# function has to be able to handle the previous function's output
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
    "re_match": (lambda tags,re: match(re,str(tags[0])) is not None),
    "re_match_text": (lambda tags,re: match(re,tags[0].text) is not None),
    "re_match_string": (lambda tags,re: match(re,tags[0].string) is not None),
    "re_search": (lambda tags,re: search(re,str(tags[0])) is not None),
    "re_search_text": (lambda tags,re: search(re,tags[0].text) is not None),
    "re_search_string": (lambda tags,re: search(re,tags[0].string) is not None)
}

# Action functions should not return anything
# If they do, the return value will be ignored
ACTION_FUNCTIONS = {
    "print_no_tag": (lambda tags,*args,**kwargs: print(*args, **kwargs)),
    "print_tag": (lambda tags,*args,**kwargs: print(tags[0], *args, **kwargs)),
    "print_tags": (lambda tags,sep,*args,**kwargs: print(f"{tags[0]}{sep}{tags[1]}", *args, **kwargs))
}
