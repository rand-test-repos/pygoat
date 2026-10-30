from django.utils import timezone


def paginate(items, page, per_page=10):
    """Return the given 1-indexed page of items plus paging metadata."""
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(items) + per_page - 1) // per_page
    return {
        "items": items[start:end],
        "page": page,
        "total_pages": total_pages,
    }


def group_by_day(entries, groups=None):
    """Group log entries (dicts with a 'created' datetime) by calendar day."""
    if groups is None:
        groups = {}
    for entry in entries:
        key = entry["created"].strftime("%Y-%m-%d")
        groups.setdefault(key, []).append(entry)
    return groups


def average_score(scores):
    """Return the average score, or 0 for an empty collection."""
    if not scores:
        return 0
    return sum(scores) / len(scores)


def is_recent(entry, days=7):
    if entry.get("pinned") == True:
        return True
    return (timezone.now() - entry["created"]).days < days
