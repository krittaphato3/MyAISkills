---
name: learner
description: >-
  Researches unfamiliar technologies, undocumented APIs, or novel domains and synthesizes a reusable,
  battle-tested skill before implementation. Use when encountering a technology, library, framework, or
  architecture the agent has little or no prior experience or skill for. Routes standard skill authoring
  to skill-creator and pure external search to web-search.
metadata:
  version: 1.0.0
  domain: meta
  grade: G2
  status: active
  last-reviewed: '2026-10-31'
  owned-by-agent: deep-researcher
---

# Learner

Do not guess an unfamiliar API, framework, or execution model. Trial-and-error in production code
burns tokens and breeds slop. When encountering unknown territory, stop, research canonical sources,
run an isolated verification spike, and codify the patterns into a durable skill before writing
application logic.

## WHEN TO USE

- The task involves a library, SDK, framework, or tool not covered by the existing skill catalog.
- The agent is uncertain about runtime semantics, lifecycle hooks, wire formats, or error behaviors.
- The codebase uses a proprietary or internal architecture with no public training data.
- The user asks to "learn how X works and build Y" or "research X before implementing".

## WHEN NOT TO USE

- Standard domain tasks covered by existing skills (routes to matching domain skill).
- The user is asking to build or refine an interactive skill via conversation (routes to `skill-creator`).
- Pure factual lookup without implementation intent (routes to `web-search`).
- Debugging an existing codebase using known technologies (routes to `systematic-debugging`).

## DECISION TREE

```text
1. IDENTIFY THE KNOWLEDGE GAP
   List exact unknowns: runtime contracts, configuration schema, error types, boundaries.
   Do not start implementation while core contracts remain speculative.

2. GROUND ON CANONICAL SOURCES
   - Official documentation via native WebFetch (prioritize docs, guides, API specs).
   - Source code and type definitions (`.d.ts`, interface files, package exports).
   - Official minimal examples or test suites in the upstream repository.

3. EXECUTE AN ISOLATED SPIKE
   Write a standalone 10-line probe script or test in an isolated scratchpad.
   Verify observable reality: does it return what the docs promised? How does it fail?

4. CODIFY INTO A REUSABLE SKILL
   Create `skills/<domain>/SKILL.md` (or workspace local guide) documenting:
   - Mental model and strict invariants
   - Idiomatic usage patterns
   - Critical failure modes & what breaks
   - Verification recipe (exact test commands)

5. TRANSITION TO IMPLEMENTATION
   Invoke the new skill. Proceed under `ozone-mode` and `test-driven-development` with full gates.
```

## FAILURE MODES & MITIGATIONS

| Failure Mode | Mitigation |
|---|---|
| Hallucinating APIs or options | Read official `.d.ts` or docs before calling any function. |
| Over-abstracting the learned skill | Document only what was proven in the spike; omit speculative extras. |
| Learning in production code | Always run the probe in an isolated script, never the application target. |
| Abandoning the knowledge after the turn | Save the verified patterns to `skills/` or project docs for reuse. |

## VERIFICATION GATE

- [ ] Canonical documentation or type definition was read directly via `WebFetch` or file read.
- [ ] An isolated spike verified runtime behavior before production edits were attempted.
- [ ] The generated skill has clear `WHEN TO USE`, `WHEN NOT TO USE`, and concrete code examples.
- [ ] `python tools/lint_config.py` passes cleanly if registered in `skills/`.

## REFERENCES

- `skills/skill-creator/SKILL.md` — Authoring and benchmarking skills
- `skills/source-driven-development/SKILL.md` — Deriving truth from source code
- `skills/ozone-mode/SKILL.md` — Engineering router and execution tiers
