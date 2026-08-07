# Engineering Excellence Transformation — Design

- **Date:** 2026-08-06
- **Status:** Approved (user: "Make sure everything work better than currently and begin")
- **Scope:** Skills catalog + operating doctrine + future-proofing mechanics for the ZCode agentic coding system
- **Precedent:** This transformation follows the same spec → plan → implement → QA cycle used for the Roblox skill suite (`2026-07-22-roblox-skill-suite-design.md`).

## 1. Background & evidence

An audit of the skill catalog (2026-08-06) found:

| Finding | Evidence |
|---|---|
| **Capability inversion** — deepest tooling for the least demanding domain, shallowest for the most demanding | 21 Roblox skills (86–220 lines each, MCP-integrated, orchestrator with verification protocol — and a consolidation target, §5 Phase 2) vs. `systems-core-architect`, `java-jvm-expert`, `ml-python-scientist` — each **5 lines** (one paragraph). These are exactly the high-intensity domains (C++/Rust/Go, JVM, ML). |
| **Cheat-sheet ceiling** — most general skills encode memory, not judgment | `performance-profiler` (77), `resilience-pattern-engineer` (125), `refactoring-intelligence` (67), `security-hardening-specialist` (70), `api-design-architect` (64), `query-performance-engineer` (103): rules + tables + snippets + output template. No failure-mode analysis, no verification gates, no references, no decision trees. |
| **Coverage gaps** — no skill for core Staff-level domains | Distributed systems design, concurrency/parallelism, production incident response, system design/capacity estimation, database-at-scale (sharding/migrations), observability/SLOs, threat modeling, general (non-Roblox) orchestration. |
| **Conflicts** | `system-instructions` claims "MANDATORY AUTO-INVOKE for ALL tasks" while ~35 skills each claim "MANDATORY AUTO-INVOKE"; `system-instructions` (main thread CANNOT read files / must not) contradicts `AGENTS.md` orchestration guidance; two copies of `system-instructions` can drift. |
| **Duplication** | 35 skills exist identically in both `C:\Users\Oz\.zcode\skills\` and `C:\Users\Oz\.agents\skills\` (maintenance hazard — updates must be applied twice). |
| **Dead weight** | 7 empty directories in `.zcode/skills` (banner-design, brand, design, design-system, slides, ui-styling, ui-ux-pro-max) and 4 empty directories in `.agents/skills` (systems-core-architect, java-jvm-expert, ml-python-scientist, readme-architect). |
| **No versioning / no evals / no manifest** | No `version`, `grade`, `last-reviewed`, `supersedes` metadata anywhere; no catalog manifest; no way to measure skill quality or trigger accuracy. |

## 2. Goals

1. **Capability:** every skill meets a Staff-grade content bar; flagship high-intensity domains reach World-class depth (quantitative rigor + evals + orchestration).
2. **Conflict elimination (permanent):** single canonical store, precedence rules, no duplicate triggers, consistent doctrine, dead weight removed.
3. **Future-proofing:** versioning metadata, catalog manifest, lint gate, eval harness, documented upgrade process, agent↔skill alignment.
4. **Consolidation:** collapse the 21-skill Roblox suite into a single capability-focused `roblox-lua-developer` skill (Luau + platform model + compressed domain workflows) instead of 21 micro-workflows.
5. **Agent expansion:** add 3 subagent types — `planner` (deep planning), `solution-architect` (system design/ADRs), `ml-engineer` (ML work) — with matching skills; also restore the 3 agent definitions missing from `agents/*.md` (cybersecurity-specialist, game-developer, mobile-developer — owners of 24 skills) in Phase 1; agent definition files grow 17 → 23, AGENTS.md registry 20 → 23.
6. **Strict "better than currently" guarantee:** no capability is lost during consolidation; every touched skill gains content, none shrink; existing triggers keep working (smoke-tested per phase).
7. **Workflow discipline (anti-vibe-coding):** replace generate-first/verify-later patterns with world-class engineering process — TDD-first, verification-before-completion (proof, not assertion), Definition of Done, review gates, measurement discipline, systematic debugging — enforced by doctrine (§4.6) and every skill's verification gate.
8. **Token efficiency & smart routing:** the system must not increase token consumption or degrade output quality — trivial doc edits are applied inline by the orchestrator, substantive work routes through subagents; no skill carries blanket-invoke language; every skill routes by precise trigger + domain + owner.
9. **Universal coverage:** the final catalog provably covers every project type — cyber/security, generic coding, advanced systems, world-class problem solving, delivery, Roblox, ML — each mapped to ≥1 skill and ≥1 owning agent (verified in Phase 4).

## 3. Non-goals

- Rewriting game/MCP server internals or the 21 Roblox skills' platform content *as separate skills* — the suite is **consolidated into one skill** (see §5, Phase 2), and the `roblox-orchestrator` protocol is generalized into `general-orchestrator` (Phase 3).
- Touching `v2/`, nested `.zcode/`, or other app runtime state.
- Changing the harness's built-in subagent types or their tool permissions (new agents are added only via `agents/*.md` config files — 3 added in Phase 3).
- Renaming skill directories (taxonomy lives in the manifest, not the filesystem — avoids churn).
- Building a web UI or dashboard.

## 4. Target architecture

### 4.1 Grade ladder (the quality bar)

| Grade | Name | Content contract |
|---|---|---|
| G1 | Baseline | Rules + snippets + output template (current state) |
| G2 | **Staff (minimum for every skill)** | + decision tree, trade-off tables, **failure modes & mitigations**, **verification gate**, references |
| G3 | **World-class (flagship skills)** | + quantitative rules of thumb (numbers, not vibes), cross-domain orchestration guidance, eval-backed, benchmark templates |

**Rule: every skill ships at G2 or above — no family exemptions.** G1 exists only as a transitional label during Phase 0. The Roblox suite is consolidated into a single G2 skill (`roblox-lua-developer`, Phase 2).

### 4.2 Standard skill skeleton (content contract)

Every skill file follows this structure:

1. Frontmatter: `name`, `version` (semver), `grade` (G2/G3), `domain` (taxonomy family), `status` (active/draft/superseded), `last-reviewed` (ISO date), `supersedes` (optional), `owned-by-agent` (one of the 23 agents, or `system`).
2. **When to use** — precise trigger conditions.
3. **When NOT to use** — trigger discipline (kills the "MANDATORY for ALL" pattern).
4. **Decision tree** — branch on the situation, not just a list of rules.
5. **Patterns with trade-offs** — when each applies, and the cost of choosing wrong.
6. **Failure modes & mitigations** — what can go wrong, how to detect it, how to fix it.
7. **Quantitative rules of thumb** (G3) — e.g., P99 > 4× P50 ⇒ queueing; retry budget math.
8. **Verification gate** — how to prove the work is correct: tests, benchmarks, review checklist.
9. **References** — authoritative standards, docs, papers.

### 4.3 Taxonomy families (in manifest, not directories)

| Family | Skills |
|---|---|
| `doctrine` | system-instructions (v2), deep-planner (new G3), AGENTS.md (alignment only) |
| `architecture` | system-design-architect (new G3), distributed-systems-engineer (new G3), concurrency-engineer (new G3), database-at-scale (new G3), observability-sre (new G3), resilience-pattern-engineer (G2 deepen), api-design-architect (G2 deepen) |
| `production` | incident-response-engineer (new G3), performance-profiler (G2 deepen), query-performance-engineer (G2 deepen), devops-pipeline-engineer, container-optimizer, monorepo-workspace-architect, github-flow-master, dependency-supply-chain-guardian |
| `security` | cybersecurity-specialist, security-hardening-specialist (G2 deepen + threat modeling) |
| `languages` | systems-core-architect (rebuild → G3), java-jvm-expert (rebuild → G2), ml-python-scientist (rebuild → G2) |
| `delivery` | game-developer, mobile-developer, animation-web-builder, readme-architect, general-orchestrator (new G3) |
| `roblox` | roblox-lua-developer (consolidated from the 21-skill suite, G2 — Task 2.0) |
| `meta` | skill-creator, find-skills, mcp-builder, skill-lint (new tool) |

### 4.4 Conflict elimination design

- **Canonical store:** `C:\Users\Oz\.zcode\skills\` is the single source of truth. Unique `.agents/skills` skills (`find-skills`, `skill-creator`, `mcp-builder`) move into it; duplicated copies are deleted from `.agents/skills`; all 11 empty directories are removed. Every duplicated pair is diff-verified before deletion (drift logged, newest content wins).
- **Precedence rules** (written into doctrine):
  1. Task-specific skill > family skill.
  2. Any skill > system-instructions.
  3. system-instructions v2 > AGENTS.md.
  4. AGENTS.md > harness defaults.
  5. Duplicate triggers are a lint error — never two active skills for the same trigger.
- **Doctrine split:** `AGENTS.md` = principles (stable, short). `system-instructions` v2 = executable workflow (delegation protocol, confidence gates, waiting protocol, verification gates, trigger policy). v2 removes "MANDATORY AUTO-INVOKE for ALL tasks" and aligns with AGENTS.md.
- **Agent↔skill mapping:** every skill declares `owned-by-agent`; the registry in AGENTS.md is updated to match the taxonomy.
- **Agent expansion:** Phase 1 restores the 3 agent definitions missing from `C:/Users/Oz/.zcode/agents/*.md` (cybersecurity-specialist, game-developer, mobile-developer — declared in AGENTS.md's registry but absent as files, owners of 24 skills); Phase 3 adds 3 new subagent types (`planner`, `solution-architect`, `ml-engineer`); agent definition files grow 17 → 23 and the AGENTS.md registry 20 → 23. `ml-engineer` also fixes the invalid owner currently assigned to `ml-python-scientist` (no such agent exists today).

### 4.5 Future-proofing mechanics

- **Manifest:** `docs/skills/SKILLS.md` (human index) + `docs/skills/skills.json` (machine-readable, generated by skill-lint): name, version, grade, domain, status, owner, last-reviewed.
- **skill-lint** (`tools/skill_lint.py`, Python 3, stdlib only): validates frontmatter completeness, duplicate names/triggers, empty dirs, dangling references, G2+ sections present (FAILURE MODES, VERIFICATION), stale `last-reviewed` (>90 days → warning). Exit code 0 = gate passed.
- **Evals:** per-skill trigger-accuracy prompts and flagship quality evals, built with the `skill-creator` evals methodology; run after each phase; results recorded in `docs/skills/evals/`.
- **Upgrade process** (documented in `docs/skills/CONTRIBUTING.md`): spec → plan → subagent implementation → red-team-qa → lint + eval → review.
- **Optional (user decision):** git init in `.zcode` for version history and PR-style review of skill changes.

### 4.6 Workflow discipline (anti-vibe-coding layer)

The system stops being a code generator and becomes an engineering agentic system. Enforced by doctrine (Phase 1) and by every skill's verification gate:

- **TDD-first:** all code-producing work writes a failing test before implementation (superpowers:test-driven-development); verification gates must be executable, not asserted.
- **Verification-before-completion:** no deliverable is "done" on assertion — tests pass, benchmarks measured, evidence attached (superpowers:verification-before-completion).
- **Definition of Done:** every task states its DoD before work starts; a task is done only when every DoD item is evidenced.
- **Gate-driven execution:** orchestration stops at every failed gate and re-verifies after the fix — replaces "no-stop" and "looks done" patterns (general-orchestrator, Phase 3).
- **Measurement discipline:** performance/optimization claims require before/after benchmarks with a pinned environment (≥5 runs, median + p90).
- **Systematic debugging:** bug work follows root-cause methodology (superpowers:systematic-debugging), never symptom patches.
- **Review gates:** red-team-qa at every phase gate; requesting-code-review for non-trivial changes.
- **Plan-before-code:** non-trivial tasks get a plan (deep-planner / superpowers:writing-plans) before implementation.

## 5. Execution phases

Each phase ends with a verification gate; each phase's work is dispatched through subagents per AGENTS.md (code-implementer/refactoring-specialist for content, deep-researcher for references, red-team-qa for QA, documentation-engineer for docs).

### Phase 0 — Hygiene & baseline (fast, low risk)
1. Final inventory; diff-verify all 35 duplicated pairs.
2. Move 3 unique `.agents` skills into `.zcode/skills`; delete duplicate copies; delete 11 empty dirs.
3. Add complete frontmatter (version 0.1.0, grade, domain, status, last-reviewed, owned-by-agent, supersedes) to all ~40 skills.
4. Write `tools/skill_lint.py` v1 + manifest skeleton (`SKILLS.md`, `skills.json`).
5. **Gate:** lint exits 0; zero duplicates; zero empty dirs; catalog still loads (smoke test: skill list unchanged in count minus removals).

### Phase 1 — Governance & doctrine
1. Rewrite `system-instructions` v2 (operational doctrine; trigger policy; precedence rules; delegation/confidence/waiting/verification protocols; **WORKFLOW STANDARDS** — TDD-first, verification-before-completion, Definition of Done, measurement, systematic debugging; references superpowers workflow skills).
2. Align `AGENTS.md` (registry matches taxonomy; contradictions removed; pipeline references the workflow standard).
3. Update agent↔skill mapping; fix any `agents/*.md` gaps.
4. Create `docs/skills/WORKFLOW.md` — the delivery-discipline doc: Definition of Done checklist, TDD protocol, verification rules, anti-vibe-coding anti-patterns.
5. **Gate:** red-team-qa review finds no contradictions; no skill claims "MANDATORY for ALL tasks"; workflow standard present in doctrine + WORKFLOW.md.

### Phase 2 — Staff-grade content (G2)
0. **Consolidate the Roblox suite (21 → 1):** synthesize all 21 skills into `skills/roblox-lua-developer/SKILL.md` — Luau language guidance, platform model (DataModel, services, replication), compressed per-domain workflow tables (UI, networking, persistence, economy, security, performance, VFX/animation, audio, terrain, testing, plugins, asset pipeline), MCP verification protocol; `supersedes` records the 21; the 21 directories are deleted; the lint roblox exemption is removed (no family exemptions remain).
1. Rebuild `systems-core-architect` → **G3** (per-language memory & concurrency models, unsafe review checklist, build systems, profiling workflow, failure modes, verification gate).
2. Rebuild `java-jvm-expert` → G2 (GC tuning methodology, JFR/async-profiler, heap analysis, threading, failure modes).
3. Rebuild `ml-python-scientist` → G2 (vectorization decision tree, training-pipeline correctness, GPU memory, reproducibility, failure modes).
4. Deepen to G2: `performance-profiler`, `resilience-pattern-engineer`, `security-hardening-specialist` (+ threat modeling), `refactoring-intelligence`, `api-design-architect`, `query-performance-engineer` (each gains decision tree, failure modes, verification gate, references).
5. **Gate:** lint passes (G2 sections present); red-team-qa per skill; nothing shrinks.

### Phase 3 — World-class flagships (G3)
Create 8 new G3 skills (7 flagships + `deep-planner`) and 3 new subagents (`planner`, `solution-architect`, `ml-engineer` in `C:/Users/Oz/.zcode/agents/`): `distributed-systems-engineer`, `incident-response-engineer`, `system-design-architect`, `concurrency-engineer`, `database-at-scale`, `observability-sre`, `general-orchestrator` (generalizes the Roblox orchestrator's verification protocol into a **gate-driven execution model** — proof-based gates per subtask, stop-and-fix on failure, per §4.6), and `deep-planner` (planning methodology — decomposition, dependency graphs, estimation, risk registers; consumes `deep-researcher` output and produces plans for `general-orchestrator`).
**Gate:** every flagship has evals + benchmark templates; red-team-qa per skill and per new agent definition; lint passes.

### Phase 4 — Future-proofing & final verification
1. skill-lint v2 (CI-ready flags, stale-review warnings).
2. `docs/skills/CONTRIBUTING.md` upgrade-process doc.
3. Optional git init (user decision).
4. **G2 sweep:** any remaining skills below G2 receive the G2 content sections (failure modes, verification gate, references) — lightweight pass.
5. Full-catalog red-team-qa pass + lint + manifest regeneration + eval summary.
6. **Gate:** all success criteria (below) verified, measured, and reported.

## 6. Success criteria (measurable)

- [ ] 0 empty skill dirs; 0 duplicated skills; 0 "MANDATORY for ALL" descriptions.
- [ ] 100% of skills have complete frontmatter (name, version, grade, domain, status, last-reviewed, owned-by-agent).
- [ ] 100% of skills are G2+ with decision tree, failure modes & mitigations, verification gate, references (lint-enforced, no exemptions).
- [ ] 14 G3 skills exist (13 new + systems-core-architect) with evals; 23 agent definition files, every skill owner resolves.
- [ ] `tools/skill_lint.py` exits 0 on the catalog; manifest regenerated and current.
- [ ] Precedence rules documented in doctrine; no contradictions between system-instructions v2 and AGENTS.md (red-team-qa verified).
- [ ] Workflow discipline enforced: system-instructions v2 has WORKFLOW STANDARDS; `docs/skills/WORKFLOW.md` exists; no verification gate is assertion-only (red-team-qa reviewed).
- [ ] Roblox consolidated: 21 skills superseded by `roblox-lua-developer` (manifest + changelog record it); triggers route to the single skill (smoke-tested after Phase 2).
- [ ] Every touched skill gained content; none shrank.

## 7. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Phase 0/1 restructuring collides with Phase 2/3 content work | Strict phasing; Phase 0 completes and gates before any content rewrite |
| Consolidation accidentally loses capability | Diff-verify every pair before deletion; smoke-test triggers per phase; success criterion "nothing shrinks" |
| Scope creep in skill content | YAGNI: each skill gets exactly what its grade requires; grade is the contract |
| Duplicate trigger regressions | Lint enforces uniqueness; `supersedes` field records history |
| Evals too heavy to maintain | Evals only for flagships + trigger-accuracy for all; quarterly re-review cycle with lint staleness warnings |
| Roblox consolidation loses platform-specific depth | Compressed per-domain workflow tables synthesized from all 21 sources; supersession recorded; MCP verification protocol preserved in the consolidated skill |
