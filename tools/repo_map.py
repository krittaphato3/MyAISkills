#!/usr/bin/env python3
"""repo_map.py — a compact symbol map for a repository, built for agent context budgets.

Why this exists: agents burn most of their tokens reading whole files to find out what
matters. This script extracts the structure (files, symbols, line numbers) once and prints
it small enough to paste into a prompt. Use it for orientation, then read only the lines a
symbol lookup points at.

Usage:
    python tools/repo_map.py                     # map the current directory
    python tools/repo_map.py <path>              # map another tree
    python tools/repo_map.py <path> --focus auth # symbol/path hits with line numbers
    python tools/repo_map.py <path> --max-tokens 2000
    python tools/repo_map.py <path> --json

Exit codes: 0 map produced, 2 path missing/unreadable.
"""
from __future__ import annotations

import argparse
import ast
import fnmatch
import io
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

IGNORED_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "__pycache__", ".venv", "venv", "env",
    "dist", "build", "out", "target", ".next", ".nuxt", ".cache", ".turbo",
    "coverage", ".mypy_cache", ".pytest_cache", ".ruff_cache", "vendor", ".idea",
    ".vscode", ".terraform", ".gradle", ".dart_tool", "Pods", "obj", "bin",
    "cache", "caches", "logs", "artifacts",
}
LANG_BY_EXT = {
    ".py": "py", ".ts": "ts", ".tsx": "tsx", ".js": "js", ".jsx": "jsx",
    ".mjs": "js", ".cjs": "js", ".lua": "lua", ".luau": "luau", ".go": "go",
    ".rs": "rs", ".java": "java", ".kt": "kt", ".swift": "swift", ".cs": "cs",
    ".rb": "rb", ".php": "php",
}
MAX_FILE_BYTES = 1_000_000

TS_PATTERNS = [
    (re.compile(r"^\s*export\s+(?:default\s+)?(?:async\s+)?function\s+(\w+)"), "fn"),
    (re.compile(r"^\s*(?:export\s+)?(?:abstract\s+)?class\s+(\w+)"), "class"),
    (re.compile(r"^\s*export\s+(?:interface|type)\s+(\w+)"), "type"),
    (re.compile(r"^\s*export\s+(?:const|let|var)\s+(\w+)\s*[=:]"), "const"),
    (re.compile(r"^\s*(?:const|function)\s+([A-Z][A-Za-z0-9]*[a-z][A-Za-z0-9]*)\s*[=(]"), "component"),
    (re.compile(r"^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)"), "fn"),
]
LUA_PATTERNS = [
    (re.compile(r"^\s*local\s+function\s+([\w.:]+)"), "fn"),
    (re.compile(r"^\s*function\s+([\w.:]+)"), "fn"),
    (re.compile(r"^\s*(?:local\s+)?(\w+)\s*=\s*function"), "fn"),
    (re.compile(r"^\s*(?:local\s+)?(\w+)\s*=\s*\w+\.\w+"), "module"),
]
GO_PATTERNS = [
    (re.compile(r"^func\s+(?:\([^)]*\)\s*)?(\w+)"), "fn"),
    (re.compile(r"^type\s+(\w+)\s+(struct|interface)"), "type"),
]
RUST_PATTERNS = [
    (re.compile(r"^\s*pub(?:\([^)]*\))?\s+(?:async\s+)?fn\s+(\w+)"), "fn"),
    (re.compile(r"^\s*(?:pub\s+)?(?:struct|enum|trait)\s+(\w+)"), "type"),
    (re.compile(r"^\s*impl\s+(?:<[^>]*>\s*)?(\w+)"), "impl"),
    (re.compile(r"^\s*fn\s+(\w+)"), "fn"),
]
JAVA_PATTERNS = [
    (re.compile(r"^\s*(?:public|private|protected|internal)?\s*(?:static\s+)?(?:final\s+)?(?:class|interface|enum|object|record)\s+(\w+)"), "type"),
    (re.compile(r"^\s*(?:public|private|protected|internal)\s+(?:static\s+)?[\w<>\[\],.\s]+\s+(\w+)\s*\("), "fn"),
]
RUBY_PATTERNS = [
    (re.compile(r"^\s*(?:def|class|module)\s+([\w:]+)"), "def"),
]
PHP_PATTERNS = [
    (re.compile(r"^\s*(?:public|private|protected|static|\s)*function\s+(\w+)"), "fn"),
    (re.compile(r"^\s*(?:abstract\s+|final\s+)?(?:class|interface|trait)\s+(\w+)"), "type"),
]
SWIFT_PATTERNS = [
    (re.compile(r"^\s*(?:public|private|internal|open)?\s*(?:final\s+)?(?:class|struct|enum|protocol|extension)\s+(\w+)"), "type"),
    (re.compile(r"^\s*(?:public|private|internal|open)?\s*func\s+(\w+)"), "fn"),
]
CSHARP_PATTERNS = [
    (re.compile(r"^\s*(?:public|private|protected|internal)?\s*(?:sealed\s+|abstract\s+|static\s+)*(?:class|interface|enum|record|struct)\s+(\w+)"), "type"),
    (re.compile(r"^\s*(?:public|private|protected|internal)\s+(?:static\s+)?[\w<>\[\],\s]+\s+(\w+)\s*\("), "fn"),
]
PATTERNS = {
    "ts": TS_PATTERNS, "tsx": TS_PATTERNS, "js": TS_PATTERNS, "jsx": TS_PATTERNS,
    "lua": LUA_PATTERNS, "luau": LUA_PATTERNS, "go": GO_PATTERNS, "rs": RUST_PATTERNS,
    "java": JAVA_PATTERNS, "kt": JAVA_PATTERNS, "rb": RUBY_PATTERNS, "php": PHP_PATTERNS,
    "swift": SWIFT_PATTERNS, "cs": CSHARP_PATTERNS,
}


@dataclass
class Symbol:
    line: int
    kind: str
    name: str


@dataclass
class FileInfo:
    path: str
    lang: str
    lines: int
    symbols: list[Symbol] = field(default_factory=list)


def load_gitignore(root: Path) -> list[str]:
    patterns: list[str] = []
    gitignore = root / ".gitignore"
    if gitignore.exists():
        for line in io.open(gitignore, encoding="utf-8", errors="replace"):
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("!"):
                patterns.append(line.rstrip("/"))
    return patterns


def ignored(rel: str, rel_dir: str, patterns: list[str]) -> bool:
    parts = rel.split("/")
    for part in parts[:-1]:
        if part in IGNORED_DIRS:
            return True
    joined = rel_dir + "/" if rel_dir else ""
    for pat in patterns:
        if "/" in pat:
            if fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(rel, pat + "/*"):
                return True
        else:
            if any(fnmatch.fnmatch(part, pat) for part in parts):
                return True
            if joined and fnmatch.fnmatch(joined.rstrip("/"), pat):
                return True
    return False


def python_symbols(text: str) -> list[Symbol]:
    out: list[Symbol] = []
    try:
        tree = ast.parse(text)
    except SyntaxError:
        for i, line in enumerate(text.splitlines(), 1):
            m = re.match(r"^\s*(?:class|def|async\s+def)\s+(\w+)", line)
            if m:
                kind = "class" if "class" in line else "fn"
                out.append(Symbol(i, kind, m.group(1)))
        return out

    def walk(node: ast.AST, depth: int) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.ClassDef):
                out.append(Symbol(child.lineno, "class", child.name))
                if depth < 1:
                    walk(child, depth + 1)
            elif isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                prefix = "  ." if depth and isinstance(node, ast.ClassDef) else ""
                out.append(Symbol(child.lineno, "fn", prefix + child.name))
                if depth < 1:
                    walk(child, depth + 1)
            elif depth == 0:
                walk(child, depth)

    walk(tree, 0)
    return out


def regex_symbols(text: str, lang: str) -> list[Symbol]:
    out: list[Symbol] = []
    seen: set[tuple[int, str]] = set()
    for i, line in enumerate(text.splitlines(), 1):
        if len(line) > 300:
            continue
        for pattern, kind in PATTERNS.get(lang, []):
            m = pattern.match(line)
            if m:
                name = m.group(1)
                key = (i, name)
                if key not in seen:
                    seen.add(key)
                    out.append(Symbol(i, kind, name))
                break
    return out


def scan(root: Path, focus: str | None) -> list[FileInfo]:
    patterns = load_gitignore(root)
    files: list[FileInfo] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS and not d.startswith(".")]
        for filename in filenames:
            ext = Path(filename).suffix.lower()
            lang = LANG_BY_EXT.get(ext)
            if not lang:
                continue
            full = Path(dirpath) / filename
            rel = full.relative_to(root).as_posix()
            rel_dir = os.path.dirname(rel)
            if ignored(rel, rel_dir, patterns):
                continue
            try:
                if full.stat().st_size > MAX_FILE_BYTES:
                    continue
                text = io.open(full, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            info = FileInfo(path=rel, lang=lang, lines=text.count("\n") + 1)
            info.symbols = python_symbols(text) if lang == "py" else regex_symbols(text, lang)
            files.append(info)
    return files


def focus_hits(files: list[FileInfo], needle: str) -> tuple[list[str], list[FileInfo]]:
    low = needle.lower()
    path_hits = [f for f in files if low in f.path.lower()]
    symbol_hits = [
        f for f in files
        if f not in path_hits and any(low in s.name.lower() for s in f.symbols)
    ]
    return [f.path for f in path_hits], symbol_hits


def estimate_tokens(parts: list[str]) -> int:
    return len("\n".join(parts)) // 4


def render_structure(files: list[FileInfo], root: Path) -> list[str]:
    dirs: dict[str, dict[str, int]] = {}
    for info in files:
        d = os.path.dirname(info.path) or "."
        bucket = dirs.setdefault(d, {})
        bucket[info.lang] = bucket.get(info.lang, 0) + 1
    out = ["## structure"]
    for d in sorted(dirs):
        langs = " ".join(f"{k}:{v}" for k, v in sorted(dirs[d].items()))
        out.append(f"{d}/  {langs}")
    return out


def render(files: list[FileInfo], root: Path, args: argparse.Namespace) -> list[str]:
    total_lines = sum(f.lines for f in files)
    header = (
        f"# repo map: {root.name or root} · {len(files)} files · {total_lines} lines"
    )
    parts = [header]

    if args.focus:
        low = args.focus.lower()
        path_hits, symbol_files = focus_hits(files, args.focus)
        parts.append(f"## focus: {args.focus}")
        parts.append("### path hits")
        parts.extend(f"{p}" for p in path_hits[: args.limit] or ["(none)"])
        parts.append("### symbol hits")
        shown = 0
        for info in symbol_files:
            hits = [s for s in info.symbols if low in s.name.lower()]
            for s in hits[: args.symbols_per_file]:
                parts.append(f"{info.path}:{s.line}: {s.kind} {s.name}")
                shown += 1
                if shown >= args.limit * 3:
                    break
            if shown >= args.limit * 3:
                break
        if shown == 0:
            parts.append("(none)")
        return parts

    parts.extend(render_structure(files, root))
    parts.append("## symbols")
    ranked = sorted(files, key=lambda f: (-len(f.symbols), f.lines, f.path))
    budget = args.limit
    for info in ranked[: budget]:
        parts.append(f"{info.path} ({info.lines}L, {info.lang})")
        for s in info.symbols[: args.symbols_per_file]:
            parts.append(f"  {s.line} {s.kind} {s.name}")
        extra = len(info.symbols) - args.symbols_per_file
        if extra > 0:
            parts.append(f"  … +{extra} more")
    if len(ranked) > budget:
        parts.append(f"… {len(ranked) - budget} more files (raise --limit)")

    # trim from the end until the token estimate fits the budget
    while len(parts) > 3 and estimate_tokens(parts) > args.max_tokens:
        parts.pop()
    return parts


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Compact symbol map for agent context budgets.")
    ap.add_argument("path", nargs="?", default=".", help="directory to map")
    ap.add_argument("--limit", type=int, default=40, help="max files in the symbols section")
    ap.add_argument("--max-tokens", type=int, default=4000, help="token ceiling (chars/4)")
    ap.add_argument("--symbols-per-file", type=int, default=20)
    ap.add_argument("--focus", default=None, help="symbol or path substring; prints hits with line numbers")
    ap.add_argument("--exclude", default="", help="comma-separated directory names to skip")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    for extra in filter(None, (d.strip() for d in args.exclude.split(","))):
        IGNORED_DIRS.add(extra)

    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    files = scan(root, args.focus)
    if args.json:
        payload = {
            "root": str(root),
            "files": [
                {
                    "path": f.path,
                    "lang": f.lang,
                    "lines": f.lines,
                    "symbols": [{"line": s.line, "kind": s.kind, "name": s.name} for s in f.symbols],
                }
                for f in files
            ],
            "estimate_tokens": 0,
        }
        text = json.dumps(payload, indent=1)
        payload["estimate_tokens"] = len(text) // 4
        text = json.dumps(payload, indent=1)
        print(text)
        return 0

    parts = render(files, root, args)
    print("\n".join(parts))
    print(f"\n~{estimate_tokens(parts)} tokens (estimate)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
