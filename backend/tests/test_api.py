from app import repository


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_get_profile_returns_default(client):
    resp = client.get("/profile")
    assert resp.status_code == 200
    body = resp.json()
    assert body["occupation"] == repository.DEFAULT_PROFILE["occupation"]
    assert "updated_at" in body


def test_put_profile_roundtrip(client):
    payload = {"postcode_area": "SW1", "age_band": "25–34",
               "occupation": "Student", "interests": "visa, tube"}
    put = client.put("/profile", json=payload)
    assert put.status_code == 200
    assert put.json()["occupation"] == "Student"

    got = client.get("/profile").json()
    assert got["postcode_area"] == "SW1"
    assert got["interests"] == "visa, tube"


def test_list_articles_with_category_filter(client):
    repository.insert_articles([
        {"source": "bbc", "source_id": "a1", "title": "A", "url": "https://x/1",
         "summary": "", "published_at": None},
        {"source": "bbc", "source_id": "a2", "title": "B", "url": "https://x/2",
         "summary": "", "published_at": None},
    ])
    rows = {a["source_id"]: a["id"] for a in repository.list_articles()}
    repository.update_categories([
        {"id": rows["a1"], "category": "Health", "tags": "[]", "affects_whom": ""},
    ])

    assert len(client.get("/articles").json()) == 2
    health = client.get("/articles", params={"category": "Health"}).json()
    assert [a["source_id"] for a in health] == ["a1"]


def test_feed_builds_cards_and_filters_unlined(client, monkeypatch):
    repository.insert_articles([
        {"source": "bbc", "source_id": "f1", "title": "Tube delays",
         "url": "https://x/1", "summary": "s", "published_at": None},
        {"source": "bbc", "source_id": "f2", "title": "Visa change",
         "url": "https://x/2", "summary": "s", "published_at": None},
    ])
    rows = {a["source_id"]: a["id"] for a in repository.list_articles()}
    repository.update_categories([
        {"id": rows["f1"], "category": "Transport", "tags": "[]", "affects_whom": ""},
        {"id": rows["f2"], "category": "Visa/Immigration", "tags": "[]", "affects_whom": ""},
    ])
    skip_id = rows["f1"]

    def fake_personalise(profile, articles):
        # Return a Korean impact line for every candidate except skip_id.
        return {a["id"]: "한국어 임팩트 문장" for a in articles if a["id"] != skip_id}

    monkeypatch.setattr("app.llm.personalise.personalise", fake_personalise)

    resp = client.get("/feed")
    assert resp.status_code == 200
    cards = resp.json()

    ids = {c["id"] for c in cards}
    assert skip_id not in ids          # filtered: no impact line
    assert rows["f2"] in ids

    for c in cards:
        assert c["label"] == "What now?"

    visa_card = next(c for c in cards if c["id"] == rows["f2"])
    assert visa_card["category_ko"] == "비자/이민"
    assert visa_card["impact_line"] == "한국어 임팩트 문장"
