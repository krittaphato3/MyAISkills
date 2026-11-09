---
name: plugin-architecture
description: >-
  Designs extension points that third parties or other teams build against: a versioned plugin
  contract, capability and permission model, lifecycle and discovery, in-process vs out-of-process
  isolation, and the conformance suite that keeps plugins working across releases. Use when adding
  a plugin system, webhooks and event hooks, a marketplace, or an internal extension API. Normal
  REST/GraphQL API design routes to api-design-architect.
metadata:
  version: 1.0.0
  domain: architecture
  grade: G3
  status: active
  last-reviewed: '2026-11-08'
  authored-by: solution-architect
---

# Plugin Architecture

A plugin API is a promise you cannot take back. Every extension point becomes a compatibility
obligation, so the design work is deciding what **not** to expose.

## WHEN TO USE

- Adding a plugin system, extension marketplace, or third-party integration surface.
- Users need to hook into your events, UI, data model, or build pipeline.
- An internal extension API already exists and has become a compatibility burden.
- Choosing between in-process hooks and an out-of-process plugin host.
- A plugin change must not break installed plugins, or must break them loudly.

## WHEN NOT TO USE

- The consumer is your own frontend calling your own backend. That is `api-design-architect`.
- The integration is one-way notification with retries. That is `webhooks` inside
  `third-party-integration`.
- The real need is configuration, not code. Ship config, not an extension point.
- There is exactly one plugin author: you. Build it as an internal module and skip the contract.

## DECISION TREE

```text
Does this need to be a plugin at all?
├─ no, it is configuration ........................ config schema + validation, not an API
├─ no, it is one partner .......................... a private integration behind a feature flag
└─ yes: unknown authors, unknown code, over time

Then pick the trust and isolation model:
├─ trusted first-party, same release train ....... in-process: hooks, shared types, fastest
│  └─ failure: a plugin's exception takes down the host → still must be sandboxed at the call site
├─ semi-trusted, versioned separately ............ out-of-process: RPC over stdio/HTTP, own memory
│  └─ cost: serialization, latency, deployment complexity → worth it for crash isolation
└─ untrusted, public marketplace ................. sandboxed runtime (WASM, worker, container)
   └─ cost: capability API, resource limits, no ambient filesystem/network

Then define the contract surface:
├─ manifest ..................................... id, version, engine range, capabilities, entry
├─ lifecycle .................................... install → activate → deactivate → uninstall
├─ extension points ............................. named, typed, and few
├─ events ....................................... versioned payloads, at-least-once, ordered per key
├─ capabilities ................................. declared, granted at install, checked at call
└─ errors ....................................... a plugin failure never fails the host request
```

### The contract decisions that hurt later

| Decision | Default | Why |
|---|---|---|
| Version scheme | Your own API semver, independent of app semver | App 4.2.0 breaking a plugin should be an API decision |
| Extension points | Named operations with typed input/output | Free-form hooks become untestable |
| Discovery | Manifest file, one per plugin | Scanning code for magic exports breaks on refactor |
| Capability grants | Declared in manifest, granted by the user/admin | Ambient authority is unrecoverable |
| Failure boundary | Every call has a timeout and a catch | One plugin must not take down the host |
| Deprecation | Mark, warn for one minor, remove at next major | Silent removal breaks installs |
| Compatibility test | Conformance suite runs against every release | Otherwise the contract rots |

## FAILURE MODES & MITIGATIONS

| Failure | Mechanism | Mitigation |
|---|---|---|
| Leaky core types | Plugin imports internal objects, then internals change | Publish DTOs only; no internal types in the signature |
| Synchronous hooks in the request path | One slow plugin multiplies your p99 | Async by default; sync hooks only with a hard timeout |
| No version negotiation | Old plugin loads into a new host and misbehaves | Manifest `engine` range checked at load, refuse loudly |
| Ambient authority | Plugin reads env vars and the filesystem | Capability API; deny by default |
| Cascade failure | Plugin throws, host request 500s | Isolate at the boundary; degrade, do not propagate |
| Plugin sprawl | 40 hooks, none documented | Cap the surface; each addition needs a written use case |
| Untested compatibility | Plugins break on every release | Conformance suite + one reference plugin per extension point |
| No uninstall path | Plugin data and hooks persist after removal | Lifecycle must include cleanup and deregistration |

## QUANTITATIVE RULES

- **One extension point per real use case.** No speculative hooks.
- **Every plugin call has a timeout** (default 100-500 ms in-request, unbounded off-path).
- **Capabilities are denied by default**; the manifest requests, the user grants.
- **Conformance suite runs in CI** against the released contract, on every build.
- **Deprecation window: one minor version**, with a runtime warning naming the replacement.
- **Reference plugin per extension point**, kept in-repo, exercised by the suite.

## VERIFICATION GATE

- [ ] A plugin that throws, hangs, or returns garbage cannot fail a host request.
- [ ] An old plugin against a new host is refused with a clear version error, not a crash.
- [ ] A plugin without a declared capability is denied at runtime and the denial is tested.
- [ ] Uninstall removes hooks, scheduled work, and stored data.
- [ ] Contract conformance suite passes in CI from a clean checkout.
- [ ] Deprecated surface emits a warning that names the replacement.

## REFERENCES

- `api-design-architect` for the contract shape when the surface is request/response.
- `third-party-integration` for outbound webhooks and signed callbacks.
- `security-hardening-specialist` for the trust boundary and capability enforcement.
- `distributed-systems-engineer` for ordering and delivery guarantees of plugin events.
- `background-jobs-engineer` for plugin work that must not block the request.
- `test-engineer` for the conformance suite.
