# observability-sre — QUANTITATIVE RULES

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
