# adr-engineering — Flagship Eval

## 1. Trigger test

Fire (5):
1. "Record the storage-engine choice with its trade-offs as an ADR before it becomes irreversible."
2. "Change an API surface (request/response shape) where downstream callers depend on it."
3. "Document a non-obvious invariant the code cannot express inline."
4. "A trade-off several contributors will influence now or in six months — write it as a decision."
5. "Reverse a decided behavior deliberately and keep the reasoning visible (supersede the old ADR)."

Not fire (3):
6. "An in-process constant / loop structure / naming micro-choice — no ADR needed."
7. "Docs for a decision being reworked daily this sprint — let the implementation land first."
8. "A decision already locked with no plausible rejected alternative — just a note, not an ADR."

## 2. Quality rubric (1-5)
(a) decision tree covers branches: 5/5 — classify (≥2 alternatives / irreversible), write-template, register, keep-fresh, document-discoverability.
(b) failure modes have detection+mitigation: 5/5 — never-accepted ADRs, doc-code drift, wrong place, stub docs, ADR-as-bureaucracy, status-not-updated all DETECT/FIX.
(c) quantitative rules are numbers: 5/5 — 1-2 pages scope, ≥2 rejected alternatives, same-PR freshness, re-walk on trigger.
(d) verification gate executable: 5/5 — ADR checklist (context/decision/alternatives/consequences/status/superseded-chain), freshness, discoverability; gate fails on missing field.
(e) references authoritative: 4/5 — Nygard (originator), RFC 2119, system-design-architect, documentation-engineer; strong but sparse.
(f) no contradictions: 5/5 — consistent with system-design-architect ADR format; no conflict.

## 3. Reference task
Choose a storage engine for a new service with real alternatives (relational vs columnar vs document) and record an ADR: status proposed, context with numbers, one decisive decision, consequences including what is given up, and ≥2 rejected alternatives with evidence. The skill must also register it and set the freshness rule for future PRs.
