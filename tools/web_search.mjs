#!/usr/bin/env node
/**
 * Universal Multi-Engine Web Search Tool for ZCode
 * Provides fast, resilient, anti-bot-immune web search across:
 * - General Web (DuckDuckGo POST bypass)
 * - GitHub (Repositories, codebases, stars)
 * - NPM (Packages and documentation)
 * - StackExchange (Technical questions & answers)
 * - Wikipedia (Foundational concepts and encyclopedia)
 */
import https from 'node:https';
import zlib from 'node:zlib';

function request(url, options = {}) {
  return new Promise((resolve) => {
    try {
      const u = new URL(url);
      const isPost = options.method === 'POST';
      const postBody = options.body || '';

      const req = https.request({
        hostname: u.hostname,
        port: u.port || 443,
        path: u.pathname + u.search,
        method: options.method || 'GET',
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,application/json,*/*;q=0.8',
          'Accept-Language': 'en-US,en;q=0.9',
          'Accept-Encoding': 'gzip, deflate',
          ...options.headers
        }
      }, (res) => {
        let stream = res;
        const encoding = res.headers['content-encoding'];
        if (encoding === 'gzip') {
          stream = res.pipe(zlib.createGunzip());
        } else if (encoding === 'deflate') {
          stream = res.pipe(zlib.createInflate());
        }

        let body = '';
        stream.on('data', chunk => body += chunk);
        stream.on('end', () => resolve({ status: res.statusCode, headers: res.headers, body }));
        stream.on('error', err => resolve({ error: err.message, status: 500 }));
      });

      req.on('error', err => resolve({ error: err.message, status: 500 }));
      req.setTimeout(10000, () => {
        req.destroy();
        resolve({ error: 'timeout', status: 408 });
      });

      if (isPost && postBody) {
        req.write(postBody);
      }
      req.end();
    } catch (e) {
      resolve({ error: e.message, status: 500 });
    }
  });
}

/**
 * High-reliability Web Search via DuckDuckGo POST
 */
export async function searchWeb(query, limit = 6) {
  const postData = 'q=' + encodeURIComponent(query) + '&b=';
  const res = await request('https://html.duckduckgo.com/html/', {
    method: 'POST',
    body: postData,
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Content-Length': Buffer.byteLength(postData),
      'Referer': 'https://html.duckduckgo.com/'
    }
  });

  if (!res.body || res.status !== 200) return [];

  const results = [];
  const blocks = res.body.split('<div class="result results_links');

  for (const b of blocks.slice(1, limit + 2)) {
    if (results.length >= limit) break;
    const titleMatch = b.match(/<a rel="nofollow" class="result__a" href="([^"]+)">([\s\S]*?)<\/a>/);
    const snippetMatch = b.match(/<a class="result__snippet"[^>]*>([\s\S]*?)<\/a>/);

    if (titleMatch) {
      let url = titleMatch[1];
      const uddg = url.match(/uddg=([^&]+)/);
      if (uddg) {
        try {
          url = decodeURIComponent(uddg[1]);
        } catch (e) {}
      }

      const title = titleMatch[2]
        .replace(/<[^>]+>/g, '')
        .replace(/&#x27;/g, "'")
        .replace(/&quot;/g, '"')
        .replace(/&amp;/g, '&')
        .replace(/&#183;/g, '·')
        .trim();

      const snippet = snippetMatch
        ? snippetMatch[1]
            .replace(/<[^>]+>/g, '')
            .replace(/&#x27;/g, "'")
            .replace(/&quot;/g, '"')
            .replace(/&amp;/g, '&')
            .trim()
        : '';

      results.push({
        title,
        url,
        snippet,
        source: 'web'
      });
    }
  }
  return results;
}

/**
 * GitHub Repository Search
 */
export async function searchGitHub(query, limit = 4) {
  const url = `https://api.github.com/search/repositories?q=${encodeURIComponent(query)}&per_page=${limit}`;
  const res = await request(url, {
    headers: { 'User-Agent': 'ZCode-Search-Tool' }
  });

  if (!res.body || res.status !== 200) return [];
  try {
    const json = JSON.parse(res.body);
    return (json.items || []).slice(0, limit).map(item => ({
      title: `${item.full_name} (⭐ ${item.stargazers_count})`,
      url: item.html_url,
      snippet: item.description || '',
      source: 'github'
    }));
  } catch (e) {
    return [];
  }
}

/**
 * NPM Package Search
 */
export async function searchNPM(query, limit = 4) {
  const url = `https://registry.npmjs.org/-/v1/search?text=${encodeURIComponent(query)}&size=${limit}`;
  const res = await request(url);
  if (!res.body || res.status !== 200) return [];
  try {
    const json = JSON.parse(res.body);
    return (json.objects || []).slice(0, limit).map(obj => ({
      title: `${obj.package.name} (v${obj.package.version})`,
      url: obj.package.links.npm || `https://www.npmjs.com/package/${obj.package.name}`,
      snippet: obj.package.description || '',
      source: 'npm'
    }));
  } catch (e) {
    return [];
  }
}

/**
 * StackOverflow Q&A Search
 */
export async function searchStackOverflow(query, limit = 4) {
  const url = `https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q=${encodeURIComponent(query)}&site=stackoverflow&pagesize=${limit}`;
  const res = await request(url, {
    headers: { 'User-Agent': 'ZCode-Search-Tool' }
  });

  if (!res.body || res.status !== 200) return [];
  try {
    const json = JSON.parse(res.body);
    return (json.items || []).slice(0, limit).map(item => ({
      title: item.title.replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, '&'),
      url: item.link,
      snippet: `Score: ${item.score} | Answers: ${item.answer_count} | Tags: ${item.tags ? item.tags.join(', ') : ''}`,
      source: 'stackoverflow'
    }));
  } catch (e) {
    return [];
  }
}

/**
 * Direct Page Content Fetcher with HTML-to-Markdown/Text extraction
 */
export async function fetchPageContent(url, maxLength = 4000) {
  const res = await request(url, {
    headers: {
      'Accept': 'text/html,application/xhtml+xml,text/plain;q=0.9,*/*;q=0.8'
    }
  });

  if (!res.body || res.status >= 400) {
    return { error: `Failed to fetch: HTTP ${res.status || 'unknown'}` };
  }

  // Strip script, style, SVG, and noisy tags
  let text = res.body
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<svg[\s\S]*?<\/svg>/gi, '')
    .replace(/<nav[\s\S]*?<\/nav>/gi, '')
    .replace(/<footer[\s\S]*?<\/footer>/gi, '')
    .replace(/<header[\s\S]*?<\/header>/gi, '');

  // Convert markdown-friendly elements
  text = text
    .replace(/<h1[^>]*>([\s\S]*?)<\/h1>/gi, '\n# $1\n')
    .replace(/<h2[^>]*>([\s\S]*?)<\/h2>/gi, '\n## $1\n')
    .replace(/<h3[^>]*>([\s\S]*?)<\/h3>/gi, '\n### $1\n')
    .replace(/<li[^>]*>([\s\S]*?)<\/li>/gi, '\n- $1')
    .replace(/<p[^>]*>([\s\S]*?)<\/p>/gi, '\n\n$1\n\n')
    .replace(/<code[^>]*>([\s\S]*?)<\/code>/gi, '`$1`')
    .replace(/<pre[^>]*>([\s\S]*?)<\/pre>/gi, '\n```\n$1\n```\n')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&quot;/g, '"')
    .replace(/&#x27;/g, "'")
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/\s+/g, ' ')
    .replace(/\n\s+\n/g, '\n\n')
    .trim();

  return {
    url,
    content: text.slice(0, maxLength),
    truncated: text.length > maxLength
  };
}

/**
 * Universal Intelligent Search
 */
export async function universalSearch(query, { limit = 6, type = 'auto' } = {}) {
  const searchTasks = [];

  if (type === 'github' || (type === 'auto' && /github|repo|code|clone/i.test(query))) {
    searchTasks.push(searchGitHub(query, 3));
  }
  if (type === 'npm' || (type === 'auto' && /npm|package|node|yarn|pnpm/i.test(query))) {
    searchTasks.push(searchNPM(query, 3));
  }
  if (type === 'so' || (type === 'auto' && /error|exception|fail|how to|fix/i.test(query))) {
    searchTasks.push(searchStackOverflow(query, 3));
  }

  // Always run primary web search
  searchTasks.push(searchWeb(query, limit));

  const taskResults = await Promise.all(searchTasks);
  const combined = taskResults.flat();

  // Deduplicate by URL
  const seen = new Set();
  const deduped = [];
  for (const r of combined) {
    if (r.url && !seen.has(r.url)) {
      seen.add(r.url);
      deduped.push(r);
    }
  }

  return deduped.slice(0, limit);
}

// CLI runner
if (process.argv[1] && process.argv[1].replace(/\\/g, '/').endsWith('tools/web_search.mjs')) {
  const args = process.argv.slice(2);
  const query = args.filter(a => !a.startsWith('--')).join(' ');
  const format = args.includes('--json') ? 'json' : 'markdown';
  const typeArg = args.find(a => a.startsWith('--type='));
  const type = typeArg ? typeArg.split('=')[1] : 'auto';

  const fetchArg = args.find(a => a.startsWith('--fetch='));

  if (fetchArg) {
    const url = fetchArg.split('=')[1];
    fetchPageContent(url).then(res => {
      if (format === 'json') {
        console.log(JSON.stringify(res, null, 2));
      } else {
        console.log(`\n### Content from: ${res.url}\n`);
        console.log(res.content || res.error);
      }
    });
  } else if (!query) {
    console.error('Usage: node web_search.mjs "query" [--type=auto|web|github|npm|so] [--fetch=url] [--json]');
    process.exit(1);
  } else {
    universalSearch(query, { limit: 6, type }).then(results => {
      if (format === 'json') {
        console.log(JSON.stringify(results, null, 2));
      } else {
        console.log(`\n### Search Results: "${query}"\n`);
        if (results.length === 0) {
          console.log('No results found.');
        }
        results.forEach((r, idx) => {
          console.log(`${idx + 1}. **[${r.title}](${r.url})** \`[${r.source}]\``);
          if (r.snippet) console.log(`   ${r.snippet}`);
          console.log('');
        });
      }
    });
  }
}
