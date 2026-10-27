---
name: third-party-integration
description: >-
  Wires external services into an application: provider selection, server-side credentials,
  OAuth, signed webhooks, idempotency, retries/timeouts, rate limits, sandbox testing, and error
  mapping. Use when integrating any outside API, SDK, or webhook (email, SMS, storage, CRM,
  calendars, maps, LLM providers, internal services). Payments route to payments-billing; sending
  email itself to email-notifications; MCP tool servers to mcp-builder.
metadata:
  version: 3.0.0
  domain: production
  grade: G2
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: integration-engineer
---

# Third-Party Integration

Every integration is a distributed system you do not control. The job is not "make the happy-path
call work" — it is to behave sanely when the provider is slow, duplicated, down, or hostile, and
to keep the user's data and credentials out of the browser.

## WHEN TO USE

- Adding any external API/SDK/webhook to a codebase.
- Choosing between providers for a capability the app needs.
- A provider is returning 429/5xx/timeouts, or webhooks are duplicated or missed.
- A credential may have leaked into client code.
- Migrating from one provider to another.

## WHEN NOT TO USE

- Money movement and subscriptions — `payments-billing` (it overrides this skill).
- Email/SMS content and deliverability — `email-notifications`.
- Building the server that others integrate with — `api-design-architect`.
- Pure resilience patterns inside your own service — `resilience-pattern-engineer` (this skill
  applies them at the provider edge).

## DECISION TREE

```text
1. CHOOSE THE PROVIDER (only if not already chosen)
   Requirements → official docs/limits → auth model → webhook support → sandbox →
   pricing at expected volume → data residency → exit path (can we export?).
   Do not pick from memory; verify the current API and pricing before writing code.

2. DEFINE THE BOUNDARY
   One adapter module owns the provider: client init, auth, calls, error mapping, retries.
   The rest of the app talks to your interface, never the SDK. This is what makes a swap or a
   mock possible later.

3. CREDENTIALS
   Server-side only. Env/secret store, never in client bundles, logs, URLs, or error messages.
   Separate keys per environment. Document required scopes, nothing broader.

4. CALLS
   Timeout on every call (connect + read). Retry only idempotent operations, with backoff +
   jitter, capped. Map provider errors to your domain errors. Never surface raw provider text.

5. WEBHOOKS
   Verify signature over the raw body BEFORE parsing. Deduplicate by event id. Process
   asynchronously and return 2xx fast. Make handlers idempotent: providers retry and reorder.
   Handle replay older than what you have already applied.

6. PROVE IT IN SANDBOX
   Real requests against the provider's test mode. Record fixtures for the paths you cannot
   trigger (declines, bounces, revocations). Add a contract test that fails if the response
   shape changes.

7. OBSERVE
   Log provider, operation, latency, status, and correlation id — never payloads with PII or
   tokens. Alert on error-rate and webhook-lag, not on every failure.
```

## PATTERNS

### 1. Adapter skeleton
```text
providers/{vendor}/
  client.ts      // auth, http, timeout, retry, rate limit
  map.ts         // provider payload ↔ domain types; one place for shape changes
  errors.ts      // provider error code → domain error
  verify.ts      // webhook signature verification (raw body, constant-time compare)
  client.test.ts // contract tests + fixtures for edge cases
```
The app imports the domain interface only. Grep rule: the vendor name appears nowhere else.

### 2. Webhook handler order
```text
1. read raw body (no JSON parse yet)
2. verify signature + timestamp window (reject >5 min skew)
3. parse; persist event id for dedupe (unique constraint = your idempotency)
4. enqueue work; return 2xx within the provider's timeout
5. worker: re-check current state, apply transition, record result
```
Returning 2xx before work completes is not optional for slow providers; it is how you avoid
retry storms doubling your side effects.

### 3. Error mapping table
| Provider signal | Your behavior |
|---|---|
| 401/403 | fail loudly: bad credentials — do not retry |
| 404 on a resource you created | treat as eventual consistency: retry bounded, then alert |
| 409/conflict | re-read state, reconcile, do not blindly retry |
| 429 | honor `Retry-After`; otherwise exponential backoff + jitter |
| 5xx / timeout | retry if idempotent, else mark indeterminate and reconcile |
| 4xx validation | never retry; surface a domain error with the field |

### 4. Idempotency
Send your own idempotency key on creates when the provider supports it. When it does not, keep a
local request ledger keyed by (operation, business key) so a retry after a timeout cannot
double-charge, double-send, or double-create.

### 5. Sandbox and fixtures
The paths that break in production are the ones nobody tested: expired cards, revoked tokens,
partial failures, duplicate webhooks, pagination beyond page 1, and rate limits. Capture one
recorded response per path and assert your adapter maps it correctly.

## FAILURE MODES & MITIGATIONS

1. **Secret in the browser** — key prefixed for public use or inlined by the bundler. *DETECT:*
   env var referenced from client code; `NEXT_PUBLIC_`/`VITE_` on a secret. *FIX:* move the call
   server-side; rotate the key; check build output.
2. **Unverified webhook** — signature checked after parsing, or not at all. *DETECT:* handler reads
   `req.body` directly. *FIX:* raw-body verification, reject unsigned, add a forged-signature test.
3. **Duplicate side effects** — provider retries create two records/two emails. *DETECT:* no event
   id dedupe. *FIX:* unique constraint + idempotency key.
4. **Retry storm** — retries on 4xx and on non-idempotent calls. *DETECT:* error-rate spikes after
   an outage. *FIX:* classify errors; retry only transient + idempotent; add jitter and a cap.
5. **No timeout** — one slow provider hangs a worker. *DETECT:* no explicit timeout config.
   *FIX:* connect/read timeouts, circuit breaker, queue isolation.
6. **SDK coupling** — vendor types leak through the app. *DETECT:* grep finds the SDK in UI/business
   code. *FIX:* adapter + domain types.
7. **Assumed API shape** — built from memory or a blog. *DETECT:* calls fail on real responses.
   *FIX:* `source-driven-development`; verify against current docs and a real sandbox call.

## QUANTITATIVE RULES

- Every outbound call: explicit timeout, bounded retries (≤3) with jitter, classified errors.
- Webhook 2xx within the provider's window (assume ≤5s); heavy work goes to a queue.
- Contract tests: at least one per error class you map, plus one duplicate-delivery test.
- ≤1 adapter module per provider; no vendor types outside it.
- Secrets: 0 in client bundles, logs, or error text — verify by grepping the build output.

## VERIFICATION GATE

- [ ] Real sandbox call succeeded (not just a mocked unit test).
- [ ] Signed webhook verified on the raw body; forged signature rejected by a test.
- [ ] Duplicate delivery produces exactly one side effect (test attached).
- [ ] Timeout + retry + error mapping demonstrated for at least one failure path.
- [ ] No secret appears in the client bundle or logs.
- [ ] Provider swap would touch only the adapter folder (checked by grep).

## REFERENCES

- `payments-billing` — overrides this skill for money movement
- `email-notifications` — deliverability and sending specifics
- `resilience-pattern-engineer` — retry/breaker primitives
- `security-hardening-specialist` — secret handling and input trust
- `source-driven-development` — verify the current provider API before coding
