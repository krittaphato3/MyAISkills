# MyAISkills — Ozone Mode World-Class Engineering System

Production-grade AI coding-agent operating system: curated skill catalog, specialized subagents, custom slash commands, MCP integration, and high-performance multi-engine search, built to an **elite Staff+ engineering standard**.

Engineered for **maximum quality with minimal token usage**, enforcing the anti-vibe-coding layer: **Dual-track parallel subagent concurrency, zero-token local defense, domain-first modeling, and anti-slop code hygiene**.

---

## ⚡ Ozone Mode: Core Pillars

1. **Dual-Track Parallel Subagents (Test & Develop Concurrency)**
   Never let an agent write code and then test its own output. For any non-trivial implementation:
   - **Track 1**: Implementer (`code-implementer`) writes the business logic and algorithms.
   - **Track 2**: Test Oracle (`test-oracle`) writes acceptance tests strictly from the specification without seeing the implementation.
   Both subagents are dispatched **simultaneously in parallel within a single turn**.
2. **Zero-Token Local Defense**
   Never waste AI tokens on syntax errors, typos, or lint checks. The local workstation (`tsc --noEmit`, linters, test runners) provides objective truth for **0 tokens**.
3. **Domain-First Modeling (`principle-model-the-domain`)**
   Model state using strict Discriminated Unions and Finite State Machines. Make invalid states mathematically unrepresentable before writing logic.
4. **Anti-Slop (`/unslop`)**
   Aggressively reject AI bloat: delete premature abstractions, remove self-evident comments, avoid unnecessary wrappers, and keep functions tight (<40 lines).
5. **Guard the Context Window (`principle-guard-the-context-window`)**
   Context is finite non-renewable currency. Large scans and verbose logs stay isolated inside subagents; the main thread receives only concise, actionable conclusions.

---

## 🛠️ Repository Layout

```text
skills/           120+ modular skills & playbooks (ozone-mode, tdd, unslop, architect, etc.)
agents/           48 specialized agent definitions (ozone-agent, comment-sicko, code-implementer, ...)
commands/         Custom ZCode slash commands (/ozone-mode, /search, /parallel-dev, /unslop, /tdd, etc.)
tools/            Universal multi-engine web search (web_search.mjs), linters, validators
mcp/              Configured MCP servers (Playwright headless, GitHub, Filesystem)
AGENTS.md         Operating principles, permission matrix, and roster routing
```

---

## 🚀 Slash Commands (`commands/`)

| Command | Usage | Description |
|---|---|---|
| **`/ozone-mode`** | `/ozone-mode [task]` | Activates full Staff-level engineering rigor: domain modeling first, parallel subagents, anti-slop, and zero-token local verification. |
| **`/search`** | `/search <query>` | High-bandwidth multi-engine search across Web (anti-bot bypass), GitHub Repos, NPM Packages, and StackOverflow. |
| **`/parallel-dev`** | `/parallel-dev <spec>` | Launches the dual-track parallel workflow: dispatches `code-implementer` and `test-oracle` simultaneously in a single turn. |
| **`/unslop`** | `/unslop [path/diff]` | Strips AI fluff, deletes dead code, removes obvious comments, and tightens functions under 40 lines. |
| **`/tdd`** | `/tdd <bug or feature>` | Enforces strict Red-Green-Refactor test-driven development. |
| **`/architect`** | `/architect <system>` | System architecture, capacity math, statechart invariants, and ADR before writing code. |
| **`/verify`** | `/verify [scope]` | Verifies deliverables with deterministic local evidence (tests, linters, types). |
| **`/blast-radius`** | `/blast-radius <module>` | Analyzes downstream imports, callers, and regression risks before refactoring. |

---

## 🔍 Universal Web Search Tool (`tools/web_search.mjs`)

Provides instant, anti-bot-immune search and content extraction with zero token bloat:
```bash
# Multi-engine search
node tools/web_search.mjs "zustand state machine typescript"

# Target specific sources
node tools/web_search.mjs "pstack" --type=github
node tools/web_search.mjs "zundo" --type=npm

# Zero-bloat page fetcher (HTML to Markdown)
node tools/web_search.mjs --fetch=https://example.com/docs
```

---

## 🛡️ Operating Doctrine & Quality Gates
- **TDD-first**: Red -> Green -> Refactor.
- **Proof, Not Assertion**: No claim of "done" without attached test, linter, or compiler artifacts.
- **Separation of Duties**: Reviewers and test oracles never edit the artifacts they evaluate.
- **Cost Discipline**: Maximize local zero-token compilers and linters before dispatching AI agents.
