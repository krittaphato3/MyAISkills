---
name: github-flow-master
description: Create professional pull requests, write conventional commit messages, and manage GitHub workflows. Use when opening/describing a PR, structuring a PR description, or applying branch/commit/review conventions.
version: 0.2.0
grade: G2
domain: production
status: active
last-reviewed: 2026-08-07
owned-by-agent: code-implementer
---

# GITHUB FLOW MASTER

You create professional PRs, write polished commit messages, and manage GitHub workflows following industry best practices.

## PR DESCRIPTION TEMPLATE

```markdown
## Summary
[1-2 sentence summary of what this PR does]

## Motivation
[Why is this change needed? Link to issue if applicable]

## Changes
- Change 1: Description
- Change 2: Description
- Change 3: Description

## Implementation Details
[Explain significant design decisions or architectural choices]

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed
- [ ] Edge cases considered

## Screenshots/Recordings
[For UI changes, include before/after]

<details>
<summary>Screenshot</summary>

![description](url)
</details>

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented below)
- [ ] Related issue linked: #

## Breaking Changes
[If applicable, describe what breaks and migration path]

## Follow-up Work
[Planned improvements or technical debt]

Closes #
Fixes #
Resolves #
```

## PR TYPES WITH EXAMPLES

### Bug Fix
```markdown
## Summary
Prevents duplicate form submissions by adding server-side idempotency check.

## Motivation
Users could submit forms multiple times, causing duplicate database entries.

## Changes
- Added debounce logic to form submit handler
- Implemented server-side idempotency key
- Added database unique constraint

## Testing
- [x] Unit tests for debounce logic
- [x] Manual testing: rapid clicking scenario

Closes #123
```

### New Feature
```markdown
## Summary
Implements dark mode toggle with automatic system preference detection.

## Motivation
Users requested dark mode for eye strain reduction.

## Implementation Details
- Uses CSS custom properties for theming
- Stores preference in localStorage
- Respects prefers-color-scheme media query

## Screenshots
<details>
<summary>Light Mode</summary>
![Light](url)
</details>
<details>
<summary>Dark Mode</summary>
![Dark](url)
</details>

Closes #456
```

### Performance Optimization
```markdown
## Summary
Implements lazy loading for images below the fold, reducing LCP by 40%.

## Motivation
Core Web Vitals showed LCP at 4.2s (threshold: 2.5s).

## Performance Metrics
- Before: LCP 4.2s, FID 180ms
- After: LCP 2.1s, FID 85ms

Closes #789
```

## COMMIT MESSAGE FORMAT (Conventional Commits)

### Format
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types
| Type | When to Use | Version Impact |
|------|-------------|----------------|
| `feat` | New feature | Minor (0.X.0) |
| `fix` | Bug fix | Patch (0.0.X) |
| `docs` | Documentation only | None |
| `style` | Formatting, no code change | None |
| `refactor` | Code restructure, no behavior change | None |
| `perf` | Performance improvement | Patch |
| `test` | Adding/updating tests | None |
| `build` | Build system changes | None |
| `ci` | CI/CD changes | None |
| `chore` | Maintenance tasks | None |

### Examples
```
feat: add user authentication with JWT

fix: resolve login timeout on slow networks

docs: update API reference for v2 endpoints

perf: optimize image loading with lazy loading

refactor: extract validation logic into separate module

feat!: redesign API response format

BREAKING CHANGE: response format changed from XML to JSON
```

## GIT WORKFLOW

### Branch Naming
```text
feature/{ticket}-{description}    → feature/123-add-auth
bugfix/{ticket}-{description}     → bugfix/456-fix-login
hotfix/{description}              → hotfix/fix-security-vuln
release/{version}                 → release/1.2.0
```

### Standard Flow
```text
1. git checkout main
2. git pull origin main
3. git checkout -b feature/{ticket}-{description}
4. Make changes
5. git add -A
6. git commit -m "feat: description"
7. git push -u origin feature/{ticket}-{description}
8. Create PR on GitHub
9. Request review
10. Address feedback
11. Merge (squash or rebase)
```

### Commit Message Best Practices
- Use imperative mood ("add" not "added")
- Keep subject line under 72 characters
- Reference issues in footer (Closes #123)
- Separate subject from body with blank line
- Use body to explain what and why, not how

## LABEL STRATEGY

### Status Labels
| Label | Use When |
|-------|----------|
| `work-in-progress` | PR not ready for review |
| `ready-for-review` | PR complete, awaiting review |
| `needs-revision` | PR requires changes |
| `approved` | PR has required approvals |

### Type Labels
| Label | Use When |
|-------|----------|
| `bug` | Addresses a bug |
| `enhancement` | New feature |
| `documentation` | Doc changes |
| `performance` | Performance improvements |
| `security` | Security changes |
| `breaking-change` | Breaking changes |

### Size Labels
| Label | Files Changed |
|-------|---------------|
| `size/XS` | 1-10 lines |
| `size/S` | 10-50 lines |
| `size/M` | 50-200 lines |
| `size/L` | 200-500 lines |
| `size/XL` | 500+ lines |

## REVIEW REQUEST BEST PRACTICES

### When to Request
- Mark PR as "Ready for Review" when complete
- Use draft PRs for work-in-progress
- Don't request review on WIP PRs

### Who to Request
1. CODEOWNERS (automatic)
2. Subject matter experts
3. Team leads for architectural decisions

### How to Request
- Use @mentions to tag reviewers
- Explain why their input is needed
- Be explicit about feedback desired
- Set timeline expectations

## PR SIZE GUIDELINES

| Size | Review Time | Recommendation |
|------|-------------|----------------|
| XS (< 50 lines) | 5-10 min | Easy review |
| S (50-200 lines) | 15-30 min | Standard review |
| M (200-500 lines) | 30-60 min | Consider splitting |
| L (500+ lines) | 1+ hours | Split into smaller PRs |

## OUTPUT FORMAT
```text
[PR CREATED]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Title: {conventional commit format}
Branch: {branch name}
Type: {feat|fix|docs|perf|refactor}
Size: {XS|S|M|L|XL}

DESCRIPTION:
{summary}

TESTING:
{checklist}

LABELS: {applied labels}
ASSIGNEES: {reviewers}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## WHEN TO USE
- Opening a pull request and you need a complete, reviewable description (summary, motivation, tests, checklist).
- Writing a commit message that must follow conventional commits and pair with the change's type.
- Creating or refining a feature/bugfix/hotfix/release branch and its naming.
- Managing review flow: whom to request, when to mark ready-for-review, how to keep the PR reviewable in size.
- Applying status/type/size labels so the PR is discoverable and triageable.

## WHEN NOT TO USE
- **A trivial, atomic change** (a one-line typo fix) — one conventional commit with no body and no PR template detail.
- **The change is unmergeable / speculative** — do not open a PR for an incomplete, unverified, or throwaway change; draft PRs are for work-in-progress.
- **Wid-egal disruptive history rewrites for its own sake** — do not squash every commit blindly; keep per-change intent (see refactoring-intelligence on history preservation).
- **Subsystem-specific leave it to the owning domain skill** — API design, mobile, data — route to the domain skill; this skill is the git/PR mechanics.

## DECISION TREE
```text
1. CHANGE SIZE → XS/S (<50-200 lines) → normal workflow. M/L (200+) → split into smaller PRs first.
2. WORKFLOW → branch off main → commit with conventional type → push → open PR.
3. PR READINESS → complete + tested? → Ready-for-review → request review (CODEOWNERS/SMEs/lead).
   Incomplete or experimental? → Draft PR, no review request until ready.
4. DESCRIBE → Summary, Motivation, Changes, Testing, Screenshots (UI), Checklist. Link the issue (Closes/Fixes).
5. REVISE → act on feedback, keep PR small, re-request when addressed.
6. MERGE → squash/rebase once checks pass; reference the issue in the squash title; clean up the branch.
```
Never thrust a draft PR for review before it's ready; an unfinished PR wastes reviewers.

## FAILURE MODES & MITIGATIONS
- **PR description bloat / vague summary.**
  DETECT: description is empty or a wall of text with no summary, no test checklist, or no related issue.
  FIX: use the PR template (1-2 sentence summary, motivation, changes, testing, checklist); fill every section a reviewer depends on.
- **A single mega-PR (500+ lines) is unmergeable.**
  DETECT: a PR spans many files/subsystems with a diffuse intent; review time jumps.
  FIX: split into focused, individually-mergeable PRs; keep each under ~500 lines; keep green main; merge incrementally.
- **Unconventional / ambiguous commit messages.**
  DETECT: messages lack a `type(scope)` prefix or a clear subject; history can't be greped or rolled back by intent.
  FIX: enforce conventional commits (`feat:`, `fix:`, `docs:`, `perf:`, `refactor:`), imperative subject <72 chars, and reference the issue in the body.
- **Branch protection bypassed / force-push lost history.**
  DETECT: commits force-pushed en masse, protected-branch checks skipped, or review requirements met.
  FIX: keep branch protected (required checks + approvals), avoid force-push on shared branches; if rebasing is needed, do it on the feature branch before merge.
- **Review requested too early / too late.**
  DETECT: draft/WIP PR marked ready-for-review prematurely (tests failing) or a fully-done change never requested review.
  FIX: request only when complete and green; for WIP use a draft PR; tag the right authors (CODEOWNERS auto, SMEs, lead for architecture).
- **Wrong labels / missing issue link.**
  DETECT: PR is untagable and the closed issue is not referenced; triage is impossible.
  FIX: apply status (work-in-progress/ready-for-review) and type/size labels; use "Closes #N" so merge auto-closes the issue; record follow-up debt.

## VERIFICATION GATE
- **Conventional commit enforced**: commit messages pass the `<type>(scope): subject` gate; subject <72 chars, imperative.
- **PR complete**: summary, motivation, changes, test checklist, and relevant screenshots are present per the template.
- **Size under budget**: Reviewable PR size (≤ ~500 lines or split); no silent mega-PR.
- **Branch protection active**: required checks and required approvals are set on main; no force-push to shared branches.
- **History preserved**: no blind squash of ownership/intent; each merge is squash-or-rebase with a clear title.
- **Checklist + links correct**: status labels align with reality and the issue is linked via `Closes #`.

## REFERENCES
- GitHub — Pull request best practices and the PR template convention.
- Conventional Commits — specification for commit message types and breaking changes.
- GitHub branch protection / CODEOWNERS docs — required checks and code ownership.
- The Git book — branch/workflow fundamentals and rebase vs merge.
