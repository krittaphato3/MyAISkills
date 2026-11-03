---
description: Resilient multi-tier web search and online documentation discovery
argument-hint: <query>
---

Execute the resilient 4-tier search and retrieval ladder (`web-search` skill):

1. Search & URL Discovery:
   • Step 1A (Native In-App WebSearch):
     Try `WebSearch(query="$ARGUMENTS")`.
     If supported by active provider, uses top candidate URLs and snippets immediately.
   • Step 1B (Playwright MCP Headless Browser Search — Mandatory fallback when provider lacks native search):
     If `WebSearch` returns `Provider API kind openai-compatible does not encode provider-native WebSearch` or is unavailable:
     Use Playwright MCP to navigate headless to Bing:
     `mcp_playwright_browser_navigate(url="https://www.bing.com/search?q=" + encodeURIComponent("$ARGUMENTS"))`
     Extract structured results using `mcp_playwright_browser_evaluate`:
     `() => Array.from(document.querySelectorAll('li.b_algo')).slice(0, 5).map(el => ({ title: el.querySelector('h2 a')?.innerText, url: el.querySelector('h2 a')?.href, snippet: el.querySelector('.b_caption p, .b_snippet')?.innerText }))`
   • Step 1C (In-App Browser Use):
     If in-app visible browsing is desired, load `browser-use:control-browser` via `mcp_node_repl_js` (`iab`).
   • Step 1D (CLI Multi-Engine Fallback):
     `node tools/web_search.mjs "$ARGUMENTS"` — multi-engine search across Web (with Bing fallback), GitHub, npm, and StackOverflow.

2. Read & Gather Documentation:
   • Priority 1 (Native WebFetch):
     `WebFetch(url="<candidate_url>", prompt="<what to extract or summarize>")`
     Keeps HTML out of context, provides 15-minute response cache.
   • Priority 2 (Playwright MCP for JS-rendered SPAs / Cloudflare):
     If `WebFetch` returns blank, "enable JavaScript", 403, or needs live DOM interaction:
     `mcp_playwright_browser_navigate(url="<candidate_url>")` and evaluate text or snapshot at depth=2.
   • Priority 3 (Portable CLI Fallback):
     `node tools/webfetch.mjs <url> --max-chars=4000`

3. Cite fetched URLs only; report findings with markdown links: `[Title](https://...)`.

Target: $ARGUMENTS
