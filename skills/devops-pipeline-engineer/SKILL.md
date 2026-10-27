---
name: devops-pipeline-engineer
description: >-
  Designs CI/CD and deployment infrastructure: GitHub Actions, caching, matrix builds,
  environment promotion, IaC, canary or blue-green rollout, and rollback. Use when
  standing up or fixing a build/release pipeline or infrastructure configuration.
  Containers route to container-optimizer; monitoring and SLOs to observability-sre; a
  live outage to incident-response-engineer.
metadata:
  version: 3.0.0
  domain: production
  grade: G2
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: devops-engineer
---

# DEVOPS PIPELINE ENGINEER SKILL

Expert knowledge in CI/CD workflows, Infrastructure as Code, deployment strategies, and pipeline optimization.

## GITHUB ACTIONS, DEPLOY STRATEGIES, IAC, ROLLBACK, BRANCH PROTECTION

See `references/actions-deploy-rollback.md` (workflow YAML, matrix/cache/secrets, blue-green/canary/rolling/flags, Terraform/Pulumi, rollback commands, branch rules) — load only the section needed.

## PIPELINE OPTIMIZATION
- Cache dependencies between runs
- Parallelize independent jobs
- Use matrix builds for multi-platform testing
- Artifact passing between jobs
- Skip CI on doc-only changes

## PIPELINE STAGES
1. **Build**: Compile, bundle, generate artifacts
2. **Test**: Unit, integration, e2e tests
3. **Scan**: Security scanning, linting, type checking
4. **Stage**: Deploy to staging environment
5. **Verify**: Run smoke tests against staging
6. **Deploy**: Deploy to production
7. **Monitor**: Health checks, metrics, alerts

## OUTPUT FORMAT
```text
[CI/CD DELIVERABLE]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Service: {name}
Platform: {GitHub Actions|GitLab CI|Jenkins}

PIPELINE:
- Stage 1: {description}
- Stage 2: {description}
- Stage 3: {description}

DEPLOYMENT: {blue-green|canary|rolling}
ROLLBACK: {procedure}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## WHEN TO USE
- Standing up or replacing a CI/CD pipeline: build, test, scan, stage, deploy stages.
- Automating deployments with a chosen strategy (blue-green, canary, rolling) and a defined rollback.
- Managing infrastructure as code (Terraform/Pulumi) as part of the delivery flow.
- Optimizing pipeline time and cost: caching, parallelization, matrix builds, artifact passing.
- Enforcing branch protection + release gates (required checks, approvals, signed commits).

## WHEN NOT TO USE
- **A single manual script is enough** — one-off backend provisioning or a local one-shot build does not need a full pipeline.
- **The image/content is already optimized and CI is only running it** — container image concerns go to container-optimizer; pipeline here is about flow, not the artifact itself.
- **Repo layout/package boundaries** — that is monorepo-workspace-architect's domain, not pipeline YAML.
- **Application performance tuning** — profiler and benchmarks go to performance-profiler.
- **Pure IaC exploration unrelated to delivery** — if there is no build/test/deploy flow, this skill adds little.

## DECISION TREE
```text
1. SCOPE   → what must CI/CD do: build? test? stage? deploy? Only what the running flow needs.
2. PLATFORM → GitHub Actions? GitLab CI? Jenkins? Self-hosted? Pick the executor available in-repo.
3. STAGES  → Build → Test(unit,integration,e2e) → Scan → Stage → Verify → Deploy → Monitor
   (lock the order; each stage must fail fast).
4. SPEED   → cache deps, parallelize independent jobs, matrix for multi-platform, skip on doc-only.
5. DEPLOY  → choose strategy by risk tolerance: blue-green (instant rollback) / canary (metrics-gated)
   / rolling (capacity-safe); for feature toggles use flags, not deploy.
6. RELEASE GATE → branch protection + status checks before merge; auto-rollback on fail.
7. VERIFY  → smoke tests against the deployed env; health checks + rollback procedure rehearsed.
```
Never deploy with no rollback — a strategy without a revert path is not a deployment strategy.

## FAILURE MODES & MITIGATIONS
- **Secret in pipeline YAML / logs.**
  DETECT: API keys, tokens, or passwords appear in `env:` as literals or in ci logs.
  FIX: use secret store variables (`${{ secrets.* }}`), OIDC/cloud IAM where possible, and rotate the secret; scrub logs.
- **Cache miss nullifies speedup.**
  DETECT: cache keys don't reflect the real inputs, so dependencies re-download every run (build time unchanged).
  FIX: derive cache key from the lockfile hash (`hashFiles('**/package-lock.json')`), tune the restore-keys setting for partial matches, and verify cache is actually hit.
- **Flaky test makes every PR red.**
  DETECT: a test intermittently fails with no code change; pipeline blocks unrelated merges.
  FIX: quarantine the flaky test, run it on a retry, or degrade to non-blocking; investigate and fix the root cause.
- **Unreviewed merge in a protected branch.**
  DETECT: a change reaches main without required approvals or status checks; branch protection is disabled.
  FIX: enforce branch protection (required review count, status checks pass, up-to-date, no force-push), and audit the protection config in CI.
- **Canary move without monitoring.**
  DETECT: traffic is shifted with no health metric gate, so a regression only surfaces after full rollout.
  FIX: gate canary steps on monitoring/SLO (error rate, latency) before increasing the share; auto-rollback on threshold breach.
- **Environment drift (staging works, prod breaks).**
  DETECT: deploy is fine in staging but fails in prod due to config, architecture, or data differences.
  FIX: keep staging configuration-identical to prod (env parity), manage all config via IaC, and run staging before prod with the same deployment path.

## VERIFICATION GATE
- **Pipeline sound on a clean repo**: a fresh checkout runs the pipeline end-to-end green (no reliance on local state).
- **Secrets check**: scan of `env:`/scripts finds no literal secrets; secret references resolve in CI.
- **Cache hit verified**: dependency-cache step reports a hit, not a miss (build time within budget).
- **Deployment rehearsal**: the chosen strategy + rollback were both exercised against the canonical env before go-live.
- **Monitoring tie-in active**: release is gated on health checks/smoke tests; rollback path is tested.
- **red-team-qa review**: adversarial check for secrets leaks, unprotected branch, or unrehearsed rollback.

## REFERENCES
- GitHub Actions documentation — workflow syntax, caching, secrets, matrix builds.
- GitLab CI / Jenkins pipeline best practices — stages, caching.
- Terraform / Pulumi docs — IaC and state management.
- SRE Google workbook — release strategy and rollback (canary/blue-green/rolling).
