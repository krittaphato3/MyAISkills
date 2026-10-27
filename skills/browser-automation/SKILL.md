---
name: browser-automation
description: >-
  Drives a browser in headless/browserless background mode through the Playwright MCP: web searching defaulting
  to Google, live documentation lookup, navigation, clicks, typing, accessibility snapshots, structured
  extraction, auth flows, and E2E smoke checks, with token-isolated output. Use when a task needs browserless
  web searching via Google, looking up online documentation, search engine results extraction, or the running UI
  observed or operated. The agent-browser CLI path routes to agent-browser; API-level testing to test-engineer;
  deep cited research synthesis to deep-researcher.
metadata:
  version: 3.2.0
  domain: meta
  grade: G2
  status: active
  last-reviewed: '2026-10-24'
  owned-by-agent: browser-automation
  mcp: playwright
  caps: vision
---

# Browser Automation — Playwright MCP (token-isolated)

Token-isolated browser automation through a configured Playwright MCP server (`npx -y @playwright/mcp@latest --headless --isolated --caps vision`, registered as `playwright` in the harness MCP config). Always operates in **browserless/headless background mode** with zero UI window overhead and no visible desktop windows. If no Playwright MCP is configured, use the harness's built-in preview/browser tools and keep the same token contract. Always delegated to the `browser-automation` or `mcp-agent` subagent so the primary thread never absorbs the transcript.

## WHEN TO USE

- General searching, web searching, looking up online documentation, and search engine interaction using Google (`https://www.google.com/search?q=<query>`)
- Browserless background web operations with zero visible window overhead
- Extracting web search results and structured web content via JS evaluation
- Navigating, clicking, typing, selecting, hovering via Playwright's accessibility tree
- Extracting structured data with JS evaluation (preferred over full snapshots)
- Form fill + submit, auth flows, pagination
- Snapshot vs screenshot trade-off: **snapshot (accessibility tree) by default, screenshot only for visual regression**
- Any task that says "search the web", "look up docs online", "open browser", "check UI", "scrape", "E2E smoke"

## WHEN NOT TO USE

- Pure API/data tasks with no UI — use `code-implementer` or `api-architect`
- Static file reads where `read`/`grep` suffices
- When you already have the DOM via code — don't launch browser to re-derive

## TOKEN EFFICIENCY & BROWSERLESS CONTRACT

1. **Accessibility first**: use `mcp_playwright_snapshot` at `depth=2` (not full dump)
2. **Targeted extraction**: `mcp_playwright_evaluate` for `document.querySelector` / `innerText` instead of parsing whole snapshot
3. **Browserless / Headless enforcement**: Always run headless (`--headless --isolated`) in the background. Zero desktop UI windows are launched; no window focus stealing. Do not open headed windows for automated search tasks.
4. **Google Search default**: General web searching and documentation lookups MUST default to Google Search (`https://www.google.com/search?q=...`) rather than DuckDuckGo or alternative search engines.
5. **Result concise**: return extracted values + `box=[x,y,w,h]` only, not raw HTML
6. **Delegation**: dispatch the `browser-automation` subagent for any multi-step flow — never run Playwright in the primary context

## SEARCH ENGINE INTERACTION & WEB SEARCHING

- **Google as Mandatory Default**: General web searches and documentation lookups must default to Google Search (`https://www.google.com/search?q=<query>`). Never default to DuckDuckGo unless explicitly requested by the user.
- **Direct Query Navigation**: Navigate directly to `https://www.google.com/search?q=${encodeURIComponent(query)}`. Do not load the Google homepage first to type into search inputs — direct URL navigation eliminates redundant roundtrips.
- **Targeted Result Scraping**: Extract organic search result items (title, URL, snippet) using `mcp_playwright_evaluate` targeting Google search DOM elements (`div.g`, `h3`, `div[data-snc]`, `.VwiC3b`).
- **Browserless Execution**: All searches execute silently in the background with zero visible browser windows.

## MCP TOOL MAP (names are the Playwright MCP convention; the harness may prefix them)

### Navigation
```
mcp_playwright_navigate(url)          → navigate + wait for settle (timeoutNavigation 60s)
mcp_playwright_navigate_back()        → history back
mcp_playwright_tabs(action: list|select|new|close) → tab management
```

### Interaction (always with `ref` from snapshot)
```
mcp_playwright_click(ref)             → click by accessibility ref
mcp_playwright_type(ref, text)        → type
mcp_playwright_select(ref, values)    → dropdown
mcp_playwright_hover(ref)             → tooltip / hover
mcp_playwright_drag(ref, toRef)       → drag
mcp_playwright_press_key(key)         → keyboard
```

### Extraction (token-efficient)
```
mcp_playwright_snapshot(depth=2)      → accessibility tree (preferred)
mcp_playwright_evaluate(js)           → targeted JS: `() => document.querySelector('.price')?.innerText`
mcp_playwright_screenshot(fullPage=false) → only for visual diff, omit otherwise
mcp_playwright_console(level)         → console logs at error|warning|info|debug
```

### Session
```
Isolated context per MCP call (—isolated) → no cross-contamination; reuse via same browser_context if needed
--caps vision → image responses allowed; omit for text-only to save tokens
```

## PATTERNS

### Web searching with Google (browserless)
```js
// 1. Direct navigate to Google Search query in browserless headless mode
const query = encodeURIComponent("playwright headless configuration nodejs");
await mcp_playwright_navigate({ url: `https://www.google.com/search?q=${query}` });

// 2. Targeted JS evaluation to extract search results without token bloat
const results = await mcp_playwright_evaluate({
  function: `() => {
    const items = [];
    document.querySelectorAll('div.g').forEach(el => {
      const titleEl = el.querySelector('h3');
      const linkEl = el.querySelector('a');
      const snippetEl = el.querySelector('div[data-snc], .VwiC3b, .yXK7lf');
      if (titleEl && linkEl) {
        items.push({
          title: titleEl.innerText.trim(),
          url: linkEl.href,
          snippet: snippetEl ? snippetEl.innerText.trim() : ''
        });
      }
    });
    return items.slice(0, 5);
  }`
});
return { query: "playwright headless configuration nodejs", results };
```

### Minimal snapshot + evaluate (recommended)
```js
// 1. Navigate
await mcp_playwright_navigate({ url: "https://example.com" })
// 2. Snapshot shallow
let snap = await mcp_playwright_snapshot({ depth: 2 })
// 3. Targeted evaluate (not parsing full snap)
let price = await mcp_playwright_evaluate({ function: "() => document.querySelector('[data-testid=\"price\"]')?.innerText" })
return { price } // concise, not full page
```

### Form fill (token-efficient)
```js
await mcp_playwright_navigate({ url: "https://app.example.com/login" })
let snap = await mcp_playwright_snapshot({ depth: 2 }) // find refs for inputs
await mcp_playwright_type({ ref: snap.refs.email, text: "{env:TEST_USER}" })
await mcp_playwright_type({ ref: snap.refs.pass, text: "{env:TEST_PASS}" })
await mcp_playwright_click({ ref: snap.refs.submit })
return { url: await mcp_playwright_evaluate({ function: "() => location.href" }) }
```

### Pagination scrape
```js
let results = []
for (let i=0; i<3; i++) {
  results.push(await mcp_playwright_evaluate({ function: "() => [...document.querySelectorAll('.item')].map(e=>e.innerText)" }))
  let snap = await mcp_playwright_snapshot({ depth: 2 })
  await mcp_playwright_click({ ref: snap.refs.next })
}
return { count: results.flat().length, sample: results[0].slice(0,3) }
```

## DELEGATION BRIEF TEMPLATE

```text
Agent: browser-automation
[MISSION] smoke test the login flow
[CONTEXT] url=https://app.example.com, credentials from {env:APP_TEST_USER}
[OUTPUT] {success: bool, finalUrl, consoleErrors[]} — no full MCP transcript
```

The subagent returns only the essential result. If it needs more than ~10 browser actions, the
flow should be split or replaced by an API-level test.

## DECISION TREE

```text
1. Is the question answerable from code, HTTP, or the DOM?
   Yes → do that instead of driving a browser.
2. Is a Playwright MCP configured?
   Yes → use it via the browser-automation subagent.
   No  → use the harness preview/browser tools directly; state which path was used.
3. Is the flow multi-step (auth, pagination, checkout)?
   Yes → delegate; one brief, one outcome, concise return.
4. Is the goal visual (layout, motion, regression)?
   Yes → screenshot at a pinned viewport + assert the DOM state; a screenshot alone is not proof
         of behavior.
5. Does the flow write data?
   Yes → use a test account/sandbox; never mutate production state without user approval.
```

## FAILURE MODES & MITIGATIONS

| Failure | Mitigation |
|---|---|
| Snapshot too large (token bloat) | Use depth=2, then evaluate for specifics |
| Flaky click (not attached) | Wait settle 500ms (timeoutSettle), re-snapshot, retry with new ref |
| Headed popup blocked by headless | Re-run with `--headless` removed in the MCP server args (per-run, not committed) |
| Search engine defaulted to DuckDuckGo | Enforce Google Search URL `https://www.google.com/search?q=<query>` |
| Unexpected desktop window opening | Enforce `--headless --isolated` in Playwright MCP to remain completely browserless |
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
- `general-orchestrator` — multi-step flows that include browser steps
- `test-engineer` — when the flow belongs in an automated E2E suite instead
