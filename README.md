# MyAISkills

> Enterprise-grade agentic operating system and skills architecture featuring dual-track parallel subagent concurrency, strict verification gates, zero-token local defense, and anti-slop code hygiene.

[![Catalog Version](https://img.shields.io/badge/version-3.16.0-blue.svg?style=flat-square)](AGENTS.md)
[![Skills Count](https://img.shields.io/badge/skills-130%20modular-emerald.svg?style=flat-square)](skills/INDEX.md)
[![Subagents Count](https://img.shields.io/badge/subagents-51%20autonomous-purple.svg?style=flat-square)](agents/)
[![Catalog Lint](https://img.shields.io/badge/catalog%20lint-0%20warnings-brightgreen.svg?style=flat-square)](tools/lint_config.py)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg?style=flat-square)](https://www.python.org/)
[![Node Version](https://img.shields.io/badge/node-18%2B-green.svg?style=flat-square)](https://nodejs.org/)
[![Platform](https://img.shields.io/badge/platform-win32%20%7C%20linux%20%7C%20macos-lightgrey.svg?style=flat-square)](https://github.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

---

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Core Operating Principles (Ozone Mode)](#core-operating-principles-ozone-mode)
  - [1. Dual-Track Parallel Subagents](#1-dual-track-parallel-subagents)
  - [2. Zero-Token Local Defense](#2-zero-token-local-defense)
  - [3. Domain-First Modeling](#3-domain-first-modeling)
  - [4. Anti-Slop Code Hygiene](#4-anti-slop-code-hygiene)
  - [5. Context Window Stewardship](#5-context-window-stewardship)
- [Work Tiers (T0–T3)](#work-tiers-t0t3)
- [Subagent Dispatch Protocol](#subagent-dispatch-protocol)
- [Permission Matrix](#permission-matrix)
- [Repository Structure](#repository-structure)
- [Autonomous Agent Roster (51 Agents)](#autonomous-agent-roster-51-agents)
  - [Orchestration & Quality (10 Agents)](#orchestration--quality-10-agents)
  - [Research & Analysis (10 Agents)](#research--analysis-10-agents)
  - [Implementation (12 Agents)](#implementation-12-agents)
  - [Roblox Game Development (9 Agents)](#roblox-game-development-9-agents)
  - [Production, Security & Delivery (8 Agents)](#production-security--delivery-8-agents)
  - [Specialized Personas (2 Agents)](#specialized-personas-2-agents)
- [Skills Ecosystem (130 Skills)](#skills-ecosystem-130-skills)
  - [Domain Breakdown](#domain-breakdown)
  - [Skill Quality Grades (G1–G3)](#skill-quality-grades-g1g3)
  - [Mandatory Relevance Gate](#mandatory-relevance-gate)
- [Slash Commands & Workflows](#slash-commands--workflows)
- [Tooling Suite & MCP Integrations](#tooling-suite--mcp-integrations)
  - [Zero-Token CLI Utilities](#zero-token-cli-utilities)
  - [Model Context Protocol (MCP) Bridges](#model-context-protocol-mcp-bridges)
  - [Example MCP Configuration](#example-mcp-configuration)
- [Verification & Quality Assurance](#verification--quality-assurance)
  - [Catalog Validation Harness](#catalog-validation-harness)
  - [Standard Definition of Done](#standard-definition-of-done)
  - [Standard Reporting Protocol](#standard-reporting-protocol)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Harness](#running-the-harness)
- [Maintenance & Extension Guide](#maintenance--extension-guide)
  - [Authoring a New Skill](#authoring-a-new-skill)
  - [Authoring a New Subagent](#authoring-a-new-subagent)
  - [Index Synchronization](#index-synchronization)
- [License](#license)

---

## Overview

The **ZCode Autonomous Engineering System** is a production-grade multi-agent operating configuration designed to orchestrate complex software engineering workflows at Staff+ quality. Rather than relying on monolithic, single-prompt LLM execution ("vibe coding"), this system enforces an adversarial, dual-track multi-agent hierarchy governed by deterministic operating rules (`AGENTS.md`), 130 modular skills, and 51 specialized autonomous subagents.

Key engineering capabilities include:
- **Subagent-First Parallelism**: Autonomous decomposition of tasks into concurrent, single-turn subagent dispatches (for example, simultaneous implementation and independent test specification).
- **Strict Verification Gates**: No task is marked complete without deterministic evidence (passing test suites, static analysis logs, or adversarial review verdicts).
- **Context Preservation**: Ranged file reads, zero-token local AST mapping, and subagent sandboxing keep the main orchestrator's context window clean and focused on high-level strategy.
- **Deep Tool & MCP Ecosystem**: Native hooks for Model Context Protocol servers (Playwright headless automation, live Roblox Studio bridge, Office documents, and Jupyter environments).

---

## System Architecture

The following diagram illustrates the interaction between the primary orchestrator, policy rails, subagent pools, toolchains, and verification gates:

```text
+---------------------------------------------------------------------------------------+
|                                    USER INSTRUCTION                                   |
+-------------------------------------------+-------------------------------------------+
                                            |
                                            v
+---------------------------------------------------------------------------------------+
|                             PRIMARY THREAD ORCHESTRATOR                               |
|               - High-level planning & decomposition (deep-planner)                    |
|               - Mandatory Skill loading (§7.1 Relevance Gate)                         |
|               - Context Window Budgeting & ledger maintenance (token-economy)         |
+-------------------+-----------------------------------------------+-------------------+
                    |                                               |
                    v                                               v
+---------------------------------------+       +---------------------------------------+
|              OZONE RAILS              |       |             LOCAL DEFENSE             |
| - Permission Matrix (§3 approval)    |       | - tools/repo_map.py (symbol graph)    |
| - Work Tiers T0-T3 escalation         |       | - tools/lint_config.py (validation)   |
| - Anti-slop & comment trimming        |       | - tools/web_search.mjs & webfetch.mjs |
+-------------------+-------------------+       +-------------------+-------------------+
                    |                                               |
                    +-----------------------+-----------------------+
                                            |
                                            v
+---------------------------------------------------------------------------------------+
|                      PARALLEL SUBAGENT SWARM DISPATCH (Single Turn)                   |
|                                                                                       |
|   +------------------------------------+    +-------------------------------------+   |
|   |         DEVELOPMENT TRACK          |    |            QUALITY TRACK            |   |
|   |   (e.g., code-implementer,         |    |   (e.g., test-oracle,               |   |
|   |    solution-architect, scripter)   |    |    red-team-qa, comment-sicko)      |   |
|   +-----------------+------------------+    +------------------+------------------+   |
|                     |                                          |                      |
|                     | [Writes code & algorithms]               | [Acceptance tests    |
|                     |                                          |  & blind validation] |
|                     v                                          v                      |
|   +------------------------------------+    +-------------------------------------+   |
|   |       PROPOSED IMPLEMENTATION      |    |        INDEPENDENT TEST SUITE       |   |
|   +-----------------+------------------+    +------------------+------------------+   |
+---------------------|------------------------------------------|----------------------+
                      |                                          |
                      +--------------------+---------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
|                                  DETERMINISTIC GATES                                  |
|               - Local Test Runner (pytest, vitest, cargo test, jest)                  |
|               - Zero-Token Typecheck (tsc --noEmit, pyright, mypy)                    |
|               - T2/T3 Critic Verdict (debate-chair adjudication if disputed)          |
+------------------------------------------+--------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
|                                FINAL STRUCTURED REPORT                                |
|                   DONE   ·   CHANGED   ·   VERIFIED   ·   GAPS                        |
+---------------------------------------------------------------------------------------+
```

---

## Core Operating Principles (Ozone Mode)

Ozone Mode provides strict operating rails designed to eliminate common generative AI failure modes such as fabricated assumptions, untested code, bloated commentary, and context exhaustion.

### 1. Dual-Track Parallel Subagents
Never allow an agent to write code and subsequently test its own output. For any non-trivial implementation:
- **Track 1 (Implementation)**: `code-implementer` writes modular business logic, data models, and algorithms according to specifications.
- **Track 2 (Quality & Acceptance)**: `test-oracle` writes independent acceptance tests derived strictly from user requirements, without viewing the implementation code.
- **Single-Turn Dispatch**: Both subagents are triggered simultaneously via concurrent `Agent` tool calls, maximizing execution speed and preventing cognitive bias.

### 2. Zero-Token Local Defense
Never spend LLM tokens or prompt context diagnosing syntax errors, bracket mismatches, or style violations.
- Local compilers, linters, and typecheckers (`tsc --noEmit`, `mypy`, `cargo check`, `ruff`, `eslint`) serve as objective judges.
- Code must compile and pass deterministic linters before proceeding to model review.

### 3. Domain-First Modeling
Following `principle-model-the-domain`:
- Structure systems using strict Discriminated Unions and finite state machines (FSMs).
- Make invalid states mathematically unrepresentable at the type level before implementing business logic.
- Avoid loose strings, primitive obsession, and untyped dictionaries across core boundaries.

### 4. Anti-Slop Code Hygiene
Enforced by `unslop` and `comment-sicko`:
- Functions must remain compact (typically under 40 lines) with a single, clear responsibility.
- Eliminate obvious, narrative, or restating comments (for example, `// increment counter`).
- Reject speculative wrappers, redundant helper abstractions, and unnecessary boilerplate.

### 5. Context Window Stewardship
Enforced by `principle-guard-the-context-window`:
- Model context is a finite resource that degrades with excessive volume.
- Unfocused repository dumps and voluminous log sweeps are restricted to isolated subagents.
- The primary orchestrator maintains an architectural plan, a verification ledger, and concise, high-signal summaries.

---

## Work Tiers (T0–T3)

Tasks are classified into four effort tiers to balance verification depth and computational cost:

| Tier | Category | Operational Scope | Orchestration Model | Relative Cost |
|---|---|---|---|---|
| **T0** | **Direct** | Minor documentation fixes, typos, single-variable renames with zero logic risk. | In-thread resolution or single lightweight subagent. | ~1.0x |
| **T1** | **Verified** | Standard bug fix or feature within an established codebase with existing test coverage. | 1 Implementer (`code-implementer`) + automated test verification suite (`test-engineer`). | ~1.5x |
| **T2** | **Adversarial** | Multi-file changes, unclear root causes, missing test oracles, or performance hot-paths. | Implementer + Independent Critic (`red-team-qa`). Adjudication by `debate-chair` on dispute. | ~2.5x–3.0x |
| **T3** | **Debate** | High-stakes architecture, authentication, billing/payments, data migrations, or security hardening. | 2 Blind Solvers (`code-implementer` + `independent-solver`) + `test-oracle` + `red-team-qa` + `debate-chair`. | ~5.0x–8.0x |

### Escalation Triggers
- Automatic promotion from **T1 to T2**: Tests fail after one automated repair attempt, or implementer and critic disagree on a verifiable fact.
- Automatic promotion from **T2 to T3**: The change directly touches authorization, cryptographic primitives, database migrations, PII storage, or financial calculations.

---

## Subagent Dispatch Protocol

The primary thread acts strictly as an **orchestrator and coordinator**, never as an inline code writer:

1. **Mandatory Skill Loading**: Before taking action, invoke the `Skill` tool for relevant domain and doctrine playbooks (§7.1).
2. **Parallel Dispatch by Default**: When subtasks are orthogonal, dispatch subagents simultaneously in a single turn using multiple `Agent` tool calls.
3. **Strict Separation of Duties**: Subagents with `mode: read-only` evaluate code without modifying it. Reviewers never edit the artifacts they audit.
4. **Isolated Work Contexts**: Long exploratory sweeps are performed inside subagents; the main thread receives only compact, actionable findings.

---

## Permission Matrix

To ensure system integrity, permissions are partitioned into automatic actions and operations requiring explicit user confirmation:

| Action Category | Operations | Permission Level |
|---|---|---|
| **Autonomous Operations** | Reading files, codebase search, running tests/linters, editing project code in scope, starting local preview servers, running `tools/` scripts. | **Allowed** (Standard work) |
| **Version Control Commit** | `git commit` (requires presenting modified files, diff summary, and proposed commit message). | **Explicit Approval Required** (Every time) |
| **Remote VCS Operations** | `git push`, opening pull requests, merging branches, creating git tags or releases. | **Explicit Approval Required** (Separate from commit) |
| **Deployment & Publishing** | Deploying containers, publishing packages to npm/PyPI, publishing sites. | **Explicit Approval Required** (Never bundled with build) |
| **Destructive Operations** | `rm -rf`, `git reset --hard`, `git clean -fdx`, dropping databases, rewriting git history. | **Explicit Approval Required** (Must list all affected assets) |
| **System & Environment** | Modifying global shell configurations, system packages, user credentials, environment secrets. | **Explicit Approval Required** |

---

## Repository Structure

```text
.zcode/
├── AGENTS.md                  # Master governance, operational rules, permissions, and work tiers
├── README.md                  # System documentation and architecture manual
├── commands/                  # 15 interactive slash command definitions
│   ├── algorithms.md          # /algorithms - Complexity analysis & structure selection
│   ├── architect.md           # /architect - Architectural review & ADR drafting
│   ├── blast-radius.md        # /blast-radius - Dependency & impact boundary analysis
│   ├── fetch.md               # /fetch - Readability web scraping utility
│   ├── handoff.md             # /handoff - Structured cross-session context persistence
│   ├── map.md                 # /map - Zero-token AST symbol map generation
│   ├── ozone-mode.md          # /ozone-mode - Activate rigorous verification rails
│   ├── parallel-dev.md        # /parallel-dev - Dual-track concurrent implementation & test
│   ├── product.md             # /product - Product framing & metric validation
│   ├── review.md              # /review - Adversarial diff & code-health review
│   ├── search.md              # /search - Headless multi-engine search CLI
│   ├── tdd.md                 # /tdd - Test-Driven Development execution loop
│   ├── unslop.md              # /unslop - Code bloat and boilerplate reduction pass
│   ├── ux-review.md           # /ux-review - Interactive UI/UX heuristic audit
│   └── verify.md              # /verify - Strict Definition of Done gate validation
├── agents/                    # 51 autonomous subagent specifications
│   ├── code-implementer.md    # Core business logic implementation
│   ├── test-oracle.md         # Independent specification-based acceptance test authoring
│   ├── red-team-qa.md         # Adversarial QA and defect reproduction
│   ├── debate-chair.md        # Impartial adjudicator for competing implementations
│   ├── roblox-scripter.md     # Roblox Luau systems and client-server architecture
│   └── ...                    # 46 additional specialized subagents
├── skills/                    # 130 modular engineering skills across 9 domains
│   ├── INDEX.md               # Automated catalog generated by lint_config.py
│   ├── doctrine/              # Operating doctrines (e.g., verification-before-completion, tdd)
│   ├── architecture/          # System design, ADRs, database scaling, API contracts
│   ├── delivery/              # Web, mobile, UI spacing, refactoring, performance
│   ├── production/            # DevOps, CI/CD, container optimization, observability
│   ├── security/              # Threat modeling, security hardening, compliance
│   ├── fundamentals/          # Algorithms, complexity analysis, data structures
│   ├── languages/             # JVM, Python scientific stack, core systems
│   ├── roblox/                # Studio MCP, Luau architecture, animations, assets
│   └── meta/                  # Catalog maintenance, skill authoring, tool integrations
├── tools/                     # Zero-token local tooling and validation suite
│   ├── lint_config.py         # Catalog validation linter & INDEX.md generator
│   ├── repo_map.py            # AST symbol graph generator (Python, TS, JS, Go, Rust, Luau)
│   ├── web_search.mjs         # Multi-engine search CLI (DuckDuckGo, Bing)
│   ├── webfetch.mjs           # Content extraction and markdown converter CLI
│   └── routing_cases.json     # Regression test cases for agent and skill routing
└── mcp/                       # Model Context Protocol configuration templates
    └── mcp-config.example.json# Example server definitions for external MCP tools
```

---

## Autonomous Agent Roster (51 Agents)

All 51 subagents are defined as isolated Markdown profiles under `agents/` specifying permissions, step limits, and operational boundaries.

### Orchestration & Quality (10 Agents)

| Agent | Mode | Purpose | Primary Dispatch Trigger Clause |
|---|---|---|---|
| `ozone-agent` | writes code | Lead orchestrator implementing Ozone Mode. | Use when leading an end-to-end task under Ozone Mode standards. |
| `comment-sicko` | read-only | Adversarial anti-slop reviewer. | Use when auditing diffs for comment bloat, redundant docs, and AI slop. |
| `planner` | read-only | Goal decomposition, milestone planning, and sequencing. | Use before code on multi-stage or multi-file initiatives. |
| `codebase-cartographer` | read-only | Architectural navigation, entry-point mapping, and symbol indexing. | Use when orienting in an unfamiliar repository or subsystem. |
| `red-team-qa` | read-only | Adversarial testing, edge-case analysis, and bug reproduction. | Use when stress-testing an implementation or challenging a "done" claim. |
| `debate-chair` | read-only | Impartial adjudicator for disputed architectural proposals. | Use when two implementations conflict or reviewers disagree. |
| `requirement-auditor` | read-only | Requirements verification and scope drift auditing. | Use when verifying final deliverables against the initial user prompt. |
| `test-oracle` | writes tests | Independent acceptance test writer working strictly from specifications. | Use under T2/T3 dual-track development to write blind acceptance tests. |
| `independent-solver` | writes code | Secondary blind solution developer for high-stakes implementations. | Use under T3 debates to build an alternative design for comparison. |
| `meta-architect` | writes config | Maintainer of agent configurations, catalog rules, and linting tools. | Use when modifying `AGENTS.md`, `skills/`, or harness tools. |

### Research & Analysis (10 Agents)

| Agent | Mode | Purpose | Primary Dispatch Trigger Clause |
|---|---|---|---|
| `deep-researcher` | read-only | In-depth technical research via web search and documentation retrieval. | Use when researching unfamiliar APIs, vendor specs, or external libraries. |
| `solution-architect` | read/write docs | High-level system design, capacity planning, and ADR authoring. | Use when defining macro-architecture, boundaries, and trade-offs. |
| `api-architect` | writes contracts | REST, GraphQL, gRPC interface contracts and OpenAPI specs. | Use when defining API schemas, versioning strategies, and endpoints. |
| `db-architect` | writes schema | Database schema modeling, migration planning, and indexing strategy. | Use when designing relational schemas, document models, or migrations. |
| `data-engineer` | writes pipelines | Data pipelines, ETL/ELT workflows, and stream processing. | Use when implementing ingestion pipelines, transformations, or batch jobs. |
| `performance-engineer` | writes code | Microbenchmarking, profiling, and algorithmic bottleneck remediation. | Use when measuring and optimizing CPU, memory, or I/O hotspots. |
| `accessibility-specialist` | read-only | WCAG compliance auditing, keyboard navigation, and ARIA semantics. | Use when validating UI accessibility standards and assistive compatibility. |
| `product-strategist` | read-only | Scope refinement, PR/FAQ drafting, and user impact metrics. | Use when evaluating feature tradeoffs, user stories, or product scope. |
| `algorithm-specialist` | read-only | Algorithmic analysis, computational complexity, and invariant proofs. | Use when evaluating hot-path complexity, sorting, graphs, or caching structures. |
| `design-critic` | read-only | Interactive UX audit, layout hierarchy, and microcopy inspection. | Use when auditing live frontend screens, flows, and user interactions. |

### Implementation (12 Agents)

| Agent | Mode | Purpose | Primary Dispatch Trigger Clause |
|---|---|---|---|
| `code-implementer` | writes code | Core business logic, backend services, and application code. | Use when implementing features, bug fixes, or backend services. |
| `ui-ux-architect` | writes UI | Frontend UI design systems, layout rhythm, and component trees. | Use when constructing web interfaces, UI component hierarchies, and styles. |
| `refactoring-specialist` | writes code | Behavior-preserving refactoring with automated test safety nets. | Use when restructuring legacy modules or decomposing monolithic files. |
| `test-engineer` | writes tests | Unit test suites, integration tests, mock harnesses, and CI automation. | Use when authoring unit test suites, regression tests, or fixing test flakes. |
| `integration-engineer` | writes code | Third-party SDK integration, OAuth, payment gateways, and webhooks. | Use when integrating external vendor APIs, webhooks, or identity providers. |
| `llm-engineer` | writes code | RAG pipelines, prompt engineering, agent harnesses, and model evals. | Use when building LLM-powered features, prompt templates, or vector stores. |
| `ml-engineer` | writes code | Machine learning pipelines, model training, evaluation, and inference. | Use when developing statistical models, training scripts, or ML inference. |
| `mobile-developer` | writes code | Native and cross-platform mobile apps (React Native, Flutter, Swift, Kotlin). | Use when writing iOS or Android client applications and mobile screens. |
| `desktop-developer` | writes code | Desktop applications (Electron, Tauri, native desktop frameworks). | Use when developing desktop clients, IPC bindings, or system packages. |
| `game-developer` | writes code | Game mechanics, rendering pipelines, physics, and game engines. | Use when developing gameplay logic in Unity, Unreal, or Godot. |
| `migration-engineer` | writes code | Legacy code modernizations, framework upgrades, and strangler migrations. | Use when upgrading legacy frameworks or modernizing legacy APIs. |
| `documentation-engineer` | writes docs | Technical documentation, architecture guides, API docs, and READMEs. | Use when creating or refining developer documentation and manuals. |

### Roblox Game Development (9 Agents)

| Agent | Mode | Purpose | Primary Dispatch Trigger Clause |
|---|---|---|---|
| `roblox-game-director` | writes code | Macro architecture, milestone sequencing, and specialist coordination. | Use when directing multi-system Roblox development projects. |
| `roblox-scripter` | writes code | Luau systems, network replication, data persistence, and gameplay. | Use when writing client/server Luau modules, remotes, or game mechanics. |
| `roblox-builder` | writes world | Level design, terrain geometry, lighting, and streaming budgets. | Use when building 3D environments, map layouts, or Studio lighting. |
| `roblox-ui-designer` | writes UI | High-polish game interfaces (ViewportFrames, sheen gloss, raybursts). | Use when designing Roblox HUDs, shop interfaces, or inventory screens. |
| `roblox-animator` | writes animation | Character rigs, animation tracks, priorities, markers, and IK. | Use when authoring or configuring character animations and cutscenes. |
| `roblox-vfx-artist` | writes effects | Particle emitters, beams, trails, sound design, and post-processing. | Use when creating combat VFX, environmental particles, or audio effects. |
| `roblox-asset-artist` | writes assets | Mesh import, PBR materials, textures, and Creator Store assets. | Use when sourcing, generating, or texturing 3D assets and PBR materials. |
| `roblox-security-engineer` | read-only | Exploit auditing, remote validation, economy audits, and anti-cheat. | Use when auditing client-server network boundaries for security flaws. |
| `roblox-qa-engineer` | writes tests | Automated Luau unit testing, playtesting, and performance monitoring. | Use when running automated tests or profiling frame performance in Studio. |

### Production, Security & Delivery (8 Agents)

| Agent | Mode | Purpose | Primary Dispatch Trigger Clause |
|---|---|---|---|
| `devops-engineer` | writes infra | CI/CD pipelines, Docker, Kubernetes, Terraform, and deployments. | Use when authoring container builds, CI workflows, or cloud configurations. |
| `security-auditor` | read-only | Defensive code audits, vulnerability scanning, and OWASP mitigation. | Use when auditing codebases for authentication flaws or security vulnerabilities. |
| `cybersecurity-specialist` | read-only | Authorized offensive testing, penetration simulations, and CTF research. | Use when performing authorized penetration testing or attack surface reviews. |
| `compliance-engineer` | writes code/docs | Privacy compliance (GDPR, CCPA), PII audits, and consent controls. | Use when auditing data retention, user consent, or privacy regulations. |
| `dependency-guardian` | read-only | Dependency tree audits, CVE triage, and license compatibility. | Use when upgrading dependencies or assessing supply chain vulnerabilities. |
| `browser-automation` | runs browser | Background headless web searches and automated Playwright workflows. | Use when performing automated web searches or headless scraping. |
| `mcp-agent` | runs MCP | Execution of token-intensive external Model Context Protocol operations. | Use when routing complex, multi-step MCP server interactions. |
| `git-master` | writes git metadata | Branching strategy, structured commit logs, and PR descriptions. | Use when preparing release branches, semantic commit messages, or PR summaries. |

### Specialized Personas (2 Agents)

| Agent | Mode | Purpose | Primary Dispatch Trigger Clause |
|---|---|---|---|
| `poteto-agent` | writes code | Playful yet rigorous implementation agent adhering to Poteto Mode. | Use when engaging poteto-mode doctrine workflows. |
| `general-purpose` | writes code | Fallback general-purpose assistant for tasks outside defined domains. | Use when no specialized subagent matches the given task. |

---

## Skills Ecosystem (130 Skills)

The configuration houses 130 modular skills distributed across 9 functional domains. Every skill provides structured guidance, explicit "when to use" / "when not to use" clauses, and concrete verification gates.

### Domain Breakdown

| Domain | Skill Count | Core Focus | Representative Skills |
|---|---|---|---|
| **doctrine** | 45 | Operating doctrines, mental models, and engineering protocols | `verification-before-completion`, `test-driven-development`, `deep-planner`, `debate-protocol`, `doubt-driven-development`, `unslop` |
| **architecture** | 12 | System boundaries, scalability, interface contracts, and storage | `system-design-architect`, `distributed-systems-engineer`, `database-at-scale`, `api-design-architect`, `adr-engineering` |
| **delivery** | 27 | Web engineering, UI layout hierarchy, mobile, and refactoring | `frontend-web-engineer`, `ui-layout-spacing`, `refactoring-intelligence`, `accessibility-audit`, `web-performance` |
| **production** | 14 | Operational stability, CI/CD pipelines, and observability | `devops-pipeline-engineer`, `container-optimizer`, `observability-sre`, `incident-response-engineer`, `dependency-supply-chain-guardian` |
| **security** | 4 | Defensive hardening, compliance, and threat mitigation | `threat-modeling`, `security-hardening-specialist`, `privacy-compliance`, `cybersecurity-specialist` |
| **fundamentals** | 1 | Mathematical foundations and core computer science | `algorithms-and-data-structures` |
| **languages** | 4 | Language runtimes and specialized platform idioms | `java-jvm-expert`, `ml-python-scientist`, `systems-core-architect`, `typescript-best-practices` |
| **roblox** | 14 | Studio MCP loop, Luau development, and game production | `roblox-studio-mcp`, `roblox-scripting`, `roblox-testing`, `roblox-toolchain`, `roblox-ui-ux`, `roblox-project-indexer` |
| **meta** | 9 | Catalog validation, search tooling, and harness maintenance | `agent-config-maintenance`, `browser-automation`, `web-search`, `find-skills`, `mcp-builder` |

### Skill Quality Grades (G1–G3)

Each skill is graded to establish its operational rigor:
- **G1 (Informational / Guidelines)**: Conceptual reference, terminology guides, and high-level best practices.
- **G2 (Playbook / Checklist)**: Step-by-step procedures, actionable checklists, and structured execution templates.
- **G3 (Enforced Doctrine)**: Rigorous protocols equipped with mandatory pre-conditions, anti-patterns, and hard verification gates.

### Mandatory Relevance Gate

Under `AGENTS.md` §7.1, the primary thread must invoke the `Skill` tool before initiating work:

| Work Category | Mandatory Core Skill | Mandatory Safety Rail | Objective |
|---|---|---|---|
| **Feature Development / Bug Fix** | `test-driven-development` | `verification-before-completion` | Enforces Red-Green-Refactor loop and requires reproducible verification. |
| **Web / UI / Frontend Work** | `frontend-web-engineer` | `ui-layout-spacing` | Enforces responsive layout, spatial mathematical rhythm, and accessible markup. |
| **Roblox Studio Development** | `roblox-scripting` | `roblox-studio-mcp` | Adheres to Roblox Studio engine budgets and safe DataModel manipulation. |
| **Security Auditing** | `threat-modeling` | `security-hardening-specialist` | Identifies attack vectors and applies defensive mitigations. |
| **Multi-Domain Work** | `general-orchestrator` | `verification-before-completion` | Coordinates multiple subagent waves with per-phase verification gates. |

---

## Slash Commands & Workflows

Interactive slash commands (stored in `commands/`) provide rapid shortcuts for common engineering workflows:

| Slash Command | Argument Hint | Description | Target Agent / Skill |
|---|---|---|---|
| `/ozone-mode` | `[task description]` | Activates Ozone Mode strict verification rails for the current session. | `ozone-agent` / `ozone-mode` |
| `/parallel-dev` | `<specification>` | Dispatches dual-track parallel subagents for simultaneous implementation and acceptance testing. | `code-implementer` + `test-oracle` |
| `/tdd` | `<feature or bug>` | Initiates a strict Test-Driven Development red-green-refactor cycle. | `code-implementer` / `tdd` |
| `/verify` | `[artifact or target]` | Executes strict Definition of Done verification against touched files. | `red-team-qa` / `verification-before-completion` |
| `/unslop` | `[file or directory]` | Scans and cleans AI bloat, over-commenting, and speculative abstractions. | `comment-sicko` / `unslop` |
| `/review` | `[diff or file path]` | Runs an adversarial code-health review on uncommitted changes. | `red-team-qa` / `doubt-driven-development` |
| `/map` | `[path] [symbol]` | Generates a compact AST symbol map of the repository with zero token overhead. | `codebase-cartographer` / `tools/repo_map.py` |
| `/blast-radius` | `<module path>` | Analyzes downstream dependency impact and regression risks prior to edits. | `codebase-cartographer` / `blast-radius` |
| `/architect` | `<system name>` | Drafts an architectural design, state invariants, and ADR before writing code. | `solution-architect` / `adr-engineering` |
| `/product` | `<feature idea>` | Evaluates user value, core problem framing, slice sizing, and success metrics. | `product-strategist` / `product-engineering` |
| `/algorithms` | `<module or path>` | Performs computational complexity and data structure analysis for hot paths. | `algorithm-specialist` / `algorithms-and-data-structures` |
| `/ux-review` | `[screen or flow]` | Audits interface usability, states, keyboard navigation, and spatial rhythm. | `design-critic` / `ux-review` |
| `/search` | `<query>` | Executes a headless, multi-engine web search without consuming model context. | `browser-automation` / `tools/web_search.mjs` |
| `/fetch` | `<url>` | Fetches a webpage and extracts clean information (prioritizes ZCode native WebFetch; falls back to CLI). | Native `WebFetch` / `webfetch.mjs` |
| `/handoff` | `[output path]` | Generates a structured handoff artifact to resume work in a new session. | `meta-architect` / `session-continuity` |

---

## Tooling Suite & MCP Integrations

### Zero-Token CLI Utilities

The `tools/` directory provides zero-token utilities that run locally to inspect, navigate, and validate code without wasting model tokens:

1. **`tools/repo_map.py`**:
   - High-speed AST and regular-expression symbol indexer.
   - Parses Python, TypeScript, JavaScript, Go, Rust, and Luau files.
   - Extracts top-level classes, exported functions, interfaces, and signatures while ignoring test fixtures and build artifacts.
   - Usage:
     ```bash
     python tools/repo_map.py .
     python tools/repo_map.py src/ --focus AuthService
     ```

2. **`tools/lint_config.py`**:
   - Comprehensive validation harness for the skill and agent catalog.
   - Validates frontmatter schemas, link integrity, description triggers, and routing fixtures.
   - Usage:
     ```bash
     python tools/lint_config.py          # Validate and print report
     python tools/lint_config.py --strict # Fail on any warning
     python tools/lint_config.py --write-index # Synchronize skills/INDEX.md
     ```

3. **`tools/web_search.mjs`**:
   - Zero-token multi-engine CLI search utility supporting DuckDuckGo and Bing.
   - Returns structured JSON or Markdown summaries for offline analysis.
   - Usage:
     ```bash
     node tools/web_search.mjs "Roblox Luau parallel actor memory limits"
     ```

4. **`tools/webfetch.mjs` (Portable Fallback Fetcher)**:
   - Zero-dependency headless content extraction script using Readability-style heuristics.
   - Whenever the host harness provides a native `WebFetch` tool, it must be used instead due to superior token efficiency and caching; `webfetch.mjs` serves as the portable fallback for non-native environments or specialized CLI piping.
   - Usage:
     ```bash
     node tools/webfetch.mjs "https://create.roblox.com/docs/reference/engine/classes/Actor"
     ```

### Model Context Protocol (MCP) Bridges

The system connects to external environments via standardized MCP servers:
- **Roblox Studio MCP**: Facilitates bi-directional communication with active Roblox Studio sessions. Enables live Luau script execution (`execute_luau`), scene tree traversal (`search_game_tree`), instance inspection (`inspect_instance`), multi-file edits (`multi_edit`), and screen capture.
- **Playwright MCP**: Provides background headless browser automation, accessibility snapshot capture, and DOM interaction testing without UI overhead.
- **Office Document Suite MCP**: Programmatic reading, querying, and rendering of `.docx` documents, `.xlsx` spreadsheets, `.pptx` presentations, and `.pdf` files.
- **Jupyter Notebook MCP**: Manages local and remote Jupyter kernels, enabling code execution, cell manipulation, and data science workflows.

### Example MCP Configuration

A template configuration is provided in `mcp/mcp-config.example.json`:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest", "--headless", "--isolated", "--caps", "vision"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "REPLACE_WITH_YOUR_TOKEN"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\Username"]
    }
  }
}
```

---

## Verification & Quality Assurance

### Catalog Validation Harness

All agent profiles, skills, and routing cases are subject to automated verification through `tools/lint_config.py`. The catalog maintains a strict **zero-warning standard**:

```bash
$ python tools/lint_config.py --strict
skills: 130   agents: 51

clean (0 warning(s))
```

Validation criteria checked by the harness:
- **Frontmatter Conformance**: Every skill must define `version`, `domain`, `grade`, `status`, `last-reviewed`, and `owned-by-agent`.
- **Trigger Clause Quality**: Descriptions must include an actionable trigger clause (`Use when...`, `Use for...`, `Use before...`).
- **Required Sections**: Every skill must include `## WHEN TO USE`, `## WHEN NOT TO USE`, and `## VERIFICATION GATE`.
- **Link Integrity**: All relative Markdown links between skills, agents, and tools are resolved and checked for broken references.
- **Routing Accuracy**: Validates sample routing queries against `tools/routing_cases.json`.

### Standard Definition of Done

Under `AGENTS.md` §8, work is declared complete only when every applicable criteria is verified with tangible evidence:

- [ ] **Requirements Satisfied**: All explicit requirements from the user request are completed.
- [ ] **Scope Bound**: No unrequested features, speculative abstractions, or out-of-scope edits introduced.
- [ ] **Mandatory Skills Loaded**: Relevant domain and safety skills invoked via the `Skill` tool prior to action.
- [ ] **Subagents Delegated**: Non-trivial implementation dispatched to subagents; parallel subagents dispatched in single turn.
- [ ] **Deterministic Proof**: Automated tests pass (unit, integration, or end-to-end), demonstrating red-to-green progression.
- [ ] **Static Analysis Clean**: Linting and typechecks pass with zero errors on all touched files.
- [ ] **Adversarial Audit**: T2/T3 changes audited by independent critic (`red-team-qa`) with attached verdict.
- [ ] **Sanitized Artifacts**: No secrets, temporary files, or unneeded debug statements committed.
- [ ] **User Authorization**: Explicit permission received for any git commit, push, or destructive action.

### Standard Reporting Protocol

Turn completions and milestone deliveries must follow this standardized reporting format:

```text
DONE      Summary of newly working functionality or completed deliverables.
CHANGED   Bulleted list of modified files grouped by architectural layer.
VERIFIED  Exact test commands run, exit codes, and output logs.
GAPS      Known limitations, deferred items, or decisions requiring user confirmation.
```

---

## Getting Started

### Prerequisites

Ensure the following tools are installed on your workstation:
- **Python**: Version 3.10 or higher (required for `repo_map.py` and `lint_config.py`).
- **Node.js**: Version 18.0.0 or higher with `npm` (required for search and fetch CLI tools).
- **Git**: Configured for command-line access.
- **PyYAML**: Required by the catalog linter (`pip install pyyaml`).

### Installation

1. Navigate to your local ZCode configuration directory:
   ```bash
   cd ~/.zcode
   ```

2. Install Python dependencies:
   ```bash
   pip install pyyaml
   ```

3. Configure Model Context Protocol servers:
   ```bash
   cp mcp/mcp-config.example.json mcp/mcp-config.json
   ```
   *Edit `mcp/mcp-config.json` with your preferred API keys and local workspace paths.*

### Running the Harness

Verify that the local configuration passes all validation checks:

```bash
# 1. Run strict catalog validation
python tools/lint_config.py --strict

# 2. Test AST symbol map extraction
python tools/repo_map.py .

# 3. Test headless documentation search
node tools/web_search.mjs "ZCode operating system"
```

---

## Maintenance & Extension Guide

### Authoring a New Skill

1. Create a directory under `skills/<domain>/<skill-name>/` with a `SKILL.md` file.
2. Include the required YAML frontmatter:
   ```yaml
   ---
   name: your-skill-name
   description: Brief summary explaining what the skill provides. Use when <explicit trigger scenario>.
   metadata:
     version: 1.0.0
     domain: delivery
     grade: G2
     status: active
     last-reviewed: 2026-10-27
     owned-by-agent: code-implementer
   ---
   ```
3. Structure the document with the required sections:
   ```markdown
   # Skill: your-skill-name

   ## OVERVIEW
   ...

   ## WHEN TO USE
   ...

   ## WHEN NOT TO USE
   ...

   ## PROTOCOL & EXECUTION
   ...

   ## VERIFICATION GATE
   ...
   ```

### Authoring a New Subagent

1. Create a Markdown file in `agents/<agent-name>.md`.
2. Include the required subagent frontmatter:
   ```yaml
   ---
   name: your-agent-name
   description: Core responsibility summary. Use when <trigger scenario>.
   mode: subagent
   permission:
     edit: allow # or deny for read-only reviewers
   steps: 30
   ---
   ```
3. Detail the subagent's role, operational boundaries, required skills, and output formatting.

### Index Synchronization

Whenever you add, modify, or deprecate a skill or agent, synchronize the catalog index:

```bash
python tools/lint_config.py --write-index
```

The script will automatically update `skills/INDEX.md` and report any validation issues.

---

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
