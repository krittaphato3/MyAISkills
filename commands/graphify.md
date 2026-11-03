---
description: Turn any codebase into a queryable knowledge graph with AST parsing, community detection, and interactive viz
argument-hint: [path or repo url] [--update] [--mode deep]
skills: graphify
---

# Graphify

Turn any codebase into a navigable knowledge graph with community detection, an audit trail, and query tools.

## Target

$ARGUMENTS

## Instructions

1. **Query Existing Graph (if `graphify-out/graph.json` exists)**:
   - When answering codebase questions and a graph exists, query before grepping:
     ```bash
     graphify query "$ARGUMENTS"
     ```
   - For specific symbols or paths:
     ```bash
     graphify explain "<symbol>"
     graphify path "<nodeA>" "<nodeB>"
     ```

2. **Build or Update Knowledge Graph**:
   - Full build on target path or URL (default is current directory):
     ```bash
     graphify $ARGUMENTS
     ```
   - Incremental update (re-extracts only modified files):
     ```bash
     graphify update
     ```

3. **Deliverables**:
   - Interactive HTML graph: `graphify-out/graph.html`
   - Architecture report: `graphify-out/GRAPH_REPORT.md`
   - Full graph model: `graphify-out/graph.json`
