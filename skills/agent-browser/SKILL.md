---
name: agent-browser
description: >-
  Uses the standalone `agent-browser` CLI for CDP-driven browser work: navigation, clicks,
  form filling, accessibility snapshots, screenshots, scraping, and exploratory QA. Use when
  the CLI is the intended path or the Playwright MCP is unavailable; the configured Playwright
  MCP path belongs to browser-automation. Not for Electron, Slack,
  or cloud-browser integrations unless explicitly requested.
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*)
hidden: true
metadata:
  version: 3.1.0
  domain: meta
  grade: G2
  status: active
  last-reviewed: '2026-11-09'
  authored-by: browser-automation
---

# agent-browser

Fast browser automation CLI for AI agents. Chrome/Chromium via CDP with accessibility-tree snapshots and compact `@eN` element refs.

Install: `npm i -g agent-browser && agent-browser install`

## Start here

This file is a discovery stub, not the usage guide. Before running any `agent-browser` command, load the actual workflow content from the CLI:

```bash
agent-browser skills get core             # start here — workflows, common patterns, troubleshooting
agent-browser skills get core --full      # include full command reference and templates
```

The CLI serves skill content that always matches the installed version, so instructions never go stale. The content in this stub cannot change between releases, which is why it just points at `skills get core`.

## Specialized skills

Load a specialized skill when the task falls outside browser web pages:

```bash
agent-browser skills get electron          # Electron desktop apps (VS Code, Slack, Discord, Figma, ...)
agent-browser skills get slack             # Slack workspace automation
agent-browser skills get dogfood           # Exploratory testing / QA / bug hunts
agent-browser skills get derive-client     # Record a HAR, derive a standalone API client for a site
agent-browser skills get vercel-sandbox    # agent-browser inside Vercel Sandbox microVMs
agent-browser skills get protected-vercel-deployments  # Access protected Vercel deployments
agent-browser skills get agentcore         # AWS Bedrock AgentCore cloud browsers
```

Run `agent-browser skills list` to see everything available on the installed version.

## Why agent-browser

- Fast native Rust CLI, not a Node.js wrapper
- Works with any AI agent (Cursor, Claude Code, Codex, Continue, Windsurf, etc.)
- Chrome/Chromium via CDP with no Playwright or Puppeteer dependency
- Accessibility-tree snapshots with element refs for reliable interaction
- Sessions, authentication vault, state persistence, video recording
- Specialized skills for Electron apps, Slack, exploratory testing, cloud providers

## Observability Dashboard

The dashboard runs independently of browser sessions on port 4848 and can also be opened through a proxied or forwarded URL such as `https://dashboard.agent-browser.localhost`. Agents should stay on the dashboard origin: session tabs, status, and stream traffic are proxied internally, so session ports do not need to be exposed.

## WHEN TO USE

Driving a real browser through the `agent-browser` CLI: navigation, clicks, typing, accessibility
snapshots, screenshots, scraping, and exploratory QA, when the CLI is the intended path.

## WHEN NOT TO USE

The Playwright MCP is configured and reachable (`browser-automation`), the target is a normal web
page that a plain HTTP fetch answers, or the task is API-level testing.

## DECISION TREE

- The task names `agent-browser` or `npx agent-browser`, or the CLI is the only driver available -> use this skill.
- The Playwright MCP is configured and reachable -> `browser-automation`; two drivers on one profile deadlock.
- The target is an Electron desktop app, Slack, or a cloud browser -> load the matching specialized skill first.
- The question is exploratory QA or a bug hunt rather than a scripted flow -> `skills get dogfood`.
- You need a repeatable API client against a site -> `skills get derive-client`.
- No `agent-browser` binary and no permission to install one -> stop and report; do not hand-roll a CDP script.

## FAILURE MODES & MITIGATIONS

- **Driving from memory of an older release.** Command surfaces change between versions. Mitigation:
  run `agent-browser skills get core` before the first command of a session, and `skills list` when a
  subcommand is missing.
- **Stale element refs.** `@eN` refs belong to one snapshot. Mitigation: re-snapshot after any
  navigation, DOM-changing click, or submit; never reuse a ref across a page change.
- **Two drivers on one profile.** The Playwright MCP and this CLI compete for the user-data dir.
  Mitigation: one driver per task, or a separate profile.
- **Credential leakage into the report.** The auth vault and saved state can carry secrets.
  Mitigation: never paste cookies, tokens, or storage state into output; report the observable result.
- **A screenshot of an error page read as success.** Mitigation: assert on accessible text or a
  selector, not on "an image came back".
- **Handing out raw session ports.** Mitigation: stay on the dashboard origin; session tabs are
  proxied internally.

## VERIFICATION GATE

The action was driven through the CLI, the result is asserted on accessible text or a selector, and
the evidence is a snapshot or screenshot the gate can read. A generated image is not proof.

## REFERENCES

- `agent-browser skills get core --full` - full command reference and templates, version-matched.
- `agent-browser skills list` - every specialized skill on the installed release.
- `browser-automation` - the Playwright MCP path this skill defers to.
- `webapp-qa` - the QA loop that consumes the browser evidence.
