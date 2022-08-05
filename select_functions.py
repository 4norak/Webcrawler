from bs4 import Tag as _Tag

def _getitem(tag, item):
    return tag[item]

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
