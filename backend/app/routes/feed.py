from fastapi import APIRouter

from .. import repository
from ..config import settings
from ..llm import personalise
from ..models import FeedCard
from ..selection import select_candidates
from ..taxonomy import CATEGORY_KO

# Fixed English brand label shown above the Korean impact line (never translated).
LABEL = "What now?"

router = APIRouter()


@router.get("/feed", response_model=list[FeedCard])
def feed():
    profile = repository.get_profile()
    candidates = select_candidates(
        repository.get_categorised_articles(), profile, settings.feed_size
    )
    lines = personalise.personalise(profile, candidates)

    cards: list[FeedCard] = []
    for a in candidates:
        line = lines.get(a["id"])
        if not line:
            continue
        cards.append(
            FeedCard(
                id=a["id"],
                title=a["title"],
                category=a["category"],
                category_ko=CATEGORY_KO.get(a["category"], a["category"]),
                label=LABEL,
                impact_line=line,
                summary=a["summary"],
                url=a["url"],
                published_at=a.get("published_at"),
            )
        )
    return cards
