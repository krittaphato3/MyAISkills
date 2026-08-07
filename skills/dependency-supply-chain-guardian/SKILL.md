---
name: dependency-supply-chain-guardian
description: Audit dependencies for vulnerabilities, supply-chain attacks, and license compliance; generate SBOMs; plan safe update strategies. Use when adding/updating dependencies, triaging a detected vulnerability, or checking licenses.
version: 0.2.0
grade: G2
domain: production
status: active
last-reviewed: 2026-08-07
owned-by-agent: dependency-guardian
---

# DEPENDENCY SUPPLY CHAIN GUARDIAN SKILL

Expert knowledge in Software Composition Analysis, supply chain attack prevention, license compliance, and SBOM generation.

## VULNERABILITY SCANNING

### JavaScript/Node.js
```bash
npm audit
npm audit fix --dry-run
npx snyk test
npx audit-ci --critical
```

### Python
```bash
pip-audit
safety check
bandit -r .
```

### Go
```bash
govulncheck ./...
go list -m all | nancy sleuth
```

### Rust
```bash
cargo audit
cargo deny check
```

### Universal
```bash
trivy fs --format json .
syft . -o spdx-json > sbom.json
```

## SUPPLY CHAIN ATTACK PATTERNS

### Typosquatting
- **Attack**: Publish similar-named package
- **Examples**: `lodahs` vs `lodash`, `expresss` vs `express`
- **Defense**: Verify publisher, check download counts, review code

### Dependency Confusion
- **Attack**: Publish private package name to public registry
- **Defense**: Use scoped packages (`@mycompany/pkg`), namespace packages

### Maintainer Compromise
- **Attack**: Compromise maintainer account, inject malicious code
- **Defense**: Pin versions, review changelogs, use 2FA for publishing

### Malicious Code Injection
- **Attack**: Inject code via postinstall scripts
- **Defense**: Review package source, disable postinstall scripts

### Brandjacking
- **Attack**: Impersonate official packages
- **Defense**: Verify repository URL, check organization ownership

## LICENSE COMPLIANCE

### License Compatibility
| License | Commercial | Modify | Distribute | Patents |
|---------|------------|--------|------------|---------|
| MIT | ✅ | ✅ | ✅ | ✅ |
| Apache 2.0 | ✅ | ✅ | ✅ | ✅ |
| BSD 2-Clause | ✅ | ✅ | ✅ | ⚠️ |
| BSD 3-Clause | ✅ | ✅ | ✅ | ⚠️ |
| LGPL 2.1 | ✅ | ✅ | ⚠️ | ⚠️ |
| LGPL 3.0 | ✅ | ✅ | ⚠️ | ✅ |
| GPL 2.0 | ✅ | ⚠️ | ⚠️ | ⚠️ |
| GPL 3.0 | ✅ | ⚠️ | ⚠️ | ✅ |
| AGPL 3.0 | ⚠️ | ⚠️ | ⚠️ | ✅ |

### Checking Tools
```bash
# JavaScript
npx license-checker --summary
npx license-checker --failOn "GPL-3.0;AGPL-3.0"

# Python
pip-licenses --format=json
pip-licenses --fail-on="GPL-3.0"

# Go
go-licenses check ./...
```

## SBOM GENERATION

### SPDX Format
```json
{
  "spdxVersion": "SPDX-2.3",
  "dataLicense": "CC0-1.0",
  "packages": [
    {
      "SPDXID": "SPDXRef-Package",
      "name": "my-project",
      "versionInfo": "1.0.0",
      "licenseConcluded": "MIT"
    }
  ]
}
```

### CycloneDX Format
```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.4",
  "components": [
    {
      "type": "library",
      "name": "lodash",
      "version": "4.17.21",
      "licenses": [{"license": {"id": "MIT"}}]
    }
  ]
}
```

### Generation Commands
```bash
# Syft (SPDX or CycloneDX)
syft . -o spdx-json > sbom.json
syft . -o cyclonedx-json > sbom.json

# npm
npx sbom-generator
```

## DEPENDENCY UPDATE STRATEGIES

### Automated Updates
- **Renovate Bot**: Configurable, supports monorepos
- **Dependabot**: GitHub native, security-focused

### Update Strategy
1. Patch updates: Auto-merge (bug fixes)
2. Minor updates: Review changelog, auto-merge if safe
3. Major updates: Manual review, test thoroughly

### Renovate Config
```json
{
  "extends": ["config:base"],
  "schedule": ["every weekend"],
  "automerge": true,
  "packageRules": [
    {"matchUpdateTypes": ["patch"], "automerge": true},
    {"matchUpdateTypes": ["major"], "automerge": false}
  ]
}
```

## OUTPUT FORMAT
```text
DEPENDENCY AUDIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Project: {name}
Package Manager: {npm|pip|cargo|go}

VULNERABILITIES:
- Critical: {count}
- High: {count}
- Medium: {count}

CRITICAL FINDINGS:
1. [{severity}] {package}@{version}
   CVE: {cve-id}
   Fix: {remediation}

LICENSES:
- MIT: {count}
- Apache-2.0: {count}
- Conflicts: {list}

UNUSED DEPENDENCIES:
- {package}

SBOM: {path}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## WHEN TO USE
- Adding or updating a dependency, and you must assess the risk (known CVEs, malicious contents, licenses) before proceeding.
- A security advisory or vulnerability scan flags a vulnerable dependency and you must triage and remediate.
- A license compliance decision is required (Can we ship this? What terms apply?) before release.
- A Software Bill of Materials (SBOM) must be produced for the project or a release.
- An automated update bot proposes a change and you must decide whether to auto-merge or review (patch/minor/major ladder).

## WHEN NOT TO USE
- **Not a general package-install helper** — deciding *which* library best fits a feature (npm search, compare ecosystem) is application design, not dependency governance.
- **Not application code review** — the vulnerability is in your own code, not a dependency; that goes to security-hardening-specialist.
- **Not a security engagement on the dependency's vendor** — you audit, and report to, your own project, not the upstream org.
- **One library with no downstream risk** — a lone dev-only utility with no runtime exposure may not justify a full audit.
- **Legal advice** — this skill applies license engineering rules (compatibility, discovery), not a counsel opinion on obligations.

## DECISION TREE
```text
1. TRIGGER   → adding/updating? vulnerability finding? license question? SBOM needed?
   → select the operative module (scan / policy / license / SBOM / update).
2. SCAN      → run the language-appropriate scanner (npm audit, pip-audit, govulncheck,
   cargo audit); note severity + patched version.
3. TRIAGE    → runtime-exposed & CRITICAL/HIGH → treat now. Else → schedule per update ladder.
4. LICENSE   → check compatibility table; conflict (e.g. GPL in a proprietary deliverable) → flag & escalate.
5. SBOM      → generate SPDX or CycloneDX; verify it lists the actual resolved tree.
6. VERIFY    → re-scan after the fix; confirm 0 unpatched criticals; record the delta.
```
Never skip step 3 — patching everything blindly churns the lockfile and can introduce breaking updates.

## FAILURE MODES & MITIGATIONS
- **Typosquatting / lookalike packages.**
  DETECT: a package name differs by one character from a popular library (`lodahs` vs `lodash`) or has an unusually high version with little history.
  FIX: verify publisher identity, install counts, repo URL, and organization ownership before adding; use scoped pins for the core dependency set.
- **Dependency confusion — a public package shadows a private name.**
  DETECT: a package intended to be private resolves to a public registry package under the same name.
  FIX: use scoped/namespaced packages and registry config that refuses the public feed for internal names; verify `lockfile` resolution points at the correct registry.
- **Malicious code in a postinstall script.**
  DETECT: a package runs arbitrary code on install (exfiltration to an external host, adware); audit shows postinstall without a known need.
  FIX: review new packages' postinstall scripts, disable `postinstall` globally where safe, establish package allowlists, and prefer well-vetted maintainers.
- **Maintainer compromise / injected tag.**
  DETECT: a trusted package ships an anomalous new version with unexpected behavior or build steps.
  FIX: review changelogs and diffs on major bumps, pin exact versions (no `^` that silently pulls compromised minors), and require 2FA-disclosure signals for critical packages.
- **License-incompatibility surprises late.**
  DETECT: the license scanner reports AGPL/GPL in a proprietary component, or you need to modify/distribute a copyleft dependency you assumed was permissive.
  FIX: gate CI on a license check (`license-checker --failOn`) for incompatible licenses, run license review at dependency-add time, and record the decision instead of deferring it.
- **SBOM drift — the manifest doesn't match the resolved tree.**
  DETECT: the SBOM lists stale or missing versions vs the actual installed/locked tree.
  FIX: generate the SBOM from the lockfile inside CI after a clean install; re-run on every dependency change; verify SPDX/CycloneDX structure with a validator.

## VERIFICATION GATE
- **Clean re-scan**: after the change, the language scanner reports zero unpatched CRITICAL/HIGH vulnerabilities (or a documented, exempt finding).
- **Lockfile pinned as intended**: exact version resolution is confirmed; no unapproved major/minor drift.
- **License gate passed**: the license check fails only the allowed set; any copyleft/conflict has a written decision.
- **SBOM valid**: generated from the resolved tree in SPDX or CycloneDX, passes a structural validator, and is recorded for the release.
- **Update ladder followed**: patch auto-merged, minor/manual reviewed, major manually tested before merge.
- **red-team-qa review**: check for typosquatting, dependency-confusion, and license conflicts an attacker could exploit.

## REFERENCES
- OWASP Dependency-Check / SCA guidance — supply-chain risk categories and scanning.
- npm security best practices + `audit-ci` / Snyk docs.
- Anchore `syft` (SBOM) and the SPDX / CycloneDX specifications — SBOM structure and validation.
- GitHub / Snyk dependency-confusion advisories — namespace scoping and registry-resolution pinning.
