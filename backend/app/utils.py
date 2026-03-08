import re

def strip_html(html: str) -> str:
    text = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def truncate(text: str, max_chars: int = 2500) -> str:
    return text[:max_chars] if len(text) > max_chars else text

def looks_incomplete(text: str) -> bool:
    t = (text or "").strip()
    if len(t) < 120:
        return True

    # if ends with an obvious dangling word/phrase
    bad_suffixes = ("based on", "because", "to", "at", "the", "a", "an", "and", "or", "with", "for", "in")
    last = re.sub(r"[^\w]+$", "", t.lower()).split()[-2:]  # last 2 tokens
    tail = " ".join(last).strip()

    if t.lower().endswith(tuple(bad_suffixes)) or tail in bad_suffixes:
        return True

    # if doesn't end with normal punctuation, likely cut
    if not t.endswith((".", "?", "!")):
        return True

    return False
