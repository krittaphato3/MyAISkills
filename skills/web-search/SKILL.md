---
name: web-search
description: "Universal high-bandwidth web search across Web, GitHub, NPM, StackOverflow, and Wikipedia with zero bot-blocking and minimal token footprint. Use whenever the user or task needs external knowledge, library documentation, repository links, bug troubleshooting, or online search."
metadata:
  version: 2.0.0
  domain: meta
  status: active
  last-reviewed: '2026-10-27'
---

# Universal Web Search Skill

This skill provides ultra-fast, zero-block search capabilities combining:
- **General Web Search**: High-relevance web search with clean snippet extraction.
- **GitHub Code & Repos**: Queries repository names, descriptions, stars, and architectures.
- **NPM Ecosystem**: Packages, versions, and descriptions.
- **StackOverflow**: Developer Q&A, error resolutions, and edge cases.
- **WebFetch Integration**: Deep page reading without HTML bloat.

## HOW TO EXECUTE SEARCH

Run the dedicated zero-token search tool via Bash:
```bash
node C:/Users/Oz/.zcode/tools/web_search.mjs "<query>"
```

### Options:
- `--type=auto`: Automatically routes based on query keywords (default).
- `--type=web`: Pure web search.
- `--type=github`: Target GitHub repositories.
- `--type=npm`: Target NPM packages.
- `--type=so`: Target StackOverflow discussions.
- `--json`: Return structured JSON array.

### Following Up on Results (Zero-Bloat Reading):
Once a search returns relevant URLs, do **not** scrape raw HTML with curl. Instead, call the built-in `WebFetch` tool:
```json
{
  "url": "https://example.com/docs",
  "prompt": "Extract the API signature for function X and its error states"
}
```
`WebFetch` converts HTML to markdown and uses a small, fast model to extract only the answer, protecting the main context window from token bloat.
