---
description: Multi-engine web search via the local CLI — works on models without native web tools
argument-hint: <query>
---

Run the zero-setup search ladder (`web-search` skill):

1. `node tools/web_search.mjs "$ARGUMENTS"` — deduped results across Web, GitHub, npm, and
   StackOverflow, with snippets. Add `--type=npm|github|so|web` to target one source, `--json`
   for structured output.
2. Read the top result before trusting it:
   `node tools/webfetch.mjs <url> --max-chars=4000` (add `--focus=<term>` to keep only
   matching lines with context).
3. Prefer native search/WebFetch tools only if the harness actually provides them; the CLIs are
   the guaranteed path on any model with bash. Google-default browser searching and interactive
   pages route to `browser-automation`.
4. Cite fetched URLs only; report fetch failures (403/404/empty/JS-only) as limitations instead
   of inventing content.

Target: $ARGUMENTS
