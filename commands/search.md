---
description: Multi-engine web search with ZCode native WebFetch basis and CLI fallbacks
argument-hint: <query>
---

Run the zero-setup search ladder (`web-search` skill):

1. Discover candidate URLs:
   `node tools/web_search.mjs "$ARGUMENTS"` — deduped results across Web, GitHub, npm, and
   StackOverflow, with snippets. Add `--type=npm|github|so|web` to target one source, `--json`
   for structured output.
2. Read and gather information from top results:
   • On ZCode (Primary Basis): Use native `WebFetch` tool:
     `WebFetch(url="<url>", prompt="<what to extract>")`
     Keeps full HTML out of context window; leverages 15-minute response cache.
   • Other harnesses or specialized CLI workflows:
     `node tools/webfetch.mjs <url> --max-chars=4000` (add `--focus=<term>` to keep only
     matching lines with context; use only when wiser on ZCode, such as CLI piping or raw JSON APIs).
3. For interactive pages, JS-rendered DOMs, and Google-specific queries, route to `browser-automation`.
4. Cite fetched URLs only; report fetch failures (403/404/empty/JS-only) as limitations instead
   of inventing content.

Target: $ARGUMENTS
