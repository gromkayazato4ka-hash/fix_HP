from collections import defaultdict


_CACHE = defaultdict(dict)


def set_cache(obj_name, payload):
    _CACHE[obj_name] = payload


def get_cache(obj_name):
    return _CACHE.get(obj_name, {})


def clear_cache(obj_name):
    _CACHE.pop(obj_name, None)
