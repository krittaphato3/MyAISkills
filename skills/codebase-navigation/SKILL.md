---
name: codebase-navigation
description: >-
  Finds and understands code fast in an unfamiliar or large repository: entry points, call
  graphs, conventions, test/build commands, blast radius, and reading order before editing. Use
  when onboarding onto a repo, when you need to know where a behavior lives, or before changing
  code whose callers are unknown. Whole-architecture mapping with a written brief routes to the
  codebase-cartographer agent; debugging a specific failure routes to systematic-debugging.
metadata:
  version: 3.0.0
  domain: delivery
  grade: G2
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: codebase-cartographer
---

# Codebase Navigation

Most wrong edits are navigation failures: the agent changed the file it found first, not the file
that owns the behavior. This skill is the reading discipline that turns "I think it's in here
somewhere" into a located symbol, its callers, its tests, and its conventions — before any edit.

## WHEN TO USE

- First contact with a repository, or first contact with an unfamiliar subsystem.
- "Where is X handled?" / "what calls this?" / "is this used anywhere?".
- Before changing a shared function, type, config key, or route.
- When a search returns 40 hits and you need to know which ones matter.

## WHEN NOT TO USE

- You already know the file and the change is local — go edit it.
- The question is *why* something fails — `systematic-debugging` (reproduce first, then navigate).
- The deliverable is a full architecture map for other agents — dispatch `codebase-cartographer`.
- Generated/vendored code — read the generator or the upstream, not the output.

## DECISION TREE

```text
1. ORIENT (≤5 minutes, no edits)
   Read: README, package/build manifest, directory tree at depth 2, CI config, AGENTS.md/docs.
   Record: language(s), framework + version, package manager, test command, lint command,
   entry points, and where business logic lives vs where glue lives.

2. LOCATE THE BEHAVIOR
   a. Exact identifier?  → definition search (rg "def |function |class |const X =")
   b. User-visible string/route? → search the literal, then trace to its handler
   c. Concept only? → search 2-3 synonyms, then grep the test names (tests name behavior)
   d. Nothing? → check generated code, config, or a different service. Widen once, then ask.

3. TRACE THE BLAST RADIUS
   For the symbol you will touch: find callers, implementations/overrides, tests, fixtures,
   schema/config references, and public exports. If it crosses a package boundary, say so.
   Rule: unknown callers = not ready to edit.

4. ABSORB LOCAL CONVENTIONS
   Copy the nearest working example instead of inventing a pattern: naming, error handling,
   logging, result types, file layout, test style, import order. Three examples beat one rule.

5. READ IN RINGS
   symbol → containing file → its imports/exports → immediate callers → tests → docs.
   Stop when the next read cannot change the change you are about to make.

6. WRITE THE MAP DOWN
   Produce the 10-line map (PATTERNS §1) before editing or dispatching. It becomes the brief.
```

## PATTERNS

### 1. Navigation map (the artifact)
```text
REPO: {name}   Stack: {lang/framework + version}   Pkg: {manager}
RUN:   {install} / {dev} / {test} / {lint} / {typecheck}
ENTRY: {files/routes}
OWNS:  {behavior → file:symbol}
TOUCH: {file:symbol — why}          # the planned edit
CALLERS: {symbol → files}            # blast radius
TESTS: {paths covering TOUCH}
CONVENTIONS: {3 concrete rules observed in code}
UNKNOWNS: {what to verify before editing}
```

### 2. Search ladder
1. `rg -n "\bSymbol\b"` — definitions and uses in one pass.
2. Definition-shaped patterns: `class X`, `def x`, `function x`, `type X`, `interface X`.
3. Route/string literals from the UI or API.
4. Test names — they describe intended behavior, not implementation.
5. `git log -S"symbol"` — when and why it appeared; often the best design doc.
6. `git blame` on the exact line — the commit message is the rationale.

### 3. Blast-radius check
Before editing a shared symbol, list: direct callers · indirect callers (one hop) · tests ·
serialized shapes (DB/JSON/API) · config keys · docs. If any list is unknown, you are guessing.
Rename/move operations need this even more than logic edits.

### 4. Conventions over preferences
The repo's existing pattern wins over your taste. If the codebase uses `Result` types, do not
throw. If it uses server actions, do not add a REST client. If conventions are genuinely harmful,
raise it once as a proposal — do not unilaterally refactor while implementing a feature.

### 5. Cheap structural queries
- Dependencies: read the manifest, not the imports.
- Boundaries: look for workspace config, path aliases, and lint rules (`no-restricted-imports`).
- Dead code: search the symbol with zero non-test hits; confirm with the bundler's tree-shake
  report rather than assuming.
- Data shape: schema/migrations/types first; implementations later.

## FAILURE MODES & MITIGATIONS

1. **First-hit editing** — patching the first grep match. *DETECT:* the changed file has no callers,
   or a duplicate implementation exists. *FIX:* run the search ladder to definitions, then blast radius.
2. **Vendored trap** — editing `node_modules`, `dist`, or generated files. *DETECT:* path contains
   build output or a "generated" banner. *FIX:* change the source/generator instead.
3. **Convention drift** — a new pattern appears for one change. *DETECT:* reviewer asks "why is this
   different from the rest?". *FIX:* copy the nearest example or get explicit agreement.
4. **Phantom usage** — assuming a symbol is unused because one search missed it. *DETECT:* runtime
   break in an untested path. *FIX:* search tests, config, dynamic imports, and string references.
5. **Map without verification** — a written map that was never checked against the code. *DETECT:*
   paths in the map do not exist. *FIX:* every line in the map cites a real path.
6. **Reading forever** — endless exploration with no edit. *DETECT:* >10 reads with no hypothesis.
   *FIX:* write the 10-line map and start; unknowns become explicit checks.

## QUANTITATIVE RULES

- Orientation ≤5 minutes / ≤5 tool calls before the first hypothesis.
- Stop reading when the next read cannot change the planned edit.
- Blast radius: list every direct caller before touching a shared symbol; >10 callers means plan a
  migration, not an edit.
- Navigation map ≤15 lines; it must fit in a subagent brief.
- One subsystem per navigation pass; do not map the whole monorepo to fix one handler.

## VERIFICATION GATE

- [ ] The target behavior is located by symbol (file:line), not by guess.
- [ ] Test/lint/build commands were read from the repo, not assumed.
- [ ] Blast radius is enumerated for every shared symbol being changed.
- [ ] At least one local convention was copied from existing code and named.
- [ ] The map's paths all exist; unknowns are listed as checks, not ignored.

## REFERENCES

- `codebase-cartographer` (agent) — produces the full onboarding brief
- `systematic-debugging` — when the navigation question is really a failure question
- `source-driven-development` — verifying framework behavior against current docs
- `refactoring-intelligence` — structural changes once the map is known
