from pytrends.request import TrendReq
from .config import settings
from .logging_conf import logger

def get_trending_topics(locale: str = "US", kw_niche: str | None = None, limit: int = 10):
    """Return a list of trending queries for a locale using Google Trends (unofficial)."""
    geo = locale or settings.default_locale
    niche = kw_niche or settings.channel_niche
    niche_terms = [t.strip() for t in niche.split(",") if t.strip()]

    pytrend = TrendReq(hl="en-US", tz=360)
    terms = []
    try:
        for term in niche_terms:
            pytrend.build_payload([term], timeframe="now 7-d", geo=geo)
            related = pytrend.related_queries().get(term, {})
            rising = related.get("rising")
            if rising is not None:
                terms += [row["query"] for row in rising.head(limit).to_dict("records")]
    except Exception as ex:
        logger.warning(f"Trends error: {ex}")

    seen, out = set(), []
    for t in terms:
        k = t.lower()
        if k not in seen:
            seen.add(k); out.append(t)
        if len(out) >= limit:
            break
    return out or ["productivity hacks", "study tips", "ai tools"]
