"""The standard lists every new installation starts with."""
import json
from pathlib import Path

from .registry import LISTS

SEED = Path(__file__).resolve().parent / "demo" / "seed.json"
COMPANY_SPECIFIC = {"depts", "locations", "models"}


def load_catalog():
    """Fills device types, components and software. Returns False if any already has data."""
    collections = {c: s for c, s in LISTS.items() if c not in COMPANY_SPECIFIC}
    if any(spec.model.objects.exists() for spec in collections.values()):
        return False
    data = json.loads(SEED.read_text(encoding="utf8"))
    ids = {}
    for coll, spec in collections.items():  # LISTS orders parents before children
        ids[coll] = {}
        for row in data[coll]:
            item = spec.model(nombre=row["nombre"])
            for key, attr in spec.fields.items():
                if row.get(key) is not None:
                    setattr(item, attr, row[key])
            for key, (attr, target) in spec.fks.items():
                parent = next(c for c, s in LISTS.items() if s.model is target)
                setattr(item, attr + "_id", ids[parent][row[key]])
            item.save()
            ids[coll][row["id"]] = item.pk
    return True
