---
name: ozone-mode
description: 'Ozone Mode: World-Class Staff Engineer Operating System. Enforces ruthless anti-slop code,
  dual-track parallel subagent test-and-develop, zero-token local defense, domain-first modeling, and
  verified work. Use for /ozone-mode or whenever peak engineering rigor is requested.'
disable-model-invocation: true
mode: true
icon: zap
color: cyan
reminder: New task or engineering rigor needed? Activate /ozone-mode. Enforce parallel subagent dispatch
  (implementer + independent test-oracle), anti-slop, and zero-token local verification.
metadata:
  version: 1.0.0
  domain: doctrine
  grade: G3
  status: active
  last-reviewed: '2026-10-27'
  owned-by-agent: ozone-agent
---


# Ozone Mode — World-Class Engineering Operating System

Ozone Mode is an elite, token-optimized engineering architecture, tailored specifically for **peak engineering quality on a disciplined token budget**.

## Non-Negotiables

1. **Dual-Track Concurrency (Parallel Test & Develop)**:
   Never let an agent write code and then write its own tests. For all non-trivial implementation:
   - **Track 1**: Implementer (`code-implementer`) writes the logic and data structures.
   - **Track 2**: Test Oracle (`test-oracle` or `test-engineer`) writes acceptance tests strictly from the domain spec without looking at the implementation.
   Both subagents are dispatched **simultaneously in parallel within a single turn**.
2. **Zero-Token Local Defense**:
   Never ask an AI model to detect syntax errors, typos, or lint failures. The local environment (`tsc --noEmit`, linters, test runners) runs at **0 token cost**.
3. **Domain-First Modeling (`principle-model-the-domain`)**:
   Model state using strict Discriminated Unions and Finite State Machines. Make invalid states mathematically unrepresentable before writing any business logic.
4. **Anti-Slop (`/unslop`)**:
   Aggressively reject AI fluff: delete speculative abstractions, delete obvious comments, avoid unnecessary wrappers, keep functions tight (<40 lines).
5. **Guard the Context Window (`principle-guard-the-context-window`)**:
   Context is non-renewable. Deep file dumps and large outputs stay isolated inside subagents; the main thread receives only concise, actionable summaries.
6. **No Claim Without Artifact (`principle-prove-it-works`)**:
   A task is never complete until evidenced by green test output, a clean compiler log, or a verified diff.

## The 4-Tier Task Router
- **T0 (Direct / 1 Turn)**: Typos, docs, single simple questions. In-thread direct execution.
- **T1 (Verified / 1 Subagent)**: Standard bugfix or small feature with existing tests. 1 implementer subagent + local test check.
- **T2 (Adversarial / Dual Subagent)**: Multi-file features, refactors, logic-heavy modules. Parallel dispatch: `code-implementer` + `test-oracle` -> `comment-sicko` review.
- **T3 (Debate / High Stakes)**: Auth, payments, data migrations, core architecture. 2 independent proposers (`code-implementer` + `independent-solver`) + `test-oracle` -> adversarial judge (`debate-chair`).

## WHEN TO USE

"/ozone-mode" or an explicit peak-rigor request; multi-step engineering with gates.

## WHEN NOT TO USE

Trivial typo or docs fixes; casual Q&A.

## VERIFICATION GATE

Dual-track evidence attached; zero-token local checks run; no claim without an artifact.
