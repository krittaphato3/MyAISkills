# observability-sre — PATTERNS

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
