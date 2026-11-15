---
description: Fetch a URL and extract readable content with automatic Playwright escalation for JS-rendered pages
argument-hint: <url> [what to extract]
---

Fetch and extract documentation from a URL using the resilient fetch ladder (`web-search` skill):

1. Native Harness WebFetch (Tier 1 Default):
   Invoke the native `WebFetch` tool directly:
   `WebFetch(url="<url>", prompt="<what to extract or summarize>")`
   Extracts targeted information via a fast model, caches for 15 minutes, and prevents raw HTML context bloat.

2. Playwright MCP (Tier 2 Escalation for JS SPAs, React/Vue Docs, and Cloudflare):
   If `WebFetch` returns blank content, "enable JavaScript", HTTP 403, or the page is a client-side SPA:
   Invoke Playwright MCP directly:
   `mcp_playwright_browser_navigate(url="<url>")`
   Extract readable content with `mcp_playwright_browser_evaluate`:
   `() => (document.querySelector('article, main, .content, #content') || document.body).innerText.slice(0, 8000)`
   Or inspect accessibility structure with `mcp_playwright_browser_snapshot(depth=2)`.

3. In-App Browser Use (Tier 3 for ZCode Desktop In-App Browser):
   If visible desktop browser interaction or localhost HTTP testing is needed:
   Load `browser-use:control-browser` via `mcp_node_repl_js` (`iab`).

4. Portable Fallback Fetcher (Tier 4 for foreign environments lacking native/MCP tools):
   `node tools/webfetch.mjs <url> --max-chars=8000` (add `--focus=<term>` to narrow content).

5. Quote only what the fetch returned. Attribute all facts with the full URL link: `[Source Title](<url>)`.

Target: $ARGUMENTS
