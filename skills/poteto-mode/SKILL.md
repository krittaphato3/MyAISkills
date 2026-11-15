---
name: poteto-mode
description: >-
  Legacy alias kept so old muscle memory still works. Use when someone types /poteto-mode or asks
  for the poteto style; it forwards to ozone-mode, which owns the router, the playbooks, and the
  verification gates. No separate doctrine lives here.
disable-model-invocation: true
mode: true
icon: crown
color: yellow
reminder: /poteto-mode is retired. Use /ozone-mode.
metadata:
  version: 2.1.0
  domain: doctrine
  grade: G2
  status: deprecated
  last-reviewed: '2026-11-09'
  authored-by: poteto-agent
---

# Poteto Mode — retired

This entry point is retired. It exists only to forward, because two routers with overlapping
triggers is how a config starts contradicting itself.

Use `ozone-mode`. It carries the principles index, the playbook table, the tiers, the subagent
contract, and the ship gate.

## WHEN TO USE

Someone types `/poteto-mode`, or asks for the poteto workflow by name. Forward immediately.

## WHEN NOT TO USE

Every other case. Do not load this alongside `ozone-mode`; pick the router once.

## DECISION TREE

- The user typed `/poteto-mode` -> acknowledge the retirement in one line and run `ozone-mode`.
- The user asks for "the poteto style" by name -> run `ozone-mode`; it is the same doctrine.
- The user wants a router and has no muscle memory for either name -> `ozone-mode`, silently.
- Anything inside this file starts looking like doctrine -> stop; doctrine lives in `ozone-mode`.
- The user asks why the alias exists -> one sentence: two routers with overlapping triggers contradict each other.

## FAILURE MODES & MITIGATIONS

- **Doctrine re-grows in the alias.** Mitigation: this file holds forwarding text only; any new rule goes
  into `ozone-mode` or `AGENTS.md`.
- **Both routers loaded in one turn.** Mitigation: forward once and drop this skill from the active set.
- **The alias silently disappears from muscle memory.** Mitigation: `disable-model-invocation` keeps it
  out of auto-routing while `/poteto-mode` still resolves.
- **A user believes a retired path is supported.** Mitigation: the forwarding reply names the replacement
  explicitly.

## VERIFICATION GATE

The forwarded `ozone-mode` gate applies. Nothing in this file is evidence of anything.

## REFERENCES

- `ozone-mode` - the router this alias forwards to.
- `AGENTS.md` - the operating contract that names `ozone-mode` as the only router.
