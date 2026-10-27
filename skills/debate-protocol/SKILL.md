---
name: debate-protocol
description: >-
  Runs adversarial multi-agent review with an impartial verdict: independent candidates,
  executable evidence first, capped critique rounds, and a rubric-based judge that cannot
  grade its own work. Use when a change is high-stakes or ambiguous (auth, payments,
  migrations, data loss, architecture trade-offs), when an implementer and reviewer
  disagree, or when the user asks for maximum assurance. Routine changes use
  requesting-code-review; single-step work needs no protocol.
metadata:
  version: 3.0.0
  domain: doctrine
  grade: G3
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: debate-chair
---

# Debate Protocol

How to get a *correct* answer out of several agents without paying for theater. The protocol
exists because the naive version — "spawn three agents and let them discuss" — reliably produces
confident agreement, not truth. Research on multi-agent debate shows most of its apparent gain
comes from **independent sampling plus aggregation**, that agents will flip *correct* answers to
incorrect ones under social pressure, and that an LLM judge prefers longer, more fluent, and
self-authored output. So this protocol is built in the opposite order: independent work, then
objective filters, then a bounded argument, then a blind verdict.

The rule underneath every step: **an executable check outranks any agent's opinion.** A judge may
not overrule a failing test because its explanation sounds better.

## WHEN TO USE

- **High stakes** — authentication, authorization, payments, PII, migrations, data deletion,
  concurrency, or anything where "mostly right" is a production incident.
- **Genuine ambiguity** — two defensible designs with material cost or risk differences, or a
  root cause that several observations support equally.
- **Disagreement** — a critic filed a finding the implementer rejects, or two reviews conflict.
- **No trustworthy oracle** — the change cannot be pinned by tests (architecture, API shape,
  performance strategy), so judgment must be structured instead of vibes.
- **Explicit request** — the user asks for a second opinion, a debate, or "be sure".

## WHEN NOT TO USE

- **Routine change with tests** — one implementer plus the suite is stronger and cheaper. Use
  `requesting-code-review` at T2.
- **Single-step, reversible work** — a typo, a rename, a doc edit. Debate is pure overhead.
- **The evidence is already decisive** — a red test, a stack trace, or a spec sentence settles it.
  Adding agents cannot improve on proof; it can only add noise.
- **You want permission to skip testing** — debate is not a substitute for an oracle. If you
  cannot check behavior at all, say so; do not launder uncertainty through three opinions.
- **Same model, same prompt, same context, three times** — that is not diversity, it is one
  opinion with extra billing.

## DECISION TREE

Pick the tier from `AGENTS.md` §5, then run only the steps that tier requires.

```text
0. FREEZE THE SPEC
   Write the original request verbatim + acceptance criteria to debate/<task>/00-spec.md.
   Include explicit out-of-scope items. Every later claim is judged against this file,
   never against a paraphrase. (Stops "disobeying the specification" and scope drift.)

1. TIER?
   T0/T1 → stop. Use the normal flow; this skill does not apply.
   T2    → steps 2, 3 (single candidate), 5; step 6 only if the critic and implementer disagree.
   T3    → steps 2, 3 (two candidates), 4, 5, 6.

2. INDEPENDENT WORK (no cross-talk)
   - T2: one implementer produces the change + evidence.
   - T3: candidate A = code-implementer (conventional, minimal-diff bias);
         candidate B = independent-solver (correctness-first, may restructure).
         Neither sees the other's diff, notes, or chat. Give each the same spec.
   - In parallel, test-oracle writes acceptance tests from 00-spec.md ONLY — it never
     reads either candidate. Its tests are the shared, neutral oracle.

3. OBJECTIVE FILTER (cheapest evidence first)
   Run the oracle tests, the existing suite, lint, and typecheck against each candidate.
   - 0 survivors  → the task is not solvable as specified. Return to requirements/spec,
                    or report the blocker. Do NOT debate which failure is nicer.
   - 1 survivor   → that is the answer. Skip step 4. Go to 5 (critique) if T2/T3 demands it.
   - 2 survivors  → continue to step 4.
   Record raw output, not a summary.

4. BOUNDED DEBATE (T3 only, max 2 rounds)
   Round 1 — each side receives: the spec, both diffs, both evidence sets, and the rubric.
     Each may file FINDINGS against the other, or concede. A finding needs
     {claim, file:line, why it is wrong, the check that shows it}. No check → label it
     HYPOTHESIS; hypotheses cannot eliminate a candidate.
   Round 2 — only if a finding is contested AND new evidence exists. Reply strictly to
     that finding. Banned: restating the design, appealing to taste, "the tests probably
     miss X" without writing the test, and arguing that a passing check is wrong.
   Stop early when: a candidate fails a check, both sides concede on the same point, one
   side declines to file, or round 2 adds no new evidence. A third round is forbidden;
   escalate to the user instead.

5. INDEPENDENT CRITIQUE (T2 and T3)
   red-team-qa reviews the survivor(s) with fresh context and the rubric. It is
   edit:deny and never fixes what it finds. Every blocking finding must be reproducible
   (a command, a test, a trace) or cite a violated spec line. Severity:
   BLOCKER (correctness/safety/spec), MAJOR (will bite in production), MINOR (clarity),
   NOTE (no action required).

6. ADJUDICATE (blind)
   debate-chair receives candidates labeled A/B with author identity and model stripped.
   It scores the rubric, checks each side's evidence itself, and returns one verdict:
   PASS / CONDITIONAL (with required follow-ups) / FAIL (restart at step 2 with the
   failure mode written into the new brief). If the top two are within 5 points, the
   chair runs the comparison again with A/B swapped; a flipped preference is recorded
   as a tie and resolved by (a) executable evidence, (b) smaller diff, (c) simpler design.
```

## PATTERNS

### 1. Independence is the product
The value is not the conversation; it is that two agents reached an answer without seeing each
other. Generate before you share. If you must share context, share the *spec and evidence*, never
the other candidate's reasoning. Correlated agents repeat the same mistake in harmony.

### 2. Evidence ladder
Rank every claim by what backs it:

```text
1. Reproduction / failing test / trace        (strongest — objective)
2. Existing suite + lint + typecheck          (strong, but only as good as coverage)
3. Spec sentence quoted verbatim              (strong for scope, silent on correctness)
4. Benchmark with pinned env, ≥5 runs         (strong for perf, says nothing about correctness)
5. Cited primary documentation                (strong for API behavior)
6. Agent reasoning with file:line references  (weak — a lead, not a verdict)
7. Unreferenced assertion / intuition         (not evidence)
```

A finding at level 6 may open a debate; only levels 1–5 may close one.

### 3. Finding format (what makes critique checkable)

```text
FINDING {id} — {BLOCKER|MAJOR|MINOR|NOTE}
Claim:      {one sentence: what is wrong}
Location:   {file:line or spec line}
Mechanism:  {why it fails — the causal chain, not "looks risky"}
Evidence:   {command/test/trace that demonstrates it, or HYPOTHESIS}
Fix shape:  {direction only; the critic does not write the patch}
```

### 4. Judge discipline (bias controls that actually matter)
- **Blind to author and model.** Self-preference is real even across models; familiarity bias
  survives a model swap.
- **Rubric first, score second.** Score dimensions separately; a single "quality 8/10" collapses
  into verbosity preference.
- **Both orders for pairwise.** Run A,B and B,A. Disagreement is data, not a tie to break quietly.
- **Allow "tie" and "insufficient evidence".** Forcing a winner manufactures confidence.
- **Different context, same spec.** The chair reads the spec and artifacts, not the argument
  transcript's rhetoric. Long, polished arguments get no credit for length.
- **The judge never grades its own artifact**, and never a candidate it proposed.

### 5. Independent tests are the real oracle
`test-oracle` writes tests from the spec before seeing any implementation. This removes the most
common verification failure: the implementer writes tests that assert what the code does, then the
suite passes by construction. Add one adversarial test per acceptance criterion, plus a regression
test per fixed bug. Where tests can lie (weak assertions), prefer property-based or mutation checks.

### 6. Cost shape
Cheapest sufficient tier, then stop:

| Path | Agents | Relative cost | Use |
|---|---|---|---|
| Solo + tests | 1 | 1× | T0/T1 |
| Solo + independent critic | 2 | ~1.6× | T2 default |
| Dual solve + oracle + critic + chair | 4–5 | ~4–6× | T3 default |
| Full debate, 2 rounds, all roles | 6–7 | ~8–10× | Only when T3 triggers stack up |

Do not run T3 because it exists. Run it because a failed check, a disagreement, or a named risk
made the cheaper path insufficient.

## FAILURE MODES & MITIGATIONS

1. **Consensus theater** — everyone agrees, nothing was verified. *DETECT:* verdict cites agreement
   instead of an artifact. *FIX:* require ≥1 level-1/2 evidence item per rubric dimension.
2. **Sycophantic flip** — a correct candidate is abandoned after pressure. *DETECT:* the winning
   candidate changed without new evidence. *FIX:* round 2 requires new evidence; revert the flip.
3. **Critic becomes author** — the reviewer patches the code, then reviews its own patch.
   *DETECT:* the same agent appears on both sides of the verdict. *FIX:* separation of duties;
   findings only, patch by the implementer, re-review by the critic.
4. **Rubber-stamp chair** — PASS with zero findings on a large diff. *DETECT:* no rubric scores or
   all-identical scores. *FIX:* re-adjudicate with per-dimension numbers and mandatory
   "what would make this fail?" line.
5. **Judge bias** — longer/more confident candidate wins. *DETECT:* winner has weaker evidence but
   more prose. *FIX:* blind labels, swapped order, score evidence first.
6. **Test collusion** — implementer supplies the only tests. *DETECT:* oracle tests and code share
   an author. *FIX:* independent `test-oracle`; treat implementer tests as smoke, not proof.
7. **Infinite refinement** — rounds keep going with no new evidence. *DETECT:* round 3 request.
   *FIX:* hard cap 2; escalate with a written decision request.
8. **Spec drift** — the debate optimizes something the user did not ask for. *DETECT:* requirement-auditor
   finds an unaddressed spec line or an out-of-scope addition. *FIX:* re-freeze the spec, re-run.
9. **Parallel writes collide** — two solvers edit the same checkout. *DETECT:* conflicting or lost
   edits. *FIX:* separate worktrees/copies per candidate, or run candidates sequentially; merge only
   the winner.
10. **Over-escalation** — T3 used on a one-line fix. *DETECT:* cost ≫ change size. *FIX:* tier check
    in step 1 is mandatory; record the trigger that justified escalation.

## QUANTITATIVE RULES

- **Debate rounds:** ≤2. A third requires a new artifact, not a new argument.
- **Candidates:** 2 at T3. More candidates help only when they are genuinely independent and an
  objective filter can rank them; otherwise cost grows faster than quality.
- **Findings per round:** each side ≤5 blocking findings; beyond that the diff is too large to
  review — split it.
- **Verdict threshold:** PASS requires every BLOCKER resolved with level-1/2 evidence and no
  rubric dimension below 6/10. CONDITIONAL requires follow-ups to have an owner and a check.
- **Cost ceiling:** if protocol cost exceeds ~10× the solo cost, stop and report what is unresolved
  rather than buying more opinions.
- **Time ceiling:** if two rounds produce no change in evidence, the bottleneck is missing
  information — go get it (`deep-researcher`) or ask the user.

## VERIFICATION GATE

The debate is complete only when all of these are true:

- [ ] `00-spec.md` exists and contains the user's request verbatim + acceptance criteria.
- [ ] Each candidate has raw evidence attached (test/lint/typecheck output), not a summary.
- [ ] Objective filter ran before any argument; failing candidates were eliminated, not debated.
- [ ] Every blocking finding carries a location and level-1–5 evidence (or is marked HYPOTHESIS).
- [ ] The chair's verdict is blind, rubric-scored, and states which evidence decided it.
- [ ] A requirement-auditor pass confirms every spec line is addressed and nothing out of scope
      shipped.
- [ ] If CONDITIONAL: follow-ups are listed with owner + check, and the user can see them.
- [ ] Cost/tier justification is recorded in one line ("T2 because auth change + 3 files").

```text
[DEBATE VERDICT]
Task: {id}   Tier: {T2|T3}   Rounds: {0|1|2}
Winner: {A|B|rework}   (blind → identity: {agent})
Rubric: spec {x}/25 · evidence {x}/30 · risk {x}/15 · security {x}/15 · maintain {x}/10 · simplicity {x}/5
Deciding evidence: {test/command/output path}
Resolved findings: {n}   Open: {n}   Deferred (user-visible): {n}
Verdict: {PASS|CONDITIONAL|FAIL}
Next action: {merge | fix {id} then re-check | escalate: {question}}
```

## REFERENCES

- `AGENTS.md` §3 (permissions), §5 (work tiers), §8 (definition of done)
- `requesting-code-review` — the T2 gate this protocol extends
- `doubt-driven-development` — the single-reviewer method underlying the critic role
- `test-oracle` (agent) — independent acceptance tests; `test-driven-development` for the loop
- `verification-before-completion` — what counts as evidence and how to attach it
- `requirement-auditor` (agent) — spec-conformance check before a verdict is accepted
- Research basis: multi-agent debate vs self-consistency (Smit et al., ICML 2024; Wang et al.,
  EMNLP 2024; *Debate or Vote*, 2025), LLM-judge bias (Zheng et al., 2023; Saito et al., 2023;
  Shi et al., 2025), MAST failure taxonomy (Cemri et al., 2025), test-oracle weakness (UTBoost,
  2025).
