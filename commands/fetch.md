---
description: Fetch a URL and extract readable content — uses native WebFetch whenever available
argument-hint: <url> [what to extract]
---

Fetch and read a page with the fetcher ladder (`web-search` skill):

1. Native Harness WebFetch (Default on ZCode):
   Invoke the native `WebFetch` tool directly:
   `WebFetch(url="<url>", prompt="<what to extract or summarize>")`
   Extracts targeted information via a fast model, caches for 15 minutes, and prevents raw HTML context bloat.

2. Fallback Fetcher (Foreign harnesses or local CLI scripting):
   `node tools/webfetch.mjs <url> --max-chars=8000` — follows redirects, decodes
   compression/charset, and renders compact text. Use when on non-ZCode environments or when
   piping output directly into local scripts or inspecting raw JSON with `--json`.
   • Narrow large pages: `--focus=<term>` keeps matching lines with two lines of context;
     `--raw` skips extraction; `--json` returns `{url,status,title,content,truncated}`.

3. For multi-source synthesis with citations, coordinate through `deep-researcher`.
4. Quote only what the fetch returned. Report non-2xx status, empty body, or JS-only pages
   as limitations (retry with `browser-automation` via Playwright MCP if essential).

Target: $ARGUMENTS
