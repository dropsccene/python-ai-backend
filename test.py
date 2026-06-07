def add_to_list(item,items=None):
    if items is None:
        items = []
    items.append(item)
    return items