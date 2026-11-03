---
name: web-search
description: >-
  Searches the web, extracts online documentation, and investigates external facts with a resilient 4-tier
  search and reading ladder. Prioritizes in-app native WebFetch for zero-token-bloat reading and native WebSearch
  for discovery; seamlessly escalates to Playwright MCP for anti-bot immune headless browser searching (Bing/Google)
  and JS-rendered SPAs; integrates in-app Browser Use (control-browser) for ZCode desktop in-app browser (iab)
  verification; and retains tools/web_search.mjs and tools/webfetch.mjs as portable CLI fallbacks. Use whenever a task
  requires gathering online information, reading library API docs, researching technical problems, or verifying URLs.
  Multi-source deep research synthesis routes to deep-researcher; complex UI interactions route to browser-automation.
metadata:
  version: 4.0.0
  domain: meta
  grade: G2
  status: active
  last-reviewed: '2026-11-03'
  owned-by-agent: browser-automation
---

# Web Search, Fetch, and Online Research Ladder

This skill establishes the comprehensive, multi-tier search and online retrieval architecture for ZCode and external harnesses. It eliminates common search and research flaws (such as anti-bot blocks, empty JavaScript pages, unhandled provider errors, and context window bloat) by orchestrating in-app built-in tools, Playwright MCP, in-app Browser Use, and portable CLI fallbacks.

## WHEN TO USE

- Searching the web for technical documentation, library APIs, framework updates, or RFCs.
- Researching bugs, troubleshooting error stack traces, and gathering community solutions from GitHub, StackOverflow, or blogs.
- Reading and extracting facts from external URLs with token efficiency.
- Inspecting JavaScript-heavy Single Page Applications (SPAs) or Cloudflare-protected documentation portals.
- Viewing or operating web pages in ZCode Desktop's In-App Browser (`iab`).
- Verifying whether a library, tool, or syntax still exists or has changed in modern releases (`source-driven-development`).

## WHEN NOT TO USE

- The local repository or workspace already contains the answer — grep/read local files first.
- Multi-source deep research synthesis with formal source verification ledger — coordinate via `deep-researcher` agent.
- Complex multi-step web interaction flows, form submissions, or visual UI testing — coordinate via `browser-automation` agent.

## DECISION TREE

```text
User asks to search, fetch, or research online:
  │
  ├─► [TASK IS URL EXTRACTION / READING A PAGE]
  │     │
  │     ├─► Step 1: Call native WebFetch(url, prompt)
  │     │     │
  │     │     ├─► Success: Extract markdown answer, quote facts with cited URL. Done.
  │     │     │
  │     │     └─► Fails (HTTP 403, Cloudflare, blank JS-only container, or login required):
  │     │           ▼
  │     ├─► Step 2: Escalate to Playwright MCP (mcp_playwright_browser_navigate)
  │     │     │     Run mcp_playwright_browser_evaluate to extract main article text,
  │     │     │     or mcp_playwright_browser_snapshot(depth=2). Done.
  │     │     │
  │     │     └─► If user requested in-app visible browsing or local HTTP testing:
  │     │           ▼
  │     └─► Step 3: Use In-App Browser Use (browser-use:control-browser via mcp_node_repl_js).
  │
  └─► [TASK IS SEARCHING / DISCOVERING INFORMATION]
        │
        ├─► Step 1: Try native WebSearch(query)
        │     │
        │     ├─► Success: Extract candidate URLs and summaries. Proceed to fetch.
        │     │
        │     └─► Fails (e.g. "openai-compatible does not encode provider-native WebSearch"):
        │           ▼
        ├─► Step 2: Escalate to Playwright MCP Headless Browser Search
        │     │     Navigate to `https://www.bing.com/search?q=<query>`
        │     │     (Bing avoids headless 429 sorry CAPTCHAs that Google triggers).
        │     │     Evaluate structured results: title, url, snippet via document.querySelectorAll.
        │     │     Proceed to fetch top candidates.
        │     │
        └─► Step 3: Portable CLI Fallback (when MCP is disconnected or in foreign shell)
                    Execute `node tools/web_search.mjs "<query>"`
                    (Auto-queries Web with Bing fallback, GitHub, npm, StackOverflow).
```

## THE 4-TIER SEARCH & FETCH HIERARCHY

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ TIER 1: IN-APP BUILT-IN NATIVE TOOLS (Zero-overhead, Fast, Token-Isolated)  │
│ • Reading URLs: WebFetch(url="...", prompt="...")                           │
│   Converts page to markdown, synthesizes targeted answer, caches for 15m.   │
│ • Searching: WebSearch(query="...")                                         │
│   Native provider search. Note: if active provider is openai-compatible,     │
│   WebSearch returns an encoding error; immediately escalate to Tier 2.      │
├─────────────────────────────────────────────────────────────────────────────┤
│ TIER 2: PLAYWRIGHT MCP (Full Headless Browser Engine, Anti-Bot Immune)      │
│ • Searching: mcp_playwright_browser_navigate to Bing Search                 │
│   https://www.bing.com/search?q=<query>                                     │
│   Use mcp_playwright_browser_evaluate to parse clean titles, URLs, snippets.│
│ • JS SPAs & Cloudflare Pages: mcp_playwright_browser_navigate to target URL │
│   Executes real client-side JavaScript, renders React/Vue DOMs, handles     │
│   redirects, extracts exact text via evaluate or snapshot(depth=2).         │
├─────────────────────────────────────────────────────────────────────────────┤
│ TIER 3: IN-APP BROWSER USE (ZCode Desktop In-App Browser `iab`)             │
│ • Load skill `browser-use:control-browser` via mcp_node_repl_js             │
│ • Drives ZCode's built-in webview tab for visible browsing, UI checks, and  │
│   localhost HTTP targets (127.0.0.1, localhost).                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ TIER 4: PORTABLE CLI FALLBACKS (Headless Scripts for Foreign Environments)   │
│ • Discover: node tools/web_search.mjs "<query>" [--type=web|github|npm|so]  │
│ • Read: node tools/webfetch.mjs <url> [--max-chars=8000] [--focus=<term>]   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## HOW TO EXECUTE

### 1. Searching the Web

#### A. In-App Built-In `WebSearch`
```json
{
  "query": "playwright browser automation best practices"
}
```
If this succeeds, use the top result URLs. If it returns `Provider API kind openai-compatible does not encode provider-native WebSearch`, immediately proceed to Playwright MCP.

#### B. Playwright MCP Headless Search (Standard Automated Fallback)
Navigate to Bing search in headless mode:
```json
{
  "url": "https://www.bing.com/search?q=playwright+browser+automation"
}
```
Then extract clean results using `mcp_playwright_browser_evaluate`:
```js
() => {
  const items = [];
  document.querySelectorAll('li.b_algo').forEach(el => {
    const a = el.querySelector('h2 a');
    const p = el.querySelector('.b_caption p, .b_snippet, .b_lineclamp');
    if (a && a.href) {
      let url = a.href;
      const uMatch = url.match(/[?&]u=a1([^&]+)/);
      if (uMatch) {
        try {
          let b64 = uMatch[1].replace(/-/g, '+').replace(/_/g, '/');
          while (b64.length % 4) b64 += '=';
          url = atob(b64);
        } catch (e) {}
      }
      items.push({
        title: a.innerText.trim(),
        url,
        snippet: p ? p.innerText.trim() : ''
      });
    }
  });
  return items.slice(0, 5);
}
```

#### C. Multi-Engine CLI Search (`tools/web_search.mjs`)
When MCP is not connected or in shell pipelines:
```bash
node tools/web_search.mjs "<query>"              # Multi-engine search with snippets
node tools/web_search.mjs "<query>" --type=npm   # Target npm registry
node tools/web_search.mjs "<query>" --type=github# Target GitHub repositories
node tools/web_search.mjs "<query>" --json       # Structured JSON output
```

### 2. Reading Web Pages & Documentation

#### A. In-App Built-In `WebFetch` (Mandatory First Choice)
Always try native `WebFetch` first:
```json
{
  "url": "https://playwright.dev/docs/intro",
  "prompt": "Extract the installation commands and core browser setup steps."
}
```
Benefits:
- Eliminates context bloat: raw HTML is stripped and summarized by a dedicated sub-model.
- 15-minute response cache across turns.

#### B. Escalating to Playwright MCP for JS-Rendered Sites & SPAs
If `WebFetch` returns an empty container, Cloudflare error, or "enable JavaScript":
1. Call `mcp_playwright_browser_navigate`:
```json
{
  "url": "https://example-spa-docs.com"
}
```
2. Extract targeted article content with `mcp_playwright_browser_evaluate`:
```js
() => {
  const main = document.querySelector('article, main, .content, #content') || document.body;
  return main.innerText.slice(0, 8000);
}
```
Or call `mcp_playwright_browser_snapshot(depth=2)` to inspect the accessibility structure.

#### C. In-App Browser Use (`browser-use:control-browser`)
For ZCode In-App Browser control:
Invoke `mcp_node_repl_js` after loading the `browser-use:control-browser` skill bootstrap.

## RESEARCH SYNTHESIS PROTOCOL (Deep Research)

When a task requires comprehensive multi-source technical investigation:
1. **Formulate targeted search queries**: Search API names, error signatures, or library versions.
2. **Retrieve sources via the Search Ladder**: Use `WebSearch` -> Playwright MCP (Bing) -> `tools/web_search.mjs`.
3. **Read top 3 authoritative sources**: Prefer official documentation, vendor release notes, or official GitHub issues.
4. **Escalate on render failure**: If a docs site is an SPA, immediately switch to Playwright MCP rather than reporting failure.
5. **Cross-validate**: Verify findings across at least 2 independent sources.
6. **Cite exact URLs**: Every quoted finding must be attributed with its live Markdown link `[Source Title](https://...)`.

## FAILURE MODES & MITIGATIONS

1. **Provider WebSearch Unsupported.** *DETECT:* `Provider API kind openai-compatible does not encode provider-native WebSearch`. *FIX:* Immediately use Playwright MCP search (`https://www.bing.com/search?q=...`) without showing errors to the user.
2. **Google Headless 429 Challenge.** *DETECT:* Navigating to Google in headless Playwright redirects to `https://www.google.com/sorry/index`. *FIX:* Default headless browser search to Bing (`https://www.bing.com/search?q=...`) which does not trigger 429 blocks in headless mode.
3. **Blank SPA / JS-Only Page.** *DETECT:* `WebFetch` returns blank or "enable JavaScript". *FIX:* Escalate to Playwright MCP (`mcp_playwright_browser_navigate`) to execute client-side JS and evaluate the DOM.
4. **Cloudflare / Bot Challenge.** *DETECT:* HTTP 403 or Cloudflare challenge in fetch. *FIX:* Use Playwright MCP with human-like navigation or in-app browser (`iab`).
5. **Hallucinated Link / Quote.** *DETECT:* Citing a URL that was not retrieved in the active session. *FIX:* Only cite URLs fetched and verified in this session.

## QUANTITATIVE RULES

- Search first, fetch at most the top 3-4 most relevant candidate URLs per subtask.
- Always include a specific `prompt` parameter in `WebFetch` calls to extract only relevant sections.
- When evaluating search results in Playwright, cap extracted results to top 5 items.
- Never output raw unprocessed HTML dumps into the main thread.
- Always report cited findings with full markdown links: `[Title](https://...)`.

## VERIFICATION GATE

- [ ] Web search was performed using the resilient search ladder (WebSearch -> Playwright MCP -> tools/web_search.mjs).
- [ ] Documentation and URLs were read using native WebFetch or Playwright MCP (never hallucinated).
- [ ] Any client-side SPA or JS-heavy page was rendered via Playwright MCP rather than abandoned.
- [ ] Every claim, version number, or code pattern is backed by an active-session citation.
- [ ] Zero unhandled provider-native search errors leaked to user output.

## REFERENCES

- Playwright MCP Server Documentation
- ZCode Desktop Browser Use Plugin (`browser-use:control-browser`)
- Local Multi-Engine Search Utility (`tools/web_search.mjs`)
- Local Portable Fetch Utility (`tools/webfetch.mjs`)
