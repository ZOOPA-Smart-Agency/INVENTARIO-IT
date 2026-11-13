"""The app's version. Raise VERSION for every release and tag it on GitHub as v<VERSION> (for example v1.1.0)."""
import os
from pathlib import Path

VERSION = "1.6.0"
ROOT = Path(__file__).resolve().parent.parent


def commit():
    """The exact build: APP_COMMIT when deployed (set at build time), else read from the local git checkout."""
    value = os.environ.get("APP_COMMIT", "").strip()
    if value:
        return value
    try:
        head = (ROOT / ".git" / "HEAD").read_text().strip()
        if not head.startswith("ref: "):
            return head
        ref = head[5:]
        loose = ROOT / ".git" / ref
        if loose.exists():
            return loose.read_text().strip()
        for line in (ROOT / ".git" / "packed-refs").read_text().splitlines():
            if line.endswith(" " + ref):
                return line.split()[0]
    except OSError:
        pass
    return ""
