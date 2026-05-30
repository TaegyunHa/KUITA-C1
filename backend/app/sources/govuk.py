import httpx

from .base import RawArticle

SEARCH_URL = "https://www.gov.uk/api/search.json"
GOVUK_BASE = "https://www.gov.uk"

# Topical queries aligned with the category taxonomy most relevant to the user.
QUERIES = ["visa immigration", "council tax", "renting housing", "rail strike"]


def fetch(per_query: int = 8) -> list[RawArticle]:
    """Pull recent gov.uk announcements per topical query. No API key needed."""
    articles: list[RawArticle] = []
    with httpx.Client(timeout=10.0) as client:
        for q in QUERIES:
            params = {
                "q": q,
                "count": per_query,
                "order": "-public_timestamp",
                "fields": "title,link,description,public_timestamp",
            }
            try:
                resp = client.get(SEARCH_URL, params=params)
                resp.raise_for_status()
                results = resp.json().get("results", [])
            except Exception:
                continue
            for r in results:
                link = r.get("link", "")
                title = (r.get("title") or "").strip()
                if not link or not title:
                    continue
                url = link if link.startswith("http") else GOVUK_BASE + link
                articles.append(
                    RawArticle(
                        source="govuk",
                        source_id=url,
                        title=title,
                        url=url,
                        summary=(r.get("description") or "").strip(),
                        published_at=r.get("public_timestamp"),
                    )
                )
    return articles
