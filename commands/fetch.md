---
description: Fetch a URL and extract readable content — works without native WebFetch
argument-hint: <url> [what to extract]
---

Fetch and read a page with the local fetcher (`web-search` skill):

1. `node tools/webfetch.mjs <url> --max-chars=8000` — follows redirects, decodes
   compression/charset, converts HTML into compact text with headings, lists, code, and links.
2. Narrow large pages: `--focus=<term>` keeps matching lines with two lines of context;
   `--raw` skips extraction; `--json` returns `{url,status,title,content,truncated}` and is the
   right mode for API endpoints.
3. For multi-source synthesis with citations, hand the extracted text to `deep-researcher`
   rather than pasting raw pages into the main thread.
4. Quote only what the fetch returned. A non-2xx status, empty body, or JS-only page is reported
   as a limitation (retry with the browser path when the content truly matters).

Target: $ARGUMENTS
