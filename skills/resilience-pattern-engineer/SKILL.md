---
name: resilience-pattern-engineer
description: Implement resilience patterns — error handling, retries, circuit breakers, rate limiting, timeouts, backoff. Use when hardening a service's failure behavior against transient errors and overload.
version: 0.2.0
grade: G2
domain: architecture
status: active
last-reviewed: 2026-08-06
owned-by-agent: code-implementer
---

# RESILIENCE PATTERN ENGINEER

Implement fault tolerance patterns for distributed systems. Read the DECISION TREE before choosing a pattern — the wrong mechanism (e.g., retry where fail-fast belongs) makes a system worse, not more resilient.

## WHEN TO USE

- You are building or extending a distributed interaction: service-to-service calls, queues, caches, databases, or third-party APIs where a dependency can fail, stall, or be slow.
- A call is already protected by a timeout or retry but behaves badly under partial failure (server errors, throttling, latency spikes).
- The system must keep serving degraded rather than fail entirely when a dependency is down — availability targets matter more than strict consistency for the path in question.
- You need to bound load a dependency receives (rate limiting, backpressure, circuit opening) to protect it from overload and protect your SLOs from its slowdowns.
- You must defend a resilience change: prove with fault injection that retries/breakers/limits do what they claim and never amplify the incident.

## WHEN NOT TO USE

- **Retry on non-idempotent operations.** If the call has a side effect that cannot be safely repeated (e.g., transfer/payment/send without an idempotency key), retry is the wrong pattern — prefer fail-fast and surface the error to a human or a compensating workflow. Only retry when the operation is idempotent or carries an idempotency key the server honors.
- **Retry on latency-critical paths.** On a tail that must stay low (interactive reads), a second synchronous attempt doubles the tail; the latency cost of retrying exceeds the availability win. Prefer fail-fast + async replay, degrade to cached/stale data, or a timeout that fits the SLO.
- **Piling patterns on an unmeasured failure.** If you do not know the failure mode (500 vs timeout vs connection refused vs slow), adding a breaker or retries is guesswork. Instrument first, then choose.
- **Where fail-fast is correct** — validation errors, 4xx client faults, permanent schema mismatches: retry cannot change the outcome, so detect and fail fast instead of amplifying cost.
- **Where a simpler mechanism fits** — a plain timeout covers a hung dependency; a bounded queue or backpressure covers overload; adding a circuit breaker to a call that never exceeds its budget adds complexity without benefit.

## DECISION TREE

Trace left to right and commit to the first leaf that matches.

1. **Classify the failure first.** Ask: is this call retryable? 
   - **Retryable errors**: transient network faults, timeouts, connection refused/reset, HTTP 429 (throttle), 5xx, "failover in progress". These are candidates for retry with backoff.
   - **Non-retryable errors**: 4xx client faults (400/401/403/422), permanent data errors, validation rejects. Fail fast — retry will produce the same result at N× the cost.
2. **Decide fail-fast vs retry vs degrade.**
   - **Fail-fast**: the caller can tolerate an error now (async job, best-effort, compensating flow) or the error is permanent. Return the error immediately; never retry non-idempotent or latency-critical work.
   - **Retry**: the failure is transient, the operation is idempotent, and you can absorb the added latency. Retry only the retryable classes above; bound attempts and cap total wait.
   - **Degrade**: a cached/stale/default response is acceptable and better than an error. Use a fallback when a degraded answer beats none (read paths, feature flags, last-known-good data).
3. **Choose the backoff + jitter.**
   - **Fixed jitter** (uniform noise added to a fixed delay) — cheapest; fine for tiny retry budgets.
   - **Full jitter** — `sleep = random(0, base * 2^attempt)` per retry. Best against thundering herd: the expected wait of a colliding client set spreads out. Use for high-concurrency fan-in where many workers hit the same dead dependency.
   - **Equal jitter** — `base * 2^attempt / 2 + random(0, base * 2^attempt / 2)`. Middle ground for moderate concurrency.
   - **Exponential backoff without jitter is almost never right** at scale — synchronized retries amplify a partial outage into a full one.
4. **Choose breaker vs bulkhead vs rate limit — they solve different problems:**
   - **Circuit breaker**: stops the caller from hammering a dependency that is already failing. Trips on failure-rate (not raw count), resets with an open timeout, probes in HALF-OPEN. Use when a dependency's health is binary and calls are cheap to start but expensive to fail.
   - **Bulkhead**: isolates failure by partitioning capacity (per-dependency thread/semaphore pools) so one slow dependency cannot starve the others. Use when dependency latency varies wildly and you must protect healthy paths.
   - **Rate limit**: protects a dependency (or self) from overload, and protects yourself from a runaway client. Use when the concern is request *volume* rather than dependency *health*.
   - Combine deliberately: rate limit at the ingress, bulkhead at the pool, breaker at the dependency call, timeout everywhere. Do not stack three mechanisms at the same layer.

## RULES
1. Never fail silently — always handle errors
2. Graceful degradation — partial functionality over none
3. Fail fast — detect issues early
4. Isolate failures — prevent cascading

## CIRCUIT BREAKER
States: CLOSED (normal) → OPEN (tripped) → HALF-OPEN (testing)

```javascript
class CircuitBreaker {
  constructor({ failureThreshold = 5, resetTimeout = 30000 } = {}) {
    this.state = 'CLOSED';
    this.failures = 0;
    this.lastFailure = null;
    this.threshold = failureThreshold;
    this.timeout = resetTimeout;
  }
  
  async execute(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailure > this.timeout) {
        this.state = 'HALF-OPEN';
      } else {
        throw new Error('Circuit open');
      }
    }
    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (e) {
      this.onFailure();
      throw e;
    }
  }
  
  onSuccess() { this.failures = 0; this.state = 'CLOSED'; }
  onFailure() { this.failures++; this.lastFailure = Date.now(); if (this.failures >= this.threshold) this.state = 'OPEN'; }
}
```

## RETRY WITH BACKOFF
```javascript
async function retry(fn, { maxRetries = 3, baseDelay = 1000 } = {}) {
  for (let i = 0; i <= maxRetries; i++) {
    try { return await fn(); }
    catch (e) {
      if (i === maxRetries) throw e;
      await new Promise(r => setTimeout(r, baseDelay * Math.pow(2, i) + Math.random() * 100));
    }
  }
}
```

## RATE LIMITING (Token Bucket)
```javascript
class TokenBucket {
  constructor(capacity, refillRate) {
    this.capacity = capacity;
    this.tokens = capacity;
    this.refillRate = refillRate;
    this.lastRefill = Date.now();
  }
  consume(n = 1) {
    this.refill();
    if (this.tokens >= n) { this.tokens -= n; return true; }
    return false;
  }
  refill() {
    const now = Date.now();
    this.tokens = Math.min(this.capacity, this.tokens + (now - this.lastRefill) * this.refillRate);
    this.lastRefill = now;
  }
}
```

## TIMEOUT
```javascript
async function withTimeout(fn, ms) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), ms);
  try { return await fn({ signal: controller.signal }); }
  finally { clearTimeout(timeout); }
}
```

## FALLBACK
```javascript
async function withFallback(primary, fallback) {
  try { return await primary(); }
  catch (e) { return await fallback(); }
}
```

## HEALTH CHECKS
```javascript
app.get('/health/live', (req, res) => res.status(200).json({ status: 'alive' }));
app.get('/health/ready', async (req, res) => {
  const checks = { db: await checkDb(), cache: await checkCache() };
  const healthy = Object.values(checks).every(c => c.ok);
  res.status(healthy ? 200 : 503).json({ status: healthy ? 'ready' : 'not ready', checks });
});
```

## OUTPUT
```text
[RESILIENCE]
Target: {service|function}
Patterns:
- Circuit Breaker: {threshold} failures, {timeout}ms reset
- Retry: {max} attempts, {base}ms delay
- Rate Limit: {capacity} tokens
- Timeout: {ms}ms
- Fallback: {strategy}
```

## FAILURE MODES & MITIGATIONS
Each entry is DETECT + FIX.

1. **Retry storms.** DETECT: dependency error rate rises and *caller* traffic to it rises even faster; every caller retries on the same clock, so a 1% failure becomes 10× the failed volume. FIX: cap retry attempts and the total retry budget, retry only retryable error classes, use backoff with jitter, and add a circuit breaker so repeated failures open the path instead of re-arming it. Never retry a 4xx.
2. **Thundering herd (all retries aligned).** DETECT: after a dependency recovery, load spikes to many multiples of normal because every client's retry fired at the same moment. FIX: **full jitter** — replace fixed or plain-exponential delay with `sleep = random(0, base * 2^attempt)`; for a request fan-in of N simultaneous waiters the expected spread makes collisions rare. Apply per-request randomness, not a shared per-process delay.
3. **Breaker flapping.** DETECT: the breaker toggles CLOSED→OPEN→HALF-OPEN rapidly; every half-open probe is immediately slammed by the waiting burst, so the circuit never stabilizes and tail latency oscillates. FIX: trip on **failure-rate over a sliding window**, not a raw failure count (a single success floods the count-based threshold); make HALF-OPEN admit a single probe (or a small trial set), not the full waiting queue; keep the open timeout long enough to let the dependency drain.
4. **Timeouts too short or too long.** DETECT (too short): healthy-but-slow calls abort, error rate tracks latency percentiles, false negatives. DETECT (too long): a hung dependency pins threads for seconds, exhausting pools and cascading. FIX: set the timeout from measured dependency latency (p99 + margin) not a guess; connect vs read vs total timeouts separately; wire timeout into the abort signal so the underlying call is cancelled, not just the caller's wait.
5. **Cascade failures.** DETECT: one slow dependency grows latency; callers hold threads; pools exhaust; downstream retries pile up; the outage spreads to healthy services. FIX: bulkhead per dependency (bounded semaphore/pool with a rejection path), always time-bound work, fail fast on pool saturation (return 503 instead of queueing forever), and trip breakers early on degradation so excess load is shed at the edge.
6. **Idempotency-key misuse.** DETECT: double-apply after retry — a payment or side effect fires twice; or an idempotency key that changes per attempt, so the server cannot deduplicate. FIX: generate the idempotency key once per logical operation and reuse it across all retries of that operation; use a random key per logical op (a per-attempt key defeats deduplication); verify the server actually honors the key before relying on retry safety; otherwise treat the operation as non-retryable and fail fast.

## VERIFICATION GATE
Run before claiming "resilient". Evidence required for each pattern added.

1. **Fault injection (chaos).** Kill the dependency, pause its network, and spike its latency — each in isolation and under real concurrency. Confirm the system degrades along the designed path (fail-fast, degraded response, or breaker opens) and recovers when the fault clears. Record the observed behavior, not a hand-wave.
2. **Degraded-load test.** Run load against the dependency at a degraded state (e.g., 50% errors or 5× latency) and assert the caller still meets its SLO: error rate stays bounded, no pool exhaustion, no process crash, no unbounded queue growth.
3. **Breaker state-transition assertions.** Unit- and integration-test the transitions: CLOSED→OPEN after the failure-rate threshold in the window; OPEN→HALF-OPEN after the reset timeout; HALF-OPEN→CLOSED on probe success, HALF-OPEN→OPEN on probe failure. Assert the circuit actually short-circuits (no dependency call) while OPEN.
4. **Retry-budget math check.** Write down the worst case before shipping: `attempts × per-call timeout × (peak concurrency)` must fit inside the client's own budget (its SLO, its pool, the dependency's capacity). If the budget math does not hold, cut attempts, cut timeout, or fail-fast — do not ship the unverified number.

## REFERENCES

- AWS Well-Architected — Reliability pillar / fault tolerance: `https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html` (and the older "Fault-Tolerance" architecture center whitepaper, `https://aws.amazon.com/architecture/`).
- Google SRE Workbook — managing load and cascading failures: `https://sre.google/workbook/managing-load/` and `https://sre.google/workbook/cascading-failure/`.
- Google SRE Book — "Overload and Failure" chapter (timeouts, retries, queuing theory): `https://sre.google/sre-book/handling-overload/`.
- Microsoft Azure Architecture Center — retry, circuit-breaker, and bulkhead patterns: `https://learn.microsoft.com/azure/architecture/patterns/circuit-breaker`, `/patterns/retry`, `/patterns/bulkhead`.
- Martin Fowler — CircuitBreaker: `https://martinfowler.com/bliki/CircuitBreaker.html`.
- Amazon Builders' Library — "Timeout, retries, and jitter with respect to timeouts and retries": `https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/`.
- Resilience engineering classics — Sidney Dekker and the resilience-engineering literature on working-conditions and incident response; start with the SRE Book's incident-management chapters for the operational side.