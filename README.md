# ZCode — An Agentic Engineering System

A configuration layer for AI coding agents that turns "plausible-looking output" into
"verified work". It is built for one developer paying per token, so every mechanism here has
to earn its cost twice: once in quality, once in tokens not spent.

The system is four layers deep and each layer is loaded only when needed:

```text
command  (/ozone-mode, /ship-check, /tdd, ...)   you type this
   ↓
mode     (skills/ozone-mode)                     the router: principles, playbook match
   ↓
playbook (skills/ozone-mode/references)          the steps for this class of task
   ↓
skill    (skills/<name>)                         the doctrine for one narrow problem
   ↓
subagent (agents/<name>)                         scoped worker with a written brief
   ↓
gate     (ship-gate + verification skills)       proof before "done"
```

Nothing above is loaded speculatively. `AGENTS.md` is the only file every request pays for.

---

## Contents

- [Why this exists](#why-this-exists)
- [The request lifecycle](#the-request-lifecycle)
- [Layer 1: commands](#layer-1-commands)
- [Layer 2: the mode router](#layer-2-the-mode-router)
- [Layer 3: playbooks](#layer-3-playbooks)
- [Layer 4: skills](#layer-4-skills)
- [Layer 5: subagents](#layer-5-subagents)
- [Layer 6: gates](#layer-6-gates)
- [Token economy](#token-economy)
- [Repository map](#repository-map)
- [Extending the system](#extending-the-system)
- [Provenance](#provenance)
- [Limits](#limits)

---

## Why this exists

Agents fail in a small number of repeatable ways, and each one has a structural fix:

| Failure | Symptom you see | Mechanism that stops it |
|---|---|---|
| Unverified "done" | "Fixed it" with no artifact | `verification-before-completion`, `ship-gate` |
| Wrong-reason green | Test passes because the test is wrong | RED-first proof, `mutation-testing`, independent oracle |
| Scope drift | Extra features, drive-by refactors | `principle-laziness-protocol`, claim-to-diff audit |
| Premise error | Three fixes, same wrong assumption | `principle-attack-the-premise` |
| Review theatre | Same context reviews itself | Separation of duties, fresh-context reviewer |
| Context decay | Quality drops late in long sessions | Tiering, subagent isolation, `handoff` |
| Repeated correction | You point out the same bug again | `correct`: encode the rule as a sensor |

The system's thesis is the same one behind Lauren Tan's pstack: throughput without quality is
not a goal. Write less, verify more, and only parallelize what you can independently check.

---

## The request lifecycle

```text
 1. CLASSIFY   size (T0–T3) and direction (read-only vs write)
 2. ROUTE      /ozone-mode matches one playbook and copies its steps into the todo list
 3. GROUND     data shape named, acceptance criterion quoted, callers found
 4. ACT        smallest diff that meets the criterion
 5. PROVE      zero-token checks (typecheck, lint, tests) then independent verification
 6. GATE       /ship-check: claim-to-diff audit, blast radius, evidence ledger
 7. REPORT     DONE / CHANGED / VERIFIED / GAPS
```

Two rules make the lifecycle real:

- Every skipped step stays visible as `skip: <reason>`.
- Step 5 happens after the last edit. Evidence from before the final change does not count.

### Worked example

Request: "the Stripe webhook fires twice and we double-credit the customer."

```text
CLASSIFY  T2. Wrong behavior, money, unknown mechanism, no oracle yet.
ROUTE     Bug fix playbook. Steps: reproduce, root-cause, regression test, fix, verify.
GROUND    Acceptance criterion: "replaying the same event id credits once."
          Data shape: (event_id, account_id, amount, applied_at) with a uniqueness constraint.
ACT       Add idempotency key + unique index; no retry logic change, no new abstraction.
PROVE     Repro fails before, passes after. Full suite green. Typecheck clean.
GATE      Independent reviewer re-runs the repro. Diff touches 3 files, all traceable to the
          criterion. Blast radius: other webhook handlers share the retry path, checked.
REPORT    DONE / CHANGED / VERIFIED (command + output) / GAPS (no staging replay).
```

The value is not the ceremony. It is that each step produces something a reviewer can re-run.

---

## Layer 1: commands

Commands are the human interface. They live in `commands/*.md` and expand into a full
instruction set with `$ARGUMENTS` substituted.

| Command | Purpose |
|---|---|
| `/ozone-mode <task>` | **Primary entry point.** Router: principles, playbook, tiers, gates. |
| `/ship-check` | Pre-ship gate. Runs deterministic checks, audits claims against the diff, states blast radius. |
| `/tdd` | Red-green cycle for one behavior, with RED evidence captured. |
| `/verify` | Prove a specific claim with the cheapest real check. |
| `/review` | Package a change and dispatch an independent reviewer. |
| `/ux-review` | Interface quality pass: states, keyboard, hierarchy, copy. |
| `/unslop` | Strip AI tells from prose, comments, and replies. |
| `/map` | Map a codebase before touching it. |
| `/architect` | Settle shape and callers before writing code. |
| `/algorithms` | Complexity, invariants, and a proof plan for hot paths. |
| `/blast-radius` | What a small diff could break outside itself. |
| `/parallel-dev` | Explicit fan-out with capped waves. |
| `/product` | Problem framing and scope cutting. |
| `/fetch`, `/search` | Read the web or search it, with citations. |
| `/handoff` | Compress state so a fresh session can resume. |

Commands are thin. They exist to set the mode and the argument, not to duplicate skill bodies.

---

## Layer 2: the mode router

`skills/ozone-mode/SKILL.md` is the spine. It does five things:

1. **States the non-negotiables** the rest of the run inherits: evidence over claims, no weakened
   checks, smallest diff, independent verification, plain prose.
2. **Indexes the principles** as one line each, with the trigger that makes each one apply. The
   agent reads the leaf skill only for principles the task actually touches.
3. **Matches a playbook** and copies its steps into the todo list verbatim.
4. **Sets the tier**, which decides how many subagents and how much adversarial review.
5. **Defines the reply**: short declarative sentences, measured/inferred/guess labels, no
   fabricated links, no emojis.

The mode is sticky for the task. It is not a persona and it does not add a second opinion; it
routes to the cheapest mechanism that can produce proof.

`skills/ozone-mode/playbooks/` holds one file per playbook. Only the matched file is read, so
the other twenty-two cost nothing.

---

## Layer 3: playbooks

A playbook is the step list for one class of task. Twenty-three are defined, and `figure-it-out`
covers the ones that do not fit by designing a bespoke, auditable sequence. The ones you will
reach for most:

| Playbook | Ends when |
|---|---|
| Investigation | A cited answer exists; no code changed |
| Bug fix | Repro failed before, passes after, regression test kept |
| Feature | Behavior meets a named criterion, with tests and types |
| Refactor | Behavior pinned by tests, structure changed, suite green throughout |
| Performance | Before/after table on a pinned environment, bottleneck named |
| Prototype | A decision is settled by observation, throwaway code deleted |
| Visual parity | Screenshots match at named breakpoints, diff explained |
| Test hardening | Tests provably fail when the behavior is broken |
| Security review | Attack cases run and rejected, with the control that rejects them |
| Session pickup | State, decisions, and next step reconstructed from artifacts |
| Multi-phase plan | Phases sequenced, each ending in a check |
| Ship | Independent verdict on the exact head, blast radius stated |

Playbooks are deliberately short. If a playbook needs a page of prose per step, the step is
probably a skill.

---

## Layer 4: skills

130+ skills across nine domains, each a directory with a `SKILL.md`:

```text
skills/<name>/SKILL.md          frontmatter + doctrine (the only file loaded on match)
skills/<name>/references/*.md   deeper material, loaded only when a step asks for it
```

**Domains.** `doctrine` (how to think and verify), `architecture` (shape, data, scale),
`delivery` (frontend, mobile, desktop, QA, docs), `production` (CI, observability, integration),
`security`, `languages`, `roblox`, `meta` (config maintenance), `fundamentals`.

**Grades.** G1 is a narrow technique. G2 requires the full section set: when to use, when not to
use, decision tree, failure modes, verification gate, references. G3 adds quantitative rules and
is reserved for doctrine that changes outcomes.

**The description is the routing surface.** It is the only part loaded before a match, so it
must say what the skill does, when to use it, and what routes elsewhere. The catalog in
`skills/INDEX.md` is generated from those descriptions; edit the skill, not the index.

Why so many skills do not blow the budget: an unmatched skill costs one description line. A
matched skill costs its body once. Long material goes in `references/` and is read on demand.

Two rules keep the catalog honest:

- No two skills may share a trigger. Duplicate descriptions are a lint error.
- A skill that overlaps a newer one points at the replacement instead of quietly competing.

---

## Layer 5: subagents

`agents/*.md` are scoped workers: a description, permissions, a step budget, and a body of
standing orders. They are grouped by function rather than listed individually here.

| Group | Examples | Used for |
|---|---|---|
| Orchestration and quality | `planner`, `red-team-qa`, `requirement-auditor`, `debate-chair`, `test-oracle` | Decomposition, adversarial review, independent verdicts |
| Research and analysis | `deep-researcher`, `solution-architect`, `db-architect`, `performance-engineer` | Grounding before design |
| Implementation | `code-implementer`, `refactoring-specialist`, `test-engineer`, `ui-ux-architect` | Writing code and tests |
| Domain | `roblox-*`, `mobile-developer`, `desktop-developer`, `llm-engineer` | Specialized execution |
| Production and security | `security-auditor`, `devops-engineer`, `dependency-guardian` | Hardening and delivery |

### The brief

Every dispatch carries six fields: goal, scope with non-goals, context as file pointers,
constraints, the evidence format wanted, and an explicit no-fanout line.

### The rules

- **Capability without a brief is cost without output.** A vague brief returns a vague report,
  and you pay for the tokens twice when you re-dispatch.
- **Reviewers never edit.** `edit: deny` agents exist so a verdict cannot be quietly repaired
  into a pass.
- **The author never certifies.** "The builder said the tests passed" is not evidence.
- **Fresh context per unit.** Resumed subagents silently drop directives added mid-run.
- **You own the result.** Read the diff, write the summary.
- **Recursion guard.** Without a no-fanout line a subagent can re-enter the router and spawn
  its own children. That is how a small task becomes a fifty-agent bill.

---

## Layer 6: gates

Quality is enforced by mechanisms, in this order of cost:

1. **Zero-token, deterministic.** Typecheck, lint, unit tests, schema validation, link checks.
   These catch most defects for no model cost. Run them before asking any model to look.
2. **Structural.** Small diff, one concern, no new abstraction with one caller, no boolean-flag
   proliferation, no dead code left behind.
3. **Independent verification.** A fresh-context agent re-runs the check on the exact head.
4. **Adversarial review.** `red-team-qa` or `/interrogate` tries to break the change; findings
   need a reproduction to count.
5. **Ship gate.** `/ship-check` audits every claim in the summary against the diff, states the
   blast radius, and lists what was not verified.

`/ship-check` is the answer to "why do I keep finding bugs after it ships": it is the step that
refuses to report done while a claim lacks an artifact.

Two failure modes it is built to catch:

- **Claim drift.** The summary says "adds tenant isolation" but the diff only filters by user id.
- **Stale green.** Tests passed before the last edit, or the test was weakened to pass.

---

## Token economy

The design assumption is one developer with a real bill.

| Mechanism | Effect |
|---|---|
| `AGENTS.md` kept to ~10KB | Saves roughly 5k tokens on every single request |
| Unmatched skills cost one description | 130 skills without a 130-body tax |
| `references/` loaded on demand | Long doctrine never rides along by default |
| Tiering T0–T3 | Trivial work pays no subagent tax |
| Local checks first | A stack trace costs zero model tokens |
| Wave cap of 5 | Prevents the fan-out bill that follows a recursion bug |
| Fresh subagent with a consolidated brief | Avoids paying twice for a dropped directive |

What this deliberately does not do: run a swarm on every task, keep a permanent review panel,
or re-read the whole repo per request. Multi-agent fan-out is roughly an order of magnitude more
expensive than a single thread; it is reserved for work that genuinely partitions.

---

## Repository map

```text
AGENTS.md                     always-loaded rules: permissions, tiers, DoD
README.md                     this document
commands/                     slash commands, the human interface
agents/                       subagent definitions (frontmatter + standing orders)
skills/                       the catalog
  INDEX.md                    generated: every skill, grade, owner, trigger
  ozone-mode/                 the router
    playbooks/                one file per task class
  <name>/SKILL.md             one skill
  <name>/references/          lazy-loaded depth
tools/
  lint_config.py              validates skills + agents, regenerates INDEX.md
  skill_lint.py               second validator, grade sections, staleness
  routing_cases.json          routing regression fixtures
  repo_map.py                 AST symbol map for orientation
docs/                         research notes, skill manifests
```

---

## Extending the system

**Add a skill.** Create `skills/<name>/SKILL.md` with frontmatter (`name`, `description`,
`metadata` carrying `version`, `domain`, `grade`, `status`, `last-reviewed`, `owned-by-agent`).
Write a description that states what it does, when to use it, and what routes elsewhere. Include
the sections your grade requires. Then run both linters and regenerate the index.

**Add an agent.** Create `agents/<name>.md` with `name`, a description carrying a "Use when"
clause, `mode: subagent`, a `permission` block, and `steps` between 5 and 200. Set `edit: deny`
for anything whose job is judgment.

**Add a command.** Create `commands/<name>.md` with a description and argument hint, then keep
the body thin: set the mode, pass `$ARGUMENTS`, point at the skill that owns the method.

**Retire a skill.** Point its description at the replacement, keep the directory until no
references remain, then delete. Do not leave two skills claiming one trigger.

```bash
python tools/lint_config.py --write-index
python tools/skill_lint.py --regen
```

---

## Provenance

The workflow is a synthesis, not a copy. Primary sources:

- **pstack** (Lauren Tan, `cursor/plugins`, v0.15.36): playbook routing, principle index,
  prove-it-works, guard-the-context-window, never-block-on-the-human, "green is not safe".
- **Superpowers** (Jesse Vincent): RED-first discipline, verification-before-completion,
  two-stage subagent review.
- **Matt Pocock's skills**: two-axis review (standards versus spec), and the warning that
  review findings are hypotheses until reproduced.
- **Birgitta Böckeler / martinfowler.com**: the harness model. Feedforward guides plus feedback
  sensors; computational checks before inferential ones. Also the honest finding that mandating
  TDD inside the agent loop shows no measurable quality gain, while mutation testing does measure
  whether tests can fail.
- **Kent Beck**: augmented coding, and the three tells of an agent off track: loops, unrequested
  functionality, tests disabled or deleted.
- **Charity Majors**: nondeterministic systems require more discipline, not less; characterization
  tests and observability over correctness theatre.
- **Simon Willison**: vibe engineering means staying accountable for the software you ship.
- **Stripe minions**: bounded retries, deterministic nodes for mechanical steps, isolation instead
  of permission prompts.

Details and URLs: `docs/RESEARCH-2026-10-30.md`.

---

## Limits

- **Correctness is not a sensor.** If the requirement was never stated, no gate can catch the
  gap. `requirements-elicitation` exists for that, and it is the cheapest skill in the catalog.
- **AI review finds hypotheses.** A finding without a reproduction is a note, not a blocker.
- **Behaviour verification is unsolved.** Browser and E2E gates catch what they are pointed at,
  not what nobody thought to check. Say what was not verified.
- **Tiers are judgment.** The tier decides cost; picking T2 for a typo wastes money, picking T0
  for a migration risks data. When unsure, size up one tier and say why.
