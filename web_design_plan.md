# What NOW? — Web UI Design Plan

> Personalised UK news for Koreans living in the UK.
> Vue 3 + Vite frontend. Card-based, colourful, Korean/English toggleable.

---

## 1. Colour System

### Brand tokens

| Token             | Hex       | Usage                                      |
|-------------------|-----------|--------------------------------------------|
| `--bg`            | `#FFFFFF` | Page background                            |
| `--main`          | `#131415` | Navbar background, heavy UI elements       |
| `--accent`        | `#03369D` | Buttons, active states, links              |
| `--accent-light`  | `#DFE9FF` | Hover states, selected category highlight  |
| `--surface`       | `#DBE0E8` | Card borders, dividers, inactive chip bg   |
| `--text-main`     | `#121416` | All body and heading text                  |
| `--text-sub`      | `#777A8E` | Secondary labels, timestamps, placeholders |

### Category colour palette

Each category has a chip background (used in section headers and card tops) and a card tint (the card background). All are desaturated pastels so `--text-main` stays readable at WCAG AA.

| Category          | Chip bg   | Card tint |
|-------------------|-----------|-----------|
| Transport         | `#BFDBFE` | `#EFF6FF` |
| Visa/Immigration  | `#C7D2FE` | `#EEF2FF` |
| Health            | `#FBCFE8` | `#FDF2F8` |
| Housing           | `#FDE68A` | `#FFFBEB` |
| Tax/Finance       | `#A7F3D0` | `#ECFDF5` |
| Work/Employment   | `#99F6E4` | `#F0FDFA` |
| Education         | `#FEF08A` | `#FEFCE8` |
| Safety            | `#FECACA` | `#FEF2F2` |

---

## 2. Typography

Font: **Inter** (system fallback: `-apple-system, sans-serif`)

| Role              | Weight    | Size  | Colour         |
|-------------------|-----------|-------|----------------|
| Logo / brand      | Bold 700  | 20px  | `#FFFFFF`      |
| Section heading   | Semi Bold | 16px  | `--text-main`  |
| Card headline     | Semi Bold | 14px  | `--text-main`  |
| "What now?" label | Semi Bold | 11px  | `--accent`     |
| Impact line (KO)  | Regular   | 12px  | `--text-main`  |
| Body / labels     | Regular   | 14px  | `--text-main`  |
| Secondary labels  | Regular   | 13px  | `--text-sub`   |
| Timestamps / meta | Regular   | 11px  | `--text-sub`   |

---

## 3. Layout Grid

- **Max content width:** 1512px (desktop)
- **Horizontal padding:** 40px left / right
- **Content starts:** 64px from top (below fixed navbar)
- **Card width:** 440px (3 per row, 16px gap between)
- **Card height:** 208px (fixed)

---

## 4. Screens

---

### Screen 1 — Feed (Home) `/`

```
┌────────────────────────────────────────────────────────────────────┐
│ NavBar  [#131415, h=64px]                                          │
│  What NOW?  (Bold 20px white)    [KO | EN]    [프로필 →]           │
└────────────────────────────────────────────────────────────────────┘
│                                          [↻ 피드 새로고침]  (btn)  │
│                                                                    │
│  [교통 chip]  Transport  ─────────────────────────────  더 보기 →  │
│  ──────────────────────────────────────────────────────────────    │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │ NewsCard         │  │ NewsCard         │  │ NewsCard         │ │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘ │
│                                                                    │
│  [비자·이민 chip]  Visa/Immigration  ───────────────  더 보기 →    │
│  ──────────────────────────────────────────────────────────────    │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │ NewsCard         │  │ NewsCard         │  │ NewsCard         │ │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘ │
│                                                                    │
│  ... (repeats for all 8 categories, hidden if 0 articles)         │
└────────────────────────────────────────────────────────────────────┘
```

**Navbar spec:**
- Background: `#131415`
- Height: 64px, full width, fixed position
- Logo: "What NOW?" — Inter Bold 20px, `#FFFFFF`, x=40
- KO/EN toggle: pill shape, bg `#282D37`, radius 20px, centred horizontally
  - "KO" Semi Bold white (active) | "|" gray | "EN" gray (inactive)
- Profile button: "프로필 →" — filled `--accent`, radius 8px, right edge at x=1472

**Refresh button:**
- "↻  피드 새로고침" — filled `--accent`, radius 8px
- Position: top-right of content area, below navbar

**Category section:**
- Category chip (coloured pill, 20px radius) + category name in `--text-sub` + "더 보기 →" link right-aligned
- 1px horizontal rule in `--surface` below header
- Card row: 3 cards × 440px with 16px gap, left-aligned at padding=40px
- 40px gap between sections

---

### Screen 2 — News Detail Page (full-page, opens from Screen 1 card flip)

Triggered by clicking a news card in Screen 1. The card flips (rotateY 180°) then expands to fill the full viewport. This page is the expanded back face — scrollable, max-width 720px, centred.

**Entry / exit animation:**
- Phase 1 — Flip: `transform: rotateY(180deg)`, `transition: 0.4s ease`
- Phase 2 — Expand: card scales to 100vw × 100vh, `transition: 0.3s ease`
- Dismiss: "← 뒤로" reverses expand then flip, returning user to Screen 1

```
┌──────────────────────────────────────────────────────┐
│ ← 뒤로                             [category chip]  🔖 │  top bar
├──────────────────────────────────────────────────────┤
│                                                      │
│  Central line closed this weekend                    │  Bold 22px
│  TfL  ·  2h ago                                      │  12px --text-sub
│                                                      │
│  ── Summary ──────────────────────────────────────   │  --accent divider label
│  (Korean AI summary, 4–6 lines)                      │  Regular 15px
│                                                      │
│  ── What's my NOW? ───────────────────────────────   │  --accent divider label
│  Impact: 토요일 출근길 우회 필요                        │  Regular 14px
│  Action: Piccadilly line 이용 권장                    │  Regular 14px
│                                                      │
├──────────────────────────────────────────────────────┤
│  Original Articles                                   │  Section label 13px Bold
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │ 📰  Central line closure — BBC News           │   │  article card
│  │     "The Central line will be suspended..."   │   │  Regular 13px --text-sub
│  │                                    ↗ bbc.co.uk│   │  opens source in new tab
│  └──────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────┐   │
│  │ 📰  Weekend travel disruption — TfL           │   │  article card
│  │     "Passengers are advised to use..."        │   │  Regular 13px --text-sub
│  │                                    ↗ tfl.gov.uk│  │  opens source in new tab
│  └──────────────────────────────────────────────┘   │
│                                                      │
├──────────────────────────────────────────────────────┤
│  Official Documents & Terms                          │  Section label 13px Bold
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │ 📄  TfL Service Update — Official Notice      │   │  doc card
│  │     "Planned engineering works on…"           │   │
│  │  💡 우회 (Bypass): 목적지까지 다른 경로를 이용  │   │  term chip, --surface bg
│  └──────────────────────────────────────────────┘   │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**Section 1 — Summary + Impact & Action Plan**
- Headline: Bold 22px, full width
- Source · timestamp: 12px, `--text-sub`
- Summary: Korean AI-generated, 4–6 lines, Regular 15px
- "What's my NOW?" block: two lines — Impact (나에게 미치는 영향) and Action (권장 행동), both Korean, Regular 14px, `--accent` label

**Section 2 — Original Articles**
- Each source rendered as a card: `--surface` bg, 12px radius, padding 16px
- Shows outlet icon, headline, 2-line excerpt
- Entire card is clickable → opens source URL in new tab (`target="_blank"`)
- Multiple sources stacked vertically

**Section 3 — Official Documents & Terms**
- Official government / institutional documents related to the story
- Each doc card includes inline term chips: difficult or jargon words highlighted with a plain-Korean explanation tooltip or inline note
- Term chip style: `--surface` background, 11px, `--accent` text

---

### Screen 3 — Profile Page `/profile`

```
┌────────────────────────────────────────────────────────────────────┐
│ NavBar  [same as Feed]                                             │
└────────────────────────────────────────────────────────────────────┘
│                                                                    │
│              ┌────────────────────────────┐                        │
│              │  프로필 설정  /  Profile     │  heading 24px Bold    │
│              │                            │                        │
│              │  기본 정보                  │  section label 12px   │
│              │  ─────────────────         │  --surface divider    │
│              │  우편번호 지역               │  label 14px           │
│              │  [SW1 ▾ dropdown]          │  --surface border     │
│              │                            │                        │
│              │  연령대                     │                        │
│              │  ○ <25  ○ 25–34  ● 35–44  ○ 45+  │  radio group   │
│              │                            │                        │
│              │  직업                       │                        │
│              │  [Student ▾ dropdown]      │                        │
│              │                            │                        │
│              │  관심사                     │  section label        │
│              │  ─────────────────         │                        │
│              │  [textarea — free text     │  min-height 80px      │
│              │   "central line commuter…"]│                        │
│              │                            │                        │
│              │  [     저장 / Save     ]    │  --accent btn, full w │
│              │                            │                        │
│              │  프로필 초기화              │  small link, --text-sub│
│              └────────────────────────────┘                        │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

- Form container: max-width 600px, centred, top margin 64px
- Section labels: 12px Semi Bold, `--text-sub`, uppercase letter-spacing
- Inputs / dropdowns: full-width, border `--surface`, radius 8px, padding 12px
- Focus state: border `--accent`, box-shadow `0 0 0 3px --accent-light`
- Save button: `--accent` fill, white text, full-width, radius 8px, height 48px
- "프로필 초기화" reset link: centred below button, 13px, `--text-sub`

---

### Screen 4 — Onboarding Modal (first visit)

Shown when `localStorage.profileComplete` is falsy. Same form as Profile Page but inside a modal overlay.

```
┌────────────────────────────────────────────────────────────────────┐
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                               ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ┌───────────────────────┐   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  What NOW?            │   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  나에게 맞는 뉴스를    │   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  시작해 보세요        │   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  ─────────────────    │   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  [form fields…]       │   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │                       │   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  [ What's my NOW? → ]  │   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  └───────────────────────┘   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
└────────────────────────────────────────────────────────────────────┘
```

- Overlay: `rgba(0,0,0,0.5)`, full viewport
- Modal card: white, radius 16px, padding 40px, max-width 480px, centred
- Logo "What NOW?" at top: Bold 24px, `--main`
- Subtitle: "나에게 맞는 뉴스를 시작해 보세요" — 16px Regular, `--text-sub`
- Same form fields as Profile Page
- CTA button: "What's my NOW? →" — `--accent`, full-width, height 48px
- On submit: save profile, set `localStorage.profileComplete = true`, close modal, load feed

---

## 5. Vue 3 Component Map

```
src/
├── App.vue                    ← <RouterView> + <NavBar>
├── views/
│   ├── FeedView.vue           ← loops CATS, renders <CategorySection> per cat
│   └── ProfileView.vue        ← /profile form page
├── components/
│   ├── NavBar.vue             ← logo, LangToggle, ProfileBtn
│   ├── LangToggle.vue         ← KO / EN pill button
│   ├── CategorySection.vue    ← chip header + horizontal card row
│   ├── NewsCard.vue           ← flip card with front/back faces
│   ├── OnboardingModal.vue    ← first-visit modal wrapping ProfileForm
│   └── ProfileForm.vue        ← shared form fields (used in modal + /profile)
├── composables/
│   └── useLanguage.js         ← locale ref, provide/inject app-wide
├── api.js                     ← fetch helpers for FastAPI endpoints
└── tokens.css                 ← all CSS custom properties (--tokens above)
```

---

## 6. KO/EN Toggle Rules

| Element                        | KO mode            | EN mode          |
|--------------------------------|--------------------|------------------|
| Nav items, buttons, labels     | Korean             | English          |
| Category names in chips        | 교통, 비자·이민…   | Transport, Visa… |
| **"What now?" card label**     | **Always English** | **Always English**|
| LLM impact lines               | Always Korean      | Always Korean    |
| Korean summary (card back)     | Always Korean      | Always Korean    |
| English article excerpt        | Always English     | Always English   |

Implementation: a `locale` ref in `useLanguage.js`, provided at `App.vue`. All static strings defined as `{ ko: '저장', en: 'Save' }` objects. Consume with `t('저장', 'Save')` helper.

---

## 7. Figma File Update Plan

File: `https://www.figma.com/design/OSsA1ngtSRiAl7KCPl4DoW/Untitled`

Frames to create / rename:

| New frame name           | Replaces / new           | Size       |
|--------------------------|--------------------------|------------|
| `Feed — Desktop`         | Old "Home" frame (2:3)   | 1512×980   |
| `Card — Front & Back`    | Old "Detail" frame (3:16)| 960×300    |
| `Profile Page`           | Old "Signup" frame (3:20)| 1512×900   |
| `Onboarding Modal`       | New                      | 1512×900   |

Existing reference screenshots (Semafor, Flipboard) should remain on canvas as inspiration.
