"""Notes when each signed-in browser was last used (Signed-in devices in the account menu)."""
from django.core.cache import cache
from django.utils import timezone

SEEN_EVERY = 300  # seconds: at most one write per session every five minutes


class SessionSeen:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            user, key = getattr(request, "user", None), request.session.session_key
            if user is not None and user.is_authenticated and key and cache.add(f"seen:{key}", 1, SEEN_EVERY):
                from .models import UserSession
                if not UserSession.objects.filter(session_key=key).update(last_seen=timezone.now()):
                    # signed in before sessions were recorded (or the record was lost): note it now, so every
                    # browser that is signed in shows up, not only those that signed in again since
                    from .api import record_session
                    record_session(request, user)
        except Exception:  # never let this get in the way of the answer
            pass
        return response
