<#
.SYNOPSIS
  Solo Enterprise Codebase Intelligence Stack Setup (codebase-memory-mcp + serena + context7)
.DESCRIPTION
  Automatically initializes and indexes any project directory for Antigravity with zero repo pollution.
  Usage:
    context-setup                   # runs on current working directory
    context-setup "C:\path\to\proj" # runs on specified path
#>

param(
    [string]$TargetDir = ""
)

$ErrorActionPreference = "Stop"

Write-Host "=== Codebase Intelligence Stack Setup ===" -ForegroundColor Cyan

# 1. Resolve Target Directory
if ([string]::IsNullOrWhiteSpace($TargetDir)) {
    # Check if inside a git repository
    $gitRoot = git rev-parse --show-toplevel 2>$null
    if ($LASTEXITCODE -eq 0 -and [string]::IsNullOrWhiteSpace($gitRoot) -eq $false) {
        $TargetDir = $gitRoot.Trim()
    } else {
        $TargetDir = (Get-Location).Path
    }
} else {
    $TargetDir = (Resolve-Path $TargetDir).Path
}

$ProjectName = (Split-Path -Leaf $TargetDir)
Write-Host "Target Project: $TargetDir ($ProjectName)" -ForegroundColor Green

# 2. Verify / Ensure codebase-memory-mcp
Write-Host "`n[1/5] Checking codebase-memory-mcp..." -ForegroundColor Yellow
$cbmExe = "C:\Users\Oz\AppData\Local\Programs\codebase-memory-mcp\codebase-memory-mcp.exe"
if (-not (Test-Path $cbmExe)) {
    Write-Host "Installing codebase-memory-mcp..." -ForegroundColor Gray
    Invoke-WebRequest -Uri "https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.ps1" -OutFile "$env:TEMP\cbm-install.ps1"
    Unblock-File "$env:TEMP\cbm-install.ps1"
    & "$env:TEMP\cbm-install.ps1"
}

# Ensure auto_index config
& $cbmExe config set auto_index true | Out-Null
& $cbmExe config set auto_index_limit 200000 | Out-Null
Write-Host "codebase-memory-mcp is ready (auto_index: true)." -ForegroundColor Green

# 3. Trigger codebase-memory-mcp indexing on this directory
Write-Host "`n[2/5] Indexing repository with codebase-memory-mcp..." -ForegroundColor Yellow
try {
    & $cbmExe cli index_repository --repo-path "$TargetDir"
    Write-Host "codebase-memory-mcp index complete." -ForegroundColor Green
} catch {
    Write-Host "codebase-memory-mcp index failed: $_" -ForegroundColor Red
}

# 4. Configure & Pre-Index Serena
Write-Host "`n[3/5] Pre-indexing Language Server symbols with Serena..." -ForegroundColor Yellow

# Ensure Serena global config stores projects centrally outside target repository
$serenaConfigFile = "$HOME\.serena\serena_config.yml"
if (Test-Path $serenaConfigFile) {
    $content = Get-Content $serenaConfigFile -Raw
    $content = $content -replace "agent_interface:\s*\w+", "agent_interface: tools"
    $content = $content -replace 'project_serena_folder_location:.*', 'project_serena_folder_location: "C:/Users/Oz/.serena/projects/$projectFolderName"'
    Set-Content -Path $serenaConfigFile -Value $content -Encoding UTF8
}

# Run Serena indexing
& uvx --from git+https://github.com/oraios/serena serena project index --name "$ProjectName" "$TargetDir"
Write-Host "Serena Language Server cache warmed for $ProjectName." -ForegroundColor Green

# Clean up any local .serena directory inside the repo if created
$localSerena = Join-Path $TargetDir ".serena"
if (Test-Path $localSerena) {
    $centralDest = "C:\Users\Oz\.serena\projects\$ProjectName"
    if (-not (Test-Path $centralDest)) {
        New-Item -ItemType Directory -Path $centralDest -Force | Out-Null
    }
    Copy-Item -Path "$localSerena\*" -Destination $centralDest -Recurse -Force
    Remove-Item -Path $localSerena -Recurse -Force
}

# 5. Update mcp_config.json
Write-Host "`n[4/5] Updating Antigravity mcp_config.json..." -ForegroundColor Yellow
$normalizedPath = $TargetDir.Replace("\", "/")
$mcpJsonPath = "$HOME\.gemini\config\mcp_config.json"

$pythonScript = @"
import json, pathlib

mcp_path = pathlib.Path(r'$mcpJsonPath')
data = {}
if mcp_path.exists() and mcp_path.stat().st_size > 0:
    try:
        data = json.loads(mcp_path.read_text(encoding='utf-8'))
    except Exception:
        data = {}

if 'mcpServers' not in data:
    data['mcpServers'] = {}

servers = data['mcpServers']

# 1. codebase-memory-mcp
cbm_exe = r'$cbmExe'.replace('\\\\', '/')
servers['codebase-memory-mcp'] = {
    'command': cbm_exe,
    'args': []
}

# 2. serena auto-detecting active workspace project (works across all repos)
servers['serena'] = {
    'command': 'uvx',
    'args': [
        '--from',
        'git+https://github.com/oraios/serena',
        'serena',
        'start-mcp-server',
        '--context',
        'ide',
        '--project-from-cwd'
    ]
}

# 3. context7
servers['context7'] = {
    'command': 'npx',
    'args': [
        '-y',
        '@upstash/context7-mcp'
    ]
}

mcp_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
"@

python -c "$pythonScript"
Write-Host "mcp_config.json updated successfully." -ForegroundColor Green

# 6. Ensure Global Policy in AGENTS.md
Write-Host "`n[5/5] Checking Global AGENTS.md policy..." -ForegroundColor Yellow
$policyHeader = "## Codebase Navigation & Surgical Editing Policy (STRICT)"
$geminiAgentsMd = "$HOME\.gemini\config\AGENTS.md"
if (-not (Test-Path $geminiAgentsMd) -or -not (Get-Content $geminiAgentsMd | Select-String -Pattern $policyHeader -Quiet)) {
    $policyBlock = @"
# Global Codebase Policy

## Codebase Navigation & Surgical Editing Policy (STRICT)

- NEVER start tasks with broad `grep`, `rg`, `search_directory`, or full-file reads on source code.
- STEP 1 (Discovery & Blast Radius): Call `codebase-memory-mcp` tools (`search_graph`, `trace_path`, `get_architecture`, `detect_changes`) FIRST to locate modules, callers, services, and impact paths.
  - Zero-Project Fallback: If `codebase-memory-mcp` reports `projects: 0` or is unindexed, DO NOT panic or loop. Immediately fall back to `serena` (`get_symbols_overview`, `find_symbol`, `find_referencing_symbols`), which parses AST/LSP directly from project source files on-the-fly without requiring a pre-indexed database.
- STEP 2 (Zero-Read Code Retrieval): To inspect function/method bodies, ALWAYS call `codebase-memory-mcp` tool `get_code_snippet(qualified_name=...)` or `serena` tool `find_symbol`. This returns the full implementation directly without triggering any file reads (`read_file`).
- STEP 3 (Anti-Fragmentation & Consolidated Reads): Do NOT make sequential micro-chunk reads (e.g., reading 30–60 lines 3+ times in the same file). If viewing surrounding JSX/hooks is strictly necessary before editing, read the entire relevant block in ONE consolidated `read_file` call (max 1 read per file).
- STEP 4 (Surgical Edits): ALWAYS use `serena` tool `replace_symbol_body` or precise `edit_file` on the target function without re-reading surrounding files.
- STEP 5 (World-Class Velocity & Proportional Testing — NO SLOW SNAIL WORKFLOWS):
  - **Questions Stay Questions**: If the user asks a diagnostic question (*"is X clickable?", "how does Y work?"*), inspect the code and answer directly with file:line proof in under 30 seconds. Do NOT silently start unsolicited multi-file refactors, builds, or test suites unless explicitly requested.
  - **Fast Lane for Scoped Changes (T0/T1)**: Verify scoped edits with targeted tests (`vitest run <file>`, `jest <file>`) and fast incremental typecheck (`tsc --noEmit`). If an exported function or shared interface is modified, run tests for direct callers too (if >3 callers, test representative callers and reserve full suite for /ship). NEVER trigger full production bundling (`npm run build` / `vite build`) during iterative development turns—reserve full workspace builds strictly for final `/ship` or deployment.
  - **Zero Bureaucracy / Anti-Slop**: Skip heavy 8-stage ceremony, multi-agent debates, or multi-page documentation logs for routine UI/logic fixes. Be concise, surgical, and fast.
- STEP 6 (External Libraries): Call `context7` (`resolve-library-id` -> `query-docs`) whenever checking external SDK or framework APIs.
- STEP 7 (Fallback Only): Use `grep` or raw file reads ONLY for plain-text config files (`.env`, `.yaml`, `.json`), SQL/migrations, or exact literal error strings.
- STEP 8 (Craftsmanship & Anti-Slop Standard):
  - **Rule of Three**: Keep logic local. No speculative helper files (`utils.ts`, `helpers.ts`) for single-use code.
  - **Nearest-Neighbor Style**: Match adjacent patterns in the same file for error handling, naming, and typing.
  - **Why, Not What**: Zero narrative comments. Only document external constraints or quirks.
  - **Zero Type Escapes**: No `as any`, `@ts-ignore`, or non-null assertions (`!`) to silence typechecks.
  - **Single-Command Proving**: Run targeted test and incremental typecheck in a single combined command (`vitest run <file> && tsc --noEmit`) to eliminate shell process latency.
"@
    Set-Content -Path $geminiAgentsMd -Value $policyBlock -Encoding UTF8
}
Write-Host "Global AGENTS.md policy is active." -ForegroundColor Green

Write-Host "`n=== Setup Complete! ===" -ForegroundColor Cyan
Write-Host "Project '$ProjectName' is now wired to codebase-memory-mcp + serena + context7." -ForegroundColor Green
Write-Host "Zero repo files modified. Ready for Antigravity!`n" -ForegroundColor Green
