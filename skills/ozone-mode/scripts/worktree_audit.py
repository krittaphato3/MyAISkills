#!/usr/bin/env python3
"""Read-only git worktree prune audit (cross-platform Windows/macOS/Linux).

Usage:
    python scripts/worktree_audit.py [repo-path]
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import time


def run(cmd: list[str], cwd: pathlib.Path | None = None) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    return proc.returncode, proc.stdout.strip()


def dir_size_mb(path: pathlib.Path) -> str:
    total = 0
    try:
        for entry in path.rglob("*"):
            if entry.is_file() and ".git" not in entry.parts:
                try:
                    total += entry.stat().st_size
                except OSError:
                    pass
    except OSError:
        return "?"
    if total >= 1024**3:
        return f"{total / 1024**3:.1f}G"
    return f"{max(1, total // (1024**2))}M"


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        repo = pathlib.Path(argv[1]).resolve()
    else:
        rc, out = run(["git", "rev-parse", "--show-toplevel"])
        if rc != 0 or not out:
            sys.stderr.write("not in a git repo; pass a repo path\n")
            return 1
        repo = pathlib.Path(out).resolve()

    rc, wt_out = run(["git", "worktree", "list", "--porcelain"], cwd=repo)
    if rc != 0:
        sys.stderr.write("failed to list git worktrees\n")
        return 1

    worktrees = [line[9:].strip() for line in wt_out.splitlines() if line.startswith("worktree ")]
    if not worktrees:
        return 0
    main_wt = worktrees[0]

    run(["git", "fetch", "origin", "main", "--quiet"], cwd=repo)
    rc_gh, gh_out = run(["gh", "pr", "list", "--author", "@me", "--state", "all", "--limit", "500",
                         "--json", "number,state,headRefName"], cwd=repo)
    prs = json.loads(gh_out) if rc_gh == 0 and gh_out.startswith("[") else []
    pr_by_branch = {p.get("headRefName"): f"#{p.get('number')}/{p.get('state')}" for p in prs if p.get("headRefName")}

    now = int(time.time())
    print("SIZE\tAGE\tMERGED\tDIRTY\tREMOTE\tPR\tBUCKET\tWORKTREE")

    for wt_str in worktrees:
        if wt_str == main_wt:
            continue
        wt = pathlib.Path(wt_str)
        size = dir_size_mb(wt)
        _, head = run(["git", "-C", str(wt), "rev-parse", "HEAD"])
        _, ts_str = run(["git", "-C", str(wt), "log", "-1", "--format=%ct", "HEAD"])
        head_ts = int(ts_str) if ts_str.isdigit() else 0
        age = f"{(now - head_ts) // 86400}d" if head_ts > 0 else "?"

        rc_m, _ = run(["git", "-C", str(wt), "merge-base", "--is-ancestor", head, "origin/main"])
        merged = "YES" if rc_m == 0 else "no"

        _, porc = run(["git", "-C", str(wt), "status", "--porcelain"])
        lines = [l for l in porc.splitlines() if l.strip()]
        if not lines:
            dirty = "clean"
        else:
            wip = sum(1 for l in lines if not l.startswith("??"))
            dirty = f"wip:{wip}" if wip else f"scratch:{len(lines)}"

        rc_b, branch = run(["git", "-C", str(wt), "symbolic-ref", "--quiet", "--short", "HEAD"])
        branch = branch if rc_b == 0 else ""
        if not branch:
            remote = "detached"
        else:
            rc_ref, _ = run(["git", "-C", str(wt), "show-ref", "--verify", "--quiet", f"refs/remotes/origin/{branch}"])
            if rc_ref != 0:
                remote = "no-remote"
            else:
                _, rhead = run(["git", "-C", str(wt), "rev-parse", f"origin/{branch}"])
                if rhead == head:
                    remote = "pushed"
                else:
                    _, ahead = run(["git", "-C", str(wt), "rev-list", "--count", f"origin/{branch}..HEAD"])
                    remote = f"ahead{ahead}"

        pr = pr_by_branch.get(branch, "-")
        if dirty.startswith("wip:"):
            bucket = "hold-wip"
        elif "OPEN" in pr:
            bucket = "hold-open-pr"
        elif merged == "YES" or pr != "-":
            bucket = "safe"
        else:
            bucket = "review"

        print(f"{size}\t{age}\t{merged}\t{dirty}\t{remote}\t{pr}\t{bucket}\t{wt_str}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
