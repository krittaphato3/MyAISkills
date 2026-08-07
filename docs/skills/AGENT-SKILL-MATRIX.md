# Agent-Skill Matrix

Routing reference mapping the 23 agent definitions to the skills they own, per `docs/skills/skills.json` (32 skills, generated 2026-08-07). Consumed by `general-orchestrator` (Phase 3, task 3.7) for agent routing.

Source of truth: `docs/skills/skills.json` (ownership) + `agents/*.md` (definitions, 23 files; 3 created by Phase 3 tasks 3.8/3.9: planner, solution-architect, ml-engineer; 3 restored by fix wave 2026-08-07: cybersecurity-specialist, game-developer, mobile-developer).

## Legend

- **Ownership**: a skill's `owned-by-agent` frontmatter field (canonical in skills.json) determines which subagent owns it. Ownership is NOT the same as invocation: any agent may be routed any skill by the orchestrator; the owner is the accountable maintainer and the default routing target for that skill's trigger family.
- **Routing rule**: the trigger family / work category that routes to this agent (one line per agent).
- **Precedence**: when skills or instructions conflict, apply the precedence chain from `system-instructions` v2 (C:/Users/Oz/.zcode/skills/system-instructions/SKILL.md, `## PRECEDENCE RULES`): task-specific skill > family skill > system-instructions > AGENTS.md > harness defaults; duplicate triggers are a lint error.
- **Index**: full catalog listing in `docs/skills/SKILLS.md`.
- **Needs alignment**: findings from cross-checking agent definitions against owned-skill domains; content fixes are scheduled for Phase 2/3 tasks; no agents/skills files modified beyond the 3 restored definitions (fix wave 2026-08-07) and 3 Phase-3 additions (planner, solution-architect, ml-engineer; tasks 3.8/3.9).

## Agents with owned skills (17 of 23)

| Agent | Owned skills | Routing rule |
|---|---|---|
| **api-architect** | `api-design-architect` (1) | API/interface contract work: RESTful/GraphQL/gRPC design, OpenAPI specs |
| **code-implementer** | `concurrency-engineer`, `general-orchestrator`, `github-flow-master`, `java-jvm-expert`, `resilience-pattern-engineer`, `systems-core-architect` (6) | Implementation family: business logic, language/platform work (Java/JVM, systems), git workflows, concurrency, resilience/patterns, orchestration |
| **db-architect** | `database-at-scale`, `query-performance-engineer` (2) | Database family: schema design, query optimization, migrations, replication/sharding |
| **dependency-guardian** | `dependency-supply-chain-guardian` (1) | Dependency family: supply-chain security, license compliance, SBOM |
| **devops-engineer** | `container-optimizer`, `devops-pipeline-engineer`, `incident-response-engineer`, `monorepo-workspace-architect`, `observability-sre` (5) | Production/ops family: Docker/K8s, CI/CD pipelines, monorepo/IaC workflows, incident response, SRE/observability |
| **documentation-engineer** | `readme-architect` (1) | Documentation family: READMEs, API docs, technical writing |
| **mcp-agent** | `mcp-builder` (1) | MCP family: MCP server/tool building and token-heavy MCP operations |
| **performance-engineer** | `performance-profiler` (1) | Performance family: profiling, bottleneck analysis, benchmarking, optimization |
| **refactoring-specialist** | `refactoring-intelligence` (1) | Refactoring family: code smells, SOLID, technical-debt reduction |
| **security-auditor** | `security-hardening-specialist` (1) | Security family: vulnerability scanning, OWASP, secrets detection, hardening |
| **ui-ux-architect** | `animation-web-builder` (1) | UI/UX family: design systems, component architecture, web animation, accessibility |
| **cybersecurity-specialist** | `cybersecurity-specialist` (1) | Cybersecurity family: penetration testing, exploit development, vulnerability research (authorized testing only) |
| **game-developer** | `game-developer`, `roblox-lua-developer` (consolidated from 21 roblox-* skills) (2) | Game-dev family: any game-engine task (Roblox/Luau, Unity, Unreal, Godot) |
| **ml-engineer** | `ml-python-scientist` (1) | ML/data-science family: Python ML, model training/eval, GPU memory, reproducibility, serving |
| **mobile-developer** | `mobile-developer` (1) | Mobile family: React Native, Flutter, native iOS (Swift), native Android (Kotlin) |
| **performance-engineer** | `performance-profiler` (1) | Performance family: profiling, bottleneck analysis, benchmarking, optimization |
| **planner** | `deep-planner` (1) | Planning family: multi-step task decomposition, dependency graphs, estimation, risk registers, plan writing |
| **refactoring-specialist** | `refactoring-intelligence` (1) | Refactoring family: code smells, SOLID, technical-debt reduction |
| **security-auditor** | `security-hardening-specialist` (1) | Security family: vulnerability scanning, OWASP, secrets detection, hardening |
| **solution-architect** | `distributed-systems-engineer`, `system-design-architect` (2) | Architecture family: system design, capacity estimation, ADRs, distributed systems |
| **ui-ux-architect** | `animation-web-builder` (1) | UI/UX family: design systems, component architecture, web animation, accessibility |
| **system** (harness) | `find-skills`, `skill-creator`, `system-instructions` (3) | Meta/doctrine infrastructure: not routed to a subagent; managed by the harness/system itself |

Owned-skill total: 32 (matches skills.json `count`).

## Zero-skill agents

Agents with no owned skills in skills.json:

| Agent | Note |
|---|---|
| **deep-researcher** | no owned skills — QA/research roles consume other skills' verification gates |
| **red-team-qa** | no owned skills — QA/research roles consume other skills' verification gates |
| **accessibility-specialist** | no owned skills — QA/research roles consume other skills' verification gates |
| **data-engineer** | no owned skills — QA/research roles consume other skills' verification gates |
| **test-engineer** | no owned skills — QA/research roles consume other skills' verification gates |
| **browser-automation** | no owned skills — QA/research roles consume other skills' verification gates (not listed in the task brief's zero-skill enumeration; recorded from data — see needs alignment) |

Routing for zero-skill agents: trigger-driven by their definition descriptions (e.g., red-team-qa = pre-commit adversarial review; test-engineer = test authoring; browser-automation = Playwright/Puppeteer ops), never by owned-skill family. Skills in their domains (e.g., roblox-lua-developer's testing/security workflows) remain owned by game-developer (agent file exists since fix wave 2026-08-07).

## Needs-alignment notes (cross-check of agents/*.md vs owned-skill domains)

Cross-checked all 23 agent definitions against the domains of their owned skills. Findings (content fixes in Phase 2/3 — no agents/skills files modified beyond the 3 restored + 3 Phase-3 definitions):

1. **Owner agent files restored/created (RESOLVED)**: `cybersecurity-specialist`, `game-developer`, `mobile-developer` agent definitions were missing while their skills were owned by them; restored in fix wave 2026-08-07. `planner`, `solution-architect`, `ml-engineer` created in Phase 3 tasks 3.8/3.9, closing the sole planned exception (`ml-engineer`). All distinct `owned-by-agent` values now resolve to an `agents/*.md` file or `system` (verified).
2. **mcp-agent**: description covers operating token-heavy MCP tools (Playwright, browser, DB queries); owned skill `mcp-builder` is about building MCP servers. Partial domain mismatch — needs alignment (either description expansion or ownership move).
3. **code-implementer**: description is atomic implementation (business logic, algorithms, API routes); owned skills include `github-flow-master` (git workflow) and `resilience-pattern-engineer` (architecture) — both outside the described implementation scope. Needs alignment (candidate reassignment: devops-engineer / performance-engineer).
4. **ui-ux-architect**: description is design systems/component architecture/accessibility; owned skill `animation-web-builder` (web animation) is adjacent but not explicitly covered. Minor — needs alignment.
5. **devops-engineer**: description covers Docker/K8s/CI-CD/IaC/cloud; owned `monorepo-workspace-architect` (repo structure) is adjacent but not explicit. Minor — needs alignment.
6. **browser-automation**: definition exists with no owned skills; task brief's zero-skill list omitted it. Data-correct listing above; alignment question for Phase 2/3 (reassign none — no browser skill exists in catalog).

## Summary counts

- Skills in catalog: 32 (skills.json `count` = 32).
- Agents with owned skills (files): 17 (api-architect, code-implementer, cybersecurity-specialist, db-architect, dependency-guardian, devops-engineer, documentation-engineer, game-developer, mcp-agent, ml-engineer, mobile-developer, performance-engineer, planner, refactoring-specialist, security-auditor, solution-architect, ui-ux-architect).
- Agent files with zero owned skills: 6 (accessibility-specialist, browser-automation, data-engineer, deep-researcher, red-team-qa, test-engineer).
- Owner labels without agent files: only `system` (harness infrastructure, by design). All other distinct owners resolve to `agents/*.md`; the planned Phase-3 owner exceptions (planner, solution-architect, ml-engineer) are now real agent files.
- Planned Phase-3 owners: 3 (planner, solution-architect, ml-engineer) — all created in tasks 3.8/3.9.
- Needs-alignment items: 6 recorded, 2 resolved (item 1 via fix wave 2026-08-07 + Phase-3 agent creation), 4 open (see section above).
