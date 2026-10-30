---
name: principle-foundational-thinking
description: 'Apply before writing logic: choosing core types and data structures, sequencing scaffold-vs-feature
  work, asking what concurrent actors share. Get the data structures right so downstream code becomes
  obvious.'
metadata:
  version: 1.0.0
  domain: doctrine
  grade: G2
  status: active
  last-reviewed: '2026-10-27'
  owned-by-agent: meta-architect
---


# Foundational Thinking

**Structural decisions** protect option value. **Code-level decisions** protect simplicity. Over-engineering is often a premature decision that closes doors. The right foundational data structure keeps doors open.

**Data structures first.** Get the data shape right before writing logic. The right shape makes downstream code obvious. Define core types early, trace every access pattern, and choose structures that match the dominant paths. A data-structure change late is a rewrite. Early, it is often a one-line diff.

At code level, DRY the structure, not every line. Types and data models should converge. Three similar statements still beat a premature abstraction. Prefer explicit over clever. Test behavior and edge cases, not line counts.

**Concurrency corollary.** Before sharing state between actors, ask "what happens if another actor modifies this concurrently?" If not "nothing", isolate.

**Scaffold first.** If something helps every later phase, do it first. Ask "does every subsequent phase benefit from this existing?" CI, linting, test infrastructure, and shared types are scaffold. Sequence for option value: setup before features, tests before fixes. Keep commits small and single-purpose.

Each increment should land a coherent abstraction or deepen one that exists. Do not spread a new capability across callers as special-case coordination.

Subtraction comes before scaffolding: remove dead weight first, then lay foundations.

## WHEN TO USE

Before writing logic: core types, data structures, sequencing, shared state.

## WHEN NOT TO USE

Core types are settled — other principles take over.

## VERIFICATION GATE

Core types and their invariants named before logic; scaffold-vs-feature order explicit.
