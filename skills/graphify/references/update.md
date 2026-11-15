# graphify reference: incremental update and cluster-only

Load this only when the user passed `--update` or `--cluster-only`. A first-time full build never reads this file.

## For --update (incremental re-extraction)

Use when files were added, modified, or deleted since the last run. It only re-extracts changed files via deterministic AST parsing, merges them into the existing graph, and regenerates reports in a few seconds without subagent overhead or token burn.

Execute this single self-contained command (substitute `TARGET_PATH` with the directory path provided by the user, or `.` if none provided):

```bash
$(cat graphify-out/.graphify_python) -c "
import sys, json, time, os
from pathlib import Path
from graphify.detect import detect_incremental, save_manifest
from graphify.extract import extract
from graphify.extractors.markdown import extract_markdown
from graphify.build import build_merge, build_from_json
from graphify.cluster import cluster, label_communities_by_hub, score_all
from graphify.export import to_json, to_html
from graphify.report import generate
from graphify.analyze import graph_diff, god_nodes, surprising_connections, suggest_questions
from graphify.paths import out_path
from graphify.watch import _read_build_excludes, _read_build_gitignore

t0 = time.time()
target_arg = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != 'TARGET_PATH' else '.'
root = Path(target_arg).resolve()

out_dir = root / 'graphify-out'
if not out_dir.exists():
    out_dir = Path('graphify-out').resolve()
graph_json = out_dir / 'graph.json'
old_json = out_dir / '.graphify_old.json'

if not graph_json.exists():
    print(f'error: no graph found at {graph_json} — run a full /graphify build first', file=sys.stderr)
    sys.exit(1)

# Snapshot old graph for diffing
try:
    old_data = json.loads(graph_json.read_text(encoding='utf-8'))
    old_json.write_text(json.dumps(old_data), encoding='utf-8')
except Exception:
    pass

# Step 1: Detect changes
inc = detect_incremental(root, extra_excludes=_read_build_excludes(out_path()), gitignore=_read_build_gitignore(out_path()))
new_files = inc.get('new_files', {})
deleted = list(inc.get('deleted_files', []))
total_changed = inc.get('new_total', 0)

print(f'[graphify update] Checked {inc.get(\"total_files\", 0)} files in {time.time()-t0:.2f}s: {total_changed} changed, {len(deleted)} deleted')

if total_changed == 0 and not deleted:
    print('No files changed since last run. Nothing to update.')
    if old_json.exists():
        old_json.unlink(missing_ok=True)
    sys.exit(0)

# Step 2: Extract changed files
code_files = [Path(p) for p in new_files.get('code', [])]
doc_files = [Path(p) for p in new_files.get('document', [])]

extractions = []
if code_files:
    ast_res = extract(code_files, parallel=False, root=root, cache_root=root)
    extractions.append(ast_res)
if doc_files:
    doc_nodes, doc_edges = [], []
    for p in doc_files:
        if p.suffix.lower() in ('.md', '.markdown', '.txt', '.qmd', '.mdx', '.skill'):
            try:
                res = extract_markdown(p)
                doc_nodes.extend(res.get('nodes', []))
                doc_edges.extend(res.get('edges', []))
            except Exception as e:
                print(f'Warning: failed extracting {p}: {e}')
    extractions.append({'nodes': doc_nodes, 'edges': doc_edges, 'hyperedges': [], 'input_tokens': 0, 'output_tokens': 0})

# Step 3: Merge into graph
prune = deleted if deleted else None
G = build_merge(extractions, graph_path=str(graph_json), prune_sources=prune, root=str(root))
communities = cluster(G)
labels = label_communities_by_hub(G, communities)

# Step 4: Export graph and community visualization
to_json(G, communities, str(graph_json), force=True, community_labels=labels)
try:
    to_html(G, communities, str(out_dir / 'graph.html'), community_labels=labels, node_limit=5000)
except Exception:
    pass

# Step 5: Regenerate report and update manifest
try:
    cohesion = score_all(G, communities)
    gods = god_nodes(G)
    surprises = surprising_connections(G, communities)
    questions = suggest_questions(G, communities, labels)
    report = generate(G, communities, cohesion, labels, gods, surprises, {'warning': 'incremental'}, {'input': 0, 'output': 0}, str(root), suggested_questions=questions)
    (out_dir / 'GRAPH_REPORT.md').write_text(report, encoding='utf-8')
except Exception as e:
    print(f'Note: report generation skipped: {e}')

save_manifest(inc['files'], str(out_dir / 'manifest.json'), root=root)

# Step 6: Diff summary
diff_summary = ''
if old_json.exists():
    try:
        old_G = build_from_json(json.loads(old_json.read_text(encoding='utf-8')))
        diff = graph_diff(old_G, G)
        diff_summary = f' (+{len(diff.get(\"added_nodes\", []))} nodes, -{len(diff.get(\"removed_nodes\", []))} nodes)'
        old_json.unlink(missing_ok=True)
    except Exception:
        pass

print(f'[graphify update] SUCCESS in {time.time()-t0:.2f}s! Graph now has {G.number_of_nodes()} nodes, {G.number_of_edges()} edges{diff_summary}')
" TARGET_PATH
```

---

## For --cluster-only

Skip Steps 1–3. Re-run clustering on the existing graph:

```bash
graphify cluster-only .
```

`graphify cluster-only .` is **self-contained**: it re-clusters, names communities, and regenerates `GRAPH_REPORT.md`, `graph.json`, and `graph.html` from the existing graph. **Do not re-run Steps 5–9**.
