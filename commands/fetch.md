---
description: Fetch a URL and extract readable content — prioritizes ZCode native WebFetch
argument-hint: <url> [what to extract]
---

Fetch and read a page with the fetcher ladder (`web-search` skill):

1. On ZCode (Primary Basis):
   Use the native harness `WebFetch` tool:
   `WebFetch(url="<url>", prompt="<what to extract or summarize>")`
   Extracts targeted information via a fast model, caches for 15 minutes, and prevents raw HTML context bloat.

2. Non-ZCode harnesses or specialized CLI workflows (Portable Fallback):
   `node tools/webfetch.mjs <url> --max-chars=8000` — follows redirects, decodes
   compression/charset, and renders compact text. Use on ZCode only when wiser (e.g. CLI piping,
   inspecting raw markup, or querying raw JSON endpoints with `--json`).
   • Narrow large pages: `--focus=<term>` keeps matching lines with two lines of context;
     `--raw` skips extraction; `--json` returns `{url,status,title,content,truncated}`.

3. For multi-source synthesis with citations, coordinate through `deep-researcher`.
4. Quote only what the fetch returned. Report non-2xx status, empty body, or JS-only pages
   as limitations (retry with `browser-automation` via Playwright MCP if essential).

Target: $ARGUMENTS
