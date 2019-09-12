from InfoString import InfoString
from typing import Dict, Tuple

info: Dict[Tuple[str, str], InfoString] = {}


def complete_info(start, max_items=None):
    ids = set()
    items = []
    queue = [start]
    while len(queue) > 0:
        current_id = queue.pop()
        if current_id in ids:
            continue
        ids.add(current_id)
        item = info[current_id]
        items.append(f"{item.colourise(*current_id)}: {item.formatted}")
        for new_id in item.refs:
            queue.append(new_id)
        if max_items is not None and len(ids) >= max_items:
            break
    return items
