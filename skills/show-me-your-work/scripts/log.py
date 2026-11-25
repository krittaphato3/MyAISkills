#!/usr/bin/env python3
"""Append a well-formed, spreadsheet-safe row to a show-me-your-work decision TSV log.

Usage:
    python scripts/log.py <logfile> <phase> <decision> <why> <evidence> <result>
"""
from __future__ import annotations

import pathlib
import sys
from datetime import datetime, timezone

HEADER = "ts\tphase\tdecision\twhy\tevidence\tresult\n"


def sanitize_cell(value: str) -> str:
    clean = " ".join(value.replace("\t", " ").splitlines()).strip()
    if clean.startswith(("=", "+", "-", "@")):
        clean = "'" + clean
    return clean


def main(argv: list[str]) -> int:
    if len(argv) != 7:
        sys.stderr.write("usage: log.py <logfile> <phase> <decision> <why> <evidence> <result>\n")
        return 1

    logfile = pathlib.Path(argv[1])
    cells = [sanitize_cell(v) for v in argv[2:]]
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    logfile.parent.mkdir(parents=True, exist_ok=True)
    write_header = not logfile.exists() or logfile.stat().st_size == 0
    with logfile.open("a", encoding="utf-8", newline="\n") as fh:
        if write_header:
            fh.write(HEADER)
        fh.write("\t".join([ts, *cells]) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
