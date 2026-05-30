from fastapi import APIRouter

from .. import repository
from ..config import settings
from ..llm import categorise
from ..sources import govuk, rss

router = APIRouter()


@router.post("/ingest")
def ingest():
    """Pull from enabled sources, store new articles (dedup), then categorise."""
    raw: list[dict] = []
    if settings.enable_rss:
        raw.extend(rss.fetch())
    if settings.enable_govuk:
        raw.extend(govuk.fetch())
    inserted = repository.insert_articles(raw)
    categorised = categorise.run(limit=settings.categorise_limit)
    return {"fetched": len(raw), "inserted": inserted, "categorised": categorised}
