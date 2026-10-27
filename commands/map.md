---
description: Build a compact symbol map of a repo and orient before any edits (low token cost)
argument-hint: [path] [symbol to focus]
---

Run the map-first orientation protocol (skill: `codebase-navigation`, cost rule: `token-economy`):

1. `python tools/repo_map.py $ARGUMENTS` — structure + symbols in roughly 1-2k tokens.
2. If a symbol or feature is named, add `--focus <name>` for `file:line` hits.
3. Read only the 20-60 lines around each hit (ranged read), never whole files.
4. Write the 10-line navigation map: REPO / RUN / ENTRY / OWNS / TOUCH / CALLERS / TESTS /
   CONVENTIONS / UNKNOWNS.
5. Deep subsystem understanding or a full onboarding brief routes to `codebase-cartographer`.

Target: $ARGUMENTS
