---
name: email-notifications
description: >-
  Implements transactional and product email or SMS: templates, provider integration,
  SPF/DKIM/DMARC, bounce and complaint handling, suppression lists, send queues, and
  provider webhooks. Use when the product must send a message and it must arrive.
  Marketing strategy and list growth are out of scope; general provider wiring routes to
  third-party-integration.
metadata:
  version: 3.0.0
  domain: production
  grade: G2
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: integration-engineer
---

# Email & Notifications

"Send a welcome email" is a one-line request with a ten-part answer: it must leave your app without blocking it, arrive, not be classified as spam, not be sent twice, and stop entirely the moment the recipient says so. This skill covers those ten parts.

## WHEN TO USE

- **Transactional sends** — verification, password reset, receipts, invitations, alerts.
- **Product notifications** — activity digests, status changes, reminders.
- **Deliverability work** — mail landing in spam, DMARC failures, provider complaints.
- **Preferences** — subscriptions, unsubscribe, frequency caps, channel choice.
- **SMS** — OTPs, alerts, opt-in/opt-out compliance.

## WHEN NOT TO USE

- **Campaign strategy, copywriting, A/B testing of marketing content** — out of scope.
- **Queue/worker mechanics** — `background-jobs-engineer` (this skill assumes a queue).
- **Provider selection and account setup** — a service-choice task first.
- **In-app UI for notification settings** — `frontend-web-engineer`.

## DECISION TREE

1. **Transactional or promotional?** Transactional may send without marketing consent; promotional needs explicit, recorded opt-in in most jurisdictions.
2. **Channel.** Email, SMS, push? Each has its own consent and compliance rules.
3. **Never block the request.** Sends go through a queue; the API returns before the provider is called.
4. **Idempotency.** Key each logical send so a retry cannot double-send.
5. **Deliverability prerequisites.** Authenticate the sending domain (SPF, DKIM, and a DMARC policy) before any volume.
6. **Bounce/complaint handling.** Wire provider webhooks to a suppression list *before* the first send.
7. **Preferences and unsubscribe.** Every promotional message has a working, one-click opt-out; transactional respects a hard-bounce/block suppression.

## PATTERNS

### 1. Send pipeline
```text
domain event → render template (versioned) → enqueue(send_key) → worker → provider → webhook
                                                                              ├ delivered
                                                                              ├ bounced  → suppress
                                                                              └ complained → suppress
```

### 2. Templates
- Templates live in code and are versioned; render with explicit, escaped variables.
- Plain-text alternative for every HTML email.
- Keep transactional templates minimal and branded consistently; avoid heavy images (spam signals).
- Localize at render time (`i18n`), not by maintaining per-locale copies.

### 3. Idempotency & ordering
- Send key = `{event}:{entity_id}:{template}:{recipient}`; the worker skips if already sent.
- Digests and reminders must be safe to re-run for the same period.

### 4. Deliverability
- Authenticate: SPF record, DKIM signing, and a DMARC policy (`p=none` → `quarantine` → `reject` as you gain confidence).
- Use a subdomain for sending so reputation is isolated from the root domain.
- Warm up a new sending domain/IP gradually; sudden volume looks like spam.
- Monitor bounce rate, complaint rate, and DMARC reports; act on them.

### 5. Suppression & preferences
- A hard bounce or complaint suppresses that address permanently (beyond unsubscribe).
- Unsubscribe must be immediate, one-click, and honored across all promotional sends.
- Frequency caps per user; never let two systems cross-send unchecked.
- Store consent with timestamp, source, and the exact text shown.

### 6. Security
- Sign webhooks and verify; templates escape user content (no HTML injection into emails).
- Never put secrets or sensitive data in a URL or subject line (they leak via logs and previews).

## FAILURE MODES & MITIGATIONS

Each entry is DETECT → FIX.

1. **Send in the request path** — DETECT: provider call inside the HTTP handler. FIX: enqueue; return early.
2. **Double send** — DETECT: retry or replayed job sends twice. FIX: idempotent send key.
3. **Spam-foldered** — DETECT: no SPF/DKIM/DMARC, or unauthenticated sending domain. FIX: authenticate the subdomain and publish a DMARC policy.
4. **No bounce handling** — DETECT: repeated sends to a hard-bounced address. FIX: suppress on bounce/complaint webhooks.
5. **Unbreakable unsubscribe** — DETECT: opt-out requires login or a ticket. FIX: one-click signed unsubscribe.
6. **HTML injection** — DETECT: unescaped user content in templates. FIX: escape/encode at render.
7. **Blocking/timeout** — DETECT: slow provider degrades the API. FIX: queued sends + timeouts + retry with backoff.
8. **Consent creep** — DETECT: promotional mail to addresses that only opted into transactional. FIX: separate consent scopes; enforce at send time.

## QUANTITATIVE RULES

- Zero sending in the request path; every send is queued.
- Idempotency key on 100% of sends; duplicate-send tolerance is zero.
- Hard bounce/complaint → suppression within one webhook cycle.
- SPF, DKIM, and a DMARC policy published before any volume; subdomain used for sending.
- One-click unsubscribe on every promotional message; honored immediately.
- Bounce < 2% and complaint < 0.1% as the health thresholds to watch.

## VERIFICATION GATE

- **Queued, not inline?** No provider call in a request handler.
- **Idempotent?** Send key present and checked.
- **Authenticated?** SPF/DKIM/DMARC verified with the actual DNS records or provider report.
- **Suppression wired?** Bounce/complaint webhooks update a suppression list, with evidence.
- **Unsubscribe works?** One-click, immediate, tested.
- **Escaped?** User content is escaped at render; no secrets in URLs/subjects.

```text
[NOTIFICATION DELIVERABLE]
Channel: {email | SMS} · Provider: {name}
Templates: {paths} · version {id} · plain-text alt {yes/no}
Pipeline: event → queue {..} → worker → provider → webhook
Idempotency: {key scheme}
Auth: SPF {ok} · DKIM {ok} · DMARC {policy}
Suppression: {bounce/complaint → list} — evidence {path}
Preferences: consent scopes {..} · unsubscribe {one-click path} · caps {..}
Test sends: {evidence path}
```

## REFERENCES

- `background-jobs-engineer` — the queue and worker mechanics.
- `privacy-compliance` — consent, retention, and PII in message content.
- `i18n`/localization work happening at render time — `frontend-web-engineer` for UI copy parity.
- `integration-engineer` agent — the implementing role.

Ownership: maintained by integration-engineer; email-notifications is the production-domain skill for outbound messaging.
