---
name: threat-modeling
description: >-
  Models security risk before code exists: trust boundaries, data-flow and attack paths, STRIDE
  per boundary, ranked threats, and mitigations that map to concrete tests. Use when adding an
  endpoint, upload, auth flow, admin surface, integration, or multi-tenant data path, or when
  asked "what could go wrong" about a design. Implementing the fixes routes to
  security-hardening-specialist; active exploitation to cybersecurity-specialist.
metadata:
  version: 3.0.0
  domain: security
  grade: G3
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: security-auditor
---

# Threat Modeling

A threat model is a short, ranked list of ways this design can be abused, each paired with a
mitigation you can test. It is not a compliance artifact and not a vulnerability scan. Its value
is timing: it is the only security activity that is cheap *before* the code exists and expensive
after.

## WHEN TO USE

- New or changed trust boundary: public endpoint, auth/session/token flow, file upload, webhook,
  admin or support surface, tenant boundary, payment path.
- A feature that moves PII, credentials, money, or permission decisions.
- Choosing between designs where one has a materially larger attack surface.
- A security review asked "is this safe?" with no model on record.

## WHEN NOT TO USE

- Single-line defensive fixes with an obvious owner (use `security-hardening-specialist`).
- Live incident — contain first (`incident-response-engineer`), model later.
- Dependency CVEs — `dependency-supply-chain-guardian`.
- Compliance mapping (GDPR/CCPA) — `privacy-compliance`. Different question, different evidence.
- You are about to write a 40-page document nobody reads. The model must fit on one page plus a
  table, or it will not be used.

## DECISION TREE

```text
1. SCOPE ONE SENTENCE
   "We are modeling {feature} from {actor} to {data} in {system}." If you cannot write it,
   the design is not ready to model.

2. DRAW THE DATA FLOW (10 lines, boxes and arrows)
   Actors → entry points → services → data stores → external services.
   Mark every trust boundary: where the identity, privilege, or network zone changes.
   Boundaries are where threats live; a diagram without them is decoration.

3. ENUMERATE WITH STRIDE, PER BOUNDARY
   Spoofing · Tampering · Repudiation · Information disclosure · Denial of service ·
   Elevation of privilege. For each boundary ask: what is the worst realistic abuse here?
   Discard categories that genuinely do not apply — say why, in one clause.

4. ATTACK PATHS, NOT LISTS
   Chain two or three weaknesses into a realistic path ("stolen low-priv token + IDOR on
   /orders/{id} = full tenant data"). A path with a plausible actor and payoff outranks
   ten theoretical weaknesses.

5. RANK
   score = likelihood (1-4) × impact (1-4), impact weighted by data sensitivity and blast
   radius. Top 5 get mitigations; the rest are recorded as accepted risk.

6. MITIGATE, THEN TEST
   Each top threat gets: control · where it lives · the test that proves it
   (401/403 case, traversal payload, replay of a signed webhook, rate-limit assertion).
   A mitigation without a test is a hope.
```

## PATTERNS

### 1. One-page model (the deliverable)
```text
FEATURE: {name}   OWNER: {agent/person}   DATE: {iso}
ACTORS: {anonymous, user, admin, service, attacker}
BOUNDARIES: {b1: internet→api, b2: api→db, b3: api→third-party}
TOP THREATS
  T1 {STRIDE} {path}            L{x} I{x} → {score}
     Control: {specific}        Test: {file::case}
  T2 ...
ACCEPTED RISK: {threat — why we accept it — review date}
OPEN QUESTIONS: {what must be decided by a human}
```

### 2. STRIDE prompts that produce real answers
- **Spoofing:** how is identity proven at this boundary? Can a token be replayed, forged, or
  borrowed across tenants? Is there a signature, and is it verified before parsing?
- **Tampering:** what inputs cross here, and which are trusted? Can a client set a price, role,
  owner_id, or status? Are webhooks signed and compared in constant time?
- **Repudiation:** is there an audit trail with actor, action, target, and time? Can a user deny
  an action the system performed?
- **Information disclosure:** does this response include fields the caller should not see? Are
  errors leaking stack traces, SQL, or existence of other tenants' records?
- **Denial of service:** what is unbounded — payload size, regex, pagination, fan-out, login
  attempts, queue depth? What is the per-principal rate limit?
- **Elevation of privilege:** is authorization checked on the object, not just the route? Can a
  user reach an admin action by ID guessing, mass assignment, or a missing middleware?

### 3. The five questions that catch most real bugs
1. Who can call this, and what proves it?
2. What object does this act on, and who is allowed to touch *that object*?
3. What is attacker-controlled, and where does it stop being trusted?
4. What happens on the error path — and what does the error reveal?
5. What is the cost to the attacker per attempt, and the cost to us?

### 4. Multi-tenant rule
Tenant identity comes from the authenticated session, never from a request field. Every query is
scoped by it, including `findById`, updates, deletes, counts, exports, and background jobs. Test
it with two accounts: account B must receive 404/403 for A's IDs, not a filtered empty list that
confirms the ID exists.

### 5. Model drift
Re-run the model when a boundary changes (new integration, new role, new public route, new data
class). A model that predates a boundary is worse than none: it creates false confidence.

## FAILURE MODES & MITIGATIONS

1. **Checklist theater** — all six STRIDE letters "considered", no path, no test. *DETECT:* zero
   concrete attack paths. *FIX:* write one realistic chain end-to-end or delete the row.
2. **No boundaries** — a diagram of components with no privilege changes marked. *DETECT:* threats
   cannot be attached to a location. *FIX:* redraw with boundaries first.
3. **Unranked dump** — 40 threats, no priorities. *DETECT:* every mitigation "should" happen.
   *FIX:* score and cut to top 5; record accepted risk explicitly.
4. **Untestable controls** — "validate input", "use least privilege". *DETECT:* no test path.
   *FIX:* name the check and the case that fails without it.
5. **Client-trusted identity** — tenant/user/role read from the request. *DETECT:* grep for
   `req.body.userId`, `tenantId` params, hidden role fields. *FIX:* derive from session; add the
   two-account test.
6. **Stale model** — design changed, model did not. *DETECT:* model date predates the last boundary
   change. *FIX:* version the model; re-run on boundary change.

## QUANTITATIVE RULES

- One page + ≤10 table rows; top 5 threats get mitigations, the rest are accepted risk with a date.
- Every mitigation has a test; every high/critical threat has a two-account or replay check.
- Likelihood × impact ≥ 9 → must be fixed before release, not deferred.
- Re-model on any new trust boundary; otherwise review at least every 6 months for live surfaces.
- Time-box: 30–60 minutes for a normal feature. Longer means the scope is too large — split it.

## VERIFICATION GATE

- [ ] Scope sentence names feature, actor, data, and system.
- [ ] Diagram marks every trust boundary; each threat is attached to one.
- [ ] At least one multi-step attack path exists (not only isolated weaknesses).
- [ ] Top threats are ranked by likelihood × impact with numbers.
- [ ] Each top threat has a control, a location, and an executable test.
- [ ] Accepted risks are written with a reason and a review date.
- [ ] Tenant/user identity is derived from the session everywhere it is used.

## REFERENCES

- `security-hardening-specialist` — implementing the controls
- `cybersecurity-specialist` — authorized validation by attack
- `privacy-compliance` — personal-data obligations and evidence
- `api-design-architect` — auth and error contracts at the edge
- `debate-protocol` — T3 path when a security decision is contested
