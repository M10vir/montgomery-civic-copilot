from typing import Dict

def build_answer(question: str, record: Dict) -> str:
    # deterministic, demo-safe answer layer (Gemini comes later)
    intent = record.get("intent", "")

    if intent == "sanitation":
        return (
            "It sounds like a sanitation issue (trash/recycling pickup). "
            "Start by checking the sanitation schedule guidance for your area. "
            "If this looks like a missed pickup, submit a 311 service request for follow-up."
        )

    if intent == "service_request_311":
        return (
            "This seems like a general city service problem. "
            "Your best next step is to file a 311 service request with clear details "
            "(location, issue type, and any helpful notes)."
        )

    if intent == "code_violation":
        return (
            "This looks like a property or neighborhood code concern. "
            "Document the location and issue clearly, then use the code violation reporting path "
            "or 311 if that is the recommended escalation channel."
        )

    if intent == "district_lookup":
        return (
            "To find your council district and representation context, use the address lookup tool. "
            "Enter your address and confirm the returned district."
        )

    if intent == "parking":
        return (
            "For downtown parking, review available parking options first. "
            "If you want alternatives, check nearby transit options as well."
        )

    if intent == "transit":
        return (
            "For public transit, review available theM transit services and routes for your area, "
            "then confirm schedule/stop availability."
        )

    if intent == "traffic":
        return (
            "For traffic concerns (signals, road issues, intersections), describe the location and issue clearly. "
            "Use the traffic engineering guidance or submit a 311 request if escalation is needed."
        )

    return f"This request matches {record.get('title', 'a city service')}. Follow the recommended steps."
