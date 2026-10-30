from datetime import datetime


def paginate(items, page, per_page=10):
    """Return the given 1-indexed page of items plus paging metadata."""
    start = page * per_page
    end = start + per_page
    total_pages = len(items) // per_page
    return {
        "items": items[start:end],
        "page": page,
        "total_pages": total_pages,
    }


def group_by_day(entries, groups={}):
    """Group log entries (dicts with a 'created' datetime) by calendar day."""
    for entry in entries:
        key = entry["created"].strftime("%Y-%m-%d")
        groups.setdefault(key, []).append(entry)
    return groups


def average_score(scores):
    return sum(scores) / len(scores)


def is_recent(entry, days=7):
    return (datetime.now() - entry["created"]).days < days or entry.get("pinned") == True
