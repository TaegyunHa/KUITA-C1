# Frontend implementation plan — "What now?"

Frontend build plan for the **"What now?"** MVP (personalised UK news feed in Korean for Korean residents in the UK). Derived from [README.md](README.md) (authoritative master plan) and [plan_backend.md](plan_backend.md) (the API it consumes). This document is the executable roadmap for the **frontend only** and is self-contained: the API contract and form enums it depends on are restated here so you don't have to cross-reference while building.

> **Branding hard rule:** the phrase **"What now?"** is the product name and a fixed English UI label. It stays in English everywhere — even inside otherwise-Korean text. The label is rendered as a literal string in the component; the backend also returns it as `label: "What now?"`. Never translate it.

---

## 1. Scope & decisions

- **Stack:** Vue 3 (Composition API, `<script setup>`) + Vite. Plain CSS, **no UI framework** (README §11). Vanilla `fetch` — no axios.
- **Single page.** Profile form + feed of flip-cards on one screen. No router (single view, MVP).
- **No auth, no state library.** One shared profile (backend stores a single row). Local component state via `ref`/`reactive` is enough — no Pinia/Vuex.
- **API base URL** via `VITE_API_BASE` env, defaulting to `http://localhost:8000`. Backend already sends CORS for `http://localhost:5173`, so the browser calls the API directly — **no Vite dev proxy needed**.
- **Back of card is English** (summary + source link). README §10's mock shows a Korean `요약`, but README §4 lists "article translation to Korean (back card stays English)" as **out of scope**, and the backend `/feed` returns a single English `summary`. Canonical decision: **back card = English `summary` + `url` only.** The §10 Korean-summary mock is aspirational, not built.
- **Refresh = re-fetch `/feed`.** The "refresh feed" button (README §4) calls `GET /feed`; it does **not** trigger ingestion. Ingestion (`POST /ingest`) and seeding are backend/demo concerns handled out-of-band (see §9).
- **Out of scope:** auth UI, routing, article-list/debug view, ingestion-trigger UI, responsive/mobile-specific layout (responsive web is enough), back-card translation.

---

## 2. Directory layout (`frontend/`, follows README §12)

```
frontend/
├── package.json
├── vite.config.js
├── .env.example            # VITE_API_BASE=http://localhost:8000
├── index.html
└── src/
    ├── main.js             # createApp(App).mount
    ├── App.vue             # layout; owns profile + feed state; wires children
    ├── api.js              # fetch wrappers (getProfile/putProfile/getFeed)
    ├── style.css           # global minimal CSS (reset + card styles)
    └── components/
        ├── ProfileForm.vue # profile editor (enums as selects + free-form interests)
        ├── Feed.vue        # refresh button + loading/empty/error + list of Cards
        └── Card.vue        # single flip-card (front/back)
```

---

## 3. API contract (consumed)

Base URL: `import.meta.env.VITE_API_BASE` (default `http://localhost:8000`). All JSON.

| Method | Path | Frontend use |
|---|---|---|
| GET | `/profile` | load profile on mount (backend auto-creates a default row, so this never 404s) |
| PUT | `/profile` | save profile form |
| GET | `/feed` | fetch personalised cards (on mount after profile, and on Refresh) |

`GET /articles` and `POST /ingest` exist (plan_backend §4) but the MVP UI does **not** call them.

### Profile shapes

`GET /profile` → `ProfileOut`, `PUT /profile` body → `ProfileIn`:

```jsonc
// PUT request body (ProfileIn)
{
  "postcode_area": "SW1",
  "age_band": "25–34",
  "occupation": "Student",
  "interests": "central line commuter, flat in Zone 2, ILR next year"
}
// GET / PUT response (ProfileOut) = ProfileIn + updated_at
{ "...": "...", "updated_at": "2026-05-30T12:00:00" }
```

### Feed card shape

`GET /feed` → array of cards (plan_backend §4):

```jsonc
{
  "id": 1,
  "title": "Central line to close for weekend engineering works",
  "category": "Transport",        // English taxonomy value
  "category_ko": "교통",           // Korean label for the chip
  "label": "What now?",           // ALWAYS this literal string — render as-is
  "impact_line": "토요일 출근길 영향 — 우회: Piccadilly + Victoria",  // Korean body
  "summary": "...",               // English back-card text
  "url": "https://www.bbc.co.uk/..."
}
```

- Front of card: category chip (`category` · `category_ko`), `title`, then the `label` ("What now?") above the Korean `impact_line`.
- Back of card: English `summary` + a "Read on …" link to `url`.

---

## 4. Profile form fields & enums (README §7–§8)

`ProfileForm.vue` supplies the fixed options (backend stores them as free strings). Use exact strings below — `age_band` contains an **en-dash** (`–`, U+2013), not a hyphen.

| Field | Control | Options |
|---|---|---|
| `postcode_area` | text input (or small select) | free-form first-half postcode, e.g. `SW1`, `E14`, `M1` |
| `age_band` | select | `<25`, `25–34`, `35–44`, `45+` |
| `occupation` | select | `Student`, `Office worker`, `Self-employed`, `Researcher`, `Homemaker`, `Other` |
| `interests` | textarea | free-form, e.g. `"central line commuter, looking for a flat in Zone 2, ILR application next year"` |

**Category taxonomy** (README §7) — only needed if you add chip colours or a future filter; the feed already returns `category` + `category_ko`, so the form does not need it:
`Transport · Housing · Visa/Immigration · Tax/Finance · Health · Education · Work/Employment · Safety`.

UI strings (headings, button labels, field labels) are **Korean**, except the brand label **"What now?"** which stays English.

---

## 5. Components

- **`api.js`** — three async functions returning parsed JSON: `getProfile()`, `putProfile(profile)` (PUT), `getFeed()`. A tiny `request()` helper prepends `VITE_API_BASE`, sets `content-type: application/json`, and throws on non-2xx so callers can show an error state.
- **`App.vue`** — owns `profile`, `feed`, and the loading/error flags; loads profile then feed on mount; passes data + callbacks down. Layout: `ProfileForm` on top/side, `Feed` below.
- **`ProfileForm.vue`** — props: `profile`; emits `save` with the edited fields. Renders the §4 controls. On save → parent calls `putProfile` then re-fetches `/feed` (so the feed reshuffles, per the demo).
- **`Feed.vue`** — props: `cards`, `loading`, `error`; emits `refresh`. Renders the Refresh button and the three UI states (§6) plus the card list.
- **`Card.vue`** — props: one card object. Local `flipped` ref toggled on click. Renders front/back per §3 and the flip animation (§7).

---

## 6. State, data flow & UX states

Flow:
1. `App` mounts → `getProfile()` → populate form.
2. Then `getFeed()` → populate cards.
3. User edits profile → `Save` → `putProfile()` → `getFeed()` again.
4. `Refresh` button → `getFeed()` again.

**`/feed` is slow:** it runs a *live, batched LLM personalisation call* per load (plan_backend §6). The UI **must** show a loading state, not a frozen button.

Three feed states to handle explicitly:
- **Loading** — spinner / "불러오는 중…"; disable the Refresh and Save buttons while in flight.
- **Empty** — `[]` (e.g. before any ingest/seed): friendly "표시할 뉴스가 없습니다" message, not a blank screen.
- **Error** — fetch throws: short Korean error + a retry affordance (the Refresh button).

---

## 7. Card flip UI (README §10)

```
┌─ FRONT ───────────────────────┐      ┌─ BACK ────────────────────────┐
│ [Transport · 교통]            │ flip │ 요약 (English summary, 3–4 lines) │
│ Central line to close ...     │ ───▶ │ ──────────────                 │
│ ── What now? ──               │      │ 🔗 Read on bbc.co.uk           │
│ 토요일 출근길 영향 — 우회: ... │      │                                │
└───────────────────────────────┘      └───────────────────────────────┘
```

- Pure CSS 3D flip: outer `.card` with `perspective`; inner wrapper with `transform: rotateY(180deg)` toggled by a `.flipped` class; front/back faces use `backface-visibility: hidden` and the back is pre-rotated `180deg`.
- Click anywhere on the card to flip; the source `🔗` link uses `target="_blank" rel="noopener"` and should `stop` propagation so opening the link doesn't also flip the card.
- The "What now?" label is a styled literal string in the template — never bound to translatable data.

---

## 8. Config & env

```
# frontend/.env.example
VITE_API_BASE=http://localhost:8000
```

`vite.config.js`: default Vue plugin, dev server on `5173` (the origin the backend's CORS already allows). No proxy.

---

## 9. Local run & demo data

```sh
# backend (terminal 1) — must be up first; seed gives the demo its cards
cd backend
SEED_ON_STARTUP=true uv run uvicorn app.main:app --reload

# frontend (terminal 2)
cd frontend
npm install
npm run dev   # http://localhost:5173
```

The feed only has content once the backend has articles — easiest for the demo is `SEED_ON_STARTUP=true` (plan_backend §9), which loads pre-categorised demo articles so `/feed` works without an ingest run. The frontend itself does not trigger ingestion.

---

## 10. Build order (phased — small branch/PR per phase, verify before moving on)

1. **Scaffold:** `npm create vite@latest` (Vue), strip boilerplate, `api.js` + `.env.example`, base layout in `App.vue`. → verify dev server runs and `getProfile()` returns the default profile.
2. **Profile form:** `ProfileForm.vue` with enums (§4), load + save wired through `App`. → verify PUT persists (re-mount shows saved values).
3. **Feed list:** `getFeed()`, `Feed.vue` with loading/empty/error states, render plain (non-flip) cards. → verify cards show `title`, Korean `impact_line`, and literal `"What now?"` label.
4. **Flip card:** `Card.vue` front/back + CSS flip; back shows English `summary` + source link. → verify click flips; link opens without flipping.
5. **Polish:** Korean UI strings, chip styling, refresh-on-save, responsive width. → verify the §11 demo flow end-to-end.

---

## 11. Verification (against the demo script, README §16)

1. Load app with default profile → feed renders (or a clean empty state).
2. Edit profile: postcode `SW1`, occupation `Student`, interests "central line commuter, looking for flat in Zone 2" → Save.
3. Feed reshuffles: relevant cards appear (Central line disruption, SW1 council-tax, student-visa change).
4. Flip a card → English source summary + working `🔗` link.
5. Change occupation to `Office worker` → Save → feed reshuffles.

Hard checks: every card shows the literal `"What now?"` (never translated); `impact_line` renders as Korean; UI chrome is Korean except the brand label; loading state shows during the (slow) `/feed` call; en-dash preserved in `age_band` values.

---

## Git

Written on `docs/plan-frontend` (separate worktree, branched from `main`, since another agent is active in the repo). Subsequent code phases each get their own branch (README §14: one task → one branch → one push).
