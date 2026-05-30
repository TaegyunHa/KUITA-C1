from typing import TypedDict


class RawArticle(TypedDict):
    """Normalised article shape every source returns before DB insert."""

    source: str          # e.g. "bbc", "guardian", "govuk"
    source_id: str       # stable dedup key (feed guid / url)
    title: str
    url: str
    summary: str
    published_at: str | None  # ISO 8601, or None if the source omits it
