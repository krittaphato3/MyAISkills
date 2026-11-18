---
description: Query or build the codebase knowledge graph via codebase-memory-mcp
argument-hint: [query or symbol] [--path <repo-path>]
skills: codebase-navigation
---

# Codebase Graph

Query and explore the codebase knowledge graph using `codebase-memory-mcp` for instant topology mapping, caller/callee tracing, and blast radius analysis.

## Target

$ARGUMENTS

## Instructions

1. **Query Knowledge Graph**:
   - For symbols, routes, or entities:
     Call `search_graph(name_pattern="$ARGUMENTS")`
   - For caller/callee dependencies:
     Call `trace_path(function_name="$ARGUMENTS", direction="inbound")` or `direction="outbound"`
   - For architecture overview:
     Call `get_architecture()`

2. **Inspect Implementation (Zero Reads)**:
   - Call `get_code_snippet(qualified_name="...")` or Serena `find_symbol`

3. **Fallback If Unindexed**:
   - If `codebase-memory-mcp` returns `projects: 0`, index the target directory:
     Call `index_repository(repo_path=".")`
     Or immediately inspect symbols via Serena (`get_symbols_overview`).
