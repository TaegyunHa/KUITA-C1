"""Curated, pre-categorised demo articles for the pitch.

Gated behind SEED_ON_STARTUP (loaded at app startup), or run on demand:
    uv run python -m app.seed

Articles are pre-categorised so the demo feed works without spending
categorisation calls; /feed still personalises them live. URLs point at
real, topical landing pages so the card "source" link goes somewhere sensible.
"""

import json
from datetime import datetime, timedelta, timezone

from . import repository


def _iso(days_ago: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat()


SEED_ARTICLES = [
    {
        "source": "seed",
        "source_id": "seed:central-line-weekend",
        "title": "Central line to close for weekend engineering works",
        "url": "https://tfl.gov.uk/tube-dlr-overground/status/",
        "summary": (
            "Transport for London says the Central line will be suspended between "
            "Liverpool Street and Ealing Broadway this weekend for signalling upgrades. "
            "TfL advises using the Elizabeth, Piccadilly and Victoria lines instead."
        ),
        "published_at": _iso(0),
        "category": "Transport",
        "tags": ["central-line", "weekend-works", "tfl"],
        "affects_whom": "Central line commuters across central and east London this weekend.",
    },
    {
        "source": "seed",
        "source_id": "seed:sw1-council-tax",
        "title": "Westminster confirms council tax band revaluation for SW1 addresses",
        "url": "https://www.gov.uk/council-tax-bands",
        "summary": (
            "Westminster City Council has confirmed a revaluation affecting several SW1 "
            "postcodes, with some flats moving up a council tax band from April. Residents "
            "can check their band and challenge it online if they think it is wrong."
        ),
        "published_at": _iso(1),
        "category": "Tax/Finance",
        "tags": ["council-tax", "sw1", "westminster"],
        "affects_whom": "Renters and owners in SW1 postcodes whose band may rise.",
    },
    {
        "source": "seed",
        "source_id": "seed:student-visa-salary",
        "title": "Salary threshold for post-study Skilled Worker visa raised",
        "url": "https://www.gov.uk/student-visa",
        "summary": (
            "The Home Office has raised the minimum salary required to switch from a "
            "Student visa to the Skilled Worker route. Graduates applying after the change "
            "will need a higher qualifying salary or an eligible shortage-occupation role."
        ),
        "published_at": _iso(1),
        "category": "Visa/Immigration",
        "tags": ["student-visa", "skilled-worker", "salary-threshold"],
        "affects_whom": "International students planning to work in the UK after graduating.",
    },
    {
        "source": "seed",
        "source_id": "seed:ihs-increase",
        "title": "Immigration Health Surcharge to rise for visa applicants",
        "url": "https://www.gov.uk/healthcare-immigration-application",
        "summary": (
            "The annual Immigration Health Surcharge (IHS) paid by most visa applicants for "
            "NHS access is going up. Students pay a discounted rate; the new amount applies "
            "to applications submitted after the change date."
        ),
        "published_at": _iso(2),
        "category": "Health",
        "tags": ["nhs", "ihs", "visa-holders"],
        "affects_whom": "Visa holders and applicants who must pay the NHS surcharge.",
    },
    {
        "source": "seed",
        "source_id": "seed:zone2-renting",
        "title": "Renters' Rights changes and easing Zone 2 rents this quarter",
        "url": "https://www.gov.uk/private-renting",
        "summary": (
            "Average asking rents in several Zone 2 areas dipped slightly this quarter as "
            "supply improved, while new renters' rights rules give tenants more notice and "
            "protection. Tenants are advised to get any agreement in writing."
        ),
        "published_at": _iso(2),
        "category": "Housing",
        "tags": ["renting", "zone-2", "renters-rights"],
        "affects_whom": "People renting or flat-hunting in London Zone 2.",
    },
    {
        "source": "seed",
        "source_id": "seed:graduate-visa-confirmed",
        "title": "Graduate visa route confirmed, allowing post-study work",
        "url": "https://www.gov.uk/graduate-visa",
        "summary": (
            "The government has confirmed the Graduate visa will continue, letting eligible "
            "students stay to work or look for work after completing a UK degree. Most get "
            "two years; PhD graduates get three."
        ),
        "published_at": _iso(3),
        "category": "Work/Employment",
        "tags": ["graduate-visa", "post-study-work"],
        "affects_whom": "Recent and soon-to-be graduates wanting to work in the UK.",
    },
]


def seed() -> int:
    """Insert the curated demo articles (idempotent via dedup). Returns inserted count."""
    rows = [{**a, "tags": json.dumps(a["tags"], ensure_ascii=False)} for a in SEED_ARTICLES]
    return repository.insert_seed_articles(rows)


if __name__ == "__main__":
    from .db import init_db

    init_db()
    print(f"seeded {seed()} demo article(s)")
