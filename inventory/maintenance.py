"""Maintenance mode: while a backup is being restored the app is closed to everyone else.

The state lives in its own table and is written through a second database connection ("side"), so other
requests see it, and the restore's progress, straight away, even though the restore itself runs in one long
transaction. If the process doing the work dies, the state goes stale after STALE and the app opens again.
"""
import time
from datetime import timedelta

from django.db.models import Q
from django.utils import timezone

from .models import Maintenance, User

SIDE = "side"
STALE = timedelta(minutes=5)


def current():
    """The active maintenance, or None."""
    state = Maintenance.objects.filter(pk=1, active=True).first()
    if state is None or state.updated_at is None or timezone.now() - state.updated_at > STALE:
        return None
    return state


def info(state, user):
    """What a visitor may know: administrators can follow the restore, everyone else only sees maintenance."""
    out = {"kind": state.kind, "canWatch": bool(getattr(user, "is_authenticated", False) and user.rol == User.Role.ADMIN)}
    if out["canWatch"]:
        out.update(startedBy=state.started_by, startedAt=state.started_at.isoformat() if state.started_at else None,
                   phase=state.phase, done=state.done, total=state.total)
    return out


def claim(kind, user):
    """Starts maintenance; False if another one is already running."""
    Maintenance.objects.using(SIDE).get_or_create(pk=1)
    now = timezone.now()
    free = Q(active=False) | Q(updated_at__lt=now - STALE)
    claimed = Maintenance.objects.using(SIDE).filter(free, pk=1).update(
        active=True, kind=kind, started_at=now, started_by=user.nombre, phase="reading", done=0, total=0, updated_at=now)
    return claimed == 1


def release():
    Maintenance.objects.using(SIDE).filter(pk=1).update(active=False, phase="", done=0, total=0, updated_at=timezone.now())


class Reporter:
    """Records progress for everyone watching, at most a few times a second."""

    def __init__(self):
        self.last = 0.0
        self.phase = None

    def __call__(self, phase, done, total):
        now = time.monotonic()
        if phase == self.phase and done < total and now - self.last < 0.25:
            return
        self.last, self.phase = now, phase
        Maintenance.objects.using(SIDE).filter(pk=1).update(phase=phase, done=done, total=total, updated_at=timezone.now())
