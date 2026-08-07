# source-driven-development — Flagship Eval

## 1. Trigger test

Fire (5):
1. "Write a React 18 component using the exact current hook signatures — fetch the docs first."
2. "Upgrade this project to a new framework major; re-verify every changed signature against official release notes."
3. "Adapt a tutorial snippet to production — check every claim against the official source."
4. "Verify existing code still matches the current API after a dependency update."
5. "Port a pattern between two framework majors; each target's own official API is fetched."

Not fire (3):
6. "Fix this one-line correction with an already-known, unchanged signature."
7. "Write pure standard-library-agnostic math logic — no external API."
8. "The user explicitly says 'just do it quickly, skip verification'."

## 2. Quality rubric (1-5)
(a) decision tree covers branches: 5/5 — detect-deps (manifest), fetch-official, exact-signature, cite-URLs, surface-conflicts.
(b) failure modes have detection+mitigation: 5/5 — deprecated-api, skipping-dependency-files, unofficial-source, version-fog, stale-recall, unverified-claims, signature-drift, wrong-source-preference all DETECT/FIX.
(c) quantitative rules are numbers: 5/5 — signature 100%, cite-priority ranks, page-depth targeted, citation-density 1/decision, freshness on major bump, 0-unsourced.
(d) verification gate executable: 5/5 — versions-identified, docs-fetched, sources-official, no-deprecated, conflicts-surfaced, unverified-flagged, citations-resolvable; output shape has dependency/decision/conflict/unverified blocks.
(e) references authoritative: 5/5 — MDN, W3C/WHATWG, caniuse, manifests, semver all canonical; hierarchy explicit.
(f) no contradictions: 5/5 — aligned with systems-core-architect (verified API ground truth) and systematic-debugging; no conflict.

## 3. Reference task
Add a React 18 hook pattern to an existing project. The skill must read the manifest, fetch the official docs, implement the exact signature, cite the full targeted page URL, and flag any doc-vs-code conflict rather than silently resolving it.
