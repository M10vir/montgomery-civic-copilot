import uuid
INSTANCE_ID = str(uuid.uuid4())[:8]

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import AskLiveRequest, AskLiveResponse
from .utils import strip_html, truncate

from .config import APP_NAME, APP_VERSION, FRONTEND_ORIGIN, GEMINI_API_KEY
from .models import (
    AskRequest, AskResponse,
    AddressLookupRequest, AddressLookupResponse,
    HealthResponse
)
from .models import EnrichRequest, EnrichResponse
from .brightdata import serp_search
from .loaders import load_all_records, load_demo_addresses
from .classifier import detect_intent
from .router import find_best_record
from .response_builder import build_answer
from .address_lookup import lookup_address

app = FastAPI(title=APP_NAME, version=APP_VERSION)

ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://gen-lang-client-0570326286.web.app",
    "https://gen-lang-client-0570326286.firebaseapp.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALL_RECORDS = load_all_records()
DEMO_ADDRESSES = load_demo_addresses()

from datetime import datetime
import uuid

import time

SERP_CACHE = {}   # key: search_q, value: (timestamp, html)
CACHE_TTL = 60

INSTANCE_ID = str(uuid.uuid4())[:8]
STARTED_AT = datetime.utcnow().isoformat() + "Z"

@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="ok",
        app=APP_NAME,
        version=APP_VERSION,
    )

@app.get("/instance")
def instance():
    return {"instance_id": INSTANCE_ID, "started_at": STARTED_AT}

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    q = req.question.strip()
    if not q:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    intent, conf = detect_intent(q)
    record = find_best_record(intent, ALL_RECORDS)
    if not record:
        raise HTTPException(status_code=404, detail="No matching service found.")

    fallback = build_answer(q, record)

    # Gemini polish layer (safe fallback)
    answer = fallback
    try:
        from .gemini_client import GeminiClient
        from .prompt_templates import polish_answer_prompt

        gc = GeminiClient()
        prompt = polish_answer_prompt(
            question=q,
            matched_service_title=record["title"],
            source_label=record["source_label"],
            source_url=record["source_url"],
            fallback_answer=fallback,
            next_steps=record["next_steps"],
        )
        polished = gc.generate(prompt)
        if polished:
            answer = polished
    except Exception:
        # If Gemini fails for any reason, we keep the deterministic fallback
        pass
    
    return AskResponse(
        intent=intent,
        matched_record_id=record["id"],
        matched_title=record["title"],
        answer=answer,
        recommended_service=record["title"],
        next_steps=record["next_steps"],
        source_label=record["source_label"],
        source_url=record["source_url"],
        confidence=conf,
    )

import re

@app.post("/ask-live", response_model=AskLiveResponse)
async def ask_live(req: AskLiveRequest):
    q = req.question.strip()
    if not q:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    intent, conf = detect_intent(q)
    record = find_best_record(intent, ALL_RECORDS)
    if not record:
        raise HTTPException(status_code=404, detail="No matching service found.")

    trusted_answer = build_answer(q, record)

    live_insights: list[str] = []
    final_answer = trusted_answer
    live_mode = "fallback"
    live_debug = "init"

    def _clean_bullets(lines: list[str]) -> list[str]:
        cleaned: list[str] = []
        bad_endings = (
            " at the.", " to the.", " of the.", " in the.", " for the.", " on the.",
            " at a.", " to a.", " of a."
        )
        stopwords = {"the", "a", "an", "to", "at", "of", "in", "for", "on", "with", "and", "or"}

        for b in lines:
            b = b.strip().lstrip("-• ").strip()
            if not b:
                continue

            # remove phone-number-like patterns
            b = re.sub(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b", "", b).strip()

            if len(b) < 18:
                continue

            if not b.endswith("."):
                b += "."

            low = b.lower().strip()
            if low.endswith(("according.", "according to.", "according to the.", "according to a.")):
                continue

            last_word = low.rstrip(".!?").split()[-1]
            if last_word in {"according", "to", "the", "a", "an"}:
                continue

            last = re.sub(r"[^\w]+$", "", low).split()[-1] if low else ""
            if last in stopwords:
                continue

            cleaned.append(b)

        return cleaned[:6]

    def _looks_incomplete(t: str) -> bool:
        t = (t or "").strip()
        if len(t) < 120:
            return True
        if not t.endswith((".", "?", "!")):
            return True
        bad_tail = ("based on", "because", "to", "at", "the", "a", "an", "and", "or", "with", "for", "in")
        tail = t.lower().rstrip()
        if any(tail.endswith(bt) for bt in bad_tail):
            return True
        return False

    try:
        # 1) Bright Data SERP
        live_debug = "serp_start"
        search_q = f"City of Montgomery {record['title']} {q}"
        now = time.time()
        cached = SERP_CACHE.get(search_q)

        if cached and (now - cached[0]) < CACHE_TTL:
            html = cached[1]
            live_debug = f"{live_debug}|serp_cache_hit=1|serp_ok_len={len(html)}"
        else:
            try:
                html = await serp_search(search_q)
                SERP_CACHE[search_q] = (now, html)
                live_debug = f"{live_debug}|serp_cache_hit=0|serp_ok_len={len(html)}"
            except Exception as bd_e:
                html = ""
                live_debug = f"{live_debug}|serp_cache_hit=0|bd_error:{type(bd_e).__name__}:{str(bd_e)[:120]}"

        # If Bright Data failed, skip live web processing (fallback mode)
        if not html:
            live_insights = []
            live_mode = "fallback"
            live_debug = f"{live_debug}|skip_live=1"
        else: 
            serp_text = truncate(strip_html(html), 5000)
            live_debug = f"{live_debug}|strip_ok_len={len(serp_text)}"
        
            # 2) Gemini
            from .gemini_client import GeminiClient
            from .prompt_templates import live_insights_prompt, polish_answer_prompt

            gc = GeminiClient()

            # Live insights bullets
            bullets = gc.generate(live_insights_prompt(q, serp_text)) or ""
            live_debug = f"{live_debug}|bullets_raw_len={len(bullets)}"

            raw_lines = [ln.strip() for ln in bullets.splitlines() if ln.strip()]
            if raw_lines and not any(ln.startswith(("-", "•")) for ln in raw_lines):
                raw_lines = [f"- {ln}" for ln in raw_lines]
   
            live_insights = _clean_bullets(raw_lines)
            live_debug = f"{live_debug}|bullets_clean_count={len(live_insights)}"

            # Prefer real live insights only if we have at least 2 clean bullets
            if len(live_insights) >= 2:
                live_mode = "brightdata+gemini"
            else:
                live_insights = []
                live_mode = "fallback"

            live_debug = f"{live_debug}|mode={live_mode}"

            # Draft for polish (trusted + live + steps)
            live_block = "\n".join([f"- {x}" for x in live_insights]) if live_insights else "- (No confirmed live insights)"
            steps_block = "\n".join([f"- {s}" for s in record["next_steps"]]) if record["next_steps"] else "- (none)"

            draft = (
                f"{trusted_answer}\n\n"
                f"Live Insights (Bright Data SERP):\n{live_block}\n\n"
                f"Next steps (trusted):\n{steps_block}\n"
            )

            final_prompt = polish_answer_prompt(
                question=q,
                matched_service_title=record["title"],
                source_label=record["source_label"],
                source_url=record["source_url"],
                fallback_answer=draft,
                next_steps=record["next_steps"],
            )

            candidate = (gc.generate(final_prompt) or "").strip()

            # Retry once if incomplete
            if _looks_incomplete(candidate):
                fallback_draft = (
                    f"{trusted_answer}\n\nNext steps:\n" +
                    "\n".join([f"- {s}" for s in record["next_steps"]])
                )
                retry_prompt = polish_answer_prompt(
                    question=q,
                    matched_service_title=record["title"],
                    source_label=record["source_label"],
                    source_url=record["source_url"],
                    fallback_answer=fallback_draft,
                    next_steps=record["next_steps"],
                )
                candidate2 = (gc.generate(retry_prompt) or "").strip()
                final_answer = candidate2 if not _looks_incomplete(candidate2) else trusted_answer
            else:
                final_answer = candidate
        
    except Exception as e:
        live_debug = f"error:{type(e).__name__}:{str(e)[:180]}"
        live_mode = "fallback"
        final_answer = trusted_answer
        live_insights = []

    # ✅ Always show something in Live Insights (demo stability)
    if not live_insights:
        live_insights = [
            "Service details may vary by neighborhood and holiday schedules.",
            "If pickup was missed after the scheduled window, file a service request for follow-up."
        ]

    # ✅ Never allow incomplete final answers
    if _looks_incomplete(final_answer):
        final_answer = trusted_answer

    live_debug = f"{live_debug}|final_len={len(final_answer)}"

    return AskLiveResponse(
        intent=intent,
        matched_record_id=record["id"],
        matched_title=record["title"],
        trusted_answer=trusted_answer,
        live_insights=live_insights,
        final_answer=final_answer,
        recommended_service=record["title"],
        next_steps=record["next_steps"],
        sources=["Montgomery Open Data Portal", "Bright Data SERP"],
        confidence=conf,
        live_mode=live_mode,
        live_debug=live_debug,
    )

@app.post("/lookup-address", response_model=AddressLookupResponse)
def lookup(req: AddressLookupRequest):
    address = req.address.strip()
    if not address:
        raise HTTPException(status_code=400, detail="Address cannot be empty.")

    result = lookup_address(address, DEMO_ADDRESSES)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Address not found in demo lookup. Try '123 Main St' or '456 Elm St'."
        )

    return AddressLookupResponse(
        address=address,
        district=result["district"],
        representative=result["representative"],
        source_label="Address Lookup & Council District Finder",
        source_url="https://opendata.montgomeryal.gov/pages/data",
        confidence=0.90,
    )

@app.post("/enrich", response_model=EnrichResponse)
async def enrich(req: EnrichRequest):
    q = req.query.strip()
    if not q:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        html = await serp_search(q)
        return EnrichResponse(
            url=f"google: {q}",
            status="ok",
            content=html[:1500],
            source_label="Bright Data SERP Enrichment",
        )
    except Exception as e:
        return EnrichResponse(
            url=f"google: {q}",
            status=f"fallback: {str(e)}",
            content="Bright Data SERP is not configured yet or the request failed.",
            source_label="Bright Data SERP Enrichment",
        )

@app.get("/ai-health")
def ai_health():
    key_ok = bool(GEMINI_API_KEY)
    details = None

    try:
        from .gemini_client import GeminiClient
        gc = GeminiClient()
        text = gc.generate("Reply with exactly: OK")
        gemini_ok = ("OK" in (text or ""))
        sample = (text or "")[:80]
    except Exception as e:
        gemini_ok = False
        sample = f"error: {type(e).__name__}"
        details = str(e)

    return {
        "gemini_key_loaded": key_ok,
        "gemini_call_ok": gemini_ok,
        "sample": sample,
        "details": details
    }
