# doubt-driven-development — Flagship Eval

## 1. Trigger test

Fire (5):
1. "Review this concurrency change for data-race / deadlock edge cases pre-merge."
2. "Fresh-context audit a 'done' claim on a subsystem whose correctness depends on many interacting choices."
3. "A change was written by the author or long ago — I need independence from that bias."
4. "This solution works for the happy path tested but has not been challenged on edge/invariant/integration boundaries."
5. "Pre-deploy review of a claim that will cost money/time/trust if wrong — attack it adversarially."

Not fire (3):
6. "A one-line constant change already covered by CI unit tests."
7. "A throwaway script with a one-day half-life and no live claim."
8. "Reviewing merely to appear diligent when there is no claim to attack."

## 2. Quality rubric (1-5)
(a) decision tree covers branches: 5/5 — fresh-context→claim→extract→doubt (≥3 vectors)→reconcile→stop/escalate, never skip.
(b) failure modes have detection+mitigation: 5/5 — rubber-stamp, no-fresh-context, style-attack, false-positive-on-verified, missing-integration-risk, deferred-defects all DETECT/FIX.
(c) quantitative rules are numbers: 5/5 — one-claim-per-pass, ≥3 vectors, ≥80% escalation cutoff, 20-30min timebox.
(d) verification gate executable: 5/5 — connection-check, evidence-check, disposition-check, gate-fails conditions; record claim+inventory+vectors+dispositions.
(e) references authoritative: 4/5 — grounded in red-team-qa gate, requesting-code-review, WORKFLOW; the adversarial-review/Microsoft norm is a secondary-style reference.
(f) no contradictions: 5/5 — feeds red-team-qa gate, consistent with requesting-code-review and WORKFLOW review gates.

## 3. Reference task
Pre-merge, review a change claimed to fix a cache race without breaking idempotency. The skill must produce a single core claim, an assumption inventory (single-writer, TTL≥latency, ordering), attack with ≥3 vectors, match each to evidence, and escalate only defects that land at ≥80% confidence.
