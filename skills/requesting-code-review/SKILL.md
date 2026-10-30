---
name: requesting-code-review
description: >-
  Packages a change for independent review and gates it on the verdict: scope, diff, tests,
  threat surface, and explicit acceptance criteria. Use before merging any non-trivial change.
  Deciding between conflicting reviews or candidate implementations routes to debate-protocol; the
  author's self-check never replaces review.
metadata:
  version: 3.1.0
  domain: doctrine
  grade: G3
  status: active
  last-reviewed: '2026-10-30'
  owned-by-agent: red-team-qa
---

# Requesting Code Review

Review is a gate, not a courtesy. Its job is to find what the author cannot see: a missed
requirement, a broken invariant, an authorization check on the wrong object, a test that asserts
nothing. A review that finds nothing on a large diff is not evidence of quality — it is evidence
that the review did not happen.

## WHEN TO USE

- Any PR, any multi-file change, anything touching auth, money, PII, migrations, or data deletion.
- After the suite is green, before commit or merge.
- When a subagent's work will be integrated and the brief's criterion is not trivially checkable.
- When the same defect class has escaped before — ask for that class explicitly.

## WHEN NOT TO USE

- Whitespace/comment/typo-only changes — the suite plus a self-read is enough.
- Active incident rollback — restore first, review in the postmortem.
- An unmerged experiment — do not spend review budget on code that will be deleted.
- As a substitute for tests. Review catches design and intent; it cannot prove runtime behavior.

## DECISION TREE

```text
1. ASSEMBLE THE PACKAGE (before dispatch)
   - Diff (surgical, no unrelated files)
   - Change intent: what behavior changes, for whom, why
   - Acceptance criteria, quoted from the user/spec
   - Evidence: test output, lint/typecheck, benchmark if perf
   - Threat surface: inputs, trust boundaries, data touched
   - Out of scope: explicitly excluded files/behaviors
   Missing any of these → the review will be vague. Fix the package first.

2. CHOOSE THE REVIEWER
   Standard change        → red-team-qa (adversarial, edit:deny)
   Security-sensitive     → red-team-qa + security-auditor (defense in depth)
   Domain-specific risk   → relevant specialist (db-architect, compliance-engineer, ...)
   Two reviewers disagree → debate-protocol with debate-chair
   Never the author. Never the agent that proposed the design.
   Split the review into two independent axes (standards, then spec) per
   `references/two-axis-review.md`. One blended verdict hides the change that is clean
   but solves the wrong problem.

3. REVIEW AGAINST THE RUBRIC, NOT VIBES
   Correctness · spec conformance · security · regressions · performance · maintainability ·
   test quality. Every finding needs {severity, location, mechanism, evidence}.

4. TRIAGE
   BLOCKER → fix before merge
   MAJOR   → fix now, or file with an owner and a date (user-visible)
   MINOR   → fix if local, defer otherwise
   NOTE    → no action; recorded for context
   A finding without evidence is a NOTE, never a BLOCKER.

5. FIX, RE-VERIFY, RE-REVIEW ONLY IF SCOPE CHANGED
   The author fixes; the reviewer verifies the fix against the finding. A fix that changes the
   design restarts the review. Do not re-review the whole diff for a one-line follow-up.

6. GATE
   Merge only on PASS, or CONDITIONAL with every follow-up owned. Record the verdict with the
   change, not just in chat.
```

## PATTERNS

### 1. Review brief
```text
REVIEW — {title}
Intent:      {behavior change in one sentence}
Spec:        {user request verbatim + acceptance criteria}
Diff:        {files, LOC, base..head}
Evidence:    {test command/output, lint, benchmark}
Threat surface: {inputs, auth, data class, boundaries crossed}
Risk class:  {logic | security | data | perf | migration | UI}
Out of scope: {explicit exclusions}
Wanted:      findings with severity + location + evidence; verdict PASS|CONDITIONAL|FAIL
```

### 2. What to interrogate, by risk class
- **Logic:** boundaries (0, 1, n, max), null/empty, ordering, duplicate calls, partial failure.
- **Security:** every input trusted? authz on the *object* not the route? tenant from session?
  secrets logged? error messages leaking?
- **Data:** migration reversible? backfill idempotent? constraint added with existing bad rows?
  transaction boundaries correct? concurrent writes?
- **Performance:** N+1, unbounded query/list, blocking work in a request, missing index.
- **Concurrency:** shared mutable state, lock ordering, cancellation, retries without idempotency.
- **UI:** loading/empty/error states, keyboard access, focus after navigation, layout shift.
- **Tests:** would they fail if the fix were reverted? are they asserting outcomes?

### 3. Finding format
```text
{BLOCKER|MAJOR|MINOR|NOTE} {file}:{line}
Claim:     {what is wrong}
Mechanism: {why — the causal chain}
Evidence:  {test/command/repro, or HYPOTHESIS}
Fix shape: {direction; reviewer does not patch}
```

### 4. Reviewer discipline
- Read the diff first, then the tests, then the surrounding code the diff depends on.
- Verify claims; do not accept "tested locally".
- Stay inside the briefed scope — redesign notes are a separate conversation.
- If nothing blocks, say so *and* name the 2–3 riskiest things you checked. Zero findings must be
  explained, not asserted.

### 5. Author discipline
- Keep diffs reviewable: one concern, one change. >400 LOC needs a stack of smaller reviews.
- Pre-empt the obvious questions in the brief (why this approach, what was rejected).
- Do not argue with a finding; either fix it, disprove it with evidence, or record it as accepted.

## FAILURE MODES & MITIGATIONS

1. **Rubber stamp** — PASS with no findings on a non-trivial diff. *DETECT:* no checklist items, no
   named risks. *FIX:* re-dispatch with explicit questions for the risk class.
2. **Review too late** — after merge/push. *DETECT:* verdict predates the commit. *FIX:* gate in the
   workflow; review before commit.
3. **Scope creep** — reviewer redesigns the feature. *DETECT:* findings about unrelated code.
   *FIX:* enforce out-of-scope; capture redesign ideas as NOTES.
4. **Unreproducible blocker** — "this could race" with no path. *DETECT:* no evidence field. *FIX:*
   downgrade to NOTE or produce the interleaving/test.
5. **Style-nit avalanche** — 30 minor comments, real bug missed. *DETECT:* findings mostly formatting.
   *FIX:* automate style (lint), spend reviewer attention on correctness.
6. **Author bias** — the author reviews their own work. *DETECT:* same agent in both roles. *FIX:*
   independent agent; for T3, `debate-protocol`.
7. **Stale verdict** — code changed after review. *DETECT:* diff hash/commit differs. *FIX:*
   re-review the delta before merge.

## QUANTITATIVE RULES

- Non-trivial = >5 lines, >1 file, or touches auth/data/money/security/config.
- One review pass; re-review only the changed delta unless scope changed materially.
- ≤400 LOC per review; larger changes are split.
- Every BLOCKER has evidence; ≤5 blockers per pass (more means split the change).
- Verdict recorded with the change: PASS / CONDITIONAL (owned follow-ups) / FAIL.

## VERIFICATION GATE

- [ ] Package complete: intent, spec, diff, evidence, threat surface, out of scope.
- [ ] Reviewer is independent and edit-denied.
- [ ] Findings carry severity + location + mechanism + evidence.
- [ ] Every BLOCKER resolved or the change is not merged.
- [ ] CONDITIONAL follow-ups have an owner and a check.
- [ ] Final verdict attached to the change, with the evidence it relied on.

## REFERENCES

- `debate-protocol` — when reviews conflict or the change is T3
- `verification-before-completion` — evidence requirements
- `security-hardening-specialist` / `threat-modeling` — security review inputs
- `AGENTS.md` §3 — commit/push permission (review is not approval to ship)
