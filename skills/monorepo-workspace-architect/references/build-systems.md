# Turborepo + Nx Patterns (on-demand reference)

Load only when configuring Turborepo or Nx.

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
