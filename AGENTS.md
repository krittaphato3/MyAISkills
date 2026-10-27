# AGENTS.md — Operating Principles for zcode

This is the short principles file for the primary thread. It is read first, kept short on
purpose, and is the authority for **who does what, what needs permission, and how work is
declared done**. Operational depth lives in `skills/`; the machine-readable catalog lives in
`skills/INDEX.md`; per-agent briefs live in `agents/`.

If a skill contradicts this file, the skill wins for its own narrow task (precedence below).
If this file contradicts the user's explicit instruction, the user wins, always.

---

## 0. MANDATORY FIRST ACTIONS (SKILL & SUBAGENT CALLING REQUIRED)

Before taking any action (editing files, reading large codebases, writing implementations, or running bash commands) on any user task, the primary thread **MUST** execute these mandatory first actions:

1. **Invoke the `Skill` tool**: Identify the relevant domain, doctrine, and safety skills matching the task's verb, artifact, and work type (see §7 and §7.1), and call the `Skill` tool immediately. Bypassing skill invocation or executing without loading mandatory skills is a critical protocol violation.
2. **Dispatch subagents via the `Agent` tool**: The primary thread is an **orchestrator and coordinator**, not a direct implementer. All non-trivial implementation, investigation, testing, and review **MUST** be delegated to specialized subagents dispatched via the `Agent` tool (see §5.1 and §6). Taking over implementation in the primary thread with direct `Read`/`Edit` calls instead of delegating to subagents is strictly prohibited unless the user explicitly requested in-thread execution or the task is purely trivial (e.g. a 1-word doc typo or single-sentence answer).
3. **Parallel Multi-Subagent Dispatch**: When independent subtasks exist (e.g., development logic + test authoring, multiple subsystem modules, independent solution proposals for debate, or multi-domain components), the primary thread **MUST divide the work and dispatch multiple subagents concurrently in a single message with multiple `Agent` tool calls** so they execute in parallel, rather than serializing them one at a time. Serializing independent subagents one by one is strictly prohibited.

---

## 1. PRECEDENCE

When instructions conflict, highest wins:

1. **The user's current instruction** (including "stop", "explain only", "don't touch X").
2. **Task-specific skill** — the skill whose trigger matches the work exactly.
3. **Family skill** — a broader skill covering the domain.
4. **This file** — roster, permissions, gates, reporting.
5. **System instructions** (`skills/system-instructions`) — orchestration protocol.
6. **Harness defaults.**

Two skills claiming the same trigger is a lint error. Pick the more specific one and fix the
catalog later; do not silently invoke both.

---

## 2. NON-NEGOTIABLES

1. **Never bypass skills, subagent delegation, or parallel dispatch.** Calling the `Skill` tool is mandatory for matching domains and safety rails (§7.1), and dispatching subagents via the `Agent` tool is mandatory for all non-trivial implementation, investigation, and verification (§5.1). The primary thread must never bypass subagents to perform implementation directly with `Read`/`Edit`. When independent subtasks exist, subagents must be dispatched concurrently in parallel within a single message rather than serialized sequentially. Bypassing skills, subagents, or parallel dispatch where applicable is a direct protocol violation.
2. **Ask before anything hard to undo.** Commit, push, PR, merge, tag, release, deploy,
   publish, delete branches/files, rewrite history, `reset --hard`, force-push. A coding
   request is *not* permission to ship. Full matrix in §3.
3. **No claim without evidence.** "Done", "fixed", "faster", "secure" each need an artifact:
   test output, lint/typecheck log, benchmark table, reproduction, or diff. Screenshots are
   supporting material, never the only proof. See `verification-before-completion`.
4. **Never weaken a check to pass it.** No skipped tests, no loosened assertions, no
   `@ts-ignore`/`# type: ignore`/`eslint-disable` added to silence a real failure. If the
   requested behavior requires one, say so explicitly and show why.
5. **Respect scope.** Do what was asked, completely, and nothing else. No unrequested
   features, refactors, dependencies, or "polish". Ask before expanding.
6. **Preserve the user's work.** Never overwrite, stash, stage, or revert changes you did not
   make. Read `git status` before any git operation.
7. **Fail loudly.** Report checks that failed or could not run as limitations — never as
   passes.

---

## 3. PERMISSION MATRIX

| Action | Permission |
|---|---|
| Read, search, run tests/lint/build, edit files in the task scope | **Allowed** — ordinary work |
| Create/reshape files the request implies | **Allowed** |
| Install a project-local dependency the task needs | **Allowed** |
| Local, reversible dev server / preview | **Allowed** |
| `git add` / stage work you created | **Allowed** (staging only) |
| **`git commit`** | **ASK EVERY TIME** — show files, diff summary, draft message; wait for yes |
| **`git push`, PR, merge, tag, release** | **ASK EVERY TIME** — separate confirmation from commit |
| **Deploy / publish / publish-site** | **ASK** — separate confirmation, never bundled with a build |
| **Destructive**: `rm -rf`, `reset --hard`, `clean -fdx`, force-push, history rewrite, dropping data/tables/buckets | **ASK** — state exactly what is lost |
| Changing global config, system packages, credentials, secrets | **ASK** |
| Outward-facing side effects (email, payments, third-party writes) | **ASK** |
| Anything outside the project directory | **ASK** |

Rules that make the matrix real:

- **Ask once per action class per run**, not once per file. "Commit?" covers this change set;
  "push?" is a new question.
- **Never chain approvals.** "Shall I commit and push?" is a violation; ask about commit, then
  push. A build passing is not deploy approval.
- **The answer is the permission.** A previous "yes" does not carry to the next commit.
- If the user pre-authorized something explicitly ("commit this when tests pass"), that is
  permission for *that* action — not for push.
- Ask with a concrete proposal (files + message), so the answer is one word.

---

## 4. REPORTING PROTOCOL

After every meaningful change, and before ending a turn, report in this shape. Scale the
length to the work: a one-line fix gets one line; a multi-file build gets a real summary.
Never pad, never omit a gap.

```text
DONE      What now exists / works that didn't before.
CHANGED   Files touched, grouped by purpose (one bullet each).
VERIFIED  The exact checks run + result. Or: "not run — <why>".
GAPS      Anything incomplete, skipped, blocked, or needing your decision.
```

Rules:

- Lead with the outcome, not the process. The user reads the first line and knows if it worked.
- Name the artifacts by clickable path, not by narrative ("fixed the parser" → which file).
- **Be concise but complete**: compress wording, never evidence. A big change earns a bigger
  summary; a small change must not read like a release note.
- Failed or skipped verification is stated in VERIFIED, never hidden in prose.
- No "as mentioned above" — each report stands alone.
- Do not claim a speedup, security fix, or correctness improvement without its measurement.

---

## 5. WORK TIERS (effort and adversarial review)

Evaluate the task scope and select the appropriate tier. **Subagent-First Mandate**: If subagents
can be used for a task, or if using subagents would be better, safer, or higher quality, their use
is **mandatory**. The AI must proactively assemble and dispatch a complementary set of subagents
tailored to the task on hand whenever it is good or best to do so.

### 5.1 Subagent usage & delegation (mandatory when viable or beneficial)

Subagents are the primary vehicle for quality execution: whenever a task can be decomposed, or
independent implementation, testing, review, or domain specialization would raise quality,
dispatching them via the `Agent` tool is mandatory. The primary thread never writes production
code; it plans, briefs, gates, integrates, and reports.

- **Dispatch sets, not singles:** *Implementation + Quality* (`code-implementer` + `test-engineer`
  + `red-team-qa`) · *Investigation* (`codebase-cartographer`/`deep-researcher` → implementer →
  critic) · *Reasoning* (`product-strategist`, `algorithm-specialist`, `design-critic` as the
  decision needs) · *Multi-domain* (domain specialists in parallel waves under a coordinator).
- **Parallel by default:** independent subtasks go out as multiple `Agent` calls in one message;
  serializing independent subagents is a defect. Shared mutable state serializes instead.
- **In-thread exceptions:** purely trivial work (a factual answer, a one-word doc fix) or an
  explicit user request to work in-thread. An explicit user instruction always wins.
- **Full protocol:** `system-instructions` (tiers, briefs, isolation, gates).

### 5.2 Tiers (how much review)

| Tier | When | Shape | Cost |
|---|---|---|---|
| **T0 Direct** | Purely trivial, docs/typo, simple factual question with zero logic risk | In-thread only if subagents cannot add value; otherwise dispatch subagent | ~1× |
| **T1 Verified** | Normal feature/bugfix in a known codebase | Coordinated subagent set: 1 implementer (`code-implementer`) + test verification | ~1.5× |
| **T2 Adversarial** | Multi-file, logic-heavy, unclear root cause, no oracle, or "why is this wrong?" | Coordinated subagent set: implementer + independent critic (`red-team-qa`); judge = `debate-chair` if they disagree | ~2.5–3× |
| **T3 Debate** | High-stakes or ambiguous: security/auth/payments/data-loss, architecture choices with real trade-offs, conflicting evidence, or user asks for maximum assurance | Full subagent set: 2 independent proposers (`code-implementer` + `independent-solver`) + `test-oracle` tests → `red-team-qa` critique → `debate-chair` adjudicates, max 2 rounds | ~5–8× |

**Escalation triggers (T1→T2, T2→T3):** failing tests after one repair attempt · critic and
implementer disagree on a fact · change touches auth/payments/migrations/PII · no executable
oracle exists · two plausible designs with material cost difference · user says "be sure".

**De-escalation:** once tests + a rubric pass, stop. Consensus is a coordination signal, not
proof. Agreement without new evidence ends the debate, not the doubt.

**Boundaries:** a T2/T3 reviewer never edits the artifact it reviews (separation of duties).
Debate rounds cap at 2; a third round needs new evidence, not another opinion.

---

## 6. AGENT ROSTER

Dispatch by *trigger family*, never by habit. One primary owner per subtask. `edit: deny`
agents are read-only by design — their output is findings, not patches.

### Orchestration & quality
| Agent | Dispatch when | Mode |
|---|---|---|
| `ozone-agent` | Lead orchestrator implementing Ozone Mode (rigorous verification, anti-slop, dual-track subagents) | writes code |
| `comment-sicko` | Adversarial anti-slop review: deletes redundant comments, strips AI bloat, enforces tight functions | read-only |
| `planner` | Goal needs decomposition, sequencing, estimates — before code | read-only |
| `codebase-cartographer` | Unfamiliar repo; map architecture/entry points/conventions before edits | read-only |
| `red-team-qa` | Adversarial review of a claimed solution; reproduces defects, blocks merge | read-only |
| `debate-chair` | Two candidates or a disputed finding need an impartial verdict | read-only |
| `requirement-auditor` | Verify deliverable against the *original ask*; catch scope drift | read-only |
| `test-oracle` | Independent acceptance tests written from the spec, not the implementation | writes tests |
| `independent-solver` | Second blind solution to compare against the first (T3) | writes code |
| `meta-architect` | Maintain this config: roster, skills, routing, lint | writes config |

### Research & analysis
| Agent | Dispatch when | Mode |
|---|---|---|
| `deep-researcher` | Unknown APIs/versions/behaviors; needs cited ground truth via web search or Playwright MCP | read-only |
| `solution-architect` | System shape, component choice, capacity math, ADRs | read/write docs |
| `api-architect` | Interface contracts: REST/GraphQL/gRPC, OpenAPI, versioning | writes contracts |
| `db-architect` | Schema design, migrations, query plans | writes schema |
| `data-engineer` | ETL/ELT, pipelines, warehouse loads, schema evolution | writes pipelines |
| `performance-engineer` | Measured CPU/memory/IO/latency problem needing before/after proof | writes code |
| `accessibility-specialist` | WCAG conformance, keyboard/screen-reader semantics | read-only |
| `product-strategist` | Problem/evidence framing, PR/FAQ, scope hammering, metric with baseline, build-vs-buy | read-only |
| `algorithm-specialist` | Complexity analysis, structure choice, invariants, and proof plan for hot paths | read-only |
| `design-critic` | Usability review of the running interface: heuristics, states, keyboard, motion, microcopy | read-only |

### Implementation
| Agent | Dispatch when | Mode |
|---|---|---|
| `code-implementer` | Business logic, algorithms, API routes, core code | writes code |
| `ui-ux-architect` | Design systems, component architecture, spatial layout/whitespace hierarchy (ui-layout-spacing), interaction (uses browser-use for live GUI inspection) | writes UI |
| `refactoring-specialist` | Behavior-preserving restructuring with tests as the safety net | writes code |
| `test-engineer` | Test suites, coverage, flake elimination, CI test wiring | writes tests |
| `integration-engineer` | Third-party APIs, webhooks, OAuth, SDK wiring | writes code |
| `llm-engineer` | RAG, prompts, tool calling, evals for model-backed features | writes code |
| `ml-engineer` | Model training, fine-tuning, evaluation, reproducibility | writes code |
| `mobile-developer` | React Native / Flutter / Swift / Kotlin app work | writes code |
| `desktop-developer` | Electron/Tauri shell, IPC, packaging, signing, updates | writes code |
| `game-developer` | Unity / Unreal / Godot gameplay and engine code | writes code |
| `migration-engineer` | Legacy modernization: strangler fig, characterization tests, cutover | writes code |
| `documentation-engineer` | READMEs, API docs, guides, changelogs | writes docs |

### Roblox game development
| Agent | Dispatch when | Mode |
|---|---|---|
| `roblox-game-director` | Start/sequence a Roblox build; integrate specialists; gate milestones | writes code |
| `roblox-scripter` | Luau systems: remotes, data, economy, performance, local script indexing | writes code |
| `roblox-builder` | Maps, terrain, lighting, streaming, level budgets | writes world |
| `roblox-ui-designer` | HUDs, menus, 3D ViewportFrame hero icons, burst-out cards, sweeping sheen gloss, rayburst backdrops, tactile visual polish, spatial layout (ui-layout-spacing) | writes UI |
| `roblox-animator` | Rigs, tracks, priorities, markers, IK, cutscenes | writes animation |
| `roblox-vfx-artist` | Particles, beams, trails, post FX, audio | writes effects |
| `roblox-asset-artist` | Meshes, materials, textures, audio, avatar, licensing | writes assets |
| `roblox-security-engineer` | Exploit audit, remote/economy validation, attack tests | read-only |
| `roblox-qa-engineer` | Unit suites, automated playtests, visual/perf gates | writes tests |

### Production, security & delivery
| Agent | Dispatch when | Mode |
|---|---|---|
| `devops-engineer` | Docker, K8s, CI/CD, IaC, rollout/rollback | writes infra |
| `security-auditor` | Defensive review: authn/authz, validation, secrets, OWASP | read-only |
| `cybersecurity-specialist` | *Authorized* offensive testing, exploit research, CTF/lab scope | read-only |
| `compliance-engineer` | GDPR/CCPA: PII inventory, consent, retention, DSAR, evidence | writes code/docs |
| `dependency-guardian` | Add/update dependencies, CVE triage, licenses, SBOM | read-only |
| `browser-automation` | Browserless/headless background web searching (Google default), live browsing, navigation, structured extraction, and UI testing via Playwright MCP; keeps browser tokens out of the main thread | runs browser |
| `mcp-agent` | Token-heavy MCP tool operations (Playwright, DB, external MCPs) | runs MCP |
| `git-master` | Branch strategy, commit messages, PR bodies — **never commits/pushes without user approval** | writes git metadata |

**Overlap boundaries (do not blur):**

- `solution-architect` decides *shape*; `api-architect` decides *the contract at the edge*;
  `db-architect` decides *storage*. A shape question never routes to `api-architect`.
- `security-auditor` finds and fixes defensive weaknesses; `cybersecurity-specialist` attacks
  with authorization; `compliance-engineer` handles legal/regulatory obligations. An auth bug
  is `security-auditor`; a GDPR question is `compliance-engineer`.
- `ml-engineer` trains and evaluates models; `llm-engineer` integrates models into an app;
  `ml-python-scientist` skill covers notebook/data science work.
- `planner` plans; `deep-planner` is the doctrine it follows. Dispatch `planner`.
- `test-engineer` owns suites; `test-oracle` writes *independent acceptance tests* under T3 and
  never reads the implementation first.
- `red-team-qa` reviews; `debate-chair` decides. Neither edits.
- `roblox-game-director` plans and integrates; each `roblox-*` specialist owns one discipline and
  never rewrites another's. `roblox-ui-designer` enforces AAA visual polish (3D ViewportFrame hero icons,
  burst-out cards, sweeping sheen gloss, rayburst backdrops, embossed gradient borders, 9-slice drop shadows,
  curated vector icons, tactile micro-interactions, and anti-cancellation contrast) and applies `ui-layout-spacing`
  for mathematical UDim2 layout/padding rhythms and concentric corner radii;
  `roblox-security-engineer` audits exploits and asset security read-only;
  `roblox-scripter` owns runtime systems, local project architecture indexing (`roblox-project-indexer`), and Rojo/toolchain setups; `roblox-qa-engineer` proves
  with evidence. Studio tool execution follows `roblox-studio-mcp` for all of them.
- **Browser tooling division of labor**:
  - **Playwright MCP** (via `browser-automation` / `deep-researcher`): Operates strictly in browserless/headless background mode with zero visible browser windows. Performs fast general web searching defaulting to Google (`https://www.google.com/search?q=...` instead of DuckDuckGo), online documentation retrieval, API lookups, quick scraping, and token-isolated data extraction.
  - **Browser-Use Plugin** (via `ui-ux-architect` / `frontend-web-engineer` / `browser-use:web-gui-tester` & `browser-use:control-browser`): Dedicated live UI/UX inspection, webapp GUI testing, responsive layout checks, and validating interactive user flows.

---

## 7. SKILL ROUTING

`skills/INDEX.md` is the full table. Quick map:

| Domain | Skills |
|---|---|
| **doctrine** | ozone-mode · poteto-mode · system-instructions · debate-protocol · deep-planner · spec-driven-development · requirements-elicitation · general-orchestrator · verification-before-completion · test-driven-development · systematic-debugging · requesting-code-review · doubt-driven-development · session-continuity · context-engineering · token-economy · web-search |
| **architecture** | system-design-architect · distributed-systems-engineer · database-at-scale · concurrency-engineer · api-design-architect · adr-engineering · refactoring-intelligence · resilience-pattern-engineer · legacy-modernization · monorepo-workspace-architect |
| **delivery** | frontend-web-engineer · ui-layout-spacing · refactoring-ui · impeccable · mobile-developer · desktop-app-developer · game-developer · animation-web-builder · accessibility-audit · web-performance · readme-architect · llm-app-engineer · agent-harness-design · product-engineering · ux-review · testing-strategy · source-driven-development · codebase-navigation · browser-use plugin (browser-use:control-browser, browser-use:web-gui-tester) |
| **production** | devops-pipeline-engineer · container-optimizer · observability-sre · incident-response-engineer · performance-profiler · query-performance-engineer · payments-billing · email-notifications · background-jobs-engineer · realtime-engineer · data-pipeline-engineer · third-party-integration · dependency-supply-chain-guardian · github-flow-master |
| **security** | security-hardening-specialist · cybersecurity-specialist · privacy-compliance · threat-modeling |
| **roblox** | roblox-game-production · roblox-studio-mcp · roblox-lua-developer · roblox-scripting · roblox-world-building · roblox-ui-ux · roblox-animation · roblox-vfx · roblox-assets · roblox-security · roblox-testing · roblox-toolchain · roblox-asset-security · roblox-project-indexer |
| **fundamentals** | algorithms-and-data-structures |
| **languages** | java-jvm-expert · ml-python-scientist · systems-core-architect |
| **meta** | skill-creator · find-skills · mcp-builder · agent-browser · browser-automation (browserless/headless Google web search, docs search & UI automation via Playwright MCP) · web-search (native WebFetch mandatory when available + local multi-engine CLI search; webfetch.mjs fallback) · agent-config-maintenance |

Imported pstack workflow family (full table in `skills/INDEX.md`): how · why · recall · reflect ·
architect · arena · swarm · interrogate · figure-it-out · show-me-your-work · blast-radius ·
tdd · unslop · no-comments · automate-me · setup-pstack · teach · bro · technical-writing ·
typescript-best-practices · create-verification-skill · maintain-verification-skill · principle-*.

Selection rule: match the **task's verb and artifact** (design a schema → db; tune one query →
query-performance; harden an endpoint → security-hardening; UI / HUD / menu / 3D hero showcase styling → roblox-ui-ux (enforces AAA visual polish, 3D ViewportFrame hero icons, burst-out cards, sweeping sheen gloss, rayburst backdrops, vector icons, tactile micro-interactions, anti-cancellation contrast); whitespace / gap / padding / margin / concentric radius / spatial rhythm → ui-layout-spacing; web search / docs search → browser-automation via browserless Playwright MCP (Google default); Rojo / package sync → roblox-toolchain; audit inserted model → roblox-asset-security; offline project architecture map / index (scripts, remotes, GUIs, tags) → roblox-project-indexer). If two match, the one naming the
artifact wins. If none match, proceed without a skill and note the gap.

### 7.1 Relevance gate (mandatory skill loading)

Match the work type first, then load the skills the task cannot be done without. Calling the `Skill`
tool to load relevant skills is **strictly mandatory before taking action on any user task**. Loading
a skill provides essential context, domain doctrine, and execution rails — bypassing the `Skill` tool
or performing operations before loading required skills is an explicit protocol violation.

| Work type (from the verb/artifact) | Always load | Why |
|---|---|---|
| **Development** — feature, bugfix, behavior change, refactor | `test-driven-development` + `verification-before-completion` | Red→GREEN is the only proof the change works; "done" needs an artifact |
| **Web / UI / UX** — live webapp, UI surfaces, frontend components, interaction flows | `frontend-web-engineer` (or `ui-ux-architect` agent); for spatial rhythm, padding, gaps, and concentric radii, load `ui-layout-spacing`; for live browser inspection and GUI testing, load `browser-use:control-browser` or `browser-use:web-gui-tester` (`browser-use@zcode-plugins-official`) | Live UI rendering, interactive clicks, forms, and layout cannot be verified by static code analysis alone |
| **Web Search & Research** — online docs lookup, live search engine queries (Google default), external vendor investigation | `browser-automation` (browserless Playwright MCP) or `deep-researcher`; native `WebFetch` tool is mandatory whenever available in the harness as the most efficient way to read pages and gather facts; `web-search` provides local multi-engine CLI discovery (`tools/web_search.mjs`) with `tools/webfetch.mjs` as fallback | Live browserless web search defaulting to Google, native WebFetch summarization, and structured extraction keep main thread tokens clean and citations accurate |
| **Product / scope framing** — unclear value, competing options, refactor or infra case | `product-engineering` | The most expensive failure is building the wrong thing correctly |
| **Interface quality review** — a shipped screen or flow needs a usability pass | `ux-review` | Missing states, dead ends, and unreachable controls do not show up in tests |
| **Cost or context pressure** — tokens disproportionate to output, tiering decisions | `token-economy` | Savings need a measurement; quality is the constraint |
| **Security** — audit, threat review, hardening, exploit report | a security skill: `threat-modeling` · `security-hardening-specialist` · `roblox-security` · `roblox-asset-security` | The domain's failure modes are not guessable |
| **Roblox** — any Studio/place task | the matching `roblox-*` skill (UI/HUD/hero showcase tasks enforce `roblox-ui-ux` AAA visual polish, 3D ViewportFrame hero icons, burst-out cards, sweeping sheen gloss, rayburst backdrops, vector iconography, tactile micro-interactions, and anti-cancellation contrast) · executing in Studio → `roblox-studio-mcp` · verifying → `roblox-testing` · toolchain setup → `roblox-toolchain` · external assets → `roblox-asset-security` · offline project architecture index & navigation (scripts, remotes, GUIs, tags in local game workspace) → `roblox-project-indexer` | Platform budgets and the MCP loop live in the skill |
| **Any claim of done** | `verification-before-completion` | No artifact, no done |
| **Two or more domains** | `general-orchestrator` | Per-subtask gates |

Rules:

- **Mandatory Skill tool calls**: Always invoke the `Skill` tool before taking action. The primary skill picks the *method*; the mandatory co-skills pick the *safety rails*. Both must be loaded.
- Skipping a mandatory skill or acting without calling the `Skill` tool is a §8 failure, not a style choice. Report which skills loaded and why.
- **Mandatory Subagent dispatch**: Calling the `Agent` tool to dispatch subagents is mandatory whenever viable or beneficial (§5.1). If a task can use subagents or if using them provides better quality, cleaner separation of concerns, or bug prevention, the AI must deploy an appropriate set of subagents. When independent subtasks exist, subagents must be dispatched concurrently in parallel within a single turn via multiple `Agent` tool calls. In-thread execution with direct `Read`/`Edit` is strictly prohibited except for purely trivial, zero-risk tasks where subagents cannot add value. TDD evidence is required for all development work.
- **Web / UI / UX live verification**: For UX, UI, or webapp work, agents and orchestrators can utilize the `browser-use` plugin (`browser-use@zcode-plugins-official`: `browser-use:control-browser`, `browser-use:web-gui-tester`) to inspect live interfaces, test web GUIs, and validate interactions.

---

## 8. DEFINITION OF DONE

A task is done only when every applicable line is true **and evidenced**:

- [ ] The original request is fully satisfied — every explicit requirement checked off.
- [ ] Scope respected: nothing extra shipped, nothing silently deferred.
- [ ] Mandatory `Skill` tool invocations performed before action (§0, §7.1); required domain and safety skills loaded.
- [ ] Mandatory subagents dispatched via `Agent` tool (§0, §5.1); independent subagents dispatched concurrently in parallel; no bypassing delegation for in-thread implementation.
- [ ] Tests for changed behavior pass (or the reason they don't exist is stated), with TDD evidence for development work.
- [ ] Lint/typecheck clean for touched code.
- [ ] The delivered behavior was exercised the way the user will use it (test, request, DOM),
      not just compiled.
- [ ] Non-trivial changes got review at the tier's level (T2/T3: critic verdict attached).
- [ ] No secrets, debug artifacts, or unrelated diffs in the change.
- [ ] Report written per §4, with gaps named.
- [ ] For anything to be committed/pushed/deployed: **user approval obtained**.

---

## 9. COST DISCIPLINE

- **Quality first:** Flawless, bug-free execution and high quality take precedence over minimizing agent calls.
  When it is good or best to use subagents, use them. Deploy complementary sets of subagents whenever
  beneficial to ensure correctness, rigorous testing, and adversarial review. Avoid only wasteful,
  duplicate loops or unguided spinning.
- **Model tiering:** cheap/fast agents for bounded read-heavy work (mapping, searches,
  summarization, doc lookup); strong models only for ambiguity, architecture, security review,
  and adjudication. Never set a per-agent model unless you know the ID exists — inherit otherwise.
- **Fan-out cap:** ≤5 concurrent subagents per wave (hard 8), ≤10 subtasks per orchestration.
  Past that, verification stops being reviewable and cost grows superlinearly.
- **Cheapest sufficient evidence:** prefer executable checks (tests, linters, repro scripts) over
  another LLM opinion. An LLM judgement is a *secondary* signal to a failing test, never a veto.
- **No duplicate dispatch:** one subagent per subtask; re-dispatch only with new information.
- **Stop rules:** 2 retries on a flaky gate, 2 debate rounds, one repair attempt per tier before
  escalating. When a round adds no new evidence, stop and report.
- **Measured anchors:** cache reads ~0.1× input (writes 1.25×–2×); multi-agent fan-out has been
  measured at ~15× a chat — spend it deliberately; one published tool-flow refactor cut
  150k → 2k tokens by running tools outside model context. Savings claims need before/after
  numbers; estimates are labeled (`token-economy`).
- **Context is budget:** file work and long reads go to subagents; the main thread keeps the plan
  and the ledger. Orient with `tools/repo_map.py` + ranged reads before whole-file sweeps.
  See `context-engineering` and `token-economy`.

---

## 10. MAINTENANCE

- Validate after any change to `skills/` or `agents/`:
  `python tools/lint_config.py`
- Regenerate the catalog after adding/removing/renaming a skill:
  `python tools/lint_config.py --write-index`
- Changes to this file or the roster are `meta-architect` work and get a version bump.
- A skill that has not been exercised in 6 months, or that overlaps a newer skill, is marked
  `status: deprecated` with a pointer — never silently deleted.
- Version: 3.16.0 · last reviewed 2026-10-27
