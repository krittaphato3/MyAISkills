---
name: observability-sre
description: Use when defining SLIs/SLOs and error budgets, choosing monitoring metrics (golden signals), setting burn-rate alerts, or structuring logs, traces, and dashboards that drive action.
version: 1.0.0
grade: G3
domain: production
status: active
last-reviewed: 2026-08-06
owned-by-agent: devops-engineer
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

- **Three pillars — metrics, logs, traces.** Metrics for signaling and SLO (cheap, cardinality-bounded); logs for detail of events; traces for request flow across services. They complement, they do not substitute. No single one answers the full golden-signal question.
- **RED method (for services):** Rate, Errors, Duration per request — the request-oriented view. **USE method (for resources):** Utilization, Saturation, Errors — the resource-oriented view. Mix them: RED for the boundary, USE for the capacity.
- **Distributed tracing with sampling.** Record a head (root) sample and a tail sample; a 1% baseline plus a fixed 100% allocation for errors/CPU-hot traffic keeps trace utility high at bounded cost. Sample the decision at the collector, not at the app, to avoid bias.
- **Structured logging standards.** Emit logs as JSON with stable keys (severity, service, trace_id, span_id, host, a stable hierarchy of context fields), never free-form prose. Centralize with the same span/trace correlation.
  - Example:
    ```json
    {"ts": 2026, "severity": "error", "service": "checkout",
     "trace_id": "ab12", "span_id": "cd34", "err": 504, "status": 504}
    ```
  - Stable keys and a shared trace id let an availability burn join to a log line and a span. A log with no trace id cannot be attached to the request that consumed the budget.
- **Alert-on-symptoms.** Alerts are keys on an SLO-signal symptom (latency breaching the budget, error rate against budget) not on the "cause" you guessed (e.g., don't alert on "the DB is slow" — alert on request latency against budget and correlate with DB). The symptom is what the user sees; a cause-alert fires when the real symptom is fine and misses it when not.

### Three-pillar consistency
Make each pillar answer one question. Metrics answer "is it in budget?" Logs answer "what happened?" Traces answer "which path was slow?" A request must carry the same trace_id across all three, or you cannot reason from a metric burn to a log line to a trace span.

### Alert rule — sampled for burn, keyed on symptom
```
# fast burn page: 1 h lookback, budget 0.001 for 99.9% SLO
sum(rate(http_5xx_total[1h])) / sum(rate(http_requests_total[1h]))
  > on () 0.001 * 14.4         # ~14.4x monthly burn, instant page
```
A symptom-keyed rule divides by a request SLI and a burn vector; it alerts when the SLO moves, not when a cause the engineer guessed is high.

## FAILURE MODES & MITIGATIONS

At least 8, detection then fix.

1. **Alert fatigue.** *Detection:* high pages-per-shift; alerts rarely actionable flags; operators start ignoring or flipping all alerts off. *Fix:* reduce count, increase threshold to SLO burn, dedupe pages into one incident, require a symptom-SLI on every page, and a working runbook gate. If it doesn't map to an SLO burn and a runbook, it is not an alert.
2. **Alerting on causes not symptoms.** *Detection:* alerts = "Check disk usage" or "This metric is high" with no user impact; a check dips but the user SLO is fine. *Fix:* alert on symptoms (latency/error/SLO), keep cause-checks as dashboards or secondary signals, and correlate cause via trace/log only when the symptom fire.
3. **Dashboards without actions.** *Detection:* pages of charts nobody interprets; each panel has no decision; no runbook step attached. *Fix:* every dashboard panel names a decision and pull-to-action; review for "what do I do next" and cut panels that don't pass.
4. **Log spam.** *Detection:* log volume dominated by debug/verbose, SysExcessive rate, no structured filtering; logs cost exceeds the value. *Fix:* cap per-source rate, promote structured logging, set log-level policy, sample low-value logs, and drop logs that are not actionable.
5. **Missing golden signals.** *Detection:* a service has latency but no error rate, or error rate without a latency; an outage causes an empty page. *Fix:* for each service list all four golden signals and confirm each is instrumented; cover at minimum availability + latency for any user-facing service.
6. **Sampling bias.** *Detection:* traces sampled by samples favour the fast path; structural data skewed; a correlation of sampled path disagrees with ground truth. *Fix:* sample at the collector with head and tail, include all errors, and check a 1% baseline against 100% on error rate.
7. **Time/season bias in the budget.** *Detection:* a 1-day budget exhausted by a busy business hour flips to "OK" twice a day and pages weirdly. *Fix:* pick the window that matches the business cycle (30-day rolling), don't gate on a 1-day reset, and aggregate the burn over the full window.
8. **Cardinality blowup.** *Detection:* a label {method, uri} or unbounded {request_id} cardinality turns a metric into high-turnover series and the query timeline or the metric fail. *Fix:* bound label sets to a cardinality limit (see QUANTITATIVE RULES), keep high-cardinality to traces/logs, not metrics.
9. **An SLO with no error budget.** *Detection:* alert thresholds hand-tuned, no residual budget math, a painful dry-out of on-call. *Fix:* compute a budget from target and window, run a burn rule, and surface remaining budget on the dashboard.
10. **Runbook-less page.** *Detection:* a pager that fires, and no runbook or checklist is available to the on-call. *Fix:* every alert has an owner, an "am I in budget" step, and a gate; drill it (see VERIFICATION GATE).
11. **Distributed tracing that misses the path.** *Detection:* traces show only the sampled healthy path; the high-error path has no spans; the sampling excludes it. *Fix:* add explicit sampling for errors and unusual paths; verify trace coverage in the VERIFICATION GATE.
12. **Dashboard drift.** *Detection:* a dashboard that no longer references the current SLO target or the real endpoints; panels stale after a rename. *Fix:* tie dashboard SLO lines to a source of truth, review on a cadence, and remove panels that diverge.

## COMMON ANTI-PATTERNS

- **A dashboard with no decision** — a wall of metrics is a chart, not observability. Each panel answers one question.
- **Alerting on every cause** (disk, DB, CPU) separately from the symptom — converts the fix into noise.
- **Logs as the only telemetry** — no metrics/traces; you cannot alert on logs alone.
- **100% tracing by default** — expensive and unsustainable; sample and correlate.
- **An SLO without a budget** and a burn rule — it is then a number nobody can act on.

## QUANTITATIVE RULES

Numbers are budgets, measured, not absolutes.

- **SLO/budget math.** Budget = 1 − SLO. For SLO 0.99 → budget 0.01 (1% of time). For 30-day window (43,200 min): budget = 0.01 × 43,200 = 432 min ≈ 7.2 h. For 0.999 → 0.1%, ~43 min/month. For 0.9999 → 0.01%, ~4.3 min/month.
- **Burn rate.** Burn = (actual failures / total) ÷ (budgeted failure / total). When you are at or above 1× you are spending exactly the budget over the window; fast-burn uses multiple of it. **14.4×** is the quoted fast-burn multiplier (e.g., a multi-duration window such as 1 h at 14.4× ≈ zeroing the monthly budget in 1/14.4 of the window) — used for immediate page.
- **Burn rule set.** Two layers: a fast rule to page immediately (window = ~14.4× burn for a short duration) and a slow rule to page within ~6 h (e.g., 1× monthly across the month with a long lookback) so both instant and slow-burn failures page, and no budget is silently flushed.
- **Example burn budget with numbers.** SLO 99.9%, window 30 days → budget ~0.1% ≈ 43 min. If the service burns 0.4% of requests for 2 h, the burn is > 4× its 30-day allowance reported as margin — it drains the budget down and flushes it; alert triggers on reaching ~2× the daily figure across the window.
- **Worked burn calculation.** Given actual failure fraction 0.012 (1.2%) and SLO budget fraction 0.001 (0.1%), burn = 0.012 / 0.001 = 12×. At 12× for a month window, the budget is exhausted in 30 d / 12 ≈ 2.5 days. So a sustained 12× burn means the SLO is broken within days, and a 14.4× equivalent for an hour means the budget for that month is gone.
- **Counting errors exactly.** Decide what counts as an error (HTTP >= 500, timeouts, a downstream failure). Never count the same failure twice (a 5xx response and a latency alarm on the same request) or the budget double-spends.
- **Budget allocation per major flows.** If one workflow (e.g., checkout) is far more critical than the rest, give it its own SLO and budget; do not let a busy but non-critical endpoint consume the whole budget. A shared budget hides which flow is failing.
- **Cardinality limit for metrics.** Keep total unique prometheus-ish metric series per service under ~10,000 to 20,000 and per-array < ~1,000 unique; put unbounded keys {url, request_id, trace-id} into traces/logs, never a metric label.
- **Sampling caps.** Baseline samples at 1%; drop to 100% only for error/needle-hot traffic, bounded by a total (e.g., ≤ 10% of spans) so the trace cost stays linear to O(total) and metadata stays correct.
- **Saturation as a number** — report utilization %, the bottleneck resource as gage percentiles, and a trigger when crossing ~80% sustained on the bottleneck for more than 30 min.

### Worked cardinality walk
A metric labeled with {service fixed, method = 8, path = 200} yields 8 × 200 = 1,600 series per service — already noise at the 1k per-array ceiling. Adding an unbounded label like {request_id} multiplies the series by the number of concurrent in-flight requests, exploding cardinality and making alerting queries slow or the storage fall over; such data belongs in traces/logs, not a metric label. Bound the label set so each metric stays countable and reportable.

### A dashboard that drives action
- Panel 1: availability SLI vs the 99.9% line. Decision: in or out of budget.
- Panel 2: P99 latency vs the 300 ms line. Decision: meet or miss.
- Panel 3: top error-budget burners by endpoint. Decision: where to look first.
- Panel 4: remaining error budget as a percent. Decision: is it safe to ship today?
Each of these answers one question with one number. A panel that cannot phrase its question gets removed from the dashboard.

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