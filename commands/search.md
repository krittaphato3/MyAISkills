---
description: Multi-engine web search with native WebFetch priority and CLI fallbacks
argument-hint: <query>
---

Run the zero-setup search ladder (`web-search` skill):

1. Discover candidate URLs:
   `node tools/web_search.mjs "$ARGUMENTS"` — deduped results across Web, GitHub, npm, and
   StackOverflow, with snippets. Add `--type=npm|github|so|web` to target one source, `--json`
   for structured output.
2. Read and gather information from top results:
   • Native WebFetch Available -> MANDATORY FIRST CHOICE:
     `WebFetch(url="<url>", prompt="<what to extract>")`
     Keeps full HTML out of context window; leverages 15-minute response cache.
   • No Native WebFetch Available (Portable Fallback):
     `node tools/webfetch.mjs <url> --max-chars=4000` (add `--focus=<term>` to keep only
     matching lines with context; use only when native WebFetch is missing or for CLI piping).
3. For interactive pages, JS-rendered DOMs, and Google-specific queries, route to `browser-automation`.
4. Cite fetched URLs only; report fetch failures (403/404/empty/JS-only) as limitations instead
   of inventing content.

Target: $ARGUMENTS
