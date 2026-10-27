# Actions, Deploy Strategies, IaC, Rollback (on-demand reference)

Load only the section needed.

## GITHUB ACTIONS PATTERNS
### Basic Workflow
```yaml
name: CI/CD
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test
      - run: npm run lint
```

### Matrix Builds
```yaml
strategy:
  matrix:
    node-version: [18, 20, 22]
    os: [ubuntu-latest, windows-latest]
  fail-fast: false
```

### Caching
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

### Secrets Management
```yaml
env:
  API_KEY: ${{ secrets.API_KEY }}
```

## DEPLOYMENT STRATEGIES
### Blue-Green
- Two identical environments
- Switch traffic atomically
- Instant rollback by switching back

### Canary
- Deploy to small percentage first
- Monitor metrics
- Gradually increase traffic
- Auto-rollback on errors

### Rolling
- Replace instances one at a time
- Maintain capacity throughout
- Slow but safe

### Feature Flags
- Deploy code with flag off
- Enable flag when ready
- No deployment needed for feature release

## INFRASTRUCTURE AS CODE
### Terraform
```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Name = "WebServer"
  }
}
```

### Pulumi (TypeScript)
```typescript
const server = new aws.ec2.Instance("web", {
  ami: "ami-0c55b159cbfafe1f0",
  instanceType: "t2.micro",
  tags: { Name: "WebServer" }
});
```

## ROLLBACK PROCEDURES
```bash
# Quick rollback (last known good)
kubectl rollout undo deployment/myapp

# Terraform rollback
terraform apply -target=module.previous_version

# Database rollback (if needed)
psql -f rollback_migration.sql
```

## BRANCH PROTECTION
- Require PR reviews (2 approvals for main)
- Require status checks to pass
- Require up-to-date branches
- Restrict force pushes
- Require signed commits
