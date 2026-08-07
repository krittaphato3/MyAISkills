# incident-response-engineer — Flagship Eval

## 1. Trigger test

FIRE (5):
1. "Checkout API is returning 100% 5xx and revenue is affected — respond now."
2. "An alert fires above threshold and the page duty is tripping; classify severity and pick who acts first."
3. "Should I roll back the last deploy, ship a forward-fix, or flip a feature flag off?"
4. "Staff a war room for a regional outage and set the comms cadence."
5. "Write a blameless postmortem for this SEV2 and define measurable action-item follow-through."

NOT FIRE (3):
6. "Fix this normal bug in local dev, no customer impact."
7. "Design a scalable architecture for a greenfield service (no live outage)."
8. "Plan capacity for next quarter in staging."

## 2. Quality rubric (1-5)
(a) decision tree covers branches: 5 — SEV classify, containment matrix, rollback vs flag vs forward-fix, escalation runbook.
(b) failure modes have detection + mitigation: 5 — 2+ modes with DETECT/FIX incl. fixing-instead-of-containing, role collision, postmortem blame.
(c) quantitative rules are numbers: 5 — MTTA 10m, containment SEV1 15m/SEV2 60m, burn-rate 2%/5% budgets, 5-15-30.
(d) verification gate executable: 5 — game-day drills, rollback rehearsal, action-item 90% gate, timeline ±2m tolerance.
(e) references authoritative: 4 — Google SRE Book/Workbook, Etsy blameless, PagerDuty all authoritative.
(f) no contradictions: 5 — consistent with observability-sre burn-rate and doctrine; no conflicts.

## 3. Reference task
A production checkout API is at 100% 5xx for 8k users; the last deploy touched auth but is schema-non-reversible. Within 5 minutes the skill must classify SEV (with escalation justice), assign war-room roles, choose the correct contain action (flag-off vs rollback given irreversible schema), pick the 5-15-30 cadence, and detail mitigation + postmortem.
