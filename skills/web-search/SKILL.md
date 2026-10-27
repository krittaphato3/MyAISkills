---
name: web-search
description: >-
  Searches the web and reads external documentation with dual-track architecture: prioritizes
  the native ZCode harness WebFetch tool for token-efficient information gathering and summarization,
  paired with local CLI tools/web_search.mjs for multi-engine querying (Web, GitHub, npm, StackOverflow, Wikipedia),
  and tools/webfetch.mjs as a zero-dependency fallback for other harnesses. Use whenever a task requires
  gathering external information, reading library documentation, verifying repository links, or troubleshooting errors.
  Multi-source research synthesis routes to deep-researcher; Google-default browser operations route to browser-automation.
metadata:
  version: 3.1.0
  domain: meta
  grade: G2
  status: active
  last-reviewed: '2026-10-28'
  owned-by-agent: browser-automation
---

# Web Search & Fetch (ZCode Native WebFetch Basis)

This skill governs web search and online documentation retrieval across environments. When operating
inside the **ZCode** desktop or CLI harness, the primary basis for reading and gathering information from
the web is the harness's **native `WebFetch` tool**. For external harnesses, headless environments without native
capabilities, or specialized CLI workflows, the zero-dependency local scripts (`tools/web_search.mjs` and
`tools/webfetch.mjs`) serve as the reliable fallback.

## WHEN TO USE

- Use when gathering external technical knowledge, reading library API docs, inspecting changelogs, or troubleshooting errors that the local repository cannot answer.
- Use native `WebFetch` on ZCode as the primary default for reading URLs, gathering information, and synthesizing answers without bloating the context window.
- Use `tools/web_search.mjs` to discover URLs across Web, GitHub, NPM, StackOverflow, and Wikipedia.
- Use `tools/webfetch.mjs` only when on a non-ZCode harness, or when on ZCode it is specifically wiser to do so (e.g. piping into local shell scripts, inspecting raw HTML tags/HTTP headers, or querying raw JSON endpoints with `--json`).

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
│ 2. READ & GATHER INFORMATION:                                               │
│    • ON ZCODE (Primary Basis): Use native WebFetch tool                     │
│      WebFetch(url="<url>", prompt="<what specific info to extract>")        │
│      -> Keeps full HTML out of context window; utilizes 15-min cache.       │
│                                                                             │
│    • OTHER HARNESSES OR SPECIALIZED CLI WORKFLOWS: Use webfetch.mjs         │
│      node tools/webfetch.mjs <url> [--max-chars=8000] [--focus=<term>]      │
│      -> Zero-dependency Node fallback for raw text, CLI pipelines, or JSON. │
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

#### A. ZCode Native `WebFetch` (Primary Basis)
On ZCode, invoke the `WebFetch` tool directly:
```json
{
  "url": "https://example.com/docs/api",
  "prompt": "Extract the authentication requirements and curl examples."
}
```
**Why this is the primary basis on ZCode:**
- **Context Protection**: Converted to markdown and processed by a dedicated fast model; only the focused answer is returned to the context window rather than raw page dumps.
- **15-Minute Cache**: Re-fetches within 15 minutes are instant and consume zero network overhead.
- **Natural Extraction**: Handles questions, summaries, and targeted extraction in natural language.

#### B. Local CLI `tools/webfetch.mjs` (Portable Fallback)
Kept for other harnesses without native tools, or on ZCode only when wiser:
```bash
node tools/webfetch.mjs <url>                    # readable text, 8000 chars default
node tools/webfetch.mjs <url> --max-chars=3000   # token budget
node tools/webfetch.mjs <url> --focus=install    # only matching lines, with context
node tools/webfetch.mjs <url> --json             # {url,status,title,content,truncated} — for raw JSON APIs
node tools/webfetch.mjs <url> --raw              # no HTML extraction / raw markup inspection
```

## PATTERNS & BEST PRACTICES

- **Verify before citing.** A search snippet is only a lead: always fetch the URL via `WebFetch` (or `webfetch.mjs` when wiser) to verify content before citing.
- **Targeted prompts for WebFetch.** Make prompts specific (e.g. "What parameters does method X accept?") to get concise, high-signal results.
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
- When using `webfetch.mjs`, default read budget is ≤8k characters.
- Every cited URL must have been fetched during the active session.

## VERIFICATION GATE

- [ ] Results were fetched during this session (not hallucinated or recalled from memory).
- [ ] On ZCode, native `WebFetch` was used as the primary basis for information gathering unless `webfetch.mjs` was explicitly wiser (CLI piping, raw JSON, or non-native harness).
- [ ] Quotes trace directly to fetched content with valid URLs.
- [ ] Failures (403, 404, JS-only) are reported as limitations with the path attempted.
