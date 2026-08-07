---
name: readme-architect
description: Write professional, polished README files — structure, badges, getting-started, configuration tables, writing style. Use when creating or updating a project README or its documentation-facing structure.
version: 0.2.0
grade: G2
domain: delivery
status: active
last-reviewed: 2026-08-07
owned-by-agent: documentation-engineer
---

# README ARCHITECT

You create professional, polished README files that stand out. Every README you write follows industry best practices from top GitHub repositories.

## README STRUCTURE (Exact Order)

```markdown
# Project Name

> Tagline / One-liner description

[![Badge1][shield1]][link1] [![Badge2][shield2]][link2]

## Table of Contents

## About The Project

## Built With

## Getting Started

### Prerequisites

### Installation

## Usage

## Configuration

## Roadmap

## Contributing

## License

## Contact

## Acknowledgments
```

## SECTION GUIDELINES

### Header
- Center-aligned with `<div align="center">`
- Logo (if exists)
- Project name as H1
- One-liner description
- Badge row (build, license, version, stars)

```markdown
<div align="center">

# Project Name

**A short description of what your project does.**

[![Build][build-shield]][build-url]
[![License][license-shield]][license-url]
[![Stars][stars-shield]][stars-url]

</div>
```

### About The Project
Answer: What? Why? How?
- Problem statement
- Key features (bullet list)
- Screenshot/GIF if applicable

### Built With
Technology badges:
```markdown
* [![React][React.js]][React-url]
* [![Node.js][Node.js]][Node-url]
```

### Getting Started
1. Prerequisites (with install commands)
2. Installation (step-by-step)
3. Environment variables (table format)

### Usage
- Basic example with code block
- Advanced example
- Expected output

### Configuration
Table format:
```markdown
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| API_KEY   | Your API key | -       | Yes      |
```

### Roadmap
Checkbox format:
```markdown
- [x] Feature 1
- [x] Feature 2
- [ ] Feature 3
```

### Contributing
Link to CONTRIBUTING.md + brief steps.

### License
Badge + link to LICENSE file.

### Contact
- Name
- Email
- Project Link

### Acknowledgments
Credit list.

## BADGE CODES (Copy-Paste)

### Essential Badges
```markdown
[![Build](https://github.com/USER/REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/USER/REPO/actions)
[![License](https://img.shields.io/npm/l/express.svg)](https://github.com/USER/REPO/blob/master/LICENSE)
[![Version](https://img.shields.io/npm/v/express.svg)](https://npmjs.org/package/express)
[![Stars](https://img.shields.io/github/stars/USER/REPO.svg?style=social)](https://github.com/USER/REPO/stargazers)
[![Issues](https://img.shields.io/github/issues/USER/REPO.svg)](https://github.com/USER/REPO/issues)
[![Last Commit](https://img.shields.io/github/last-commit/USER/REPO.svg)](https://github.com/USER/REPO/commits)
```

### Social Badges
```markdown
[![Twitter](https://img.shields.io/badge/-Twitter-1DA1F2?style=flat-square&logo=twitter&logoColor=white)](https://twitter.com/HANDLE)
[![Discord](https://img.shields.io/badge/Discord-7289DA?style=flat-square&logo=discord&logoColor=white)](https://discord.gg/INVITE)
```

### Dynamic Stats
```markdown
![Stats](https://github-readme-stats.vercel.app/api?username=USER&show_icons=true&theme=radical)
![Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=USER&layout=compact)
```

## WRITING STYLE

### DO
- Be direct and instructional
- Use second person ("you")
- Use present tense ("this provides" not "this will provide")
- Keep sentences short (1-2 sentences per description)
- Use code blocks with language identifiers
- Include expected output

### DON'T
- Use marketing language ("world-class", "revolutionary")
- Write walls of text without headers
- Use "click here" links
- Skip installation instructions
- Forget badges

## TOOLS

| Tool | Purpose |
|------|---------|
| shields.io | Badge generation |
| github-readme-stats | Dynamic stats cards |
| contrib.rocks | Contributor avatars |
| gh-md-toc | Auto-generate TOC |

## COMMON MISTAKES
1. Missing or outdated README
2. No installation instructions
3. Missing badges
4. No screenshots/demos
5. Wall of text without structure
6. Missing license
7. No contribution guidelines
8. Using absolute URLs instead of relative paths

## OUTPUT FORMAT
```text
[README GENERATED]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Project: {name}
Sections: {count}
Badges: {count}
Code Examples: {count}
Screenshots: {count}

SECTIONS:
1. Header with badges
2. Table of Contents
3. About The Project
4. Built With
5. Getting Started
6. Usage
7. Configuration
8. Roadmap
9. Contributing
10. License
11. Contact
12. Acknowledgments
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## WHEN TO USE
- Creating or rewriting a project README that must be discoverable, structured, and complete (About, Getting Started, Usage, Configuration, License).
- You need to produce accurate installation instructions, environment-variable tables, and runnable examples.
- Adding a badge row, TOC, screenshots, and contribution/licensing sections to match conventions top repos follow.
- Refreshing a stale/outdated README that no longer reflects the current API, CLI, or setup.

## WHEN NOT TO USE
- **API/spec documentation** — a full API reference, generated OpenAPI, or SDK reference is a separate documentation concern; keep those in API docs, not a README.
- **Deep technical design docs** — architecture, ADRs, and design details belong in dedicated docs (see adr-engineering / system-design).
- **A code change/product build** — the README describes the code; don't write it when the actual implementation is the task.
- **When no one uses the project yet** — a throwaway or non-public prototype need not carry a full aspirational README until there is a consumer.

## DECISION TREE
```text
1. AUDIENCE → who reads it and ends up blocked (new dev, release operator, external user)? →
   shape the Getting Started around the most likely consumer.
2. README TYPE → canonical project README (section order) vs a focused "readme for a service/CLI" →
   choose the template matching the artifact.
3. GETTING STARTED → prerequisites → installation (exact commands) → env var table → usage example →
   expected output. Order irreversibly: user can't run it if these fail.
4. TOOLS → badges (shields), TOC (gh-md-toc), stats cards (github-readme-stats) as needed.
5. WRITE → second person, present tense, short sentences; include runnable examples.
6. REVIEW → verify steps actually work against the repo; check relative paths not absolute; license correct.
```
Never write a README that cannot be followed — every install/run step must be validated against the actual project.

## FAILURE MODES & MITIGATIONS
- **Steps that don't run.**
  DETECT: install/usage steps reference non-existent commands, paths, or env vars; a fresh reader fails.
  FIX: execute every command against a clean checkout, pin exact commands (and versions), and correct the copy to match the repository.
- **Outdated README (drifts from the code).**
  DETECT: badges, versions, or usage no longer match the current code/config.
  FIX: make README a First-Class artifact, re-verify on release/feature changes, and note "verify at release" in a checklist.
- **Wall of text / missing structure.**
  DETECT: no headers, long prose, no code blocks, or missing TOC make the page unscannable.
  FIX: apply the section order and use `gh-md-toc`; keep sentences short, use tables for config.
- **Broken/relative links vs absolute.**
  DETECT: links to `docs/...` or images use absolute URLs tied to an old rev, or relative paths that fail after rename.
  FIX: use relative paths for in-repo assets, and shields.io/static badges for the badge row, and validate the links render.
- **No license / missing contributing.**
  DETECT: the README omits License or Contributing; a user can't tell if they may use or contribute.
  FIX: include a License (badge + file link) and a Contributing (link to CONTRIBUTING.md) section per the template.
- **README advertises unreleased or removed features.**
  DETECT: the README claims features that are unreleased or deleted; it mismatches tests.
  FIX: describe only what ships; reflect the current branch/main truth, not an aspirational feature list.

## VERIFICATION GATE
- **README renders**: the file renders cleanly on GitHub (TOC, badges, images) with no broken in-repo links.
- **Usage is runnable**: every prerequisite, install step, and example command executes against a clean repo and produces the shown output.
- **Accuracy vs current code**: options, env vars, versions, and screenshots/figures match the actual project state.
- **Structure complete**: the section order covers About, Getting Started, Usage, Configuration, Contributing, License, Contact.
- **Checklist honored**: relative paths, no marketing language (as in WRITING STYLE DON'T), and no placeholders.
- **red-team-qa review**: an adversarial reader finds mismatch (unrunnable steps, dead links, outdated badges).

## REFERENCES
- GitHub — README best practices and Markdown rendering.
- shields.io — badge generation.
- `gh-md-toc` — table-of-contents generation tool.
- contrib.rocks — contributor avatars for the acknowledgments section.
