from app import repository


def raw(source_id, title="Title", source="bbc", url="https://example.com",
        summary="", published_at=None):
    return {
        "source": source,
        "source_id": source_id,
        "title": title,
        "url": url,
        "summary": summary,
        "published_at": published_at,
    }


# --- profile ---------------------------------------------------------------

def test_get_profile_creates_default(tmp_db):
    profile = repository.get_profile()
    assert profile["age_band"] == repository.DEFAULT_PROFILE["age_band"]
    assert profile["occupation"] == repository.DEFAULT_PROFILE["occupation"]
    assert profile["updated_at"]


def test_upsert_profile_updates_single_row(tmp_db):
    repository.upsert_profile(
        {"postcode_area": "SW1", "age_band": "25–34", "occupation": "Student",
         "interests": "visa"}
    )
    updated = repository.upsert_profile(
        {"postcode_area": "E1", "age_band": "35–44", "occupation": "Researcher",
         "interests": "tube"}
    )
    assert updated["postcode_area"] == "E1"
    assert updated["occupation"] == "Researcher"
    assert updated["updated_at"]

    with tmp_db.connection() as conn:
        count = conn.execute("SELECT COUNT(*) FROM profile").fetchone()[0]
    assert count == 1


# --- articles --------------------------------------------------------------

def test_insert_articles_dedups_by_source_id(tmp_db):
    assert repository.insert_articles([raw("a"), raw("b")]) == 2
    # re-inserting the same source_ids yields zero new rows
    assert repository.insert_articles([raw("a"), raw("b")]) == 0
    assert repository.insert_articles([raw("c")]) == 1


def test_list_articles_filter_and_ordering(tmp_db):
    repository.insert_articles([
        raw("old", title="Older", published_at="2020-01-01T00:00:00+00:00"),
        raw("new", title="Newer", published_at="2024-01-01T00:00:00+00:00"),
    ])
    ids = {a["source_id"]: a["id"] for a in repository.list_articles()}
    repository.update_categories([
        {"id": ids["old"], "category": "Health", "tags": "[]", "affects_whom": ""},
    ])

    # newest-first ordering by published_at
    titles = [a["title"] for a in repository.list_articles()]
    assert titles == ["Newer", "Older"]

    # category filter
    health = repository.list_articles(category="Health")
    assert [a["source_id"] for a in health] == ["old"]


def test_categorisation_roundtrip(tmp_db):
    repository.insert_articles([raw("x"), raw("y"), raw("z")])
    pending = repository.get_uncategorised_articles(limit=2)
    assert len(pending) == 2

    repository.update_categories([
        {"id": pending[0]["id"], "category": "Transport",
         "tags": '["tube"]', "affects_whom": "Commuters"},
    ])
    categorised = repository.get_categorised_articles()
    assert len(categorised) == 1
    row = categorised[0]
    assert row["category"] == "Transport"
    assert row["tags"] == '["tube"]'
    assert row["affects_whom"] == "Commuters"
    assert row["categorised_at"]
