# Backend implementation plan — "What now?"

Backend build plan for the **"What now?"** MVP (personalised UK news feed in Korean for Korean residents in the UK). Derived from [README.md](README.md), which remains the authoritative master plan. This document is the executable roadmap for the backend only.

> **Branding hard rule:** the phrase **"What now?"** is the product name and a fixed English UI label. It stays in English everywhere — never translated, never sent to the LLM as translatable text. The label is added in code; only the Korean impact-line body comes from the LLM.

---

## 1. Scope & decisions

- **Stack:** FastAPI + raw stdlib `sqlite3` + Anthropic `claude-haiku-4-5`. Python via `uv`.
- **Sources (MVP):** RSS (BBC / Guardian / Sky / Reuters) + gov.uk Content/Search API. **No auth keys except `ANTHROPIC_API_KEY`.** TfL and the Guardian Open Platform are deferred stretch sources.
- **DB layer:** raw `sqlite3` + a small helper module. No ORM (simplest path for a 3-hour build).
- **Auth:** none. Single user, single profile row (README §8).
- **Seed data:** curated demo articles exist as a seed script, **gated behind a `SEED_ON_STARTUP` flag** so it can be enabled/disabled.
- **LLM:** two calls (README §9) — categorisation cached in the DB (run once per article); personalisation fresh per feed load.
- **Out of scope (README §4):** auth, scheduled ingestion, TfL/Guardian APIs, back-card translation, deployment.

---

## 2. Directory layout (`backend/`, follows README §12)

```
backend/
├── pyproject.toml          # uv-managed deps
├── .env.example            # documented env vars (real .env is gitignored)
├── app/
│   ├── main.py             # FastAPI app, CORS, startup: init_db + optional seed
│   ├── config.py           # env settings (pydantic-settings)
│   ├── db.py               # sqlite connection, schema DDL, init_db()
│   ├── repository.py       # SQL CRUD helpers (articles, profile)
│   ├── models.py           # pydantic request/response schemas
│   ├── taxonomy.py         # fixed category list + Korean labels (README §7)
│   ├── seed.py             # curated demo articles (flag-gated)
│   ├── routes/
│   │   ├── profile.py      # GET/PUT /profile
│   │   ├── feed.py         # GET /feed
│   │   ├── articles.py     # GET /articles
│   │   └── ingest.py       # POST /ingest
│   ├── sources/
│   │   ├── base.py         # RawArticle shape + dedup id helper
│   │   ├── rss.py          # feedparser over feed URL list
│   │   └── govuk.py        # gov.uk Search API via httpx
│   └── llm/
│       ├── client.py       # Anthropic client + messages helper
│       ├── categorise.py   # Call A (batched, cached in DB)
│       └── personalise.py  # Call B (batched, fresh)
└── data/                   # sqlite file lives here (gitignored)
```

---

## 3. SQLite schema (`db.py`)

**`articles`**

| Column | Type | Notes |
|---|---|---|
| `id` | INTEGER PK | |
| `source` | TEXT | e.g. `bbc`, `guardian`, `govuk` |
| `source_id` | TEXT UNIQUE | RSS guid / API id / url — dedup key on re-ingest |
| `title` | TEXT | |
| `url` | TEXT | |
| `summary` | TEXT | English body/summary (back-of-card source text) |
| `published_at` | TEXT | ISO |
| `fetched_at` | TEXT | ISO |
| `category` | TEXT NULL | one fixed taxonomy value (NULL until categorised) |
| `tags` | TEXT NULL | JSON array string of free-form tags |
| `affects_whom` | TEXT NULL | short LLM "affects whom" note |
| `categorised_at` | TEXT NULL | |

**`profile`** — single row, `id` PK with `CHECK(id = 1)`:
`postcode_area`, `age_band`, `occupation`, `interests`, `updated_at`.

Categories are a hard-coded list in `taxonomy.py`, **not** a DB table.

---

## 4. Endpoints

| Method | Path | Behaviour |
|---|---|---|
| GET | `/health` | sanity check |
| GET | `/profile` | return profile; create a sensible default row if none exists |
| PUT | `/profile` | upsert the single profile row |
| POST | `/ingest` | pull enabled sources → dedup-insert by `source_id` → categorise new/uncategorised rows → return `{fetched, inserted, categorised}` |
| GET | `/articles` | raw list (optional `?category=` filter) — debugging/visibility |
| GET | `/feed` | candidate-select against profile → batched personalise → return cards |

**Feed card response shape** (per article):

```json
{
  "id": 1,
  "title": "Central line to close for weekend engineering works",
  "category": "Transport",
  "category_ko": "교통",
  "label": "What now?",
  "impact_line": "토요일 출근길 영향 — 우회: Piccadilly + Victoria",
  "summary": "...",
  "url": "https://www.bbc.co.uk/..."
}
```

`label` is always the literal English string `"What now?"`. `impact_line` is the Korean body from the LLM.

---

## 5. Sources (`sources/`)

- **`base.py`** — each source returns `list[dict]` with keys `source, source_id, title, url, summary, published_at`. Helper to normalise/derive the dedup id.
- **`rss.py`** — `feedparser` over a configured list of feed URLs (BBC News UK, Guardian UK, Sky, Reuters UK). Map entries → RawArticle.
- **`govuk.py`** — query the gov.uk **Search API** (`https://www.gov.uk/api/search.json`) for recent announcements/news relevant to visa/immigration, tax, housing, transport; map results → RawArticle. No key needed.
- Ingestion orchestration lives in `routes/ingest.py`: gather from enabled sources (toggled via config), insert with `INSERT OR IGNORE` on `source_id`.

---

## 6. LLM (`llm/`) — README §9

- **`client.py`** — build the Anthropic client from `ANTHROPIC_API_KEY`; thin `complete()` helper using `claude-haiku-4-5`. Apply `cache_control` to the static system prompt (taxonomy/instructions) so repeated categorisation calls within one ingest reuse it (only meaningful above the cache token minimum — keep simple, don't over-engineer).
- **Call A — `categorise.py`** (cached): batch ~10 uncategorised articles per call. System prompt = fixed taxonomy + "pick exactly one category, add free-form tags, one-line affects-whom". Output a strict JSON array keyed by article id → write `category / tags / affects_whom / categorised_at`. Only runs where `category IS NULL`, so each article is categorised once.
- **Call B — `personalise.py`** (fresh): one batched call with the user profile + the selected candidate articles. Output = per-article Korean **impact-line body** (≤ ~40 자, action-oriented), returned as JSON keyed by article id. The system prompt **explicitly forbids translating or replacing "What now?"** — and we don't send that string for translation; the label is added in code.

---

## 7. Candidate selection for `/feed` (plain Python, pre-LLM)

Keep it simple and cheap; only personalise the final shortlist.

- Consider only categorised articles.
- Score each: category ↔ occupation/interest relevance + tag overlap with the free-form `interests` text + recency. `Visa/Immigration` treated as broadly relevant; `Transport` boosted when interests/postcode mention a line or commuting.
- Take top `FEED_SIZE` (default 6) → single batched `personalise` call.

---

## 8. Config & env (`config.py`, `.env.example`)

```
ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=claude-haiku-4-5
ENABLE_RSS=true
ENABLE_GOVUK=true
SEED_ON_STARTUP=false      # flag to enable/disable curated demo seed
FEED_SIZE=6
CORS_ORIGINS=http://localhost:5173
```

`pydantic-settings` loads `.env`. CORS configured for the Vite dev origin so the frontend can call the API.

---

## 9. Seed (`seed.py`) — flag-gated

~5–6 curated, pre-categorised demo articles matching the README §16 demo (Central line weekend closure, SW1 council-tax band change, student-visa salary threshold, NHS surcharge, Zone-2 rental update). Inserted when `SEED_ON_STARTUP=true` at startup, or on demand via `uv run python -m app.seed`. Pre-categorised so the demo feed works without spending LLM calls on categorisation; `/feed` still personalises them live.

---

## 10. Dependencies (`pyproject.toml`, via `uv`)

`fastapi`, `uvicorn[standard]`, `httpx`, `feedparser`, `anthropic`, `pydantic`, `pydantic-settings`.

---

## 11. Build order (phased — each phase is a small branch/PR, verify before moving on)

1. **Scaffold:** `pyproject`, `config`, `db` + schema, `/health`, `/profile` GET/PUT. → verify with curl.
2. **Ingestion:** `sources/` (RSS + gov.uk), `POST /ingest`, `GET /articles`. → verify rows land in `data/` DB.
3. **Categorise:** wire `llm/categorise` into `/ingest`. → verify `category / tags / affects_whom` populated.
4. **Feed:** candidate selection + `llm/personalise` + `GET /feed`. → verify cards with Korean impact lines and literal `"What now?"` label.
5. **Seed:** `seed.py` + flag. → verify demo feed appears with `SEED_ON_STARTUP=true`.

---

## 12. Verification (end-to-end)

```sh
cd backend
uv sync
SEED_ON_STARTUP=true uv run uvicorn app.main:app --reload
# in another shell:
curl localhost:8000/health
curl -X PUT localhost:8000/profile -H 'content-type: application/json' \
  -d '{"postcode_area":"SW1","age_band":"25–34","occupation":"Student","interests":"central line commuter, flat in Zone 2, ILR next year"}'
curl -X POST localhost:8000/ingest
curl localhost:8000/articles
curl localhost:8000/feed
```

Checks: `/feed` returns cards; each `label` is the literal `"What now?"` (never translated); `impact_line` is Korean and action-oriented; back-card `summary` / `url` present.

---

## Git

Write this doc on `docs/plan-backend`; ask before committing. Subsequent code phases each get their own branch (README §14: one task → one branch → one push).
