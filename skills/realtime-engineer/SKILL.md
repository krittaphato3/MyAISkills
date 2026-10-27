---
name: realtime-engineer
description: >-
  Adds live update features: WebSockets, Server-Sent Events, presence, pub/sub fan-out,
  reconnection and backfill, delivery guarantees, and scaling long-lived connections. Use
  when users must see changes without polling. In-process concurrency routes to
  concurrency-engineer; request and response contracts to api-design-architect.
metadata:
  version: 3.0.0
  domain: production
  grade: G2
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: code-implementer
---

# Realtime Engineer

Real-time is not "a socket instead of a request" — it is a state-synchronization problem over an unreliable link. The connection will drop, the client will sleep, messages will arrive out of order or twice, and the server will scale to more than one process. Design for the reconnect, not the happy path.

## WHEN TO USE

- **Live updates** — chat, collaboration, notifications, live dashboards, presence.
- **Push streams** — SSE for one-way server→client feeds, WebSockets for bidirectional.
- **Scaling sockets** — multiple server instances, sticky sessions, pub/sub fan-out.
- **Reliability problems** — missed messages after reconnect, duplicate events, ghost presence.

## WHEN NOT TO USE

- **In-process concurrency** — locks, threads, async primitives: `concurrency-engineer`.
- **Plain request/response API design** — `api-design-architect`.
- **Polling that is good enough** — a 5-second poll is often cheaper and simpler; choose it deliberately.
- **Background/queued work** — `background-jobs-engineer`.

## DECISION TREE

1. **Do you actually need realtime?** Polling, long-poll, or SSE may meet the requirement with far less operational cost. State why the choice is justified.
2. **One-way or bidirectional?** SSE for server→client streams; WebSockets when the client must push frequently.
3. **What is the source of truth?** The server's persisted state — the socket is a delivery channel, not the store.
4. **How does a reconnect recover?** Cursor/sequence number + backfill from persisted state. Without this, you have an unreliable toy.
5. **How does it scale past one process?** A broker (pub/sub) fans out between instances; never rely on in-memory broadcast.
6. **What is the auth model?** Authenticate at connect (token), authorize per channel/topic, and re-check on sensitive actions.
7. **What happens under load?** Backpressure, message coalescing, and a cap on concurrent connections per user.

## PATTERNS

### 1. Delivery and recovery
```text
server state (versioned) ──▶ broker ──▶ instance ──▶ socket ──▶ client
client reconnect: last_seen_version ──▶ server sends delta or a full resync
```
- Every message carries a monotonically increasing version/sequence per channel.
- On reconnect the client sends its last version; the server backfills or tells the client to resync.
- Full resync is always a valid fallback — cheap insurance against gaps.

### 2. Idempotency and ordering
- Clients apply events by id and ignore duplicates; the server never assumes single delivery.
- Out-of-order arrivals resolve by version, not by arrival time.
- Don't rely on delivery order for correctness; carry enough state to reconcile.

### 3. Presence
- Presence is **ephemeral TTL state**, not durable truth: heartbeats with expiry.
- A dropped connection must age out automatically; never let a "user online" flag persist forever.
- Derive presence from the broker, not a single instance's memory.

### 4. Scaling
- Stateless instances + a pub/sub broker; a connection lives on one instance, messages fan out via the broker.
- Sticky routing at the load balancer if the transport requires it (or route by connection at the edge).
- Reconnect storms after a deploy: add jittered backoff on the client and a connection ramp.

### 5. Security
- Authenticate on connect; authorize every subscribe/unsubscribe; never trust a channel name from the client.
- Rate-limit inbound messages per connection and per user.
- Treat client messages as untrusted input — validate the same as any API request.

### 6. Backpressure
- Coalesce high-frequency updates (send latest state, not every intermediate change).
- Cap outbound queue per connection; drop-to-latest beats unbounded buffering.
- Shed connections gracefully when saturated — an overloaded server that drops cleanly beats one that dies.

## FAILURE MODES & MITIGATIONS

Each entry is DETECT → FIX.

1. **Missed messages after reconnect** — DETECT: client state diverges from server. FIX: versioned cursor + backfill or resync.
2. **Duplicate application** — DETECT: the same event applied twice. FIX: id-based idempotency on the client.
3. **Single-instance assumption** — DETECT: in-memory broadcast works locally, fails behind a LB. FIX: broker-mediated fan-out.
4. **Ghost presence** — DETECT: users shown online forever. FIX: TTL heartbeat presence, aged out centrally.
5. **Unauthenticated channels** — DETECT: client subscribes to any topic. FIX: authorize per channel on subscribe.
6. **Reconnect storm** — DETECT: mass reconnect after a deploy overwhelms the server. FIX: jittered client backoff + connection ramp.
7. **Unbounded buffering** — DETECT: memory grows with slow clients. FIX: coalesce + per-connection cap.
8. **Socket as a database** — DETECT: state only exists in messages. FIX: persist to the store; sockets deliver, they do not store.

## QUANTITATIVE RULES

- Every message carries a per-channel version; every client can resync from a version.
- Heartbeat/TTL for presence; age-out window explicit (commonly 30–60s).
- Client reconnect uses jittered exponential backoff; no tight retry loops.
- Outbound buffer per connection is capped; coalescing enabled for high-frequency feeds.
- Inbound messages rate-limited per connection and per user.
- At least one multi-instance test before claiming the design scales.

## VERIFICATION GATE

- **Recovery proven?** A forced disconnect reconnects and reconciles state, with evidence.
- **Idempotent + ordered?** Duplicates ignored and out-of-order resolved by version.
- **Scales beyond one process?** Broker fan-out verified across ≥ 2 instances.
- **Presence ages out?** A killed client disappears within the TTL.
- **Authorized?** Subscribe/authz checked per channel; untrusted channel names rejected.
- **Backpressure handled?** Slow-client behavior defined and bounded.

```text
[REALTIME DELIVERABLE]
Transport: {WebSocket | SSE} · Endpoint: {path}
Source of truth: {store} · Delivery: broker {name} → instance → client
Recovery: version {scheme} · backfill {path} · resync {path}
Presence: TTL {x}s · derived from {broker}
Authz: connect {scheme} · per-channel {rule}
Backpressure: coalescing {on} · buffer cap {n} · inbound rate limit {n/s}
Multi-instance test: {evidence path}
```

## REFERENCES

- `concurrency-engineer` — in-process primitives, carved out above.
- `api-design-architect` — the request/response API beside the socket.
- `background-jobs-engineer` — durable work triggered by realtime events.
- `observability-sre` — connection counts and message-rate metrics.

Ownership: maintained by code-implementer; realtime-engineer is the production-domain skill for live state sync.
