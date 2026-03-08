import json
from typing import Any, Dict, List
from .config import (
    SERVICES_FILE,
    DISTRICTS_FILE,
    TRANSPORT_FILE,
    DEMO_ADDRESSES_FILE,
)

def _load(path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_all_records() -> List[Dict]:
    records: List[Dict] = []
    records.extend(_load(SERVICES_FILE))
    records.extend(_load(DISTRICTS_FILE))
    records.extend(_load(TRANSPORT_FILE))
    return [r for r in records if r.get("active", True)]

def load_demo_addresses() -> Dict[str, Dict]:
    raw = _load(DEMO_ADDRESSES_FILE)
    return {k.lower().strip(): v for k, v in raw.items()}
