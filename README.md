# Autonomous Engineering System (v4.0.0 / beta-v2)

> Production-grade agentic operating system and skills architecture featuring dual-track parallel subagent concurrency, strict verification gates, zero-token local defense, git revert circuit breakers, and zero-slop engineering hygiene.

---

## Executive Overview

The **ZCode Autonomous Engineering System** is a disciplined, multi-agent operating configuration designed to orchestrate complex software engineering workflows at Staff+ quality. Rather than relying on monolithic, single-prompt LLM execution ("vibe coding"), ZCode enforces a layered, adversarial multi-agent hierarchy governed by a compact operating contract (`AGENTS.md`), 141 modular domain and doctrine skills, 23 deterministic playbooks, and 51 specialized autonomous subagents.

Key engineering capabilities include:
- **Disciplined Token Economics**: Slashes always-loaded per-request context by ~60% (from 32.5 KB to 12.9 KB in `AGENTS.md`), preserving context window capacity for actual code and reasoning.
- **Genuine Test-Driven Development**: Mandates capturing raw pre-fix failure artifacts (RED proof) before production code is written; prohibits single-file test runs as final verification.
- **Real-Engineer Git Circuit Breaker**: Enforces a strict revert-over-sprawl protocol (`git restore` on uncommitted edits after 2 failed repairs) to prevent patch-on-patch degradation.
- **Autonomous Knowledge Acquisition**: The `learner` meta-skill enables agents to ground themselves in unfamiliar technologies via canonical documentation and isolated verification spikes before authoring application logic.
- **Strict Pre-Ship Gating**: The `ship-gate` engine (`/ship-check`) audits every reported claim line-by-line against git diff hunks, verifies caller blast radiuses across packages, and enforces whole-workspace regression passes.

---

## Table of Contents

- [System Architecture](#system-architecture)
- [Core Operational Flows](#core-operational-flows)
  - [1. Request-to-Ship Lifecycle](#1-request-to-ship-lifecycle)
  - [2. The Real-Engineer Git Circuit Breaker](#2-the-real-engineer-git-circuit-breaker)
  - [3. Dual-Track Concurrency (Author vs. Oracle)](#3-dual-track-concurrency-author-vs-oracle)
  - [4. The Learner Protocol (Just-in-Time Knowledge Acquisition)](#4-the-learner-protocol-just-in-time-knowledge-acquisition)
- [The Six-Layer Hierarchy](#the-six-layer-hierarchy)
  - [Layer 1: Commands & User Entry Points](#layer-1-commands--user-entry-points)
  - [Layer 2: Mode Router (`ozone-mode`)](#layer-2-mode-router-ozone-mode)
  - [Layer 3: Workflow Playbooks](#layer-3-workflow-playbooks)
  - [Layer 4: Modular Skills Ecosystem (141 Skills)](#layer-4-modular-skills-ecosystem-141-skills)
  - [Layer 5: Autonomous Subagent Swarm (51 Agents)](#layer-5-autonomous-subagent-swarm-51-agents)
  - [Layer 6: Verification & Quality Assurance Gates](#layer-6-verification--quality-assurance-gates)
- [Work Tiers (T0–T3) & Cost Discipline](#work-tiers-t0t3--cost-discipline)
- [Permission Matrix](#permission-matrix)
- [Repository Structure](#repository-structure)
- [Maintenance & Validation Harness](#maintenance--validation-harness)
- [Engineering Provenance](#engineering-provenance)

---

## System Architecture

The following diagram illustrates the interaction between the primary orchestrator, policy rails, subagent pools, toolchains, and verification gates:

```text
+---------------------------------------------------------------------------------------------------+
|                                         USER INSTRUCTION                                          |
|                               (Natural Language Request or Slash Command)                         |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                LAYER 0: ROOT OPERATING CONTRACT                                   |
|                                            (AGENTS.md)                                            |
|    - Non-Negotiables: Evidence over claims, Zero test-loosening, Zero decorative emojis            |
|    - Git Revert Circuit Breaker: Max 2 repairs; revert to clean baseline before sprawling         |
|    - Pre-flight baseline: Verify `git status` & suite health before editing                      |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                LAYER 1: UNIFIED MODE ROUTER                                       |
|                                     (skills/ozone-mode)                                           |
|    - Tier Classifier: Assigns T0 (in-thread), T1 (verified), T2 (adversarial), T3 (debate)        |
|    - Playbook Selector: Matches 1 of 23 task playbooks                                            |
|    - Principle Index: Lazy-loads 1-line architectural principles on demand                        |
+-------------------+-----------------------------------------------------------+-------------------+
                    |                                                           |
                    v                                                           v
+---------------------------------------+                   +---------------------------------------+
|          WORKFLOW PLAYBOOKS           |                   |         LOCAL ZERO-TOKEN DEFENSE      |
|         (skills/ozone-mode/playbooks) |                   | - tools/repo_map.py (AST graph)       |
| - bug-fix.md (Repro -> TDD -> Fix)    |                   | - tools/lint_config.py (validation)   |
| - feature.md (Model -> Slice -> Gate) |                   | - Typecheckers: tsc --noEmit, pyright |
| - refactoring.md, perf-issue.md, etc. |                   | - Local linters: eslint, ruff, biome  |
+-------------------+-------------------+                   +-------------------+-------------------+
                    |                                                           |
                    +-----------------------------+-----------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                           LAYER 2: MODULAR SKILLS & ADAPTIVE LEARNING                             |
|                                                                                                   |
|   +------------------------------------+                 +------------------------------------+   |
|   |         CATALOG SKILLS             |                 |       LEARNER PROTOCOL             |   |
|   |   (141 verified domain skills)     |                 |   (skills/learner/SKILL.md)        |   |
|   | - test-driven-development          |                 | - Identifies unfamiliar APIs/SDKs  |   |
|   | - blast-radius, mutation-testing   |                 | - Grounds via WebFetch & .d.ts     |   |
|   | - architecture, security, roblox   |                 | - Runs isolated probe spike        |   |
|   +-----------------+------------------+                 | - Codifies just-in-time skill      |   |
|                     |                                    +-----------------+------------------+   |
+---------------------|------------------------------------------------------|----------------------+
                      |                                                      |
                      +---------------------------+--------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                           LAYER 3: PARALLEL SUBAGENT DISPATCH (Single Turn)                       |
|                                                                                                   |
|   +------------------------------------+                 +------------------------------------+   |
|   |         DEVELOPMENT TRACK          |                 |            QUALITY TRACK           |   |
|   |   (e.g., code-implementer,         |                 |   (e.g., test-oracle,              |   |
|   |    solution-architect, scripter)   |                 |    red-team-qa, comment-sicko)     |   |
|   +-----------------+------------------+                 +-----------------+------------------+   |
|                     |                                                      |                      |
|                     | [Writes code & data structures]                      | [Writes blind tests  |
|                     |                                                      |  against spec]       |
|                     v                                                      v                      |
|   +------------------------------------+                 +------------------------------------+   |
|   |       PROPOSED IMPLEMENTATION      |                 |        INDEPENDENT ORACLE SUITE    |   |
|   +-----------------+------------------+                 +-----------------+------------------+   |
+---------------------|------------------------------------------------------|----------------------+
                      |                                                      |
                      +---------------------------+--------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                           LAYER 4: PRE-SHIP VERIFICATION & GATING                                 |
|                                       (commands/ship-check)                                       |
|    - Whole-Workspace Regression: Runs full suite (single-file passes rejected as final proof)     |
|    - Claim-to-Diff Audit: Maps every summary sentence to an actual diff hunk                     |
|    - Caller Blast Radius: Enforces `rg -w` symbol search and verifies downstream safety            |
|    - Diff Hygiene: Line-by-line audit stripping debug prints, dead code, and test weakening       |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                     STRUCTURED REPORT & SHIP                                      |
|                      DONE   ·   CHANGED   ·   VERIFIED   ·   GAPS                             |
|          (Explicit user permission required before `git commit`, `git push`, or deploy)          |
+---------------------------------------------------------------------------------------------------+
```

---

## Core Operational Flows

### 1. Request-to-Ship Lifecycle

The sequential lifecycle every engineering task executes from receipt to completion:

```text
[ USER REQUEST ]
       │
       ▼
[ 1. BASELINE AUDIT ] ───► Read `git status`; run baseline tests. Confirm clean starting point.
       │
       ▼
[ 2. TIER & ROUTE ] ────► Classify T0-T3; match playbook (e.g., bug-fix.md) & domain skills.
       │
       ▼
[ 3. GROUND & SEARCH ] ─► Define types & state machines; search all callers (`rg -w <symbol>`).
       │
       ▼
[ 4. GENUINE TDD ] ─────► Write repro test; execute; capture raw failing RED output (expected vs actual).
       │
       ▼
[ 5. SURGICAL EDIT ] ───► Write smallest code diff that turns the RED test GREEN.
       │
       ▼
[ 6. REVERT GATE? ] ────► Did repair fail twice or cascade into 3+ files?
       │                    ├── YES ──► STOP. `git restore <files>`; attack premise; restart clean.
       │                    └── NO  ──► Proceed to full verification.
       ▼
[ 7. FULL REGRESSION ] ─► Run full workspace test suite + typecheck + linter (no single-file pass).
       │
       ▼
[ 8. DIFF SELF-AUDIT ] ─► Line-by-line review: strip debug logs, dead code, and unrequested diffs.
       │
       ▼
[ 9. SHIP CHECK ] ──────► Execute `/ship-check`: audit claims against hunks; prove caller invariants.
       │
       ▼
[ 10. REPORT & ASK ] ───► Print DONE/CHANGED/VERIFIED/GAPS. Request approval for commit/push.
```

---

### 2. The Real-Engineer Git Circuit Breaker

The circuit breaker stops the "patch-on-patch" death spiral where an agent turns a minor bug into
a sprawling architectural defect:

```text
       [ IMPLEMENTATION / REPAIR ATTEMPT ]
                       │
                       ▼
            [ RUN DETERMINISTIC CHECKS ]
                       │
       ┌───────────────┴───────────────┐
       ▼                               ▼
  [ CHECKS PASS ]             [ CHECKS FAIL / REGRESSION ]
       │                               │
       │                               ▼
       │                    [ EVALUATE FAILURE SCOPE ]
       │                               │
       │               ┌───────────────┴───────────────┐
       │               ▼                               ▼
       │      [ Simple local typo ]          [ Cascading Errors / 2nd Fail ]
       │               │                               │
       │               ▼                               ▼
       │      [ 1 targeted fix ]               [ TRIGGER CIRCUIT BREAKER ]
       │               │                               │
       │               └───────────────┬───────────────┘
       │                               │
       │                               ▼
       │                    [ STOP DIGGING: git restore ]
       │                    Discard uncommitted dirty diffs.
       │                               │
       │                               ▼
       │                    [ ATTACK THE PREMISE ]
       │                    Identify the false assumption.
       │                               │
       │                               ▼
       │                    [ CLEAN RE-GROUNDING ]
       │                    Restart clean from baseline.
       ▼                               │
[ PROCEED TO SHIP GATE ] ◄─────────────┘
```

---

### 3. Dual-Track Concurrency (Author vs. Oracle)

For all non-trivial tasks (T2/T3), ZCode separates the author of the logic from the author of the test
to prevent self-grading confirmation bias:

```text
                     [ TASK DISPATCH (Single Turn) ]
                                    │
            ┌───────────────────────┴───────────────────────┐
            ▼                                               ▼
 [ TRACK 1: IMPLEMENTER ]                       [ TRACK 2: TEST ORACLE ]
   Agent: code-implementer                        Agent: test-oracle
   Input: Architecture spec                       Input: Domain requirements only
          & data structures                              (Implementation hidden)
            │                                               │
            ▼                                               ▼
 [ PRODUCES: Logic & Types ]                    [ PRODUCES: Blind Test Suite ]
   - Algorithm implementation                     - Acceptance boundary tests
   - Discriminated unions                         - Malformed input tests
   - State transition machine                     - Edge-case invariant checks
            │                                               │
            └───────────────────────┬───────────────────────┘
                                    │
                                    ▼
                    [ CROSS-VALIDATION EXECUTION ]
                    Run Track 2 tests against Track 1 code.
                    Discrepancies indicate specification flaws
                    or unhandled domain edges.
```

---

### 4. The Learner Protocol (Just-in-Time Knowledge Acquisition)

When encountering unfamiliar frameworks, undocumented APIs, or novel external SDKs:

```text
[ UNKNOWN DOMAIN / UNFAMILIAR TECH ENCOUNTERED ]
                       │
                       ▼
[ 1. IDENTIFY KNOWLEDGE GAPS ] ──► Enumerate exact unknowns (types, lifecycles, error states).
                       │
                       ▼
[ 2. CANONICAL RESEARCH ] ──────► Pull official docs via `WebFetch`; read `.d.ts` & source interfaces.
                       │
                       ▼
[ 3. ISOLATED PROBE SPIKE ] ────► Execute 10-line standalone probe script in scratchpad. Verify behavior.
                       │
                       ▼
[ 4. CODIFY JIT SKILL ] ────────► Author `skills/<domain>/SKILL.md` (mental model, recipes, gotchas).
                       │
                       ▼
[ 5. GROUNDED EXECUTION ] ──────► Execute original task under `ozone-mode` with zero guesswork.
```

---

## The Six-Layer Hierarchy

### Layer 1: Commands & User Entry Points (`commands/`)
Thin entry points invoked directly by the user or harness:
- `/ozone-mode [task]`: Activates the staff engineering router, selects playbooks, and establishes tiers.
- `/ship-check`: Executes the comprehensive pre-ship claim-to-diff verification gate.
- `/tdd [task]`: Enforces strict test-first development with mandatory RED failure capture.
- `/fetch [url]`, `/search [query]`: Information gathering prioritizing native harness tools.
- `/unslop`: Strips AI fluff, conversational padding, decorative comments, and speculative abstractions.

### Layer 2: Mode Router (`skills/ozone-mode/SKILL.md`)
The single operational spine governing all sessions:
- **Non-Negotiables**: Evidence over claims, zero test loosening, smallest safe diff, plain prose.
- **Principle Catalog**: One-line indexing of 24 core architectural principles (lazy-loaded).
- **Tiers & Ceilings**: Sets concurrency caps (5 concurrent subagents per wave, hard ceiling of 8).
- **Stop Rules**: Maximum 2 repair attempts before triggering circuit-breaker rollbacks.

### Layer 3: Workflow Playbooks (`skills/ozone-mode/playbooks/`)
23 deterministic playbooks defining exact, non-skippable steps for distinct engineering situations:
- `bug-fix.md`: Minimal repro -> binary search -> RED test artifact -> fix -> full regression.
- `feature.md`: Domain modeling -> slice-by-slice TDD -> blast-radius audit -> independent review.
- `refactoring.md`: Characterization tests -> structural transformation -> zero-regression proof.
- `perf-issue.md`: Baseline trace -> single-metric hypothesis -> before/after benchmark verification.
- `autonomous-run.md`, `autopilot-full.md`: Long-running and multi-phase execution management.

### Layer 4: Modular Skills Ecosystem (141 Skills)
141 modular domain and doctrine skills categorized across 9 core domains:

| Domain | Skill Count | Primary Focus |
|---|---|---|
| **doctrine** | 48 | Engineering principles: TDD, mutation testing, anti-premise, model-the-domain. |
| **delivery** | 32 | Verification & QA: ship-gate, webapp-qa, benchmark-checklist, ketchup. |
| **production** | 14 | Deployment, release engineering, and GitHub flow management. |
| **roblox** | 14 | Roblox Studio MCP integration, Luau scripting, UI/UX, and physics. |
| **architecture** | 12 | Systems design, API contracts, blast radius analysis, monorepos. |
| **meta** | 12 | System maintenance: learner, correct, skill-creator, agent-config. |
| **security** | 4 | Threat modeling, security hardening, vulnerability audits. |
| **languages** | 4 | Deep language expertise: TypeScript, Python, JVM, Luau. |
| **fundamentals**| 1 | Foundational computer science and data structures. |

### Layer 5: Autonomous Subagent Swarm (51 Agents)
Specialized subagents tailored for specific operational roles:
- **Orchestration**: `ozone-agent`, `general-purpose`, `meta-architect`, `debate-chair`.
- **Implementation**: `code-implementer`, `refactoring-specialist`, `frontend-web-engineer`, `mobile-developer`.
- **Quality & Review**: `test-oracle`, `red-team-qa`, `comment-sicko`, `design-critic`, `security-auditor`.
- **Research & Discovery**: `deep-researcher`, `codebase-cartographer`, `algorithm-specialist`.

### Layer 6: Verification & Quality Assurance Gates
Enforced via `skills/ship-gate/SKILL.md` before any task is marked complete:
- **Head Freezing**: Bind all testing artifacts to the exact final commit head.
- **RED Evidence Ledger**: Require captured failure output for bugfixes and features.
- **Whole-Workspace Regression**: Run full package/workspace test suites (no single-file bypass).
- **Claim-to-Diff Traceability**: Every sentence in the completion report must cite a diff hunk.
- **Direct-Caller Blast Radius**: Identify all direct callers via `rg -w` and verify contracts.
- **Diff Hygiene**: Line-by-line self-audit confirming zero debug code, dead code, or test weakening.

---

## Work Tiers (T0–T3) & Cost Discipline

Cost discipline ensures compute is invested where risk resides, eliminating wasteful multi-agent overhead
on routine edits:

| Tier | When to Use | Execution Shape | Adversarial Review | Token Cost Multiplier |
|---|---|---|---|---|
| **T0 Direct** | Typos, documentation, 1-line trivial fix, factual query | In-thread, zero subagents | Self-audit | 1x baseline |
| **T1 Verified** | Standard feature or bugfix in known codebase | 1 implementer subagent, local checks | Claim-to-diff gate | ~1.5x |
| **T2 Adversarial** | Multi-file logic, unknown root cause, no oracle | Implementer + test author (parallel) | Independent reviewer (`red-team-qa`) | ~2.5x |
| **T3 Debate** | Auth, money, data migrations, PII, architectural forks | 2 independent proposers + test oracle | Critic + formal adjudication | ~5x |

### Cost Discipline Invariants
- **Zero-Token Local Defense**: Run compilers (`tsc --noEmit`), linters (`eslint`, `ruff`), and local test suites first. Never pay model tokens for syntax errors that local tooling prints instantly.
- **Lazy Loading**: Unmatched skills cost only their one-line description in memory (~30 tokens). Detailed references and playbooks are loaded strictly on demand.
- **Stop Rules**: Maximum 2 retries on a flaky gate; maximum 2 debate rounds; maximum 2 repair attempts before triggering the circuit breaker. A round yielding no new evidence halts execution.

---

## Permission Matrix

ZCode respects clear boundaries between autonomous local actions and outward-facing operations:

| Action Class | Autonomous Permission | Human Approval Required |
|---|---|---|
| Read files, AST search, grep, symbol navigation | Allowed | No |
| Run local test suites, linters, compilers, builds | Allowed | No |
| Write or edit files within task scope | Allowed | No |
| Install project-local dependencies | Allowed | No |
| Stage changes (`git add`) | Allowed | No |
| **`git commit`** | **PROHIBITED** | **MANDATORY**: Display diffstat, draft message, and wait. |
| **`git push`, PR creation, merge, release** | **PROHIBITED** | **MANDATORY**: Separate approval from commit. |
| **Deploy / publish** | **PROHIBITED** | **MANDATORY**: Explicit standalone confirmation. |
| **Destructive commands** (`rm -rf`, `reset --hard`, force push) | **PROHIBITED** | **MANDATORY**: State exactly what will be lost. |
| Secrets, credentials, global system modifications | **PROHIBITED** | **MANDATORY**: Requires explicit approval. |

---

## Repository Structure

```text
.zcode/
├── AGENTS.md                         Always-loaded operational contract (12.9 KB)
├── README.md                         Comprehensive system architecture and guide
├── commands/                         User-facing slash commands (ozone-mode, ship-check, etc.)
├── agents/                           51 specialized autonomous subagent profiles
├── skills/                           141 modular domain & doctrine skills
│   ├── INDEX.md                      Auto-generated catalog index
│   ├── ozone-mode/                   Unified engineering router
│   │   ├── playbooks/                23 deterministic task workflows
│   │   └── references/               Deep architectural principles
│   ├── ship-gate/                    Pre-ship claim and diff verification gate
│   ├── learner/                      Autonomous research & skill synthesizer
│   ├── test-driven-development/      Genuine TDD & regression methodology
│   ├── blast-radius/                 Caller search and safety invariant proof
│   └── <skill-name>/                 Domain skills with decision trees & gates
├── tools/
│   ├── lint_config.py                Catalog validator and index generator
│   ├── skill_lint.py                 Deep skill schema and grade validator
│   ├── routing_cases.json            Router regression test fixtures
│   └── repo_map.py                   Zero-token AST repository mapping utility
└── docs/
    ├── RESEARCH-2026-10-30.md        Engineering research foundation and citations
    └── skills/skills.json            Machine-readable skill catalog manifest
```

---

## Maintenance & Validation Harness

To maintain zero-defect catalog integrity, ZCode includes strict automated linters:

```bash
# Validate catalog configuration and regenerate skills/INDEX.md
python tools/lint_config.py --write-index

# Strict validation (warnings treated as build failures)
python tools/lint_config.py --strict

# Validate structural sections (Decision Tree, Gates, References) and regenerate skills.json
python tools/skill_lint.py --regen
```

### Style & Typography Doctrine
- **Zero Decorative Emojis**: Strictly prohibited in code, comments, documentation, commit messages, and PR descriptions.
- **Plain-Text Status Labels**: Use clean labels: `PASS`, `FAIL`, `DONE`, `CHANGED`, `VERIFIED`, `GAPS`, `HOLD`, `SHIP`.
- **Professional Prose**: Clear, imperative, declarative sentences without corporate AI fluff or conversational padding.

---

## Engineering Provenance

The ZCode system synthesizes verified principles from leading software and AI systems engineering:

- **pstack** (Lauren Tan, Staff Engineer at Cursor / React Core): Playbook routing, principle indexing, domain modeling, and "green is not safe" doctrine.
- **Superpowers** (Jesse Vincent): RED-first failure artifacts, verification-before-completion, and two-stage subagent review.
- **Matt Pocock**: Two-axis review protocol (Standards vs. Spec), and treating unverified review findings as hypotheses rather than blockers.
- **Birgitta Böckeler & Martin Fowler**: Harness engineering, computational feedback sensors, and mutation testing over superficial test metrics.
- **Kent Beck**: Augmented coding principles, red-first signal analysis, and early detection of agent drift (loops, unrequested code, test disabling).
- **Charity Majors**: Rigorous observability and characterization testing over correctness theatre.
- **Simon Willison**: Accountability in agentic coding; treating generated code as personal responsibility.
- **Stripe Minions**: Deterministic execution nodes, bounded retries, and strict subagent brief isolation.

Detailed citations, links, and comparative benchmarks are preserved in `docs/RESEARCH-2026-10-30.md`.
