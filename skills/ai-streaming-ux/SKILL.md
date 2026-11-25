---
name: ai-streaming-ux
description: "Builds resilient React AI chat, SSE/WebSocket streaming states, tool-call card reconciliation, and optimistic updates. Use when implementing AI drawers, clarify cards, or live UI state."
metadata:
  version: 1.0.0
  domain: delivery
  grade: G2
  status: active
  last-reviewed: '2026-11-25'
  authored-by: ui-ux-architect
---

# AI Streaming UX & State Reconciliation

Fixes the exact failure modes of AI web UIs: stale tool cards clickable after completion, phantom partial JSON crashes, lost abort signals, and out-of-order optimistic messages.

## WHEN TO USE

- Building or debugging AI chat drawers, Clarify/Proposal cards, streaming markdown, or SSE/WebSocket UI flows.
- Reconciling optimistic client state with persisted server session history on reload or revisit.

## WHEN NOT TO USE

- Backend WebSocket/pub-sub transport infrastructure alone — `realtime-engineer`.
- Visual CSS layout spacing without state logic — `ui-layout-spacing`.

## DECISION TREE

```text
1. MODEL CARD LIFECYCLE AS A STRICT DISCRIMINATED UNION
   status: "pending" | "submitting" | "accepted" | "rejected" | "expired"
   Never derive actionability from loose booleans (`!isLoading && !clicked`).
   On session revisit/hydration: derive terminal state from server ledger (`answeredAt` / `resolvedToolCallId`),
   locking interactive controls deterministically when terminal.

2. STREAMING & ABORT DISCIPLINE
   - One `AbortController` per active turn; abort previous stream before starting a new message or unmount.
   - Buffer partial SSE chunks cleanly; parse tool payloads defensively at frame boundaries.

3. OPTIMISTIC ROLLBACK & IDEMPOTENCY
   - Attach stable client `idempotencyKey` (`clientMessageId`) to every user action so double-clicks or reconnects merge instead of duplicating.
   - On mutation error, revert optimistic card state cleanly and expose explicit retry.
```

## FAILURE MODES & MITIGATIONS

1. **Zombie Clickable Card on Revisit** — DETECT: local `useState(false)` resets to clickable after navigating away and back. FIX: persist resolution in session state / server payload and disable whenever `status !== "pending"`.
2. **Double-Submit Race** — DETECT: rapid clicks fire duplicate tool confirmations. FIX: transition synchronously to `"submitting"` before awaiting network call.
3. **Stale Closure Over Stream** — DETECT: chunk callback overwrites newer messages. FIX: accumulate via functional state updater (`setMessages(prev => ...)`) keyed by `turnId`.

## VERIFICATION GATE

- [ ] Card state is a discriminated union with terminal lock verified across page/session reload.
- [ ] Rapid double-click and stream-abort unit tests pass (`vitest run <file> && tsc --noEmit`).

## REFERENCES

- `frontend-web-engineer` — React component & state boundaries
- `typescript-best-practices` — discriminated unions without `as any`
- `realtime-engineer` — transport reconnect and backfill semantics
