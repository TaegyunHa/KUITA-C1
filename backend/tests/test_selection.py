import json
from datetime import datetime, timedelta, timezone

from app.selection import _recency_score, score_article, select_candidates


def make_article(id=1, category="Health", title="Generic headline",
                 affects_whom="", tags=None, published_at=None):
    return {
        "id": id,
        "category": category,
        "title": title,
        "affects_whom": affects_whom,
        "tags": json.dumps(tags or []),
        "published_at": published_at,
    }


def make_profile(occupation="Other", interests="", postcode_area=""):
    return {"occupation": occupation, "interests": interests, "postcode_area": postcode_area}


# --- _recency_score --------------------------------------------------------

def test_recency_none_is_zero():
    assert _recency_score(None) == 0.0


def test_recency_unparseable_is_zero():
    assert _recency_score("not a date") == 0.0


def test_recency_old_decays_to_zero():
    old = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
    assert _recency_score(old) == 0.0


def test_recency_now_is_near_one():
    now = datetime.now(timezone.utc).isoformat()
    assert _recency_score(now) > 0.9


# --- score_article (published_at=None isolates each contribution) ----------

def test_occupation_category_match_adds_2():
    article = make_article(category="Education")
    assert score_article(article, make_profile(occupation="Student")) == 2.0


def test_broadly_relevant_adds_2_5():
    article = make_article(category="Visa/Immigration")
    assert score_article(article, make_profile(occupation="Other")) == 2.5


def test_tag_in_interests_adds_1_5():
    article = make_article(category="Health", tags=["student-visa"])
    profile = make_profile(occupation="Other", interests="student-visa things")
    assert score_article(article, profile) == 1.5


def test_postcode_in_text_adds_1_5():
    article = make_article(category="Health", title="News about SW1 area")
    profile = make_profile(occupation="Other", postcode_area="SW1")
    assert score_article(article, profile) == 1.5


def test_transport_with_commute_hint_adds_1_5():
    article = make_article(category="Transport", title="Rail news")
    profile = make_profile(occupation="Other", interests="i commute by tube")
    assert score_article(article, profile) == 1.5


# --- select_candidates -----------------------------------------------------

def test_select_candidates_orders_by_score_and_respects_size():
    profile = make_profile(occupation="Student")
    high = make_article(id=1, category="Visa/Immigration")  # student set + broadly = 4.5
    mid = make_article(id=2, category="Education")           # student set = 2.0
    low = make_article(id=3, category="Health")              # 0.0
    selected = select_candidates([low, high, mid], profile, size=2)
    assert [a["id"] for a in selected] == [1, 2]
