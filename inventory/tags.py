"""Asset tags: the suggested next one, and which identifiers are already taken.

A tag is the prefix, the device type's code and a number: Z + LAP + 001 = ZLAP001. The number (the identifier)
is counted, as Settings > General chooses:

- "type": separately for each code (ZLAP001, ZMB001, ZLAP002). Types sharing a code share it.
- "global": once across every device (ZLAP001, ZMB002, ZLAP003).

The next number is one more than the highest in use. A type without a code gets the prefix and the number: Z0001.
No two devices can share a tag (ignoring case), nor an identifier counted together (ZLAP1 and ZLAP001 are the same).
"""
import re

from . import models as m

CODED_DIGITS = 3
PLAIN_DIGITS = 4
NUMBERED = re.compile(r"([A-Za-z]*)(\d+)")
SCOPES = {"type", "global"}


def parts(tag, prefix):
    """(code, number) for a tag in the scheme, such as ("LAP", 1) for ZLAP001; None for any other tag."""
    if not tag.lower().startswith(prefix.lower()):
        return None
    found = NUMBERED.fullmatch(tag[len(prefix):])
    return (found.group(1).upper(), int(found.group(2))) if found else None


def _settings(prefix, scope):
    if prefix is None or scope is None:
        s = m.AppSettings.load()
        prefix = s.tag_prefix if prefix is None else prefix
        scope = s.tag_numbering if scope is None else scope
    return prefix, scope


def next_tag(dtype=None, prefix=None, scope=None):
    prefix, scope = _settings(prefix, scope)
    code = dtype.code if dtype is not None else ""
    used = [p for tag in m.Device.objects.values_list("tag", flat=True) if (p := parts(tag, prefix))]
    if scope != "global":
        used = [p for p in used if p[0] == code]
    number = max((n for _, n in used), default=0) + 1
    return f"{prefix}{code}{number:0{CODED_DIGITS if code else PLAIN_DIGITS}d}"


def conflict(tag, exclude_pk=None, prefix=None, scope=None):
    """The device that already has this tag, or this tag's identifier; None when it is free."""
    others = m.Device.objects.exclude(pk=exclude_pk) if exclude_pk else m.Device.objects.all()
    same = others.filter(tag__iexact=tag).first()
    if same or not tag:
        return same
    prefix, scope = _settings(prefix, scope)
    mine = parts(tag, prefix)
    if mine is None:
        return None
    for other in others.filter(tag__istartswith=prefix).only("pk", "tag"):
        theirs = parts(other.tag, prefix)
        if theirs and theirs[1] == mine[1] and (scope == "global" or theirs[0] == mine[0]):
            return other
    return None
