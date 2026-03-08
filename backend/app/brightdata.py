import urllib.parse
import httpx
from .config import BRIGHTDATA_API_KEY, BRIGHTDATA_ZONE_SERP

BRIGHTDATA_REQUEST_ENDPOINT = "https://api.brightdata.com/request"

async def serp_search(query: str, country: str = "us") -> str:
    if not BRIGHTDATA_API_KEY:
        raise ValueError("BRIGHTDATA_API_KEY is missing.")
    zone = (BRIGHTDATA_ZONE_SERP or "").strip()
    if not zone:
        raise ValueError("BRIGHTDATA_ZONE_SERP is missing. Set it in .env (e.g., serp_api1).")

    headers = {
        "Authorization": f"Bearer {BRIGHTDATA_API_KEY}",
        "Content-Type": "application/json",
    }

    encoded_q = urllib.parse.quote_plus(query.strip())
    url = f"https://www.google.com/search?q={encoded_q}"
    
    payload = {
        "zone": zone,
        "url": url,
        "format": "raw"
    }

    async with httpx.AsyncClient(timeout=45.0) as client:
        resp = await client.post(BRIGHTDATA_REQUEST_ENDPOINT, headers=headers, json=payload)
        if resp.status_code >= 400:
            raise RuntimeError(f"Bright Data error {resp.status_code}: {resp.text[:800]}")
        return resp.text
