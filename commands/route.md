---
description: Show which skill and subagent a request would route to, without doing the work
---
Using the routing table in AGENTS.md §3, show how this request would be handled — do not perform the work yet.

Request: $ARGUMENTS

Output exactly this shape:

```text
ROUTE CARD
Intent family:  {the family the prompt belongs to}
Skill(s):       {skill(s) to load, in order}
Subagent(s):    {agent(s) to dispatch, and whether parallel or sequential}
Pipeline:       {which stages of AGENTS.md §4 apply, and where the gates are}
Confidence:     0-100  (below 80 → which clarifying question comes first)
Ambiguity:      {which other route was considered and why this one wins}
```

If nothing in the table matches, say so explicitly and name the closest two rows. Flag any reasoning where the router itself looks wrong so `meta-architect` can fix it.
