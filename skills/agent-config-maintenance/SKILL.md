---
name: agent-config-maintenance
description: >-
  Maintains the agent and skill configuration itself: roster hygiene, routing accuracy, duplicate
  triggers, description tuning, deprecation, version bumps, and the lint/registry loop. Use when
  adding, renaming, merging, or retiring a skill or subagent, when delegation picks the wrong
  agent, or when the catalog has drifted from reality. Authoring a single skill's content routes
  to skill-creator; running skill evals to find-skills/skill-creator.
metadata:
  version: 3.0.0
  domain: meta
  grade: G3
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: meta-architect
---

# Agent Config Maintenance

The roster is a user interface for a model: names and descriptions are all it sees before choosing.
Most "the agent did the wrong thing" failures are routing failures, not intelligence failures. This
skill is how the configuration stays correct as skills and agents are added.

## WHEN TO USE

- Adding, renaming, splitting, merging, or retiring a skill or subagent.
- Delegation repeatedly chooses the wrong agent, or never chooses one it should.
- Two descriptions overlap, or a skill references a file/agent that no longer exists.
- After a model or harness change that alters routing behavior.
- Before committing any config change (lint + registry regeneration).

## WHEN NOT TO USE

- Writing the content of one new skill — `skill-creator`.
- A task that merely *uses* skills — this is about maintaining the catalog.
- Cosmetic wording changes with no behavioral effect; batch them with a real change instead.
- You are tempted to add an agent for a one-off task: use a skill or run it inline first.

## DECISION TREE

```text
1. IS THIS A NEW CAPABILITY OR A ROUTING FIX?
   New capability → does an existing skill cover 80% of it? If yes, extend that skill. Otherwise
   add one, with a boundary sentence naming what it does NOT cover.
   Routing fix → change descriptions first. Only split/merge when two skills genuinely differ
   in workflow.

2. WRITE THE DESCRIPTION AS A ROUTER
   {what it does}. Use when {triggers, including indirect phrasing}. {what routes elsewhere}.
   ≤1024 chars, third person, no blanket "use for all tasks".

3. NAME FOR THE JOB
   lowercase-kebab, matches the directory, verb-or-artifact oriented, no generic `helper`/`utils`.
   Agent names: one clear role, not a hierarchy of prefixes.

4. UPDATE THE REGISTRY, NOT JUST THE FILE
   Add to skills/INDEX.md and the AGENTS.md domain table if it belongs to a new family. A skill
   that is not in the registry is invisible in practice.

5. LINT
   python tools/lint_config.py      # frontmatter, names, duplicates, links, stale paths
   python tools/lint_config.py --write-index

6. TEST THE ROUTING
   Take 5 realistic prompts (3 should route here, 2 near-misses that should not). Check which
   skill/agent is selected. Fix descriptions until both directions are right.

7. VERSION AND RECORD
   Bump metadata.version, set last-reviewed, note the change in the skill's REFERENCES/CHANGELOG
   or the ADR if it changes the architecture of the config.
```

## PATTERNS

### 1. Description router template
```yaml
description: >-
  {Capability in third person, naming the artifact}. Use when {primary triggers}, including
  {indirect phrasings a user would actually type}. {Nearest neighbour} routes to {other skill}.
```
Why it works: the first clause gives the capability, the second gives recall (undertriggering is
the common failure), the third gives precision against the nearest lookalike.

### 2. Overlap test (do this before adding anything)
Two entries may coexist only if all three differ:
- **Artifact** — what it produces (a schema vs a contract vs a dashboard).
- **Decision** — the question it answers (is it slow? is it safe? is it shippable?).
- **Failure mode** — what goes wrong if you skip it.
If any two are identical, merge. If all three are identical, you are duplicating.

### 3. Routing eval set (keep it small and real)
```text
{ "query": "the stripe webhook fires twice and we credit twice", "expect": "payments-billing" }
{ "query": "add retry to this call and a circuit breaker",      "expect": "resilience-pattern-engineer" }
{ "query": "why is /orders slow in prod, p95 4s",               "expect": "query-performance-engineer" }
{ "query": "audit our deps before release",                     "expect": "dependency-supply-chain-guardian" }
{ "query": "write a fibonacci function",                        "expect": null }   # must not trigger
```
Five to ten cases catch most regressions. Near-misses matter more than obvious positives.

### 4. Deprecation, not deletion
`status: deprecated` + a pointer in the description ("replaced by X for new work") + keep the file
for one release. Deletion breaks references and other people's muscle memory. Deleting a skill
whose name appears in another skill's REFERENCES is a broken link, not a cleanup.

### 5. Change budget
Every addition has a carrying cost: description tokens in every prompt and one more thing to choose
between. Prefer extending an existing skill; add an agent only when the work needs a *separate
context* or a different permission/model profile.

### 6. Registry generation
`skills/INDEX.md` is generated, never hand-edited. It lists domain, grade, owner agent, and status.
If the index and the files disagree, the files win — regenerate.

## FAILURE MODES & MITIGATIONS

1. **Description collision** — two skills both claim "performance". *DETECT:* routing a question
   picks either at random. *FIX:* add an explicit boundary clause to both; test with a near-miss.
2. **Orphan skill** — exists on disk, absent from the registry/roster. *DETECT:* lint reports a skill
   not in INDEX, or an agent nobody dispatches. *FIX:* register it or deprecate it.
3. **Broken reference** — a skill cites a deleted file, agent, or skill. *DETECT:* lint link check.
   *FIX:* update or remove the reference in the same change.
4. **Roster bloat** — dozens of near-duplicate agents; the router guesses. *DETECT:* agents whose
   descriptions differ only by adjectives. *FIX:* merge, or make boundaries explicit.
5. **Stale paths** — docs point at a previous harness/config location. *DETECT:* grep for old roots.
   *FIX:* make paths relative to the project, or point at `AGENTS.md`.
6. **Silent deletion** — removing a skill other files reference. *DETECT:* broken links after the
   change. *FIX:* deprecate with a pointer; delete only after refs are gone.
7. **Untested routing change** — descriptions edited without a routing check. *DETECT:* a near-miss
   prompt now triggers the wrong skill. *FIX:* run the eval set before committing.

## QUANTITATIVE RULES

- One skill per capability; one primary agent per trigger family.
- Description ≤1024 chars; target 250–400. Always-loaded catalog should stay under ~30k chars total.
- Routing eval set: 5–10 prompts, ≥2 near-misses, re-run after every description change.
- Deprecation window: one release before deletion, with a pointer.
- Lint must pass with zero errors before a config commit.
- Adding an agent requires: a distinct context need, a distinct permission profile, or a distinct
  model tier — otherwise it is a skill.

## VERIFICATION GATE

- [ ] `python tools/lint_config.py` exits 0.
- [ ] `INDEX.md` regenerated and matches the files on disk.
- [ ] Every new/changed description has what + when + boundary, and is ≤1024 chars.
- [ ] Routing eval set run; positives and near-misses both route as intended.
- [ ] No broken references (skills/agents/files/paths) introduced.
- [ ] Version bumped, `last-reviewed` set, change noted.
- [ ] Deprecated entries point at their replacement instead of disappearing.

## REFERENCES

- `AGENTS.md` §7 (routing map), §10 (maintenance commands)
- `skill-creator` — authoring and evaluating an individual skill
- `find-skills` — discovering external skills before writing one
- `system-instructions` — delegation policy the roster feeds
- `tools/lint_config.py` — frontmatter, duplicate-trigger and link validation
