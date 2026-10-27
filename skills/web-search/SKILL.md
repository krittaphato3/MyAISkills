---
name: web-search
description: >-
  Searches the web and reads external documentation with dual-track architecture: strictly prioritizes
  the native harness WebFetch tool whenever available for maximum token efficiency and built-in caching,
  paired with local CLI tools/web_search.mjs for multi-engine querying (Web, GitHub, npm, StackOverflow, Wikipedia),
  and tools/webfetch.mjs as a zero-dependency fallback only when no native tool exists. Use whenever a task requires
  gathering external information, reading library documentation, verifying repository links, or troubleshooting errors.
  Multi-source research synthesis routes to deep-researcher; Google-default browser operations route to browser-automation.
metadata:
  version: 3.2.0
  domain: meta
  grade: G2
  status: active
  last-reviewed: '2026-10-28'
  owned-by-agent: browser-automation
---

# Web Search & Fetch (Native Harness WebFetch Priority)

This skill governs web search and online documentation retrieval across environments. **Whenever the host
harness provides a native `WebFetch` tool (as ZCode does), it MUST be used instead of CLI scripts.** In most cases,
native `WebFetch` is vastly more efficient: it keeps raw HTML dumps out of the conversation context window,
uses a fast internal model to synthesize targeted answers, and automatically leverages a 15-minute response cache.

The local CLI `tools/webfetch.mjs` is strictly a portable fallback for non-ZCode harnesses lacking native web
capabilities, or for rare edge cases where local shell piping / raw byte inspection is required.

## WHEN TO USE

- Use when gathering external technical knowledge, reading library API docs, inspecting changelogs, or troubleshooting errors that the local repository cannot answer.
- **Always use the native `WebFetch` tool whenever available in the current harness.** It is the primary, default, and most efficient method to read web pages and extract facts.
- Use `tools/web_search.mjs` to discover candidate URLs across Web, GitHub, NPM, StackOverflow, and Wikipedia.
- Use `tools/webfetch.mjs` ONLY when the harness lacks a native fetch tool, or in rare edge cases where piping raw stdout to a local script is necessary.

## WHEN NOT TO USE

- The local codebase already answers the question — grep first.
- Multi-source synthesis with structured citations — `deep-researcher` (agent), which coordinates these tools.
- Google-default browser searching, interactive SPA navigation, authenticated flows, or visual regression — `browser-automation`.

## EXECUTION HIERARCHY

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. SEARCH: Discover URLs & Candidates                                       │
│    node tools/web_search.mjs "<query>" [--type=web|github|npm|so] [--json]  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. READ & GATHER INFORMATION (Strict Efficiency Rule):                      │
│    • NATIVE WEBFETCH AVAILABLE (ZCode / Native Harness) -> MANDATORY DEFAULT│
│      WebFetch(url="<url>", prompt="<what specific info to extract>")        │
│      -> Keeps full HTML out of context window; utilizes 15-min cache.       │
│                                                                             │
│    • NO NATIVE TOOL AVAILABLE (Portable Fallback) -> tools/webfetch.mjs     │
│      node tools/webfetch.mjs <url> [--max-chars=8000] [--focus=<term>]      │
│      -> Zero-dependency Node fallback for headless/minimal environments.    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. INTERACTIVE / JS-HEAVY / GOOGLE-SPECIFIC:                                │
│    • Use browser-automation via Playwright MCP in background headless mode. │
└─────────────────────────────────────────────────────────────────────────────┘
```

## HOW TO EXECUTE

### 1. Search with `tools/web_search.mjs`

```bash
node tools/web_search.mjs "<query>"              # deduped results with snippets across all sources
node tools/web_search.mjs "<query>" --type=npm   # web | github | npm | so | auto (default)
node tools/web_search.mjs "<query>" --json       # structured JSON output
```

Auto-routing inspects the query to include GitHub, NPM, or StackOverflow when technical keywords appear.

### 2. Read and Extract Content

#### A. Native Harness `WebFetch` (Mandatory First Choice)
Whenever available, call `WebFetch` directly:
```json
{
  "url": "https://example.com/docs/api",
  "prompt": "Extract the authentication requirements and curl examples."
}
```
**Why native `WebFetch` is prioritized:**
- **Zero Token Bloat**: Raw HTML, stylesheets, and scripts are stripped and processed by a dedicated lightweight model; only the concise, relevant answer enters the conversation context.
- **15-Minute Response Cache**: Repeated lookups within 15 minutes are instantaneous and zero-cost.
- **Natural Language Extraction**: Directly extracts specific sections, function signatures, or parameters from the page.

#### B. Portable Fallback `tools/webfetch.mjs`
Used only when no native tool is present, or when piping raw stream output to a shell command:
```bash
node tools/webfetch.mjs <url>                    # readable text, 8000 chars default
node tools/webfetch.mjs <url> --max-chars=3000   # token budget
node tools/webfetch.mjs <url> --focus=install    # only matching lines, with context
node tools/webfetch.mjs <url> --json             # {url,status,title,content,truncated} — for raw JSON APIs
node tools/webfetch.mjs <url> --raw              # no HTML extraction / raw markup inspection
```

## PATTERNS & BEST PRACTICES

- **Verify before citing.** A search snippet is only a lead: always fetch the URL via `WebFetch` (or `webfetch.mjs` when on a headless environment without native tools) to verify content before citing.
- **Targeted prompts for WebFetch.** Formulate specific prompts (e.g. "What parameters does method X accept?") to get concise, high-signal results.
- **API and Version checks.** Always verify library syntax against current live docs rather than relying on training memories (`source-driven-development`).
- **Error diagnostics.** Search the exact error message with `--type=so`, then fetch the accepted answer.

## FAILURE MODES & MITIGATIONS

1. **Hallucinated URL.** *DETECT:* citing a link never fetched. *FIX:* fetch first; verify HTTP 200 before quoting.
2. **Empty body / non-2xx.** *DETECT:* HTTP 403/404, bot walls, empty responses. *FIX:* report as a limitation; switch to Playwright MCP (`browser-automation`) if the content is vital.
3. **JS-only SPA pages.** *DETECT:* `WebFetch` or static fetch returns an empty container. *FIX:* route to `browser-automation` subagent to execute client-side JavaScript headlessly.
4. **Stale snippet.** *DETECT:* search snippet contradicts fetched documentation. *FIX:* the fetched document wins.

## QUANTITATIVE RULES

- Search first, fetch at most the top 3 relevant results per query.
- Make `WebFetch` prompts specific to extract only what is needed for the task.
- If native `WebFetch` is available, never fall back to `webfetch.mjs` unless shell piping or raw JSON stream inspection is required.
- Every cited URL must have been fetched during the active session.

## VERIFICATION GATE

- [ ] Results were fetched during this session (not hallucinated or recalled from memory).
- [ ] If native `WebFetch` was available in the harness, it was used instead of CLI fetchers.
- [ ] Quotes trace directly to fetched content with valid URLs.
- [ ] Failures (403, 404, JS-only) are reported as limitations with the path attempted.
