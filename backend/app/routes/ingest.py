from fastapi import APIRouter

from .. import repository
from ..config import settings
from ..sources import govuk, rss

router = APIRouter()


@router.post("/ingest")
def ingest():
    """Pull from enabled sources and store new articles (dedup by source_id)."""
    raw: list[dict] = []
    if settings.enable_rss:
        raw.extend(rss.fetch())
    if settings.enable_govuk:
        raw.extend(govuk.fetch())
    inserted = repository.insert_articles(raw)
    return {"fetched": len(raw), "inserted": inserted}
