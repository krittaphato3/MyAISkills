# CONTRIBUTING.md — Skill Upgrade Process

How to add, upgrade, or replace a skill in the ZCode catalog (`skills/<name>/SKILL.md`, manifest `docs/skills/skills.json`). Every change follows the lifecycle and must clear the gates below. Companion guides: system-instructions v2, WORKFLOW.md, AGENT-SKILL-MATRIX.md, SKILLS.md. All mechanics assume a skill already carries the standard frontmatter (Phase 0.3).

## 1. Skill lifecycle

propose → spec → plan → implement → red-team-qa → lint → eval → review

1. **propose** — state the gap: because no skill covers an existing need, or because a skill is below the grade floor (G2). Record the rationale.
2. **spec** — set frontmatter: `name`, precise `description` trigger, `version`, `grade`, `domain`, `status`, `last-reviewed`, `owned-by-agent`. Confirm domain and owner against AGENT-SKILL-MATRIX.md.
3. **plan** — non-trivial work gets an approved plan (deep-planner or writing-plans) before code, per WORKFLOW.md §8.
4. **implement** — write content to grade, keeping all pre-existing sections (never shrink; density over placeholders).
5. **red-team-qa** — adversarial review for contradictions with the rest of the catalog and ambiguity.
6. **lint** — `python tools/skill_lint.py --json`; zero E1–E5 errors for the changed skill before proceeding.
7. **eval** — add or run an eval for the skill (see docs/skills/evals/) if the change alters behavior or claims capability.
8. **review** — requesting-code-review for non-trivial changes; gate passes recorded in the task report.

A task is DONE only when tests/lint pass, red-team-qa passed, the changelog is updated, and evidence is attached (WORKFLOW.md §1).

## 2. Frontmatter standard

Frontmatter is YAML delimited by `---`. All skills carry these fields verbatim from the Global Constraints:

- `name` — kebab-case identifier matching the directory.
- `description` — a precise, behavior-first trigger. Never "MANDATORY for ALL" or auto-invoke language (E5 is a lint error).
- `version` — semver; bump on content change.
- `grade` — G1/G2/G3 (grade ladder below).
- `domain` — one of: doctrine, architecture, production, security, languages, delivery, roblox, meta.
- `status` — active / draft / superseded.
- `last-reviewed` — ISO date (e.g. 2026-08-07); update on every review.
- `supersedes` — optional; the name(s) this skill replaces.
- `owned-by-agent` — one of the 23 agents or `system`.

## 3. Grade ladder

Verbatim from the Global Constraints:

> **G2 = the floor for every skill — no exemptions.** G3 adds a `## QUANTITATIVE RULES` section.

| Grade | Meaning | Required sections |
|---|---|---|
| G1 | Transitional — draft/incomplete, never shipped alone as final | any (no hard requirement) |
| G2 | Staff minimum — every skill meets this | WHEN TO USE, WHEN NOT TO USE, DECISION TREE, FAILURE MODES & MITIGATIONS (≥5, each DETECT+FIX), VERIFICATION GATE, REFERENCES (≥3) |
| G3 | World-class — flagship skills also require | the above plus QUANTITATIVE RULES |

The exact G2/G3 section sets are lint-enforced (E4 fires when any is missing). Keep existing content and add missing sections in domain-specific, dense form; no placeholders.

## 4. Version-bump rules

- **`version` bump** — bump when content changes (mini bump for section additions, patch for google-answering fixes — semver). A change with no version bump is a lint/review failure.
- **`supersedes`** — when a new skill fully replaces an old one, list the replaced name(s) and mark the old skill `status: superseded` (or remove it, per the change). The replacing skill carries `supersedes`.

## 5. Quarterly re-review cycle

Every skill is re-reviewed at least every 90 days:

- Run `python tools/skill_lint.py --stale` to find skills whose `last-reviewed` is older than the STALE_DAYS window.
- For each flagged skill, re-verify the sections, grade, and trigger description; update `last-reviewed` to the review date; bump `version` if content changed.
- Record the re-review in the changelog.

## 6. Changelog rules

`docs/skills/CHANGELOG.md` records every catalog change. Format, one line per change:

```
YYYY-MM-DD | <change> | <skills affected, comma-separated>
```

Append (do not rewrite history); include the date, a one-line summary, and the affected skill/file path. Domino-count lines and add a new line for each independent change. The manifest and this catalog index are not edited by hand — run `python tools/skill_lint.py --regen` after a completed set of changes.

## 7. Trigger-policy rule

- Skills declare their trigger in the `description` field — precise, behavior-first, honest about when it applies.
- Never write a blanket "invoke for ALL tasks" or "MANDATORY for ALL" claim; the lint flags it as **E5**, a hard error.
- When multiple skills match, pick the most task-specific; duplicate triggers are a lint error (system-instructions v2: TRIGGER POLICY, PRECEDENCE RULES).
- Precedence: task-specific skill > family skill > system-instructions > AGENTS.md > harness defaults.

## Definition of Done

All the following are true before a change merges: no E4 (grade sections) or E5 (blanket trigger) errors for the changed skill; nothing shrank; red-team-qa passed; changelog updated; recommended evals added; manifest regenerated.