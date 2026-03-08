from .intent_map import INTENT_MAP

def detect_intent(question: str) -> tuple[str, float]:
    q = question.lower().strip()

    if "missed pickup" in q:
        return "sanitation", 0.95
    if "council district" in q or "who represents me" in q:
        return "district_lookup", 0.95
    if "code violation" in q:
        return "code_violation", 0.95

    scores = {}
    for intent, cfg in INTENT_MAP.items():
        scores[intent] = sum(1 for kw in cfg["keywords"] if kw in q)

    best_intent = max(scores, key=scores.get)
    best_score = scores[best_intent]
    if best_score == 0:
        return "service_request_311", 0.55

    confidence = min(0.6 + (best_score * 0.1), 0.95)
    return best_intent, confidence
