# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## Project: "What now?"

A 3-hour hackathon — a personalised UK news feed for Korean residents in the UK.

**[README.md](README.md) is the master plan.** Read it before non-trivial work — it is authoritative for everything about the product. This file (CLAUDE.md) is the *harness* — how to work. README is the *plan* — what to build. If the two appear to conflict, flag it rather than silently picking; treat README as canonical for *what* and CLAUDE.md as canonical for *how*.

**Stack:** FastAPI · Vue 3 (Vite) · SQLite · Anthropic Claude (`claude-haiku-4-5`). Python via `uv`; JS via `npm`.

**MVP focus:** this is a timeboxed build. Prefer the simplest path that makes the demo work; defer hardening, generality, and stretch features unless explicitly asked.

**Branding (hard rule):** the phrase **"What now?"** is the product name and a UI label — it stays in English everywhere, even within Korean text. Never translate it; never instruct an LLM to translate it.

## Git workflow

- **Never work on `main`.** Always work on a feature branch when making changes.
- **One task → one branch → one push.** Keep PRs small and reviewable.
- **Use git actively throughout the build** — small, focused commits as work lands, not one mega-commit at the end.
- **Commit without asking** when you reach a logical stopping point. (Pushing and opening PRs still need confirmation.)
- **Use `git worktree`** when parallelising work across tasks.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.