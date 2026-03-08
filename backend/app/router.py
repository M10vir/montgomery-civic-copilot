from typing import Dict, List, Optional
from .intent_map import INTENT_MAP

def find_best_record(intent: str, all_records: List[Dict]) -> Optional[Dict]:
    targets = INTENT_MAP.get(intent, {}).get("targets", [])
    candidates = [r for r in all_records if r["id"] in targets]
    if not candidates:
        return next((r for r in all_records if r["intent"] == intent), None)
    candidates.sort(key=lambda r: r.get("priority", 0), reverse=True)
    return candidates[0]
