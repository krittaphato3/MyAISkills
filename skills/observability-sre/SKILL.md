---
name: observability-sre
description: >-
  Designs observability and reliability targets: SLIs and SLOs, error budgets,
  golden-signal metrics, burn-rate alerts, structured logs, traces, and dashboards that
  drive action. Use when defining 'healthy', reducing alert noise, or instrumenting a
  service. Active outages route to incident-response-engineer.
metadata:
  version: 3.0.0
  domain: production
  grade: G3
  status: active
  last-reviewed: '2026-10-22'
  authored-by: devops-engineer
---

# observability-sre

World-class reference for making a service measurably reliable rather than merely monitored. Covers SLI selection from the four golden signals, SLO targets and windows, error-budget accounting, burn-rate alerting, the three pillars (metrics/logs/traces), structured logging, RED/USE, and a verification gate that must pass before an operability claim is made. Every rule is a number, not an adjective.

## WHEN TO USE

- You are defining the availability or latency contract for a service and must pick an SLI, set an SLO target and window, and account an error budget.
- You must turn "alert me when things break" into alerting on burn rate against an SLO instead of on a vague threshold.
- You must choose which golden signals matter for a service and map them to a decision (latency, traffic, errors, saturation).
- You are building the three-pillar pipeline (metrics/logs/traces), instrumenting a request path, or picking a sampling scheme.
- You must build or review a dashboard, and it must answer whether the service is healthy and what to do next — not merely render pretty charts.
- You are detecting a runbook gap, alert fatigue, log spam, or a coverage hole and need a targeted, quantified fix.
- A fresh subagent must inherit and extend an SLO policy, an alerting rule, or an observability stack with specific budget numbers.

Self-assign this skill before defining an SLO, drafting an alert rule, instrumenting a service, or building a dashboard.

## WHEN NOT TO USE

- A service with no traffic or no reliability contract where SLO/alerting machinery is overkill.
- Incident response triage that is already running; this is the make-metrics-and-alerts design time, not the firelight.
- A security, cost, or single-query audit that has its own dedicated tooling and workflow.
- UI/UX accessibility or data-modeling work that has no operational SLO.
- Drafts where the team cannot yet a target number; an SLO with a guessed target and no battle history is worse than none at all.

### Common SLO targets for reference
- Internal tooling / non-UI batch: availability 99% (budget ~7.2 h/mo), P95 latency 2 s.
- B2B API / checkout: availability 99.9% (budget ~43 min/mo), P95 latency 300 ms.
- Money / ledger: availability 99.95%+ (budget ~21 min/mo), P99 latency 100 ms, plus strong consistency.
- A pure-batch data pipeline: a latency SLO on batch completion per run, not a rate.

Use these as starting targets, not entitlements. The point is that the budget is measurable, not that a specific number is canonical.

## DECISION TREE

Walk this chain in order — each stage feeds the next.

1. **Choose an SLI from the golden signals.** Pick the least-being-for-the-user signal for the service: availability (success rate), latency (a percentile), errors, or saturation (usage of capacity). Ask which one breaks first and what the user actually experiences.
2. **Set the SLO target and window.** Convert the SLI into an objective (e.g., availability at or above 99.9% over a 30-day rolling window, P99 latency at or under 300 ms). The window is the natural period: 30 days is standard for a budget that resets; a year is not actionable.
3. **Derive the error budget.** Budget = 1 − SLO. With an SLO of 99.9% the budget is 0.1% of time; each month you can be 'unavailable' for ~43 minutes (0.1% of 730 hours). That is the real limit, not an anecdotal one.
4. **Alert on burn rate.** Set the alert so it fires only when you are spending the budget too quickly relative to the SLO, not on a static threshold. Burn rate = actual failure fraction ÷ allowed fraction; a sustained 30 min at 14.4× is a fast-over into the budget.
5. **Build dashboards.** Each panel must map to a decision and a named SLI/SLO; a dashboard should show the top error-budget consumers and the likely cause, not raw noise.
6. **Write runbooks.** Every alert that fires must have a runbook owning an owner, an "am I in budget" first step, and a known remediation with a measurable gate.

### Dashboard and runbook gate
- A panel that does not name the question it answers is deleted. A dashboard with "what do I do now?" unanswered is a wall of charts, not an operating tool.
- Every alert maps to exactly one runbook step; the runbook states its owner, the first command to run, and the decision rule that ends it (a measurable gate such as "error rate < 0.2% for 15 minutes"). A runbook without an end gate is an unbounded on-call shift.

### SLI selection by golden signal

- **Availability:** measure good requests over total requests (e.g., HTTP 2xx/4xx-counted-success over all). Use it when a returned value or a refusal is the dominant failure.
- **Latency:** percentile latency over the window (P95 and P99). Alert on a percentile crossing the budget, not the mean, which hides the long tail. Fast request sample counts matter for the tail.
- **Errors:** rate of bad requests (5xx, error subresponses) independent of availability to catch semantic failures.
- **Saturation:** utilization that is delta-neutral over time, e.g. request-queue depth vs capacity, and the top-1 bottleneck resource (CPU, memory, I/O, network, connections). Saturation is often the reason latency degrades.

Which of the above is least? Often the answer is that a single linear fraction (available requests) covers the main story; add latency when a response being slow is a distinct user harm. Choose one primary SLI per service unless a second changes a decision.

### Worked example — checkout service

Service: checkout of 200 req/s, P95 target 250 ms, five 5xx signals.

1. SLI: availability = successful / total; latency = P95.
2. SLO: availability ≥ 99.9% over a rolling 30-day window; P95 ≤ 250 ms.
3. Budget: 0.1% of 30 days → drift ≤ 43 min/month of downtime-equivalent; P95 250 ms counted equally at slower.
4. Alerting: fast 14.4× 1 h burn rule and a slow 1× over 30 day rule; burn report each month. Any alert that would page must have a runbook with "am I in budget" first step.

## Worked triple — the canonical latency+availability pair

- SLI: availability = (successful requests)/total; latency = P99.
- SLO: availability ≥ 99.9% over rolling 30-day; P99 ≤ 300 ms over same.
- Budget: 0.1% of 30 days ≈ 43.8 minutes of total downtime; at P99 you may spend 9-seconds-but-times-N. So a 1-downtime or a 300-ms-over-time is measured against one shared budget.
- Alerting: fast-burn rule at 14.4× for 1h (see QUANTITATIVE RULES) and a multi-day rule at 1× for 6h; page only when the budget would be exhausted in the window.

### Worked slow burn
A service that is 99.95% good (0.05% failures) for a 99.9% SLO is burning faster than the budget: 0.05% > 0.1% allowance for a month, so over a 30-day window it spends the full budget. A slow rule with a 6 h lookback catches a sustained 1×-to-2× burn that the fast rule may miss for hours.

### Which SLI to write in the record
Prefer the least-complex SLI: count successful versus total. Do not hand off "availability, latency, throughput" as adjectives; state the exact formula (e.g., success == status < 500 and not client_timeout) and its window. Ambiguity about "what counts as an error" is the source of most SLO disputes.

## PATTERNS

- **Three pillars — metrics, logs, traces.** Metrics for signaling and SLO (cheap, cardinality-bounded); logs for detail of events; traces for request flow across services. They complement, they do not substitute.
No single one answers the full golden-signal question. - **RED method (for services):** Rate, Errors, Duration per request — the request-oriented view. **USE method (for resources):** Utilization, Saturation, Errors — the resource-oriented view.

Full detail: `references/patterns.md`.

## FAILURE MODES & MITIGATIONS

At least 8, detection then fix.

Full detail: `references/failure-modes-mitigations.md`.

## COMMON ANTI-PATTERNS

- **A dashboard with no decision** — a wall of metrics is a chart, not observability. Each panel answers one question.
- **Alerting on every cause** (disk, DB, CPU) separately from the symptom — converts the fix into noise.
- **Logs as the only telemetry** — no metrics/traces; you cannot alert on logs alone.
- **100% tracing by default** — expensive and unsustainable; sample and correlate.
- **An SLO without a budget** and a burn rule — it is then a number nobody can act on.

## QUANTITATIVE RULES

Numbers are budgets, measured, not absolutes.

Full detail: `references/quantitative-rules.md`.

## VERIFICATION GATE

Nothing below is optional; a service is only observable when these are green.

- **Error-budget reporting.** A monthly report on each SLO returns: actual availability/latency P99 against the window, remaining error budget in minutes/percent, and the top 5 contributors. Publish at a fixed cadence.
- **Alert drill.** Do a tabletop/fire drill on each page: confirm the right symptoms and SLO burn fire, the runbook is buntsteps, the owner is named and the recall path is complete, the time-to-recover is measured, and the alert actually fires in a copy of the production telemetry.
- **Trace coverage check.** Choose N likely user-request and error paths and verify they all produce a linked trace_id and span tree in the tracing store; confirm it is representative, not only the one free sample.
- **Dashboard review.** On a review cadence, walk each dashboard and answer per panel: which decision, which SLI/SLO, does it repeat. Bluntly the whole review: remove or fix any panel that does not drive action.
- Record the OTel/SLI, the SLO/error-budget numbers, the burn/alert rule, a runbook, and the drill/trace/dashboard evidence before calling SRE setup "done".

### Drill pacing
Run the alert drill at least once per quarter and after a change to an alert rule. A fire-the-test process must trigger the burn alert, open the runbook, and step the OIC through it; record time-to-ack and time-to-recover as separate numbers. An alert that never fires in a drill is an untested alert, and an alert that fires so often it cannot be validated is a noise source.

### Trace coverage method
Pick N user flows (e.g., 5 endpoints × 3 auth states) and error paths (forced 5xx, timeout), run them, and confirm each produces a complete root→leaf span tree in the tracing store. If N flows share only the default sampler, raise the sample rate for those paths or add explicit propagation. A service whose slow calls are not traced is a service you cannot fix under load.

### Tracing budget guard
A trace plan must stay under the quantitative cap (baseline 1%, total ≤ 10% of samples) while covering the error path. If a full error-path trace exceeds the cap, raise the error-path rate and cut the healthy path instead of the reverse.

## SHIP-GATE (summary of this skill)

- One SLI per loud signal + latency where slow-beats-wrong.
- One SLO target + window; budget = 1 − SLO; burn rule 14.4× fast / 1× slow.
- Alert on symptoms against the budget, not on a guessed cause.
- Dashboard panels each answer a question or are removed.
- Runbook with owner, first command, and a terminal gate.
- Cardinality bounded; traces/logs carry the high-cardinality detail; all three share trace_id.

## REFERENCES

- **Google SRE Book**, chapters 4–5: monitoring distributed systems, and alerting (SLO, burn rate, alerts, on-call). The source of the golden-signals and error-budget definitions.
- **Google SRE Workbook** — chapter 5 on SLOs, error budgets and alerting, plus the concrete rules and examples.
- **OpenTelemetry** — documented standards for metrics, logs, traces, and context propagation.
- **Prometheus** best practices on naming conventions, labels/cardinality, and good alerting rules.
- **Canonical guidance** — the SRE Workbook's four golden signals (latency, traffic, errors, saturation) and the RED/USE patterns above come from the referenced Google and Prometheus material; use them as the source of the specific numbers you calibrate on your own telemetry.

## CHANGELOG

- 2026-08-06 | Phase 3.6: observability-sre created (G3: SLI/SLO, error budgets, metrics/logs/traces, burn-rate alerting) | observability-sre