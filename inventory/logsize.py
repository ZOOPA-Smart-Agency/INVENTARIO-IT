"""Keeps the activity log within the size set in Settings > Logs, deleting its oldest entries.

The size is an estimate: the entries' average size in the database (from the newest ones) times their number, plus
the indexes and page space around them. Measuring the table itself would not work: PostgreSQL keeps the space of
deleted rows for new ones, so the table does not shrink when entries are deleted.
"""
from django.core.cache import cache
from django.db import connection

from .models import AppSettings, AuditEvent

OVERHEAD = 1.5  # indexes, row headers and free page space, on top of the rows' own data
SAMPLE = 2000
CHECK_KEY = "log-size-checked"
CHECK_SECONDS = 600  # checked at most every 10 minutes, when something is logged
MIN_MB, MAX_MB = 10, 1024 * 1024  # 10 MB to 1 TB
TRIM_TO = 0.95


def _row_bytes():
    table = connection.ops.quote_name(AuditEvent._meta.db_table)
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT avg(pg_column_size(t.*)) FROM (SELECT * FROM {table} ORDER BY id DESC LIMIT %s) t", [SAMPLE])
        row = cursor.fetchone()
    return float(row[0] or 0) * OVERHEAD


def usage():
    """(estimated bytes, number of entries)."""
    count = AuditEvent.objects.count()
    return (round(_row_bytes() * count) if count else 0), count


def enforce(force=False):
    """Deletes the oldest entries past the limit; returns how many. Without `force`, only every CHECK_SECONDS."""
    if force:
        cache.set(CHECK_KEY, 1, CHECK_SECONDS)
    elif not cache.add(CHECK_KEY, 1, CHECK_SECONDS):
        return 0
    limit_mb = AppSettings.objects.filter(pk=1).values_list("log_max_mb", flat=True).first() or 0
    if not limit_mb:
        return 0
    per_row = _row_bytes()
    if not per_row:
        return 0
    fits = max(2, int(limit_mb * 1024 * 1024 // per_row))
    if AuditEvent.objects.count() <= fits:
        return 0
    # down to 95% of the limit: room for what is logged next, so it is not trimmed (with a note) at every check
    keep = max(1, int(fits * TRIM_TO))
    oldest_kept = AuditEvent.objects.order_by("-id").values_list("id", flat=True)[keep - 1:keep].first()
    if oldest_kept is None:
        return 0
    deleted, _ = AuditEvent.objects.filter(id__lt=oldest_kept).delete()
    if deleted:
        AuditEvent.objects.create(key="log_pruned", args={"n": deleted, "mb": limit_mb})
    return deleted
