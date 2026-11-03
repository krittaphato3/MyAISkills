---
name: browser-automation
description: >-
  Drives a browser in headless/browserless background mode through the Playwright MCP: resilient web searching
  via Bing/Google, live documentation lookup, navigation, clicks, typing, accessibility snapshots, structured
  extraction, auth flows, and E2E smoke checks, with token-isolated output. Use when a task needs browserless
  web searching, looking up online documentation, search engine results extraction, or the running UI
  observed or operated. The agent-browser CLI path routes to agent-browser; API-level testing to test-engineer;
  deep cited research synthesis to deep-researcher.
metadata:
  version: 4.0.0
  domain: meta
  grade: G2
  status: active
  last-reviewed: '2026-11-03'
  owned-by-agent: browser-automation
  mcp: playwright
  caps: vision
---

# Browser Automation — Playwright MCP (token-isolated)

Token-isolated browser automation through a configured Playwright MCP server (`npx -y @playwright/mcp@latest --headless --isolated --caps vision`, registered as `playwright` in the harness MCP config). Always operates in **browserless/headless background mode** with zero UI window overhead and no visible desktop windows. If no Playwright MCP is configured, use the harness's built-in preview/browser tools (`browser-use:control-browser` for ZCode In-App Browser `iab`) or native `WebFetch`/`WebSearch` (`web-search` skill). Always delegated to the `browser-automation` or `mcp-agent` subagent so the primary thread never absorbs the transcript.

## WHEN TO USE

- Resilient web searching and search engine result extraction (Bing search `https://www.bing.com/search?q=<query>` by default to bypass headless Google 429 CAPTCHAs, or Google search with automated Bing fallback).
- Browserless background web operations with zero visible window overhead.
- Extracting web search results and structured web content via targeted JS evaluation.
- Reading and navigating JavaScript-heavy Single Page Applications (SPAs, React/Vue docs) where static `WebFetch` returns blank pages.
- Navigating, clicking, typing, selecting, hovering via Playwright's accessibility tree.
- Extracting structured data with JS evaluation (preferred over full snapshots).
- Form fill + submit, auth flows, pagination.
- Snapshot vs screenshot trade-off: **snapshot (accessibility tree) by default, screenshot only for visual regression**.
- Any task that says "search the web with browser", "look up docs online with browser", "open browser", "check UI", "scrape", "E2E smoke".

## WHEN NOT TO USE

- Pure API/data tasks with no UI — use `code-implementer` or `api-architect`.
- Static documentation where in-app native `WebFetch` succeeds — prefer `WebFetch` for speed and caching.
- When you already have the DOM via code — don't launch browser to re-derive.

## TOKEN EFFICIENCY & BROWSERLESS CONTRACT

1. **Accessibility first**: use `mcp_playwright_snapshot` at `depth=2` (not full dump).
2. **Targeted extraction**: `mcp_playwright_evaluate` for `document.querySelector` / `innerText` instead of parsing whole snapshot.
3. **Browserless / Headless enforcement**: Always run headless (`--headless --isolated`) in the background. Zero desktop UI windows are launched; no window focus stealing. Do not open headed windows for automated search tasks.
4. **Resilient Search Engine Default**: Headless Google searches trigger automated 429 rate limit / CAPTCHA challenge pages (`/sorry/index`). Headless search operations MUST default to Bing (`https://www.bing.com/search?q=<query>`) which returns clean, unblocked DOM results, or fall back to Bing immediately if Google redirects to `/sorry`.
5. **Result concise**: return extracted values + `box=[x,y,w,h]` only, not raw HTML.
6. **Delegation**: dispatch the `browser-automation` subagent for any multi-step flow — never run Playwright in the primary context.
7. **Harness In-App Browser Integration**: When visible browsing or desktop webview verification is needed, integrate with `browser-use:control-browser` (`iab`).

## SEARCH ENGINE INTERACTION & WEB SEARCHING

- **Resilient Search Default**: Headless web searching defaults to Bing Search (`https://www.bing.com/search?q=<query>`). Google search redirects automated headless browser sessions to `google.com/sorry/index` with HTTP 429 bot challenges. If Google is used and encounters a sorry/challenge redirect, immediately navigate to Bing.
- **Direct Query Navigation**: Navigate directly to `https://www.bing.com/search?q=${encodeURIComponent(query)}`. Do not load the homepage first to type into search inputs — direct URL navigation eliminates redundant roundtrips.
- **Targeted Result Scraping**: Extract organic search result items (title, URL, snippet) using `mcp_playwright_evaluate` targeting Bing search DOM elements (`li.b_algo`, `h2 a`, `.b_caption p, .b_snippet`). Decode any tracking redirect parameters (`u=a1<base64>`) to return clean destination URLs.
- **Browserless Execution**: All searches execute silently in the background with zero visible desktop windows.

## CONCRETE PATTERNS

### Browserless Headless Web Search (Resilient Bing Pattern)
```js
// 1. Direct navigate to Bing Search query in browserless headless mode
const query = encodeURIComponent("playwright headless configuration nodejs");
await mcp_playwright_navigate({ url: `https://www.bing.com/search?q=${query}` });

// 2. Targeted JS evaluation to extract search results without token bloat
const results = await mcp_playwright_evaluate({
  function: `() => {
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
  }`
});
return { query: "playwright headless configuration nodejs", results };
```

### Minimal snapshot + evaluate (recommended for SPAs)
```js
// 1. Navigate to target URL
await mcp_playwright_navigate({ url: "https://example.com/docs" });
// 2. Snapshot shallow or evaluate targeted text
let content = await mcp_playwright_evaluate({
  function: "() => (document.querySelector('article, main, .content') || document.body).innerText.slice(0, 8000)"
});
return { content };
```

### Form fill (token-efficient)
```js
await mcp_playwright_navigate({ url: "https://app.example.com/login" });
let snap = await mcp_playwright_snapshot({ depth: 2 });
await mcp_playwright_type({ ref: snap.refs.email, text: "{env:TEST_USER}" });
await mcp_playwright_type({ ref: snap.refs.pass, text: "{env:TEST_PASS}" });
await mcp_playwright_click({ ref: snap.refs.submit });
return { url: await mcp_playwright_evaluate({ function: "() => location.href" }) };
```

### Pagination scrape
```js
let results = [];
for (let i = 0; i < 3; i++) {
  results.push(await mcp_playwright_evaluate({ function: "() => [...document.querySelectorAll('.item')].map(e=>e.innerText)" }));
  let snap = await mcp_playwright_snapshot({ depth: 2 });
  await mcp_playwright_click({ ref: snap.refs.next });
}
return { count: results.flat().length, sample: results[0].slice(0, 3) };
```

## DELEGATION BRIEF TEMPLATE

```text
Agent: browser-automation
[MISSION] search for modern Next.js 15 routing changes and extract top docs
[CONTEXT] use Bing search in headless mode, extract top 3 authoritative docs
[OUTPUT] {results: [{title, url, snippet}], contentSummary} — no full MCP transcript
```

The subagent returns only the essential result. If it needs more than ~10 browser actions, the
flow should be split or replaced by an API-level test.

## DECISION TREE

```text
1. Is the question answerable from code, HTTP, or the DOM?
   Yes → do that instead of driving a browser.
2. Is a Playwright MCP configured?
   Yes → use it via the browser-automation subagent (defaulting to Bing for search, or rendering SPAs).
   No  → fall back in this order: (a) the in-app browser via browser-use:control-browser;
         (b) the local CLIs: `node tools/web_search.mjs "<query>"` and `node tools/webfetch.mjs <url>`.
3. Is the flow multi-step (auth, pagination, checkout)?
   Yes → delegate; one brief, one outcome, concise return.
4. Is the goal visual (layout, motion, regression)?
   Yes → screenshot at a pinned viewport + assert the DOM state; a screenshot alone is not proof of behavior.
5. Does the flow write data?
   Yes → use a test account/sandbox; never mutate production state without user approval.
```

## FAILURE MODES & MITIGATIONS

| Failure | Mitigation |
|---|---|
| Snapshot too large (token bloat) | Use depth=2, then evaluate for specifics |
| Flaky click (not attached) | Wait settle 500ms (timeoutSettle), re-snapshot, retry with new ref |
| Headed popup blocked by headless | Re-run with `--headless` removed in the MCP server args (per-run, not committed) |
| Google Search returns 429 sorry index | Immediately navigate to Bing Search `https://www.bing.com/search?q=<query>` |
| Unexpected desktop window opening | Enforce `--headless --isolated` in Playwright MCP to remain completely browserless |
| No Playwright MCP configured | Fallback to in-app browser (`control-browser`) or CLI: `node tools/web_search.mjs` |
| Secrets in URL | Pass via `{env:VAR}` not hardcoded |
| Isolated context loses auth | Persist via `storage-state` or re-login per task |

## VERIFICATION GATE

- The MCP server (or harness preview tools) is confirmed available before the flow starts; if
  neither is available, the task is reported as blocked rather than simulated.
- The flow was actually exercised (final URL + asserted state), not just navigated.
- Snapshot depth ≤2 unless deep inspection is justified.
- No screenshot unless visual proof was requested; behavior claims carry a DOM/HTTP assertion.
- Returned payload <500 tokens and contains no secrets or full page HTML.

## REFERENCES

- Harness MCP config — server entry named `playwright` (command + `--headless --isolated`)
- `agents/browser-automation.md` and `agents/mcp-agent.md` — token-isolated executors
- Playwright MCP: `npx -y @playwright/mcp@latest --help` (caps: vision, pdf, devtools)
- `skills/web-search/SKILL.md` — the 4-tier search and fetch hierarchy
- `browser-use:control-browser` — ZCode Desktop In-App Browser (`iab`)
- `tools/web_search.mjs`, `tools/webfetch.mjs` — the portable CLI fallback
