# observability-sre — Flagship Eval

## 1. Trigger test

Fire (5):
1. "Define the SLI and SLO + error budget for our checkout service (target P95 300ms, SLO 99.9%)."
2. "Turn 'alert me when it breaks' into a burn-rate alert rule against an SLO, not a static threshold."
3. "Choose the four golden signals that matter for this service and map them to decisions."
4. "Build the metrics/logs/traces pipeline and pick a sampling scheme for a request path."
5. "Review this dashboard — every panel must answer whether the service is healthy and what to do next."

Not fire (3):
6. "Respond to an active incident already being triaged (that's incident-response-engineer)."
7. "Run a security/compliance/query audit that has its own tooling."
8. "Add pretty graphs to a dashboard with no SLI or SLO attached."

## 2. Quality rubric (1-5)
(a) decision tree covers branches: 5 — SLI→SLO→budget→burn→dashboard→runbook chain, golden-signal selection, worked checkout.
(b) failure modes have detection + mitigation: 5 — 12: alert fatigue (add time-bias, cardinality, dashboard-drift), causes-not-symptoms, dashboards-without-action, log-spam, sampling-bias, cardinality-blowup, runbook-less-page, etc, all DETECT/FIX.
(c) quantitative rules are numbers: 5 — budget=1−SLO, 14.4× burn, 2-layer burn rule, cardinality <10-20k, sampling 1% baseline.
(d) verification gate executable: 5 — monthly error-budget report, alert drill, trace-coverage method (5 endpoints×3 auth), dashboard review cadence.
(e) references authoritative: 5 — Google SRE Book/Workbook, OpenTelemetry, Prometheus docs.
(f) no contradictions: 5 — burn-rate and error-budget rules align with incident-response-engineer's burn gates; no conflict.

## 3. Reference task
Define the observability contract for a 200 rps checkout with P95 250ms SLO. The skill must produce the SLI formula, a 30-day error budget in minutes, a fast+slow burn-alert rule with exact rate math, a RED vs USE choice, and the trace/log/metric sampling scheme.
