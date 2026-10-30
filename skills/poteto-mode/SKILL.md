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
  version: 2.0.0
  domain: doctrine
  grade: G1
  status: active
  last-reviewed: '2026-10-30'
  owned-by-agent: poteto-agent
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

## VERIFICATION GATE

The forwarded `ozone-mode` gate applies. Nothing in this file is evidence of anything.
