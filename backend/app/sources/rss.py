import re
from datetime import datetime, timezone

import feedparser

from .base import RawArticle

FEEDS = {
    "bbc": "https://feeds.bbci.co.uk/news/uk/rss.xml",
    "guardian": "https://www.theguardian.com/uk/rss",
    "sky": "https://feeds.skynews.com/feeds/rss/uk.xml",
    "reuters": "https://www.reutersagency.com/feed/?taxonomy=best-regions&post_type=best",
}

_TAG_RE = re.compile(r"<[^>]+>")


def _clean(text: str) -> str:
    return _TAG_RE.sub("", text or "").strip()


def _published_iso(entry) -> str | None:
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if parsed:
        return datetime(*parsed[:6], tzinfo=timezone.utc).isoformat()
    return None


def fetch() -> list[RawArticle]:
    """Pull entries from all configured RSS feeds. Dead/erroring feeds are skipped."""
    articles: list[RawArticle] = []
    for source, url in FEEDS.items():
        try:
            feed = feedparser.parse(url)
        except Exception:
            continue
        for entry in feed.entries:
            link = entry.get("link", "")
            title = _clean(entry.get("title", ""))
            if not link or not title:
                continue
            articles.append(
                RawArticle(
                    source=source,
                    source_id=entry.get("id") or link,
                    title=title,
                    url=link,
                    summary=_clean(entry.get("summary", "")),
                    published_at=_published_iso(entry),
                )
            )
    return articles
