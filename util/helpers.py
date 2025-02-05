def sort_dicts_by_key(data, key):
    return sorted(data, key=lambda x: x.get(key))