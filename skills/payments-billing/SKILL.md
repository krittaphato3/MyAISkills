---
name: payments-billing
description: >-
  Integrates payments and billing: checkout, one-time and subscription charges, plans and
  proration, invoices, refunds, disputes, and signed webhooks, with idempotency and
  PCI-scope avoidance. Use when money moves through the product. General provider wiring
  routes to third-party-integration; pricing and refund policy are product decisions.
metadata:
  version: 3.0.0
  domain: production
  grade: G3
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: integration-engineer
---

# Payments & Billing

Money code is where a bug is not a bug, it is a loss. This skill covers the parts that are easy to get subtly wrong: where the amount is decided, how entitlement is derived, why webhooks and not redirects are the source of truth, and how to survive duplicate deliveries and disputes.

## WHEN TO USE

- **Taking money** — checkout, one-time payment, tips, invoices.
- **Subscriptions** — plans, trials, upgrades/downgrades, proration, cancellations, dunning.
- **Money events** — refunds, chargebacks, failed payments, disputes.
- **Entitlement** — deciding what a paying customer can access.
- **Reviewing** existing payment code for correctness or PCI scope.

## WHEN NOT TO USE

- **Generic outbound HTTP/retry mechanics** — `resilience-pattern-engineer`.
- **General auth and access control** — `security-hardening-specialist`; this skill only consumes identity.
- **Tax law or business pricing strategy** — surface it; do not invent it.
- **Provider selection** — a service-choice decision before this skill applies.

## DECISION TREE

1. **Identify the money model.** One-time, subscription, usage-based, or marketplace? Each changes the objects and the failure surface.
2. **Decide server vs client authority.** Amounts, currency, and plan are computed **server-side, always**. The client receives a session/intent id, never a price.
3. **Choose the source of truth for entitlement.** It is the provider's subscription state, reconciled via webhooks — never the checkout success redirect.
4. **Design idempotency.** Every charge/refund carries an idempotency key; every webhook handler is replay-safe.
5. **Enumerate the unhappy paths** before writing happy-path code: failed payment, duplicate event, out-of-order event, refund, dispute, cancellation mid-period.
6. **Stay in scope.** Card data never touches your server (SAQ-A). Use the provider's hosted/embedded elements.
7. **Verify in test mode end-to-end**, then define the live cutover and rollback.

## PATTERNS

### 1. Checkout
```text
client → server (plan id + user) → server computes amount → provider session
      → client redirected/embedded → provider processes
      → webhook confirms → server grants entitlement
```
The redirect is a UX event. The webhook is the fact. Never grant access on the redirect alone.

### 2. Webhook handling
```text
raw body → verify signature → dedupe by event id → enqueue → ack 2xx → process async
```
- Verify against the **raw** bytes; re-serializing breaks the signature.
- Persist processed event ids; providers retry and can deliver out of order.
- Reconcile to absolute state (`subscription.status = active`) rather than applying deltas.
- Handle `invoice.payment_failed`, `charge.dispute.created`, and cancellation events explicitly.

### 3. Subscriptions & proration
- Model plan changes as provider operations, not local math; local proration math drifts.
- Trials and dunning: define what access exists during grace and after failure.
- Cancellation: distinguish "cancel at period end" from "cancel now", and reflect both.

### 4. Idempotency
- Key per logical operation (`order:{id}:charge`), stored server-side; retries reuse the key.
- Refunds and credits are idempotent operations with their own keys.

### 5. Reconciliation & audit
- Periodically reconcile local subscription/entitlement state against the provider.
- Keep an append-only ledger of money events with the provider id — disputes need it months later.

### 6. Environments & cutover
- Separate test/live keys; live keys never in dev.
- Cutover checklist: switch key, verify one real charge, confirm webhook endpoint is live and verified, confirm refund path.

## FAILURE MODES & MITIGATIONS

Each entry is DETECT → FIX.

1. **Client-supplied price** — DETECT: amount in the request body. FIX: compute server-side; ignore client amounts.
2. **Entitlement from redirect** — DETECT: access granted before webhook. FIX: grant only on verified webhook event.
3. **Unverified/unparsable webhook** — DETECT: signature checked against re-serialized body, or not checked. FIX: verify raw bytes first.
4. **Duplicate charge** — DETECT: retry or double-click produces two charges. FIX: idempotency key per logical operation.
5. **Replay double-grant** — DETECT: same event id processed twice. FIX: dedupe table + idempotent handler.
6. **Out-of-order state** — DETECT: subscription state wrong after late events. FIX: reconcile to absolute provider state.
7. **PCI creep** — DETECT: card fields posted to your server. FIX: use hosted/embedded elements; remove those fields.
8. **Untested unhappy path** — DETECT: no test for failed payment/refund/dispute. FIX: exercise each in test mode with recorded evidence.
9. **Secret exposure** — DETECT: secret key in the client bundle. FIX: server-side only; rotate the key.

## QUANTITATIVE RULES

- Webhook ack target < 5s; all real work queued (`background-jobs-engineer`).
- Idempotency key per logical money operation; zero duplicate-charge tolerance.
- Signature verification on 100% of money webhooks — no exceptions, no "internal" endpoints.
- Entitlement derived from provider state; local ledger reconciled at least daily.
- Every money flow has a recorded test-mode run before live keys are enabled.

## VERIFICATION GATE

- **Amount server-authoritative?** No client-supplied price on any path.
- **Webhooks verified + deduped?** Raw-body signature check and an event-id dedupe store exist.
- **Entitlement correct?** Derived from provider state, with the reconciliation path shown.
- **Unhappy paths exercised?** Failure, refund, dispute, and cancellation each tested with evidence.
- **Ledger recorded?** Money events stored append-only with provider ids.
- **Test-mode run attached?** End-to-end evidence before live cutover.

```text
[PAYMENTS DELIVERABLE]
Model: {one-time | subscription | usage} · Provider: {name, API version}
Files: {changed paths}
Authority: amount {server} · entitlement {provider-reconciled}
Webhooks: {endpoint} · signature {scheme} · dedupe {store} · async {queue}
Idempotency: {key scheme}
Unhappy paths: failed ✓ refund ✓ dispute ✓ cancel ✓ — evidence {path}
Test-mode run: {path}
Live cutover: {checklist + rollback}
```

## REFERENCES

- `resilience-pattern-engineer` — retries, timeouts, circuit breakers for outbound calls.
- `background-jobs-engineer` — queueing webhook processing.
- `security-hardening-specialist` — secret handling and access control.
- `integration-engineer` agent — the implementing role.

Ownership: maintained by integration-engineer; payments-billing is the production-domain skill for money.
