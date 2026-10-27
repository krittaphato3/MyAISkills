---
name: roblox-toolchain
description: >-
  Configures and operates the modern Roblox development toolchain: Rojo project synchronization
  (default.project.json, sourcemap generation, partition mappings), Wally and pesde package
  management, and luau-lsp type checking integrated with Studio MCP. Use when configuring Rojo,
  managing external Luau dependencies or package manifests, setting up sourcemaps, or running
  CI/CD Luau typecheck gates. Studio script execution routes to roblox-studio-mcp; game architecture
  and runtime logic route to roblox-scripting; Luau language fundamentals to roblox-lua-developer.
metadata:
  version: 1.0.0
  domain: roblox
  grade: G3
  status: active
  last-reviewed: '2026-10-24'
  owned-by-agent: roblox-scripter
---

# Roblox Toolchain

Professional Roblox engineering relies on external version control, file-system-driven development,
and automated toolchains. This skill governs the integration between the external filesystem
(Rojo, package managers, type checkers) and Roblox Studio via Studio MCP.

## WHEN TO USE

- Setting up or maintaining Rojo project configurations (`default.project.json`).
- Generating and updating `sourcemap.json` for external tools and Luau Language Server.
- Managing external packages and dependencies with Wally (`wally.toml`, `wally.lock`) or pesde (`pesde.toml`).
- Configuring type checking and linting workflows with `luau-lsp`, `selene`, and `stylua`.
- Establishing synchronization pipelines between local Git repositories and Roblox Studio.
- Setting up CI/CD automation for Roblox places (building place files via `rojo build`, running headless tests).

## WHEN NOT TO USE

- Direct in-Studio instance or script execution via MCP — `roblox-studio-mcp`.
- Writing gameplay logic, networking, and runtime systems — `roblox-scripting`.
- Luau syntax, type definition authoring, and OOP patterns — `roblox-lua-developer`.
- Adversarial security audits of game scripts or remotes — `roblox-security`.
- Auditing marketplace/Creator Store assets for backdoors — `roblox-asset-security`.

## DECISION TREE

```text
1. PROJECT STRUCTURE & SYNC (Rojo)
   Local filesystem is the source of truth for all scripts and code assets.
   Map partitions cleanly in `default.project.json`:
   - src/server -> ServerScriptService
   - src/client -> StarterPlayer.StarterPlayerScripts
   - src/shared -> ReplicatedStorage
   Keep non-script binary instances (models, terrain, sounds) managed via Studio place files or Wally packages.

2. DEPENDENCY MANAGEMENT (Wally vs pesde)
   Wally: Standard community registry. Uses `wally.toml`.
   - Install packages into Packages/ (ReplicatedStorage) or ServerPackages/ (ServerStorage).
   - Use `wally-package-types` to generate typing definitions for Wally dependencies.
   pesde: Multi-target Luau package manager. Uses `pesde.toml`.
   - Generates typed export paths natively.

3. TYPE CHECKING & SOURCEMAPS
   Run `rojo sourcemap default.project.json --output sourcemap.json`.
   luau-lsp consumes `sourcemap.json` to resolve `game.ReplicatedStorage...` and cross-module requires.
   Ensure strict typing passes before syncing to Studio.

4. STUDIO MCP SYNCHRONIZATION
   When working with Studio MCP:
   - For local-first workflows, write files locally and verify Rojo live sync reflects changes in Studio.
   - For Studio-first edits, use `multi_edit` or `execute_luau` and immediately sync back or export.
```

## WORKFLOW PATTERNS

### 1. Rojo Configuration (`default.project.json`)
```json
{
  "name": "RobloxProject",
  "tree": {
    "$className": "DataModel",
    "ReplicatedStorage": {
      "$className": "ReplicatedStorage",
      "Shared": {
        "$path": "src/shared"
      },
      "Packages": {
        "$path": "Packages"
      }
    },
    "ServerScriptService": {
      "$className": "ServerScriptService",
      "Server": {
        "$path": "src/server"
      },
      "ServerPackages": {
        "$path": "ServerPackages"
      }
    },
    "StarterPlayer": {
      "$className": "StarterPlayer",
      "StarterPlayerScripts": {
        "$className": "StarterPlayerScripts",
        "Client": {
          "$path": "src/client"
        }
      }
    }
  }
}
```

### 2. Dependency Management Rules
- Never commit downloaded dependency code directly without manifest tracking.
- Commit `wally.lock` or `pesde.lock` to guarantee deterministic builds.
- Scope dependencies strictly: client/shared dependencies in `Packages` (replicated); server-only dependencies in `ServerPackages` (never replicated).

### 3. Sourcemap & Type Checking
- Keep `sourcemap.json` synchronized when adding, moving, or renaming files:
  `rojo sourcemap default.project.json -o sourcemap.json`
- Configure `luau-lsp` with sourcemap path:
  `luau-lsp analyze --sourcemap=sourcemap.json --definitions=definitions/ ...`

## QUANTITATIVE RULES

- 100% of codebase partitioned in `default.project.json` without ambiguous overlaps.
- 0 server-side packages exposed in `ReplicatedStorage` or client paths.
- `sourcemap.json` regenerated whenever the filesystem project tree changes.
- Luau type checking in strict mode (`--!strict`) on all core shared libraries.
- Package manifest and lockfile committed together on dependency updates.

## VERIFICATION GATE

- [ ] `default.project.json` parses as valid JSON with correct DataModel container mapping.
- [ ] Dependencies documented in manifest (`wally.toml` or `pesde.toml`) and locked.
- [ ] Server-only dependencies segregated from replicated containers.
- [ ] `sourcemap.json` generated and resolves all external and internal module paths.
- [ ] `luau-lsp analyze` passes with zero type errors.
- [ ] Rojo sync connects cleanly to Studio or `rojo build` produces a valid place file.

## REFERENCES

- `roblox-scripting` — system architecture and runtime implementation
- `roblox-lua-developer` — Luau language features, typing contracts, and idioms
- `roblox-studio-mcp` — Studio DataModel inspection and script execution
- `roblox-testing` — automated unit and integration tests
