# What now? — Personalised UK news for Korean residents

> *영국에 사는 한국인을 위한 맞춤형 뉴스 — "이 뉴스가 나에게 어떤 영향을 줄까?"*

"What now?" surfaces UK news that **actually affects you**, and tells you **what to do about it** — in Korean. Tube strike on your line? Visa rule changed for your status? Council tax band shifted in your postcode? You'll see it on the front of the card, in one sentence, in Korean, under a **"What now?"** label.

> **Branding note:** The phrase **"What now?"** is the product name and the card-front section label. It stays in English everywhere in the UI, even within an otherwise-Korean interface. Only the impact-line body that follows it is translated to Korean.

A 3-hour hackathon MVP.

---

## 1. Problem

Koreans living in the UK consume news through a mix of UK English-language outlets and Korean-language community boards. Neither tells them, in their language, *which* UK story matters to *them* and *what they should do next*. The signal-to-noise ratio is poor, and consequential changes (visa, transport, tax, housing) often get missed until they bite.

## 2. Solution

A personalised feed that:

1. Ingests UK news from RSS + structured government / transport APIs.
2. Uses an LLM to categorise each article and extract who it affects.
3. Matches articles against a lightweight user profile (postcode, age, occupation, interests).
4. Presents matched articles as flip-cards: front shows a Korean impact line under a "What now?" label; back shows a Korean summary and a link to the English source.

## 3. Target user

- Korean nationals living in the UK (students, workers, families, long-term residents).
- Comfortable reading Korean; English fluency varies.
- Cares about practical impact, not headline volume.

## 4. MVP scope (3-hour build)

### In scope

- [ ] Single-user local profile (no auth) — stored in SQLite.
- [ ] Profile fields: postcode (first half, e.g. `SW1`), age band, occupation (from fixed list), free-form interests.
- [ ] Ingestion job that pulls from the four source types and writes raw articles to SQLite.
- [ ] LLM categorisation pass: assigns one fixed category + optional free-form tags + an "affects whom" summary.
- [ ] Feed endpoint: given the local profile, returns top-N articles with a Claude-generated Korean **impact-line body** per article (on-demand). The label above it on the card is the literal English string "What now?".
- [ ] Vue card-based UI with flip animation; Korean labels everywhere *except* the "What now?" brand label which stays English; English article body on the back; source link.
- [ ] Manual "refresh feed" button.

### Out of scope (stretch goals if time permits)

- Multi-user accounts / auth.
- Background scheduled ingestion (manual trigger only in MVP).
- Article translation to Korean (back card stays English).
- Push notifications / email digests.
- Hosted deployment (local-first; deploy is a stretch goal).
- Mobile-specific layout (responsive web is enough).

## 5. Architecture

```
┌─────────────────┐     ┌──────────────────────────────────┐
│  Vue 3 frontend │◀───▶│  FastAPI backend                 │
│  (cards, flip)  │     │  ├─ /profile  GET/PUT            │
│                 │     │  ├─ /feed     GET (personalised) │
└─────────────────┘     │  ├─ /ingest   POST (manual run)  │
                        │  └─ /articles GET (raw)          │
                        └────────────┬─────────────────────┘
                                     │
                  ┌──────────────────┼──────────────────┐
                  ▼                  ▼                  ▼
            ┌──────────┐      ┌──────────────┐   ┌──────────────┐
            │ Sources  │      │   SQLite     │   │  Anthropic   │
            │  - RSS   │      │  articles    │   │  Claude      │
            │  - Guard │      │  profile     │   │  (Haiku)     │
            │  - gov   │      │  categories  │   │              │
            │  - TfL   │      └──────────────┘   └──────────────┘
            └──────────┘
```

## 6. Data sources

| Source | Type | Purpose | Auth |
|---|---|---|---|
| BBC, Guardian, Sky, Reuters | RSS | General UK news baseline | None |
| Guardian Open Platform | REST API | Richer body + tags for Guardian articles | Free key |
| gov.uk Content API | REST API | Government announcements (visa, tax, policy) | None |
| TfL Open Data | REST API | Real-time tube/bus/rail disruption | Free key |

## 7. Category taxonomy

Fixed list (LLM must pick exactly one):

`Transport` · `Housing` · `Visa/Immigration` · `Tax/Finance` · `Health` · `Education` · `Work/Employment` · `Safety`

The LLM may additionally attach **free-form tags** (e.g. `student-visa`, `central-line`, `council-tax-band`) to support finer-grained matching against the user's free-form interests.

## 8. User profile

| Field | Type | Example |
|---|---|---|
| `postcode_area` | fixed list (first half) | `SW1`, `E14`, `M1` |
| `age_band` | enum | `<25`, `25–34`, `35–44`, `45+` |
| `occupation` | enum | `Student`, `Office worker`, `Self-employed`, `Researcher`, `Homemaker`, `Other` |
| `interests` | free-form text | `"central line commuter, looking for a flat in Zone 2, ILR application next year"` |

Stored as a single row in SQLite. No auth — whoever opens the browser sees the same profile.

## 9. LLM usage (Anthropic Claude)

Two distinct calls, both using `claude-haiku-4-5` for speed and cost:

**Call A — Categorisation (per article, run during ingest):**
- Input: article title + body (or summary).
- Output: `{category, free_form_tags, affects_whom_summary}` as JSON.
- Cached in SQLite — each article is categorised exactly once.

**Call B — Personalisation (per feed load, batched):**
- Input: user profile + top candidate articles (filtered by category↔interest overlap).
- Output: per-article Korean **impact-line body** (≤25 words / ~40 자, action-oriented). The body is Korean; the **"What now?"** label rendered above it on the card is a fixed English string and is **not** part of the LLM output.
- Prompt must explicitly instruct the model **not to translate or replace the phrase "What now?"** — it is a brand string.
- Not cached — always fresh.

## 10. UI — the card

```
┌────────────────────────────────────────┐         ┌────────────────────────────────────────┐
│ FRONT                                  │  flip   │ BACK                                   │
│                                        │  ───▶   │                                        │
│ [Tube · 교통]                          │         │ 요약 (Korean summary, 3–4 lines)        │
│                                        │         │                                        │
│ Central line closed this weekend       │         │ ──────────────                          │
│                                        │         │ Original article (English):            │
│ ── What now? ──                        │         │ "Central line to close for weekend     │
│ 토요일 출근길에 영향 —                  │         │  engineering works..."                 │
│ 우회로: Piccadilly + Victoria          │         │                                        │
│                                        │         │ 🔗 Read on bbc.co.uk                    │
└────────────────────────────────────────┘         └────────────────────────────────────────┘
```

## 11. Tech stack

- **Backend:** FastAPI (Python), SQLite via SQLAlchemy or raw `sqlite3`.
- **Frontend:** Vue 3 (Vite), no heavy UI framework — minimal CSS + a flip animation.
- **LLM:** Anthropic SDK (`anthropic` Python package), `claude-haiku-4-5`.
- **Python tooling:** `uv` for dependency management and runs.
- **Sources:** `feedparser` for RSS, `httpx` for the REST APIs.

## 12. Repository layout (proposed)

```
KUITA-C1/
├── README.md
├── idea_brainstorm.md
├── backend/
│   ├── pyproject.toml
│   ├── app/
│   │   ├── main.py            # FastAPI entry
│   │   ├── db.py              # SQLite setup + schema
│   │   ├── models.py
│   │   ├── routes/
│   │   │   ├── profile.py
│   │   │   ├── feed.py
│   │   │   ├── articles.py
│   │   │   └── ingest.py
│   │   ├── sources/
│   │   │   ├── rss.py
│   │   │   ├── guardian.py
│   │   │   ├── govuk.py
│   │   │   └── tfl.py
│   │   └── llm/
│   │       ├── categorise.py
│   │       └── personalise.py
│   └── data/                  # SQLite file lives here (gitignored)
└── frontend/
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── App.vue
        ├── main.js
        ├── components/
        │   ├── Card.vue
        │   ├── Feed.vue
        │   └── ProfileForm.vue
        └── api.js
```

## 13. Run locally

```sh
# backend
cd backend
uv sync
uv run uvicorn app.main:app --reload

# frontend (new terminal)
cd frontend
npm install
npm run dev
```

Set `ANTHROPIC_API_KEY` and `GUARDIAN_API_KEY` (and `TFL_APP_KEY`) in `backend/.env`.

## 14. Development workflow

(carried over from the brainstorm — these are team rules for this hackathon)

- Never work directly on `main`. Create a branch per task.
- Commit actively; ask before committing if uncertain.
- Use `git worktree` when parallelising work between teammates.
- Push per task so PRs stay small.

## 15. Three-hour timeboxing (suggested)

| Time | Goal |
|---|---|
| 0:00 – 0:30 | Skeleton: FastAPI app, Vue scaffold, SQLite schema, profile CRUD. |
| 0:30 – 1:15 | Source ingestion (RSS + at least gov.uk and TfL) → raw articles in DB. |
| 1:15 – 2:00 | LLM categorise pass + feed endpoint with on-demand personalisation. |
| 2:00 – 2:45 | Card UI with flip animation, Korean labels, profile form. |
| 2:45 – 3:00 | Demo polish, seed a good demo profile, rehearse the pitch. |

Stretch slot: deploy.

## 16. Demo script (for the pitch)

1. Show empty feed with default profile.
2. Edit profile: postcode `SW1`, "student" occupation, interest "central line commuter, looking for flat in Zone 2".
3. Hit refresh — three cards land: a Central line disruption, a council tax update for SW1, a visa rule change for students.
4. Flip a card to show the source.
5. Change occupation to "office worker" and refresh — feed reshuffles. Done.
