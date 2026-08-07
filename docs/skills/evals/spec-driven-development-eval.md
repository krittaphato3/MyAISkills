# spec-driven-development — Flagship Eval

## 1. Trigger test

Fire (5):
1. "A feature about half a day or more of work needs a PRD before any code (objectives, commands, structure, testing, boundaries)."
2. "This flow will be invoked repeatedly by other agents — it needs a written contract."
3. "Multi-party work with a requester, implementer, and reviewer — the PRD is the shared reference."
4. "The ask is underspecified and needs the concrete shape decided before build."
5. "Anything a reviewer will gate benefits from a spec the review can check against."

Not fire (3):
6. "A one-line config fix with an obvious shape — no PRD needed."
7. "A timeboxed exploration spike with an explicit stop condition and no production contract."
8. "A pure mechanical rename/format refactor where the diff explains itself."

## 2. Quality rubric (1-5)
(a) decision tree covers branches: 5/5 — intent-confirm gate, objectives, commands/UX, structure, testing, sign-off, build-then-trace.
(b) failure modes have detection+mitigation: 5/5 — underspecified-criteria, scope-creep, PRD-vs-code drift, no-boundaries, gold-plating, reviewer-rubber-stamp all DETECT/FIX.
(c) quantitative rules are numbers: 5/5 — 1-page 15-25 bullets, 100% testable criteria, slice S=0.5-1d, 100% traceability, 0 code before sign-off, version-bump revision.
(d) verification gate executable: 5/5 — objective-testable, boundaries-explicit, commands-exact, testing-stated, reviewer-approved, output-shape no-blank.
(e) references authoritative: 5/5 — addyosmani/agent-skills spec-driven, requirements-elicitation, INVEST, ATDD, vertical slicing all canonical.
(f) no contradictions: 5/5 — consistent with deep-planner sizing, requirements-elicitation handoff; no doctrine conflict.

## 3. Reference task
A request for a "notification feature" (half a day to a few days) needs a one-page PRD with measurable objectives, user stories, acceptance criteria mapped to tests, explicit out-of-scope, and recorded sign-off before any code. The skill must produce that PRD and refuse code before sign-off.
