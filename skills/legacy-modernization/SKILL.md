---
name: legacy-modernization
description: >-
  Modernizes legacy systems safely: characterize current behavior, find seams, migrate
  incrementally (strangler fig), run old and new in parallel, cut over with rollback, and
  decommission. Use when replacing a framework, extracting a service, upgrading a major version,
  untangling a monolith, or when "we can't touch it because nobody understands it". Ordinary
  behavior-preserving cleanup routes to refactoring-intelligence; greenfield design to
  system-design-architect.
metadata:
  version: 3.0.0
  domain: architecture
  grade: G3
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: migration-engineer
---

# Legacy Modernization

Legacy code is code that works and that nobody can safely change. The goal is not a rewrite; it is
a sequence of small, reversible moves that each leave the system working, each proven by
characterization tests, and each independently deployable. Big-bang rewrites fail because they
concentrate all risk at the end, when the deadline is closest and the knowledge is thinnest.

## WHEN TO USE

- Replacing a framework, runtime, or major dependency version.
- Extracting a module or service out of a monolith.
- A system with no tests that must change anyway.
- Data/schema migration with existing production rows.
- A codebase where "don't touch it" is the standing policy.

## WHEN NOT TO USE

- The code is covered by tests and the change is local — just refactor
  (`refactoring-intelligence`).
- A greenfield component with no legacy constraint — design it (`system-design-architect`).
- The real problem is one bug — `systematic-debugging`.
- There is no business pressure and no risk: modernization for its own sake burns the budget that
  the next incident needs.

## DECISION TREE

```text
1. WHY NOW?
   Name the forcing function (EOL runtime, security, velocity, cost, hiring). If it is only
   aesthetic, stop. The reason determines what "done" means.

2. CHARACTERIZE BEFORE YOU CHANGE
   Write tests that pin CURRENT behavior, including the weird parts. Golden/snapshot outputs,
   recorded requests, property tests over real inputs. If behavior is undocumented, the tests
   ARE the documentation. Never "fix" behavior during characterization — record it.

3. MAP THE SEAM
   Find the narrowest boundary you can cut at: a module interface, an HTTP route, a queue
   consumer, a DB view. The seam is where old and new can coexist. Prefer seams with few
   callers and a stable contract.

4. STRANGLE INCREMENTALLY
   New implementation behind the seam → route a slice of traffic/callers to it → compare →
   widen. Each step ships. Nothing is "almost done" for weeks.

5. PARALLEL RUN AND COMPARE
   Old and new both produce output; diff them on real inputs (shadow traffic, replay, sampled
   production data). Differences are either bugs or intentional changes — classify every one.

6. CUT OVER WITH A ROLLBACK
   Feature flag or routing switch, not a deploy. Define the rollback trigger and rehearse it.
   Keep the old path deployable until the new one has survived real load for an agreed window.

7. DECOMMISSION
   Delete the old path, the flag, the dual writes, and the compatibility shims. Un-deleted
   migration code becomes the next legacy. Update docs/ADRs.
```

## PATTERNS

### 1. Characterization tests (the safety net)
- Capture real inputs and current outputs; assert equality, not intent.
- Cover the ugly cases first: nulls, legacy encodings, timezone quirks, rounding, empty lists,
  duplicate keys, partial records.
- Golden files for large outputs; property tests for invariants the old code accidentally holds.
- Run them against the OLD code first. A characterization test that fails on legacy is a bug in
  your understanding, not permission to change behavior.

### 2. Seam selection ladder (prefer top)
1. Pure function with a stable signature.
2. Module/package boundary with an interface.
3. HTTP route or RPC handler.
4. Queue/topic consumer.
5. Database view or read replica (last resort; hides coupling rather than removing it).

### 3. Strangler shape
```text
Callers → [router/flag] → old impl (default)  ─┐
                       → new impl (slice)      ├→ compare/diff → metrics
Both write/read behind an adapter; no caller knows which side answered.
```
Routing lives in one place. If callers start branching on "old vs new", the seam leaked.

### 4. Data migration rules
- Expand → migrate → contract: add nullable column, dual-write, backfill in batches, verify
  counts/checksums, switch reads, then drop the old column in a later release.
- Every backfill is idempotent, resumable, and rate-limited. Assume it will be interrupted.
- Never migrate and change semantics in the same step; you lose the ability to tell which caused
  the difference.

### 5. Parallel-run comparison
Sample or replay real traffic. Compare outputs field by field, with a tolerance policy for
timestamps/float noise. Track: match rate, difference classes, and the top 5 diff causes. Cut over
only when the diff classes are all explained and accepted.

### 6. Rollback rehearsal
Before cutover: flip the flag back in staging, confirm the old path still works with data written
by the new path. A rollback that corrupts data is not a rollback.

## FAILURE MODES & MITIGATIONS

1. **Big-bang rewrite** — months of work, one cutover. *DETECT:* no intermediate deploys. *FIX:*
   re-plan as strangler slices; each slice must ship.
2. **Characterization by assumption** — tests assert what the code "should" do. *DETECT:* tests fail
   on legacy. *FIX:* record actual behavior; move desired changes to a later step.
3. **Dual-write drift** — old and new diverge silently. *DETECT:* no comparison metrics. *FIX:*
   shadow compare + reconciliation job + alert on divergence.
4. **Flag debt** — the old path never dies. *DETECT:* flags older than 90 days. *FIX:* schedule
   decommission as part of the migration, with an owner and a date.
5. **Semantic change smuggled in** — behavior differs and nobody knows if it is a bug. *DETECT:*
   unexplained diff class. *FIX:* separate behavior change into its own release with its own tests.
6. **Irreversible data step** — destructive migration with no backup/rollback. *DETECT:* drop/alter
   without a rehearsal. *FIX:* expand/contract, backups, and a tested restore.
7. **Knowledge loss** — the only person who understood it leaves. *DETECT:* bus factor 1. *FIX:*
   characterization tests + ADR + pair review before they go.

## QUANTITATIVE RULES

- Every migration slice deploys independently and leaves the system working.
- Characterization coverage: every entry point touched by the seam has at least one pinned test.
- Backfills: batched (≤10k rows/step), resumable, idempotent, throttled, with a verification query.
- Parallel run: ≥99% match on sampled traffic before cutover; every diff class explained.
- Flag lifetime ≤90 days from cutover; decommission is part of Done.
- No step may both migrate data and change behavior.

## VERIFICATION GATE

- [ ] Forcing function and "done" definition written down.
- [ ] Characterization tests pass against the OLD implementation.
- [ ] The seam is named and has one routing point.
- [ ] Every slice shipped behind a flag; rollback rehearsed in staging.
- [ ] Parallel-run match rate recorded, with each diff class classified.
- [ ] Old path, dual writes, flags, and shims deleted (or a dated plan exists).
- [ ] ADR updated with the migration shape and the decommission date.

## REFERENCES

- `refactoring-intelligence` — behavior-preserving cleanup within a slice
- `database-at-scale` — zero-downtime migration mechanics
- `system-design-architect` — target architecture and capacity
- `adr-engineering` — recording the migration decision and its exit criteria
- `devops-pipeline-engineer` — flags, staged rollout, rollback automation
