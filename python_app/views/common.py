import html
from datetime import datetime, timezone

from config import STATUS_LABELS

EXCERPT_LENGTH = 160


def format_time_ago(iso_timestamp: str) -> str:
    created = datetime.fromisoformat(iso_timestamp)
    seconds = max(0, int((datetime.now(timezone.utc) - created).total_seconds()))
    if seconds < 60:
        return "just now"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes} min ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours} hr ago"
    days = hours // 24
    if days < 7:
        return f"{days} day{'s' if days != 1 else ''} ago"
    return created.strftime("%b %d, %Y")


def status_label(status: str) -> str:
    return STATUS_LABELS[status]


def escape(text: str) -> str:
    return html.escape(text, quote=True)
