"""Candidate selection for the feed (plain Python, runs before the LLM call)."""

import json
from datetime import datetime, timezone

# Categories that matter most per occupation.
OCCUPATION_CATEGORIES = {
    "Student": {"Visa/Immigration", "Education", "Transport", "Housing"},
    "Office worker": {"Transport", "Tax/Finance", "Work/Employment", "Housing"},
    "Self-employed": {"Tax/Finance", "Work/Employment", "Health"},
    "Researcher": {"Visa/Immigration", "Education", "Work/Employment"},
    "Homemaker": {"Health", "Housing", "Education", "Safety"},
    "Other": set(),
}

# Affects almost all Korean residents regardless of profile.
BROADLY_RELEVANT = {"Visa/Immigration"}

COMMUTE_HINTS = ("line", "commut", "tube", "train", "zone", "bus", "underground")


def _recency_score(published_at: str | None) -> float:
    if not published_at:
        return 0.0
    try:
        dt = datetime.fromisoformat(published_at)
        age_days = (datetime.now(timezone.utc) - dt).total_seconds() / 86400
    except Exception:
        return 0.0
    return max(0.0, 1.0 - age_days / 7.0)  # decays to 0 over a week


def score_article(article: dict, profile: dict) -> float:
    score = 0.0
    category = article["category"]
    interests = (profile["interests"] or "").lower()
    postcode = (profile["postcode_area"] or "").lower()
    text = (article["title"] + " " + (article["affects_whom"] or "")).lower()

    if category in OCCUPATION_CATEGORIES.get(profile["occupation"], set()):
        score += 2.0
    if category in BROADLY_RELEVANT:
        score += 2.5

    for tag in json.loads(article["tags"] or "[]"):
        if tag and (tag in interests or tag.replace("-", " ") in interests):
            score += 1.5

    for word in {w for w in interests.split() if len(w) > 3}:
        if word in text:
            score += 0.5

    if category == "Transport" and any(h in interests for h in COMMUTE_HINTS):
        score += 1.5
    if postcode and postcode in text:
        score += 1.5

    score += _recency_score(article["published_at"])
    return score


def select_candidates(articles: list[dict], profile: dict, size: int) -> list[dict]:
    ranked = sorted(articles, key=lambda a: score_article(a, profile), reverse=True)
    return ranked[:size]
