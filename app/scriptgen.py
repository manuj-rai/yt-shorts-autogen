import httpx
from .config import settings
from .logging_conf import logger

SYS_PROMPT = (
    "You write 30–60 second YouTube Shorts scripts. "
    "Return plain text with short punchy lines (max 12 words per line)."
)

def generate_script(topic: str, niche: str) -> str:
    """Generate a concise script. Uses OpenAI if configured, else rules."""
    if settings.openai_api_key:
        try:
            headers = {"Authorization": f"Bearer {settings.openai_api_key}"}
            prompt = (
                f"Topic: {topic}\n"
                f"Niche: {niche}\n"
                "Write a ~110-word script with: "
                "1) hook, 2) 3–5 actionable points, 3) short CTA."
            )
            data = {
                "model": "gpt-4o-mini",
                "messages": [{"role":"system","content":SYS_PROMPT},
                             {"role":"user","content":prompt}],
                "temperature": 0.7,
                "max_tokens": 220
            }
            resp = httpx.post("https://api.openai.com/v1/chat/completions",
                              json=data, headers=headers, timeout=30)
            resp.raise_for_status()
            txt = resp.json()["choices"][0]["message"]["content"].strip()
            return safety_filter(txt)
        except Exception as ex:
            logger.warning(f"OpenAI fallback: {ex}")

    # Fallback deterministic script
    lines = [
        f"Stop scrolling! {topic} in 30 seconds — let’s go!",
        "Tip 1: Apply the 80/20 rule.",
        "Tip 2: Batch similar tasks to avoid context switching.",
        "Tip 3: Use 25-minute focus blocks + 5-minute breaks.",
        "Follow for more quick tips. #shorts",
    ]
    return "\n".join(lines)

BLOCKLIST = {"violence", "hate", "explicit"}

def safety_filter(text: str) -> str:
    low = text.lower()
    if any(b in low for b in BLOCKLIST):
        return "Let’s focus on positive, helpful tips you can use today."
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    trimmed = [(ln[:80]) for ln in lines][:18]
    return "\n".join(trimmed)
