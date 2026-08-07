---
name: monorepo-workspace-architect
description: Configure multi-package monorepos and their build systems — Turborepo, Nx, Lerna, npm/pnpm/yarn workspaces. Use when structuring workspaces, optimizing build caching/affected commands, or enforcing package boundaries.
version: 0.2.0
grade: G2
domain: production
status: active
last-reviewed: 2026-08-07
owned-by-agent: devops-engineer
---

# MONOREPO WORKSPACE ARCHITECTECT SKILL

Expert knowledge in monorepo tooling, workspace configuration, build optimization, and cross-package dependency management.

## MONOREPO TOOL SELECTION

| Tool | Language | Best For |
|------|----------|----------|
| Turborepo | JavaScript/TS | Fast builds, remote caching |
| Nx | JavaScript/TS | Enterprise, affected commands |
| Lerna | JavaScript/TS | Package publishing |
| Moon | Rust | Multi-language |
| Pants | Python | Large Python monorepos |
| Bazel | Multi | Google-scale builds |

## WORKSPACE CONFIGURATION

### npm Workspaces
```json
{
  "name": "my-monorepo",
  "workspaces": [
    "packages/*",
    "apps/*"
  ]
}
```

### pnpm Workspaces
```yaml
# pnpm-workspace.yaml
packages:
  - 'packages/*'
  - 'apps/*'
```

### Yarn Workspaces
```json
{
  "name": "my-monorepo",
  "workspaces": [
    "packages/*",
    "apps/*"
  ]
}
```

## TURBOREPO PATTERNS

### turbo.json
```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    },
    "test": {
      "dependsOn": ["build"]
    },
    "lint": {},
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

### Commands
```bash
# Build all packages (with caching)
turbo run build

# Build only affected packages
turbo run build --filter=...[HEAD^]

# Build package and its dependents
turbo run build --filter=@myorg/ui...

# Run test for specific package
turbo run test --filter=@myorg/core
```

### Remote Caching
```json
{
  "remoteCache": {
    "signature": true
  }
}
```

## NX PATTERNS

### nx.json
```json
{
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": ["production", "^production"]
    },
    "test": {
      "inputs": ["default", "^production"]
    }
  },
  "defaultBase": "main"
}
```

### Affected Commands
```bash
# Build only affected packages
nx affected --target=build

# Test only affected packages
nx affected --target=test

# Lint only affected packages
nx affected --target=lint
```

### Project Graph
```bash
# Visualize dependencies
nx graph

# Show affected projects
nx affected:graph
```

## PACKAGE BOUNDARY ENFORCEMENT

### ESLint Rules
```json
{
  "rules": {
    "import/no-restricted-paths": ["error", {
      "zones": [{
        "target": "./packages/core",
        "from": "./packages/ui"
      }]
    }]
  }
}
```

### Dependency Rules
```json
{
  "rules": {
    "import/no-extraneous-dependencies": "error",
    "import/no-relative-parent-imports": "error"
  }
}
```

## BUILD GRAPH OPTIMIZATION

### Parallelization
- Identify independent packages
- Use `--concurrency` flag
- Avoid unnecessary dependencies

### Caching Strategies
```json
{
  "cache": {
    "inputs": ["src/**", "package.json", "tsconfig.json"],
    "outputs": ["dist/**"]
  }
}
```

### Incremental Builds
- Only rebuild changed packages
- Use content hashing for cache keys
- Share build artifacts between packages

## CODE SHARING PATTERNS

### Shared Configuration
```
packages/
  config/
    eslint/
      base.js
      react.js
    typescript/
      base.json
      react.json
```

### Shared Components
```
packages/
  ui/
    src/
      Button/
        Button.tsx
        Button.test.tsx
      index.ts
    package.json
```

### Package References
```json
{
  "dependencies": {
    "@myorg/ui": "workspace:*"
  }
}
```

## CI/CD FOR MONOREPOS

### GitHub Actions
```yaml
name: CI
on: [push, pull_request]

jobs:
  main:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: pnpm install
      - run: pnpm turbo run build test lint
```

### Selective Testing
```bash
# Only test affected packages
turbo run test --filter=...[origin/main]

# Only build changed packages
turbo run build --filter=...[HEAD^1]
```

## OUTPUT FORMAT
```text
[MONOREPO CONFIGURATION]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tool: {Turborepo|Nx|Lerna|Moon}
Packages: {count}

PACKAGE STRUCTURE:
- {package}: {description}
- {package}: {description}

BUILD OPTIMIZATION:
- Parallel: {enabled/disabled}
- Caching: {local|remote|both}
- Affected: {enabled/disabled}

CI/CD:
- Pipeline: {description}
- Selective testing: {enabled/disabled}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## WHEN TO USE
- Multiple packages/shared code must live in one repo with reliable dependency resolution.
- You want to build only the affected packages (not the whole graph) to keep CI fast at scale.
- You need to enforce package boundaries (which package may depend on which) at the tooling level.
- Shared config, components, or types must be reused across packages without duplication.
- A build graph/caching strategy (Turborepo/Nx/Lerna) must be selected and tuned.

## WHEN NOT TO USE
- **A single-package repo** — no monorepo complexity to manage; adding a workspace tool is overhead.
- **The problem is package publishing only** (registry, tagging) — that's a publishing/release concern, largely Lerna's release mechanics, not workspace builds.
- **Very heterogeneous unrelated projects** that share nothing — a monorepo adds shared-tooling cost without reuse benefit; separate repos better isolate.
- **Linux tooling build scale (Bazel/Moon) is a fit but too much for a small team** — pick the simplest tool that meets the actual needs.
- **A migration restructure is out of scope** — splitting/merging repos is an architectural move; scope the boundary first.

## DECISION TREE
```text
1. SCOPE   → multiple packages sharing tooling/config? → monorepo worth it. Single pkg → skip.
2. TOOL    → JS/TS? Turborepo (fast+cache) or Nx (affected + graph enforcement);
   needing release/publish-first? Lerna. Multi-language/Google-scale? Bazel/Moon. Python? Pants/Moon.
3. WORKSPACES → npm/pnpm/yarn workspaces: define packages/*, apps/*; pick pnpm for strict deps.
4. BOUNDARIES → restrict `import/no-restricted-paths` per zone; enforce no extraneous/relative-parent.
5. BUILD GRAPH → declare dependsOn + inputs/outputs; enable affected-only and caching (local/remote).
6. CI      → affected build/test/lint; selective testing; shared cache.
7. VERIFY  → affected build only touches changed tree; cache reports hits; boundaries enforced.
```
Never skip the boundary/viz step — a monorepo without enforced boundaries becomes a dependency minefield.

## FAILURE MODES & MITIGATIONS
- **Workspace hoisting/dedup drift.**
  DETECT: some packages resolve duplicate, mismatched versions of a shared dependency; builds succeed/fail inconsistently.
  FIX: use pnpm's strict resolver (or the tool's workspace protocol), centralize shared deps at the root, and run a single `install --lockfile-only`-consistent update.
- **Cache poisoning / stale outputs.**
  DETECT: a rebuilt package serves an old `dist/` or cache returns a stale artifact; incremental build is wrong.
  FIX: define precise `inputs`/`outputs` for every task (src, configs, lockfiles in; dist out), enable content hashing, and clear/remote-cache on mismatch.
- **Secret in a shared CI workflow.**
  DETECT: an API key/credential used across many packages is committed or exposed in the shared pipeline.
  FIX: scope secrets per repo/org, never in `.env`-committed files, and rotate; make the shared workflow reference injected secrets only.
- **Unauthorized package-to-package coupling.**
  DETECT: `core` imports `ui` (against the boundary), so a change to ui ripples into core unexpectedly.
  FIX: enforce `import/no-restricted-paths` / dependency-cruiser; merge-gate the build so boundary violations fail CI.
- **Affected-only misses a dependant.**
  DETECT: changing `shared/config` doesn't retrigger the dependents' builds; stale deps break runtime.
  FIX: build the "affected + its dependents" (`--filter=...[HEAD^]` and `...[target]`), and rely on the package graph, not a manual list.
- **Root-level bloat / poor separation.**
  DETECT: every package accumulates its own node_modules scaffold and config is repeated everywhere; build graph grows unbounded.
  FIX: hoist shared deps, centralize config packages, share lint/tsconfig via a config package, and enforce per-package boundaries.

## VERIFICATION GATE
- **Clean affected build**: after a change, `--affected`-build rebuilt exactly the changed tree + dependents and passed.
- **Cache verified**: the incremental cache reports hits (not cold rebuilds) for unchanged packages.
- **Boundaries enforced**: `import/no-restricted-paths`/dependency check passes in CI; no cross-boundary import.
- **Workspace lock consistent**: a single resolved lock matches the declaration across all packages; no version drift.
- **Faster-by-measure**: total build time / artifact count is recorded before → after with the selective-testing delta.
- **red-team-qa review**: check for dependency-version drift, cross-package coupling, and stale/poisoned caches.

## REFERENCES
- Turborepo documentation — `turbo.json`, `dependsOn`, `inputs`/`outputs`, remote cache.
- Nx documentation — affected commands, project graph, target defaults.
- pnpm / npm / yarn workspaces documentation — workspace root, hoisting, dependency resolution.
- monorepo.tools — comparison and selection handbook for monorepos.
