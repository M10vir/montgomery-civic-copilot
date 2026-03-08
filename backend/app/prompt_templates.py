# backend/app/prompt_templates.py

from typing import List


def polish_answer_prompt(
    question: str,
    matched_service_title: str,
    source_label: str,
    source_url: str,
    fallback_answer: str,
    next_steps: List[str],
) -> str:
    """
    Takes a deterministic (fallback) answer and returns a prompt that asks Gemini to rewrite it
    into a clearer, civic-friendly final response while staying grounded.
    """
    steps = "\n".join([f"- {s}" for s in next_steps]) if next_steps else "- (none)"

    return f"""
You are a civic assistant for the City of Montgomery. Your goal is public-good clarity.

USER QUESTION:
{question}

MATCHED CITY SERVICE:
{matched_service_title}

TRUSTED SOURCE:
{source_label} ({source_url})

DRAFT ANSWER (trusted but may be rough):
{fallback_answer}

NEXT STEPS (trusted):
{steps}

TASK:
Rewrite the answer to be:
- concise (3–6 sentences)
- action-first (what the resident should do next)
- friendly, simple English (no jargon)
- grounded: do NOT invent contacts, phone numbers, addresses, or policies
- if information is uncertain, say you are not sure and recommend checking the source
- mention the source label exactly once (e.g., "Based on {source_label}...")
- end with ONE short follow-up question that helps clarify the resident’s situation
- if referencing 311, say "city service request / reporting portal" (no phone numbers)

OUTPUT FORMAT:
Return only the rewritten answer text. No headings. No bullet lists.
""".strip()


def live_insights_prompt(question: str, serp_text: str) -> str:
    return f"""
You are assisting an AI civic helper for the City of Montgomery.

USER QUESTION:
{question}

LIVE WEB CONTEXT (text extracted from Google results; may contain noise):
{serp_text}

TASK:
Return 3 to 6 "Live Insights" bullets.

STRICT RULES:
- Each bullet must be a COMPLETE sentence (ends with a period).
- DO NOT include phone numbers, email addresses, or exact contact instructions.
- DO NOT include URLs.
- Prefer official city/government sources when possible.
- If uncertain, write "Not confirmed." as the whole bullet.
- Max 18 words per bullet.

OUTPUT FORMAT:
Return ONLY lines starting with "- " (dash+space). No other text.
""".strip()

def combine_trusted_and_live_prompt(
    question: str,
    trusted_answer: str,
    live_insights: List[str],
    matched_service_title: str,
    source_label: str,
    source_url: str,
    next_steps: List[str],
) -> str:
    """
    Optional: if you want an even cleaner final answer that explicitly blends
    the trusted city guidance + live insights in a safe way.
    """
    steps = "\n".join([f"- {s}" for s in next_steps]) if next_steps else "- (none)"
    insights = "\n".join([f"- {x}" for x in live_insights]) if live_insights else "- (No confirmed live insights)"

    return f"""
You are a civic assistant for the City of Montgomery. Your goal is public-good clarity.

USER QUESTION:
{question}

TRUSTED CITY GUIDANCE (from Montgomery data):
{trusted_answer}

LIVE INSIGHTS (from web context; may be incomplete):
{insights}

MATCHED CITY SERVICE:
{matched_service_title}

TRUSTED SOURCE:
{source_label} ({source_url})

NEXT STEPS (trusted):
{steps}

TASK:
Write a final answer that:
- starts with the trusted city guidance
- optionally adds 1–2 short sentences using the live insights (only if relevant)
- never contradicts the trusted source
- never invents contacts/phone numbers/URLs
- ends with ONE short follow-up question

OUTPUT FORMAT:
Return only the final answer text. No headings.
""".strip() 
