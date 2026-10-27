---
name: context-engineering
description: >-
  Manages what an agent knows at each step: context budgets, retrieval over dumping, file-based
  handoffs, subagent isolation, compaction, and durable project conventions. Use when a task
  outgrows one context window, an agent starts forgetting earlier decisions, long sessions
  degrade, or output quality drops as the conversation grows. Prompt wording alone routes to
  llm-app-engineer; whole-session state transfer routes to session-continuity.
metadata:
  version: 3.0.0
  domain: doctrine
  grade: G3
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: meta-architect
---

# Context Engineering

Context is the scarcest resource in agentic coding, and it degrades before it runs out. Models
attend less reliably to the middle of a long prompt, instructions compete with retrieved code,
and every pasted stack trace crowds out the plan. The discipline is not "fit more in" — it is
**decide what the next step actually needs, put that in, and keep everything else on disk**.

## WHEN TO USE

- A task spans multiple files or sessions and the thread is visibly losing earlier decisions.
- You are about to paste a large file, log, or search result into the main thread.
- You are writing a brief for a subagent (what it sees *is* its world).
- Output quality degrades late in a session: repeated questions, re-read files, contradicted plans.
- You are designing a long-running agent, a memory file, or a compaction strategy.

## WHEN NOT TO USE

- Short, single-file tasks — retrieval overhead exceeds the benefit.
- The answer is one command away (`git diff`, `--help`, one grep) — run it instead of theorizing.
- You are really designing prompts/model behavior for a product feature: that is
  `llm-app-engineer`, not this.

## DECISION TREE

```text
1. WHAT DOES THE NEXT STEP NEED?
   Write the decision the agent must make next. List only the facts required for it.
   Everything else is out of scope for this context window.

2. POINT, DON'T PASTE
   Files: give path + line range, not the whole file.
   Search: give the query and the 3-10 relevant hits, not the raw 400-line output.
   Logs: give the failing section + the command that produced it.
   Docs: give the URL + the quoted rule, not the page.

3. IS THIS THE MAIN THREAD OR A SUBAGENT?
   Main thread keeps: the plan, the ledger, open questions, the user's constraints.
   Subagent gets: one brief, its files, its acceptance criterion, its output contract.
   A subagent that needs the whole conversation is a sign the subtask is too big.

4. WILL THIS OUTLIVE THE WINDOW?
   Yes → write it to a file now: decisions.md, plan.md, handoff.md. Files survive compaction;
   chat does not. Name the next action explicitly in the handoff.

5. COMPACT DELIBERATELY
   Summarize completed work into outcome + artifact path + open risk. Drop raw reads, dead
   ends, and superseded plans. Never drop: user constraints, irreversible decisions, red gates.

6. RE-ANCHOR AFTER COMPACTION
   Restate the goal, the spec, and the current gate in one short block before continuing.
   Compaction loses *why* first; the *what* survives.
```

## PATTERNS

### 1. Context budget by role
- **Main thread (orchestrator):** plan, ledger, constraints, verdicts. Target ≤30% of the window
  before the first dispatch; file work belongs to subagents.
- **Implementer:** spec + target files + test command + output contract. Nothing about other
  subtasks.
- **Reviewer:** diff + tests + acceptance criteria + rubric. Never the author's reasoning, or the
  review inherits the author's blind spots.
- **Judge/chair:** spec + artifacts + rubric, authors blinded. See `debate-protocol`.

### 2. Durable instruction files
Put conventions where they are cheap to read and hard to lose:
- `AGENTS.md` — invariants: permissions, tiers, roster, definition of done.
- `docs/decisions.md` (or ADRs) — why things are the way they are.
- `docs/handoff.md` — current state, next action; rewritten, not appended.
Keep the always-loaded file short. Every line competes with the task; a 400-line rules file is
mostly ignored. Rules that matter are short, imperative, and testable.

### 3. Retrieval discipline
- Search by symbol/definition first (`rg -n "func Name|class Name|export function"`), then by
  call site, then by concept.
- Read in expanding rings: target symbol → its file's imports/exports → immediate callers → tests.
- Prefer the type/interface file over the implementation when you need the contract.
- Stop when the next read would not change the decision. "One more file" is how contexts die.

### 4. Briefs as the isolation boundary
A subagent's prompt is a context spec. Include: mission, files, non-goals, acceptance criterion,
evidence to produce, and output format. Exclude: conversation history, unrelated subtasks, your
own uncertainty (state it as a question, not as fog).

### 5. Compaction without amnesia
```text
[COMPACTION]
Goal: {one sentence, user's words}
Constraints: {non-negotiables + permissions}
Done: {item → artifact path}
Current gate: {criterion + status}
Open questions: {n items, with owner}
Next action: {single concrete step}
Do not redo: {dead ends, rejected approaches + why}
```

## FAILURE MODES & MITIGATIONS

1. **Context dumping** — whole files/logs pasted "just in case". *DETECT:* window fills before the
   first edit; the agent re-reads what it already has. *FIX:* point-don't-paste; extract the
   relevant 20 lines.
2. **Instruction bloat** — a rules file so long the model follows none of it. *DETECT:* rules
   violated that are stated in the file. *FIX:* cut to the invariants; move detail into skills.
3. **Compaction amnesia** — the goal or a constraint vanishes after summarization. *DETECT:* the
   agent proposes something the user already rejected. *FIX:* files for decisions; re-anchor block.
4. **Subagent context leak** — the brief includes unrelated history, so the subagent wanders.
   *DETECT:* output touches files outside the brief. *FIX:* tighten the brief; restate out-of-scope.
5. **Stale retrieval** — old code/docs outrank current ones. *DETECT:* recommendations contradict
   the installed version. *FIX:* `source-driven-development`; read the version file first.
6. **Middle-of-window loss** — critical facts buried in a long prompt get ignored. *DETECT:* the
   agent contradicts a fact stated mid-context. *FIX:* restate critical facts at the decision point.

## QUANTITATIVE RULES

- Main-thread tool calls before first dispatch: <5 reads/searches; use subagents for sweeps.
- Target ≤30% window used before the first subagent; compact at ~70%.
- One brief = one subtask; ≤8 files or ≤2 subsystems per brief. More means split it.
- Always-loaded instruction files: target <200 lines total; hard ceiling 300.
- Handoff files: ≤60 lines, rewritten not appended, next action in the first 10 lines.

## VERIFICATION GATE

- [ ] The next action is stated in one sentence and needs only the context you kept.
- [ ] No raw file/log dump in the main thread where a path + range would do.
- [ ] Every subagent brief has mission, files, out-of-scope, acceptance criterion, output format.
- [ ] Irreversible decisions and open risks are written to a file, not only in chat.
- [ ] After compaction, the goal + constraints + current gate were restated and match the user's
      original request.

## REFERENCES

- `session-continuity` — handoff format for long/resumed sessions
- `token-economy` — the cost model (caches, tiering, fan-out) behind these budgets
- `debate-protocol` — who sees what during adversarial review
- `AGENTS.md` §9 — cost and fan-out discipline
- `system-instructions` — delegation and waiting protocol
