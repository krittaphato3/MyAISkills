#!/usr/bin/env python3
"""Keep the deployed catalog identical to this repo.

The harness loads skills from the deployed location while edits happen here, so the
two trees drift silently. This tool makes this repo authoritative and treats the
deployed copy as a build artifact.

Usage:
    python tools/sync_catalog.py              # report drift (exit 1 if any)
    python tools/sync_catalog.py --apply      # copy source -> deployed, backing up first
    python tools/sync_catalog.py --target DIR # override the deployed location

Exit codes: 0 in sync, 1 drift found (report mode), 2 error.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TREES = ("skills", "agents", "commands")
DEFAULT_TARGET = Path.home() / ".config" / "opencode"
BACKUP_ROOT = ROOT / "backup"
# Generated at runtime by a skill, not part of the source catalog.
IGNORE = {".graphify_version"}
# The deployed AGENTS.md must be a pointer to this repo's copy, not a second doctrine file.
POINTER_LIMIT = 4000


def source_files(rel: str) -> dict[str, Path]:
    root = ROOT / rel
    if not root.is_dir():
        return {}
    return {str(p.relative_to(root)): p for p in root.rglob("*")
            if p.is_file() and p.name not in IGNORE and "__pycache__" not in p.parts}


def compare(target: Path) -> tuple[list[str], list[str], list[str]]:
    missing, changed, extra = [], [], []
    for rel in TREES:
        src = source_files(rel)
        dst_root = target / rel
        for name, path in src.items():
            dst = dst_root / name
            if not dst.is_file():
                missing.append(f"{rel}/{name}")
            elif path.read_bytes() != dst.read_bytes():
                changed.append(f"{rel}/{name}")
        if dst_root.is_dir():
            for dst in dst_root.rglob("*"):
                if dst.is_file() and dst.name not in IGNORE and str(dst.relative_to(dst_root)) not in src:
                    extra.append(f"{rel}/{dst.relative_to(dst_root)}")
    return sorted(missing), sorted(changed), sorted(extra)


def apply(target: Path, prune: bool = False) -> list[str]:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = BACKUP_ROOT / f"deployed-{stamp}"
    written = []
    for rel in TREES:
        for name, path in source_files(rel).items():
            dst = target / rel / name
            if dst.is_file() and dst.read_bytes() == path.read_bytes():
                continue
            if dst.is_file():
                saved = backup / rel / name
                saved.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(dst, saved)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dst)
            written.append(f"{rel}/{name}")
    if prune:
        _, _, extra = compare(target)
        for item in extra:
            src = target / item
            if not src.is_file():
                continue
            saved = backup / item
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, saved)
            src.unlink()
            written.append(f"pruned {item}")
        # drop directories left empty by the prune, deepest first
        for rel in TREES:
            for d in sorted((target / rel).rglob("*"), key=lambda p: len(p.parts), reverse=True):
                if d.is_dir() and not any(d.iterdir()):
                    d.rmdir()
    if written:
        print(f"backup of changed files: {backup.relative_to(ROOT)}")
    return written


def check_pointer(target: Path) -> list[str]:
    """The deployed AGENTS.md must point here, not duplicate the doctrine."""
    problems = []
    deployed = target / "AGENTS.md"
    if not deployed.is_file():
        return problems
    size = deployed.stat().st_size
    if size > POINTER_LIMIT:
        problems.append(
            f"deployed AGENTS.md is {size} bytes (> {POINTER_LIMIT}); a second copy of the "
            f"doctrine probably reappeared — replace it with a pointer to {ROOT / 'AGENTS.md'}"
        )
    text = deployed.read_text(encoding="utf-8", errors="replace")
    if "zcode" not in text and "AGENTS.md" not in text:
        problems.append("deployed AGENTS.md does not point at the canonical file")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--prune", action="store_true",
                    help="with --apply: remove deployed files absent from the source, after backup")
    ap.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    args = ap.parse_args(argv)

    target = args.target.expanduser()
    if not target.is_dir():
        print(f"deployed directory not found: {target}", file=sys.stderr)
        return 2

    if args.apply:
        written = apply(target, prune=args.prune)
        for line in written:
            print(line if line.startswith("pruned ") else f"copied {line}")
        if not written:
            print("already in sync")
        for problem in check_pointer(target):
            print(f"WARN  {problem}")
        return 0

    missing, changed, extra = compare(target)
    pointer = check_pointer(target)
    for problem in pointer:
        print(f"WARN  {problem}")
    if not (missing or changed or extra or pointer):
        print(f"in sync with {target}")
        return 0
    for label, items in (("only in source", missing), ("differs", changed), ("only in deployed", extra)):
        if items:
            print(f"{label} ({len(items)}):")
            for item in items:
                print(f"  {item}")
    if pointer:
        return 1
    print(f"\n{len(missing) + len(changed) + len(extra)} difference(s) from {target}")
    print("run with --apply to make the deployed copy match this repo")
    return 1


if __name__ == "__main__":
    sys.exit(main())
