---
name: web-search
description: >-
  Searches the web and reads pages with zero native dependencies: the local CLIs
  `tools/web_search.mjs` (Web, GitHub, npm, StackOverflow) and `tools/webfetch.mjs`
  (redirects, compression, readable extraction, focus filter). Use whenever a task needs
  external knowledge, library documentation, repository links, or bug troubleshooting,
  including on models and harnesses that have no built-in web search or WebFetch.
  Multi-source synthesis with citations routes to deep-researcher; Google-default browser
  searching to browser-automation.
metadata:
  version: 3.0.0
  domain: meta
  grade: G2
  status: active
  last-reviewed: '2026-10-27'
  owned-by-agent: browser-automation
---

# Web Search & Fetch (no native tools required)

Both tools run on Node 18+ (this machine: v24) with zero dependencies. They exist so that a
model with only `bash` — no native web search, no WebFetch, no browser — can still search and
read the web. Run paths relative to this config root (`~/.zcode`), or use the absolute path
when the working directory is elsewhere.

## WHEN TO USE

- External knowledge, library docs, changelogs, repository links, or troubleshooting that the
  repo cannot answer.
- The harness/model has no native web search or fetch tool and the task needs one.
- A specific URL needs reading, quoting, or verifying before it is cited.

## WHEN NOT TO USE

- The repo already answers it — grep first.
- Multi-source synthesis with citations — `deep-researcher` (agent), which uses these tools too.
- Google-default browser searching, interactive pages, logged-in flows — `browser-automation`.

## HOW TO EXECUTE

### 1. Search

```bash
node tools/web_search.mjs "<query>"              # deduped results with snippets
node tools/web_search.mjs "<query>" --type=npm   # web | github | npm | so | auto (default)
node tools/web_search.mjs "<query>" --json       # structured array
```

Auto-routing adds GitHub/npm/StackOverflow results when the query looks code-, package-, or
error-related. Output is compact: title, URL, snippet — safe to paste into context.

### 2. Read the page before trusting it

```bash
node tools/webfetch.mjs <url>                    # readable text, 8000 chars default
node tools/webfetch.mjs <url> --max-chars=3000   # token budget
node tools/webfetch.mjs <url> --focus=install    # only matching lines, with context
node tools/webfetch.mjs <url> --json             # {url,status,title,content,truncated} — good for APIs
node tools/webfetch.mjs <url> --raw              # no HTML extraction
```

The fetcher follows redirects, decodes gzip/brotli and non-UTF8 charsets, strips
script/style/nav/footer, and renders headings, lists, code, and links as compact text.

### 3. Path ladder (cheapest that works)

```text
1. Native web search / WebFetch tools, if the harness actually provides them.
2. Local CLIs above — the guaranteed path on any model with bash.
3. Playwright MCP / browser tools — interactive pages, Google-default searching, auth flows.
```

Note on engines: the CLI searches DuckDuckGo's HTML endpoint because it needs no browser.
The config's Google default applies to browser search (`browser-automation`); when a Playwright
MCP is configured, use Google there.

## PATTERNS

- **Verify before citing.** A snippet is a lead, not evidence: fetch the URL and quote the
  fetched text. Never cite a URL that was not fetched successfully.
- **Budget the read.** `--max-chars` for orientation, `--focus` for one answer, `--json` for
  API payloads; paste extracted lines, not whole pages, into the main thread.
- **Version checks.** Fetch the package page or changelog before relying on an API remembered
  from training (`source-driven-development`).
- **Error messages.** Search the exact error string with `--type=so`, then fetch the accepted
  answer to confirm it matches the installed version.

## FAILURE MODES & MITIGATIONS

1. **Hallucinated URL.** *DETECT:* citing a link never fetched. *FIX:* fetch first; the gate
   below requires status + content.
2. **Empty body / non-2xx.** *DETECT:* HTTP 403/404, consent walls, empty content. *FIX:* report
   it as a limitation; try the browser path or the site's API instead of inventing content.
3. **JS-only pages.** *DETECT:* extraction returns almost nothing though the page "exists".
   *FIX:* use the Playwright path (`browser-automation`); static fetch cannot run scripts.
4. **Stale snippet.** *DETECT:* the snippet contradicts the fetched page. *FIX:* the fetch wins;
   note the discrepancy if it matters.
5. **Rate limits (GitHub API, search).** *DETECT:* 403 with rate-limit text. *FIX:* back off,
   retry once, or narrow the query; do not hammer.

## QUANTITATIVE RULES

- Search first, fetch at most the top 3 results per question; more reading is usually a worse
  question, not a need for more pages.
- Default read budget ≤8k chars; `--focus` for single-fact reads.
- Every cited URL was fetched this session; quote at most a few lines per source.
- If two sources conflict, fetch the primary one (vendor docs, changelog, RFC) to adjudicate.

## VERIFICATION GATE

- [ ] Results were fetched, not recalled; each cited URL returned HTTP 2xx this session.
- [ ] Quotes trace to fetched text; no invented links or snippets.
- [ ] Failures (403/404/empty/JS-only) are reported as limitations, with the path that was tried.

## REFERENCES

- `tools/web_search.mjs` — multi-engine search (Web/GitHub/npm/StackOverflow), zero dependencies
- `tools/webfetch.mjs` — redirect-following readable fetcher with `--focus`/`--json`
- `deep-researcher` (agent) — multi-source synthesis on top of these tools
- `browser-automation` — Playwright MCP path for interactive or Google-default searching
- `source-driven-development` — verify APIs against current docs before using them
