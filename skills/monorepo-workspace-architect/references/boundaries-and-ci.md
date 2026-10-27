# Boundaries, Build Graph, Sharing, CI (on-demand reference)

Load only the section needed.

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
