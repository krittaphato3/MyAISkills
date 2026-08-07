---
name: incident-response-engineer
description: Use when a production service is degraded, unavailable, or failing its SLOs and you must classify severity, contain the blast radius, coordinate a war room, and drive a blameless postmortem with measurable follow-through.
version: 1.0.0
grade: G3
domain: production
status: active
last-reviewed: 2026-08-06
owned-by-agent: devops-engineer
supersedes: ""
---
# incident-response-engineer

World-class reference for running a production incident from first page to closed postmortem. Covers SEV1-3 classification with time-to-mitigate targets, contain-first sequencing (rollback vs forward-fix vs feature-flag off), war-room roles and communication cadence, quantitative MTTR/MTTD and error-budget burn-rate rules, and a verification gate built on game-day drills and postmortem action-item follow-through. Numbers, not adjectives; every rule is measurable and every metric has a target. Self-contained and actionable in the field without external tooling.

## WHEN TO USE

Use this skill when any of the following is true:

- A service or dependency is degraded, erroring, or down and customers are affected or at risk.
- An alert fires above its configured threshold or paging duty is tripping, and you must decide severity and who acts first.
- An error budget is burning fast enough that a launch, deploy, or experiment must stop.
- You are choosing between rollback, forward-fix, and feature-flag off, and need the decision-latency budget and the criteria for each spelled out.
- You are staffing or participating in a war room and need defined roles, handoffs, and a communication cadence.
- You are writing, running, or reviewing a postmortem and need the blameless format and measurable action-item follow-through.
- You are building alerting, runbooks, or game-day drills and need them validated against real incident practice.
- You are deciding whether an incident is closed and need the explicit closure criteria.

Self-assign this skill when you receive a page, when an SLO burn check trips, or when a production change is being rolled back.

## WHEN NOT TO USE

- Local development, staging-only, or test-environment issues with no customer or production impact — fix normally, without incident machinery.
- Already-resolved single root cause with no customer impact and no SLO breach; do not open an incident for every alert.
- Capacity or architecture planning not tied to an active or imminent outage.
- Outages of third-party SaaS where you hold no ownership or response levers.
- Routine feature development, unless the change is part of an active rollback or forward-fix.
- Routine change management where the standard CI/CD gates are the appropriate control.

## DECISION TREE

Walk each step in order. The first decision is severity; every later fork depends on it. All time-to-mitigate targets are measured from the first page, and containment (impact plateau) is the midpoint of every target, distinct from remediation (root-cause fix live).

### Step 1 — Classify severity

Classify within 5 minutes of the page. When in doubt, escalate one level; de-escalation is free, a missed SEV1 is not. Severity is set by actual or projected customer impact plus SLO breach, never by how hard the bug is to fix. A one-line config error that breaks all login is SEV1.

| Severity | Definition | Containment target | Remediation target | Example |
|---|---|---|---|---|
| SEV1 | Service down or core function unusable for a material set of customers; revenue, safety, or confirmed-data-breach impact | 15 minutes | 60 minutes | checkout API at 100% 5xx; confirmed data exposure |
| SEV2 | Significant degradation or partial outage; SLO breach sustained past 15 minutes; a workaround exists | 60 minutes | 4 hours | P95 latency at 3x budget for 30 minutes; one region degraded |
| SEV3 | Minor or isolated issue; no current customer impact; actionable on next business day | same-shift | 24 hours | single-customer data anomaly; cosmetic admin bug |

Escalation rules: any single page classified SEV1 or SEV2 summons a commander and opens a war room. Two related pages in 24 hours force an SEV escalation review. Every misclassification is logged and fed back to the training data, not the judged engineer.

### Step 1.5 — Open the incident and assign roles

On any SEV1 or SEV2, within the same 5-minute classification window, open the incident channel, name the commander, and spawn the comms and ops leads. Record the opening time as the page timestamp epoch. Announce severity, affected surface, and the containment target out loud so the whole team converges on the same deadline before any work starts. The first 5 minutes buy the discipline for the next hours.

### Step 2 — Contain before fixing

Containment is the objective, not diagnosis. Declare it only after the page metric has plateaued or dropped. Choose the fastest safe action from this matrix:

| Situation | Action | Criterion |
|---|---|---|
| Last change is the likely cause; schema is backward-compatible | rollback | rollback plan exists; revert completes within 10 minutes |
| Last change is likely; schema changed irreversibly | flag off, do not roll back | a kill-switch flag can disable in under 60 seconds |
| No flag and rollback unsafe; single-line proven fix | forward-fix | fix follows normal review; tested in staging first |
| Cause unknown but one service is saturated | scale out / shed load | deterministic rate limiting with RSVP or drop, queue depth bounded |

Contain means: stop the bleed AND confirm impact stopped growing. If the page metric has not moved within 5 minutes of the action, the action failed — revert the action and try the next candidate rather than repeating it. Do not declare containment on hope.

**Containment decision runbook — walk in this order, logging each skip:**

1. Is the failure isolated to one deploy? If the suspect change is reversible on its schema, issue rollback and time-stamp it.
2. Is there a kill-switch flag for the suspect path? Flip it off. Confirm the flag is live at deploy time before the incident, not while on fire.
3. Is saturation local and not coupled to a bad change? Shed load deterministically (drop lowest-value requests, raise queue-deadline) and scale out the saturated tier.
4. Can traffic be redirected to a healthy zone? Fail over at the edge with a single command, then stop new writes to the bad zone.
5. Is none of the above viable? Only then authorize a forward-fix, scoped to one line or one validated patch, reusing the existing pipeline.

Any containment action that takes longer than its budget defeats the purpose. When in doubt, prefer the most reversible action; reversibility is worth more than correctness in the heat of the page.

### Step 3 — Mitigate

While containment holds, reduce residual impact: fail over to a healthy region, shed load with deterministic rate limiting, switch to a degraded-but-available mode, or serve from cache. Record every mitigation in the timeline. Mitigation is complete when impact is at zero or within the degraded-mode SLO.

### Step 4 — Remediate

Fix the root cause with normal change discipline: the same review gates as any production change, a tested rollback for the fix itself, and a release note. Do not use the incident as an excuse to skip review. If the fix rolls out and the page repeats, re-enter Step 2 immediately — the containment interrupt budget of 5 minutes applies to the second page too.

### Step 5 — Postmortem

Declare closure only after: the timeline is reconstructed and verified, every action item has an owner and a due date, and the incident channel is archived. No postmortem, no closure.

**Closure checklist — every item must be green before "closed":**

- Timeline reconstructed and cross-checked against the page metric and chat logs (2-minute tolerance on containment and remediation events).
- Every action item has an owner, a due date, and a verification method; none read "improve monitoring".
- The postmortem exists and names root cause, contributing controls, and the action items that follow.
- Customers notified per the communication SLA; internal status page closed out.
- Any misclassification from the SEV review is logged for the responder-learning loop.
- Ops and comms hand their notes to the owner who files the timeline artifact.

Step 3 and 4 operators re-measure the page metric after each change; no "closed" on an unverified fix.

## PATTERNS

- **Rollback-first discipline.** Every deploy carries a rollback plan reviewed before release: what to revert, what schema constraints exist, expected revert latency, and a named rollback owner. The plan lives in the runbook, not in someone's head. Discipline means rehearsing it, not just writing it.
- **Feature-flag kill switch.** Every risky toggle (migration, refactor, new routing) is flag-protected so any change can be disabled in under 60 seconds without a deploy. A flag that requires a redeploy to change is not a kill switch; a real kill switch is evaluated at deploy time and cheap to flip either way.
- **Status-communication cadence (5-15-30).** Initial triage announcement within 5 minutes of the page; a status update every 15 minutes while the incident is active; a post-incident summary within 30 minutes of containment even if analysis is unfinished. Each update states what is affected, what is being done, current severity, and the next update time. Silence reads as escalation to command's manager.

  Status template, filled verbatim every 15 minutes:

  1. Severity — current SEV and change direction.
  2. Trigger — affected surface, metric values, error rate.
  3. Action — what is being contained and the containment action taken.
  4. Response — the timestamp of the next update, always present.

  A blank field is a signal flagged for correction, not something silently omitted.

- **War-room roles.** Exactly three roles, one owner each: commander (owns severity, containment decisions, and role assignment; decides rather than debugs), communications lead (owns the status page, customer updates, executive briefing, and the 5-15-30 cadence), and ops lead (owns investigation, mitigation execution, and rollback execution). Role badges are explicit; one person holding two roles is itself a failure mode above SEV3. Rotate the on-call engineer to a notetaker when they have worked more than 2 hours continuous.

  Responsibility split — who decides, who executes, who speaks:

  | Capability | Commander | Ops | Comms |
  |---|---|---|---|
  | Severity decision | yes | no | no |
  | Choose containment action | yes | executes | no |
  | Root-cause investigation | no | yes | no |
  | Status page and customer updates | no | no | yes |
  | Escalate to management | yes | no | no |
- **Runbook-first alerting.** Every paging alert links a runbook stating expected impact, the first three diagnostic steps, and the default containment action. An alert without a runbook is unactionable; a runbook that opens with investigate is not a runbook — it must prescribe, not prompt.
- **Timeline as a first-class artifact.** Every action, observation, and decision gets a timestamped entry with the actor. The timeline is the raw material for the postmortem; reconstructing it from memory produces a wrong postmortem.
- **Escalation ladder defined in advance.** Each service names its SEV1 commander and backup, the exact paging path, and the people authorized to roll back and to flip flags before any incident. Rehearsed yearly with role rotation so no individual becomes a single point of the incident response.

## FAILURE MODES & MITIGATIONS

Each entry states how the failure appears (DETECT) and the corrective action (FIX).

- **Fixing instead of containing.** DETECT: an engineer is deep in the codebase while the metric is still red, or the channel shows debugging but no rollback decision. FIX: the commander re-asserts contain-first; rollback or flag-off is the only permitted activity until impact plateaus. Suspected and confirmed cause need not match for containment to proceed.
- **Investigation tunnel vision.** DETECT: more than 10 minutes without a communicated switch of hypothesis, or one engineer unilaterally deep-diving a single theory. FIX: time-box each hypothesis; the commander forces a re-scope every 10 minutes and rotates investigators when a branch stalls. Two parallel investigations on different hypotheses beat one fixated branch.
- **Missing telemetry.** DETECT: the timeline cannot answer what that metric was at page time, or the runbook's diagnostic steps point at dashboards that do not exist. FIX: capture the four golden signals (traffic, errors, latency, saturation) and deploy-time annotations for every service; backfill dashboards from the incident so the next one is answerable. Missing telemetry is a postmortem action item, never a footnote.
- **Postmortem blame.** DETECT: any sentence attributing the outcome to a person's mistake or carelessness, or a decision judged only with fuller hindsight. FIX: rewrite in blameless format — what happened, what systems and controls allowed it, what control changes in response. Blame destroys the data the process depends on; repeat incidents follow.
- **Alert silence.** DETECT: a page is answered but no status entry exists after 5 minutes, or updates stop for more than 15 minutes while the incident is open. FIX: comms owns the cadence, not the on-call engineer; a no-new-information update still posts on time. Silence is a live escalation signal.
- **Bad rollback (schema mismatch).** DETECT: the rollback plan is absent, or a rollback would re-apply a migration that breaks on new data, or code and schema versions are coupled. FIX: before rolling back, check whether the change includes a non-reversible migration; if it does, prefer flag-off or forward-fix and keep the release path forward-compatible so old code runs on new schema. A rollback that lands worse than the outage is a double incident.
- **War-room role collision.** DETECT: the person who rolled back is also writing the status page, or the commander is also debugging. FIX: reassign roles immediately; the commander delegates investigation and comms. Commander and ops are separated from SEV2 up, always.
- **Postmortem with no actionable items.** DETECT: the postmortem has no owner, no due date, or only improve-monitoring. FIX: every item has an owner, a due date, and a verification method; items are tracked and followed through to closure in the verification gate, never closed the day they are written.
- **Reverting incomplete pre-incident state.** DETECT: a rollback restores code but not config, flags, or data, leaving the service half-old. FIX: rollback plan names every artifact (code, config, feature state) and rollback rehearses restore all of them; the page metric verifies the full revert.
- **Cascading action without recheck.** DETECT: an engineer issues containers/rate-limits/redirects and never returns to the page metric. FIX: after every action, re-read the page metric within 2 minutes; log the before/after values into the timeline. Every action is a hypothesis with a measurement.

## QUANTITATIVE RULES

- **MTTD target:** 5 minutes from page to classification (severity assigned, commander named).
- **MTTA target:** 10 minutes from page to acknowledgment, on 100% of pages.
- **Containment target:** SEV1 15 minutes, SEV2 60 minutes, from page to impact plateau.
- **Remediation target:** SEV1 60 minutes, SEV2 4 hours, SEV3 24 hours, from page to root-cause fix live.
- **Rollback decision latency:** at most 10 minutes from the moment the last change becomes a suspect; under 5 minutes when the pre-verified rollback plan exists. Any longer and the incident floor is SEV2.
- **Error-budget burn rates:** a rolling 6-hour window consuming 2% or more of the 30-day error budget pages and halts all deploys. A 24-hour window consuming 5% or more escalates to SEV2 with a mandatory postmortem. Baseline: normal daily share of a 30-day budget is 3.33%; crossing it is an SLO breach in progress, not a forecast.
- **Communication intervals (5-15-30):** triage announcement within 5 minutes of the page; status update every 15 minutes while active; post-incident summary within 30 minutes of containment.
- **Alert hygiene:** every paging alert links a runbook; over a rolling 90 days an alert either fired or was exercised in a drill. An alert ignored or silent for 90 days is a dead alert — decommission or rewire it.
- **Drill cadence:** game-day drills per service at least quarterly, including one unannounced and one rollback rehearsal each year; every release-candidate rollback is rehearsed quarterly.
- **On-call rotation:** shifts last at most 7 days; an engineer who held a SEV1 may not authorize a production change within 24 hours of containment. Fatigue is a measurable risk, not a morale note.
- **Repeat-incident rule:** the same root cause twice in 30 days floors the second occurrence at SEV2 with a mandatory postmortem and a corrective action time-boxed to 7 days.
- **Postmortem SLA:** a draft postmortem is published within 72 hours of containment and finalized with owners and due dates within 7 days. A postmortem older than 7 days without owners is itself a tracked defect.

## VERIFICATION GATE

"Done" only when every check below is green. Run them each quarter and after any change.

- **Game-day drills (quarterly):** inject a scripted failure (downstream dependency outage, traffic spike, bad deploy) in staging or shadow. Assert: severity within 5 minutes, containment action chosen within 10 minutes, impact plateaued within the SEV target, and the 5-15-30 cadence held with no silent gaps.
- **Checklist dry-runs:** execute the DECISION TREE and the containment matrix against three recorded past incidents without reading their resolutions. Assert: it selects the same severity, action, and outcome the incident actually had, in under 10 minutes per incident.
- **Action-item follow-through:** for every incident in the past 90 days, assert 100% of items have an owner and due date, and at least 90% are completed or re-triaged by their due date. Overdue items gate the next release, not merely the review.
- **Timeline reconstruction check:** independently rebuild the timeline of a sample incident from logs and chat; compare to the postmortem. Assert timestamps agree within 2 minutes for containment and remediation events, and no containment action is missing. Disagreement means under-recording; the next drill repeats that failure class.
- **Rollback rehearsal:** run a full rollback of the most recent release in staging. Assert: completion within the rollback latency budget, schema remains consistent, and the golden signals return to baseline.
- **Alert-to-runbook mapping:** sample 10 paging alerts at random and assert each links a runbook naming expected impact, the first three diagnostic steps, and a default containment action.

**Results matrix — record one row per gate per quarter, all green to pass:**

| Gate | Fail only if | Re-run trigger |
|---|---|---|
| Game-day drill | severity or containment outside target, or a cadence gap | immediately, corrected scenario |
| Checklist dry-run | a selected action differs from the recorded incident | next quarter, new incidents |
| Action-item follow-through | completion below 90%, or any item overdue | next release |
| Timeline reconstruction | timestamp drift over 2 minutes or a missing containment | next drill, same class |
| Rollback rehearsal | schema drift or golden signals not restored | every release |
| Alert mapping | any of 10 alerts with no runbook | next alert added |

A single red gate blocks the skill from "done". Recording the matrix is not optional; an unreported gate is a red gate.

## REFERENCES

- **Google SRE Workbook** — chapters on incident response and postmortems. The canonical treatment of severity, incident management, and blameless postmortems; source of the 5-15-30 cadence and contain-first framing.
- **Google SRE Book (Site Reliability Engineering), Chapter 14 "Managing Incidents" and Chapter 15 "Postmortem Culture".** Role separation (commander, ops, comms) and blameless-culture practice.
- **"Blameless PostMortems and a Just Culture" (Code as Craft / John Allspaw, Etsy) and related just-culture talks.** Practical blameless-writing and timeline-first templates.
- **PagerDuty Incident Response documentation** (page escalation, runbook standards) and **incident.io incident-management practices** (status page cadence, war-room workflow) that ground the runbook and cadence rules.

Primary external references in the training corpus: the Google SRE Workbook and SRE Book chapters are the load-bearing sources; the Etsy and PagerDuty/incident.io material validates the war-room, runbook, and cadence rules.

## CHANGELOG

- 2026-08-06 | Phase 3.2: incident-response-engineer created (G3: SEV classification, containment, war-room, postmortem, quantitative rules) | incident-response-engineer