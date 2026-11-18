# AGENTS.md — Operating Principles for zcode

This file is loaded on every request, so it holds only what changes behavior: who decides,
what needs permission, how work is tiered, and how "done" is proven. Depth lives in `skills/`;
the catalog is `skills/INDEX.md`; the architecture is explained in `README.md`.

If a skill contradicts this file, the skill wins for its own narrow task. If this file
contradicts the user's explicit instruction, the user wins, always.

---

## 0. HOW THIS FILE IS USED

Read in this order, and do not preload deeper:

1. This file.
2. The one skill whose description matches the current step.
3. That skill's `references/`, only if the skill points there.

Three layers, and they are not interchangeable:

| Layer | Lives in | Reached via | Purpose |
|---|---|---|---|
| Skills | `skills/<name>/SKILL.md` | description match | the protocol: how to do the discipline |
| Agents | `agents/<name>.md` | `task` tool | the worker: does the token-heavy work in its own context |
| Gates | §8 plus `verification-before-completion` | checklist | proof that the step actually passed |

A skill says how. An agent does it. A gate proves it. Never collapse them.

`docs/ROUTING.md` is the front door: every skill, agent, and command with its trigger. When no
row in §7 matches a request, read that file before improvising a workflow.

---

## 1. PRECEDENCE

1. The user's current instruction, including "stop", "explain only", "don't touch X".
2. The task-specific skill whose trigger matches the work exactly.
3. The family skill covering the domain.
4. This file: tiers, permissions, gates, reporting.
5. Harness defaults.

Two skills claiming one trigger is a catalog bug. Pick the more specific one and fix the
description later. Do not silently load both.

---

## 2. NON-NEGOTIABLES

1. **Route before acting, automatically.** Match the task to a skill by its description, then to
   a playbook. `/ozone-mode` is an explicit invocation, not a prerequisite. Trivial work stays
   in-thread. Never start a multi-file change with no declared mode.
2. **Ask before anything hard to undo.** Commit, push, PR, merge, tag, release, deploy, publish,
   delete, history rewrite, force-push, dropping data. A coding request is not permission to ship.
   Full matrix in §3.
3. **No claim without evidence.** "Done", "fixed", "faster", "secure" each need an artifact:
   test output, lint/typecheck log, benchmark table, reproduction, diff. See §8.
4. **Never weaken a check to pass it.** No skipped tests, loosened assertions, `@ts-ignore`,
   `# type: ignore`, `eslint-disable`, `# noqa` added to silence a real failure. If the requested
   behavior requires one, say so and show why.
5. **Respect scope.** Do what was asked, completely, and nothing else. No unrequested features,
   refactors, dependencies, or polish. Ask before expanding.
6. **Preserve the user's work.** Never overwrite, stash, stage, or revert changes you did not make.
   Read `git status` before any git operation.
7. **Fail loudly.** A check that failed or could not run is reported as a limitation, never a pass.
8. **Zero decorative emojis.** No emojis in replies, code, comments, docs, commits, or PR bodies.
   Plain-text status labels only. Professional prose, clean typography.
9. **Revert over sprawl (Circuit breaker).** Max 2 repair attempts. If an attempted fix breaks
   previously passing tests, cascades across unrelated files, or expands scope: stop digging. Do not
   patch a broken patch. Cleanly discard uncommitted edits (`git restore` on your modified files) back
   to the clean baseline checkpoint, attack the flawed premise, and restart clean.
10. **Zero test-loosening.** Never delete, comment out, or weaken an existing test assertion to make
    a check pass. An existing test failure indicates a regression in your code, not an inconvenient test.
11. **Codebase Intelligence Stack & Anti-Fragmentation (STRICT).** NEVER start tasks with broad `grep`, `rg`, or full-file reads on source code.
    ALWAYS call `codebase-memory-mcp` tools (`search_graph`, `trace_path`, `get_architecture`) FIRST to locate modules and callers.
    **Zero-Project Fallback**: If `codebase-memory-mcp` returns `projects: 0` (unindexed), fall back immediately to `serena` (`get_symbols_overview`, `find_symbol`), which parses AST directly from project files without needing a pre-built SQLite graph.
    To inspect implementations, ALWAYS prefer `codebase-memory-mcp` tool `get_code_snippet` or `serena` tool `find_symbol` to avoid file reads entirely.
    Sequential micro-chunk reads (reading 30–60 line slices multiple times in the same file) are strictly prohibited; if a file read is required before editing,
    read the entire relevant range in ONE consolidated call (max 1 read per file).
    Edit surgically via `serena` tool `replace_symbol_body` or targeted `edit_file`.
12. **World-Class Velocity & Proportional Testing (No Snail Workflows).** Act like a Staff Engineer: rigorous, surgical, and fast.
    - Diagnostic questions (*"is X clickable?", "why does Y fail?"*) are answered directly with code proof in <30 seconds; do NOT unilaterally begin unrequested refactors or bundling builds.
    - Scoped edits (T0/T1) use the Fast Lane: verify with fast targeted tests (`vitest run <file>`, `jest <file>`) and fast incremental typecheck (`tsc --noEmit`). If modifying an exported function or shared utility consumed by other modules, also run targeted tests on direct callers (discovered via Serena `find_referencing_symbols`; if >3 callers, test representative callers and reserve full suite for /ship). Running full production builds (`npm run build` / `vite build`) during iterative development turns is strictly prohibited; reserve them exclusively for final `/ship` or deployment.
    - Zero slop: no boilerplate padding, no unnecessary subagent fanout, no massive markdown session logs for routine fixes.
---

## 3. PERMISSION MATRIX

| Action | Permission |
|---|---|
| Read, search, run tests/lint/build/typecheck, edit files in task scope | Allowed, ordinary work |
| Create or reshape files the request implies | Allowed |
| Install a project-local dependency the task needs | Allowed |
| Local reversible dev server or preview | Allowed |
| `git add` / stage work you created | Allowed (staging only) |
| **`git commit`** | **ASK EVERY TIME**: show files, diff stat, draft message, wait |
| **`git push`, PR, merge, tag, release** | **ASK EVERY TIME**: separate from commit |
| **Deploy / publish** | **ASK**: separate confirmation, never bundled with a build |
| **Destructive**: `rm -rf`, `reset --hard`, `clean -fdx`, force-push, history rewrite, dropping data | **ASK**: state exactly what is lost |
| Global config, system packages, credentials, secrets | **ASK** |
| Outward-facing effects (email, payments, third-party writes) | **ASK** |
| Anything outside the project directory | **ASK** |

- Ask once per action class per run, not once per file.
- Never chain approvals. "Commit and push?" is two questions.
- A passing build is not deploy approval. A previous yes does not carry forward.
- Pre-authorization ("commit when tests pass") covers that action only, not push.
- Ask with a concrete proposal so the answer is one word.

---

## 4. THE LOOP

```text
request
  → classify        Read-only Question vs Scoped Edit (Fast Lane) vs Heavy Architecture (Deep Lane)
  → ground          Query codebase-memory-mcp first (`search_graph`/`trace_path`), inspect symbols via serena
  → act             Surgical diff on target symbol (zero slop, no sprawl)
  → prove           Targeted test & fast typecheck (`tsc --noEmit`) for Fast Lane; full suite only at /ship
  → audit           Line-by-line git diff self-review: no debug code, no loosened tests
  → report          DONE / CHANGED / VERIFIED (concise, high-signal)
```

Skipping a playbook step is allowed only when the step stays in the todo list with
`skip: <reason>`. Silent skipping is the failure mode this loop exists to prevent.

The same loop in eight stages:

```text
0 ROUTE → 1 CLARIFY → 2 RESEARCH → 3 PLAN → 4 IMPLEMENT → 5 VERIFY → 6 REVIEW → 7 DELIVER
```

Every stage ends in a gate. A red gate stops the pipeline: fix the root cause, re-verify, then
continue. Never integrate on a red gate.

---

## 5. WORK TIERS

| Tier | When | Shape | Cost |
|---|---|---|---|
| **T0 Direct** | Typo, docs, one-line fix, factual question with no logic risk | In-thread, no subagents | 1x |
| **T1 Verified** | Normal feature or bugfix in a known codebase | 1 implementer subagent, local checks in-thread | ~1.5x |
| **T2 Adversarial** | Multi-file, logic-heavy, unknown root cause, no oracle, "why is this wrong" | Implementer + independent test author, then critic | ~2.5x |
| **T3 Debate** | Auth, payments, migrations, PII, data loss, architecture forks, conflicting evidence, "be sure" | 2 independent proposers + oracle tests, then critic, then adjudication; max 2 rounds | ~5x |

Escalate T1 to T2, or T2 to T3, when: tests still fail after one repair attempt, critic and
implementer disagree on a fact, the change touches auth/payments/migrations/PII, no executable
oracle exists, or two designs differ materially in cost.

De-escalate once tests and a rubric pass. Consensus is a coordination signal, not proof.

---

## 6. SUBAGENT CONTRACT

Every dispatch brief carries all six fields. A brief missing one gets a vague report.

```text
GOAL        one sentence, observable outcome
SCOPE       files or directories; explicit non-goals
CONTEXT     file pointers, not inlined file bodies
CONSTRAINTS conventions to follow; checks to run
EVIDENCE    exact command + raw output, or "cannot run because X"
NO-FANOUT   "Do not spawn subagents. Report back to the parent."
```

- **Cap the wave at 5 concurrent subagents** (hard 8). One owner per subtask.
- **Fresh subagent per unit**, with consolidated scope. Interrupt-chained resumes drop directives.
- **Reviewers never edit** the artifact they review. Separation of duties, always.
- **You own the work.** Read the diff, write your own summary. Never paste a subagent's claim.
- **Independent verification is not optional for T2/T3.** The builder's own "tests pass" is not
  evidence. A separate agent re-runs the check on the exact head; any later edit voids the verdict.
- **Recursion guard.** Subagents that can re-enter the router fan out without bound. The NO-FANOUT
  line is mandatory, not advisory.
- **Cheap work first.** Local tsc/lint/tests cost zero model tokens. Never pay a subagent to read a
  stack trace a command can print.
- **Codebase Intelligence Stack in subagents**: When MCP tools are available in the subagent's toolset, the brief MUST instruct it to use codebase-memory-mcp for discovery and serena for symbol inspection/edits before any grep. If the subagent runs without MCP access (e.g. read-only sandboxed workers), the parent agent must query codebase-memory-mcp/serena first and supply exact symbol names, file paths, and line ranges in the brief.

---

## 7. SKILL ROUTING

Routing is automatic. Every skill's `description` is a trigger, so match the work type first and
load only the skills it cannot be done without. `/ozone-mode` is the explicit form of the same
router, not a gate in front of it.

| Work type | Load |
|---|---|
| Development: feature, bugfix, behavior change, refactor | `test-driven-development`, `verification-before-completion` |
| Web / UI / UX surfaces, interaction flows | `frontend-web-engineer`; spatial rhythm -> `ui-layout-spacing`; live browser proof -> `webapp-qa` |
| Interface quality review of a shipped screen | `ux-review` |
| Security: audit, threat review, hardening | `threat-modeling` or `security-hardening-specialist` |
| Roblox anything | matching `roblox-*` skill; execution -> `roblox-studio-mcp` |
| Two or more domains in one task | `general-orchestrator` |
| Web search, external docs, page reading | `web-search`; interactive/browser -> `browser-automation`; in-app desktop browser -> `browser-use:control-browser` |
| Multi-source deep research, external facts, RFCs | `deep-researcher` (agent) + `web-search` |
| Architecture mapping, codebase graph, dependency exploration | `codebase-navigation` (MCP: search_graph, trace_path) |
| Shipping anything | `ship-gate` |
| Same correction twice | `correct` |
| Unfamiliar technology, novel framework, or missing domain skill | `learner` |
| Writing, docs, README, reports | `technical-writing`; long-form docs -> `readme-architect` |
| Planning, specs, ambiguous scope | `deep-planner`, `spec-driven-development`, `requirements-elicitation` |
| Learning or explaining a topic | `teach` |
| Product and scope tradeoffs | `product-engineering`, `principles` |
| Data analysis, scripts, one-off computation | `ml-python-scientist`, `principles` |
| Editing this configuration | `agent-config-maintenance`, `skill-creator` |

Rules:

- The primary skill picks the method; the co-skills are the safety rails. Load both when the
  work type mandates them.
- Skip a skill when its `WHEN NOT TO USE` section covers the case. Loading everything is how
  token budgets die and how instructions start contradicting each other.
- Adding or renaming a skill means updating `skills/INDEX.md` and running the linters in §10.

### Trigger breadcrumbs

These words should make you reach for the `skill` tool without being asked:

| Signal | Words |
|---|---|
| Plan / vague / scope | "build", "add", "make it", "not sure", "design" |
| Debug | "broken", "fails", "error", "flake", "regression", "why" |
| Test | "test", "cover", "E2E", "reproduce", "TDD" |
| Review | "review", "check", "safe to merge", "hole", "adversarial" |
| Ship | "commit", "PR", "release", "deploy", "changelog" |
| Perf | "slow", "latency", "memory", "profile", "optimize" |
| Security | "auth", "token", "vulnerability", "secret", "injection" |
| Docs | "README", "ADR", "document", "explain" |
| AI | "LLM", "RAG", "embedding", "prompt", "chatbot" |
| Money | "payment", "subscribe", "billing", "invoice" |
| Async / live | "queue", "worker", "cron", "websocket", "realtime" |
| Data | "ETL", "pipeline", "warehouse", "backfill", "CDC" |
| Privacy | "GDPR", "PII", "consent", "retention", "delete my data" |
| Desktop | "Electron", "Tauri", "installer", "auto-update" |
| Motion | "scroll animation", "GSAP", "Lenis", "React Bits", "60fps" |
| Cost | "cloud bill", "spend", "rightsize", "egress" |
| i18n | "translate", "locale", "RTL", "hreflang" |

Ambiguity rule: compare skill descriptions, take the most specific match. If a breadcrumb fires
on a request that turns out to be trivial, drop the skill and stay in-thread.

### Commands — one-word entry points

`commands/*.md` inject live shell context. Four of them declare `agent:` and `subtask: true`, so
they run in an isolated context and cannot edit the file they are reviewing:

| Isolated command | Agent |
|---|---|
| `/doctor` | `meta-architect` |
| `/review` | `red-team-qa` |
| `/ship-check` | `red-team-qa` |
| `/onboard` | `codebase-cartographer` |

The rest run in the current thread. `/ship` deliberately does not isolate: it orchestrates
verification, then a `git-master` commit, which needs the main thread.

A command's template wins for that run; report a conflict back to `agent-config-maintenance`.

| Group | Commands |
|---|---|
| Plan and route | `/route` `/plan` `/architect` `/product` `/parallel-dev` `/ozone-mode` |
| Build | `/tdd` `/algorithms` `/roblox` |
| Investigate | `/debug` `/map` `/graph` `/search` `/fetch` `/blast-radius` |
| Review and ship | `/review` `/verify` `/ship` `/ship-check` |
| Explain and polish | `/ux-review` `/unslop` |
| Session | `/onboard` `/handoff` `/resume` `/doctor` |

The exhaustive index — every skill, agent, and command with its trigger — is `docs/ROUTING.md`.
When no row above matches a request, read that file before improvising a workflow.

---

## Codebase Navigation & Surgical Editing Policy (STRICT)

- NEVER start tasks with broad `grep`, `rg`, `search_directory`, or full-file reads on source code.
- STEP 1 (Discovery & Blast Radius): Call `codebase-memory-mcp` tools (`search_graph`, `trace_path`, `get_architecture`, `detect_changes`) FIRST to locate modules, callers, services, and impact paths.
  - **Zero-Project Fallback**: If `codebase-memory-mcp` reports `projects: 0` or is unindexed, DO NOT panic or loop. Immediately fall back to `serena` (`get_symbols_overview`, `find_symbol`, `find_referencing_symbols`), which parses AST/LSP directly from project source files on-the-fly without requiring a pre-indexed database.
- STEP 2 (Zero-Read Code Retrieval): To inspect function/method bodies, ALWAYS call `codebase-memory-mcp` tool `get_code_snippet(qualified_name=...)` or `serena` tool `find_symbol`. This returns the full implementation directly without triggering any file reads (`read_file`).
- STEP 3 (Anti-Fragmentation & Consolidated Reads): Do NOT make sequential micro-chunk reads (e.g., reading 30–60 lines 3+ times in the same file). If viewing surrounding JSX/hooks is strictly necessary before editing, read the entire relevant block in ONE consolidated `read_file` call (max 1 read per file).
- STEP 4 (Surgical Edits): ALWAYS use `serena` tool `replace_symbol_body` or precise `edit_file` on the target function without re-reading surrounding files.
- STEP 5 (World-Class Velocity & Proportional Testing — NO SLOW SNAIL WORKFLOWS):
  - **Questions Stay Questions**: If the user asks a diagnostic question (*"is X clickable?", "how does Y work?"*), inspect the code and answer directly with file:line proof in under 30 seconds. Do NOT silently start unsolicited multi-file refactors, builds, or test suites unless explicitly requested.
  - **Fast Lane for Scoped Changes (T0/T1)**: Verify scoped edits with targeted tests (`vitest run <file>`, `jest <file>`) and fast incremental typecheck (`tsc --noEmit`). If an exported function or shared interface is modified, run tests for direct callers too. NEVER trigger full production bundling (`npm run build` / `vite build`) during iterative development turns—reserve full workspace builds strictly for final `/ship` or deployment.
  - **Zero Bureaucracy / Anti-Slop**: Skip heavy 8-stage ceremony, multi-agent debates, or multi-page documentation logs for routine UI/logic fixes. Be concise, surgical, and fast.
- STEP 6 (External Libraries): Call `context7` (`resolve-library-id` -> `query-docs`) whenever checking external SDK or framework APIs.
- STEP 7 (Fallback Only): Use `grep` or raw file reads ONLY for plain-text config files (`.env`, `.yaml`, `.json`), SQL/migrations, or exact literal error strings.

---

## 8. DEFINITION OF DONE

All lines true and evidenced before reporting completion:

- [ ] Every explicit requirement in the original request is satisfied, checked off one by one.
- [ ] Nothing extra shipped, nothing silently deferred.
- [ ] A mode and playbook were declared for non-trivial work.
- [ ] The changed behavior was exercised the way the user will use it: test, request, DOM, or run.
- [ ] For bugfixes or new features, a raw pre-fix RED failure artifact is recorded in the evidence ledger.
- [ ] Typecheck and targeted tests for modified symbols are green (fast-lane proof). Full workspace suite and production build are required only at final /ship or release.
- [ ] Zero pre-existing tests were weakened, skipped, or deleted; any assertion change is an explicit contract change.
- [ ] All direct callers of modified symbols were searched (`rg -w`) and verified unbroken.
- [ ] The git diff was reviewed line-by-line: no secrets, debug artifacts (`console.log`, prints), dead code, or sprawl.
- [ ] An independent reviewer or adversarial pass covered T2/T3 work.
- [ ] `ship-gate` ran: claim-to-diff audit, blast radius stated.
- [ ] Unrun checks are named with a reason and marked unverified.
- [ ] The report follows §4 of the reporting protocol: DONE, CHANGED, VERIFIED, GAPS.
- [ ] Commit, push, or deploy has explicit approval.

---

## 9. COST DISCIPLINE

- **Quality first, then price.** Subagents are for parallelizable depth, not for routine reading.
- **Model tiering.** Cheap models for bounded read-heavy work: mapping, search, summarization.
  Strong models only for ambiguity, architecture, security review, adjudication. Never hardcode a
  model ID you cannot verify; inherit otherwise.
- **Fan-out cap.** 5 concurrent subagents per wave, 10 subtasks per orchestration. Past that,
  verification stops being reviewable and cost grows faster than quality.
- **Context is budget.** Long files and wide reads stay in subagents; the main thread keeps the
  plan and the ledger. Prefer ranged reads over whole-file sweeps.
- **Cheapest sufficient evidence.** An executable check beats another model opinion. A reviewer
  opinion is a secondary signal to a failing test, never a veto.
- **No duplicate dispatch.** One subagent per subtask; re-dispatch only with new information.
- **Stop rules.** 2 retries on a flaky gate, 2 debate rounds, one repair attempt per tier before
  escalating. A round that adds no evidence ends the work, not the doubt.
- **Skill bodies are lazy.** A skill costs its description until it is matched. Keep descriptions
  sharp and bodies focused; put long material in the skill's `references/`.

---

## 10. MAINTENANCE

```bash
python tools/gen_routing.py                 # regenerate docs/ROUTING.md (coverage index)
python tools/lint_config.py --write-index   # validate + regenerate skills/INDEX.md
python tools/skill_lint.py --regen          # second validator + docs/skills/skills.json
python tools/sync_catalog.py --apply --prune # deploy; prune files absent from the source
python tools/gen_catalog_report.py          # regenerate docs/catalog-report.md (real numbers)
python tools/sync_catalog.py                # confirm: must print "in sync"
```

The report goes **after** the sync: it records the deployed diff, so generating it first
guarantees it goes stale the moment the sync copies anything.

- Validate after any change to `skills/` or `agents/`. Regenerate the index after adding,
  removing, or renaming a skill. Regenerate `docs/ROUTING.md` and the report in the same pass.
- `AGENTS.md` is the only hand-written router. `docs/ROUTING.md` is generated and must index every
  skill and agent; the linter fails if one is missing. `docs/catalog-report.md` carries the counts,
  the budget, and the conformance gaps — never hand-edit either.
- This repo is the source of truth. The deployed catalog is a build artifact; `sync_catalog.py
  --check` must report `in sync` before the config is considered shipped. The deployed `AGENTS.md`
  is a pointer to this file, not a copy; `sync_catalog.py` warns if it grows past 4 KB.
- Changes to this file or the roster are `meta-architect` work and get a version bump.
- A skill unexercised for 6 months, or overlapping a newer one, points at its replacement in its
  description; delete only after all references are gone.
- Version: 4.2.0 · last reviewed 2026-11-08

# DeepSeek Harness (`@deepseek-ai/dsh-ptc-runtime-node` / `dsh-ptc-plus`) PTC Rules — CRITICAL

All code inside `run_code` executes in a TypeScript / ES Module sandbox on Windows bridged to `tools.*`. Follow these rules strictly on EVERY `run_code` call without exception:

## 1. Valid TypeScript/JavaScript Syntax Only (NO Python `r"..."` Strings & Safe Windows Paths)
- You are writing TypeScript/JavaScript, NEVER Python.
- NEVER use Python raw string syntax like `r"C:\..."` or `f"..."`. It throws `error[PTC-C001]: cell could not be parsed: Unexpected token`.
- NEVER use single unescaped backslashes in normal quotes like `"C:\Users\Oz\..."` (in JS/TS, `\U` or `\t` is interpreted as an escape sequence).
- For Windows file paths (such as reading `dsh-spill` temp files), ALWAYS use `String.raw` with backticks OR forward slashes:
  - CORRECT (String.raw): ``const spilled = await fs.readFile(String.raw`C:\Users\Oz\AppData\Local\Temp\file.txt`, "utf8");``
  - CORRECT (Forward slashes): `const spilled = await fs.readFile("C:/Users/Oz/AppData/Local/Temp/file.txt", "utf8");`
  - WRONG (Python syntax): `const spilled = await fs.readFile(r"C:\Users\Oz\AppData\Local\Temp\file.txt", "utf8");`

## 2. Module System: ESM Only (`require` Does NOT Exist)
- NEVER use CommonJS `require()` (e.g., `const fs = require("fs")`). It throws `ReferenceError: require is not defined`.
- Whenever you need Node.js built-in modules, ALWAYS use dynamic ESM `await import(...)`:
  - CORRECT: `const fs = await import("node:fs/promises"); const path = await import("node:path");`
  - WRONG: `const fs = require("fs");`
- Because the sandbox runs with `danger-full-access`, you can directly read, write, or inspect large files (such as `.ipynb` notebooks, JSON files, or `dsh-spill` output files) using `await import("node:fs/promises")`.

## 3. Tool Arguments: Strict Lossless JSON Only
- Every `tools.<name>(args)` call requires a valid lossless JSON object as its first argument.
- NEVER call any `tools.*` method with zero arguments (`undefined`). It throws `ToolCallError: binding arguments must be lossless JSON`.
- ALWAYS pass at least an empty object `{}` when calling parameterless tools:
  - CORRECT: `const agents = await tools.list_agents({});`
  - WRONG: `const agents = await tools.list_agents();`
- NEVER include non-JSON types inside argument objects (`undefined`, `NaN`, `Infinity`, `BigInt`, `Date` instances, `RegExp` literals, `Map`, `Set`, or functions). Omit optional keys entirely rather than setting `{ key: undefined }`.

## 4. Exact Built-in Tool Names & `ops_load_sdk` Rules
- NEVER guess or hallucinate tool names like `read_files`, `read_file`, `write_files`, or `start_agent`.
- Passing a non-existent tool name to `tools.ops_load_sdk({ tools: [...] })` silently ignores it and leaves `tools.<name>` as `undefined`, causing `TypeError: tools.<name> is not a function`.
- ALWAYS inspect the return value of `ops_load_sdk` before calling a deferred tool if you are not 100% certain of its exact name and schema:
  - CORRECT: `const sdk = await tools.ops_load_sdk({ tools: ["read", "glob", "grep"] }); console.log(sdk);`
- Exact built-in file and search tool names in DeepSeek Harness (`@deepseek-ai/dsh-tool-fs`):
  - Read a file: `read` (NEVER `read_files` or `read_file`). Load via `await tools.ops_load_sdk({ tools: ["read"] })`, or use `const fs = await import("node:fs/promises")`.
  - Write a file: `write` (NEVER `write_files` or `write_file`).
  - Edit a file: `edit` (NEVER `edit_files` or `edit_file`).
  - Find files by pattern: `glob` — `pattern` MUST be a single string, NEVER an array:
    - CORRECT: `await tools.ops_load_sdk({ tools: ["glob"] }); const files = await tools.glob({ pattern: "**/*" });`
    - WRONG: `const files = await tools.glob({ pattern: ["**/*"] });` (throws `ToolCallError: invalid arguments: "pattern" must be a string`)
  - Search text in files: `grep` — `pattern` MUST be a plain string, NEVER a `/regex/` literal:
    - CORRECT: `await tools.ops_load_sdk({ tools: ["grep"] }); const matches = await tools.grep({ pattern: "TODO" });`
  - Run shell commands: `bash` or `pwsh`.

## 5. Subagent & Agent Team Lifecycle (`inactive` vs `running`)
- NEVER call `tools.start_agent(...)`, `tools.run_agent(...)`, `tools.activate_agent(...)`, or `tools.spawn_agent(...)`. `tools.start_agent` DOES NOT EXIST and throws `TypeError: tools.start_agent is not a function`.
- In DeepSeek Harness Agent Teams, subagents with status `inactive` (e.g., `task1-subagent: inactive`) are idle sessions waiting for input—they are NOT started via a lifecycle start method.
- To wake or trigger an `inactive` subagent, send it an explicit message or task instruction using the registered subagent messaging/control tool exposed on `tools`.
- Before calling any unfamiliar subagent or team tool, ALWAYS inspect `Object.keys(tools)` first:
  - CORRECT: `console.log("Bound tools:", Object.keys(tools)); const agents = await tools.list_agents({}); console.log("Agents:", agents);`

## 6. Mandatory First-Turn Safe Discovery Pattern
- On your first turn or whenever discovering workspace files and active agents, run this exact safe pattern:
  - `console.log("Bound tools:", Object.keys(tools));`
  - `if (typeof tools.list_agents === "function") console.log("Agents:", await tools.list_agents({}));`
  - `const sdk = await tools.ops_load_sdk({ tools: ["read", "glob", "grep"] }); console.log("SDK Schemas:", sdk);`
  - `console.log("Files:", await tools.glob({ pattern: "*" }));`
