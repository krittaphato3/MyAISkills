#!/usr/bin/env node
/**
 * webfetch.mjs — read a URL and return clean, readable content for agents.
 *
 * Built for models/harnesses WITHOUT native WebFetch or browser tools: it only needs
 * Node 18+ and network access. Follows redirects, decodes compression and charset,
 * and converts HTML into compact markdown-ish text (headings, bullets, code, links).
 *
 * Usage:
 *   node tools/webfetch.mjs <url>                    # readable text (default 8000 chars)
 *   node tools/webfetch.mjs <url> --max-chars=3000
 *   node tools/webfetch.mjs <url> --focus=install    # keep only matching lines + context
 *   node tools/webfetch.mjs <url> --raw              # no HTML extraction
 *   node tools/webfetch.mjs <url> --json             # {url,status,contentType,title,content,truncated}
 *
 * Exit codes: 0 fetched (any HTTP status), 2 usage/network error.
 */
import zlib from 'node:zlib';

const DEFAULT_UA =
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36';

const DECODE_ENTITIES = (s) =>
  s
    .replace(/&quot;/g, '"')
    .replace(/&#x27;|&#39;|&apos;/g, "'")
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&nbsp;/g, ' ')
    .replace(/&#183;/g, '·')
    .replace(/&#x2F;/g, '/')
    .replace(/&amp;/g, '&');

const ENTITY_DECODED = (s) => {
  // numeric entities first, then the common named set
  s = s.replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(Number(n)));
  s = s.replace(/&#x([0-9a-fA-F]+);/g, (_, n) => String.fromCodePoint(parseInt(n, 16)));
  return DECODE_ENTITIES(s);
};

export function htmlToMarkdown(html) {
  let text = html
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<svg[\s\S]*?<\/svg>/gi, '')
    .replace(/<noscript[\s\S]*?<\/noscript>/gi, '')
    .replace(/<(aside|footer|nav|form)[\s\S]*?<\/\1>/gi, '');

  const titleMatch = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  const title = titleMatch ? ENTITY_DECODED(titleMatch[1].replace(/<[^>]+>/g, '')).trim() : '';

  text = text
    .replace(/<h1[^>]*>([\s\S]*?)<\/h1>/gi, '\n# $1\n')
    .replace(/<h2[^>]*>([\s\S]*?)<\/h2>/gi, '\n## $1\n')
    .replace(/<h3[^>]*>([\s\S]*?)<\/h3>/gi, '\n### $1\n')
    .replace(/<h4[^>]*>([\s\S]*?)<\/h4>/gi, '\n#### $1\n')
    .replace(/<li[^>]*>([\s\S]*?)<\/li>/gi, '\n- $1')
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<\/(p|div|section|article|tr|table|ul|ol|blockquote|pre|li)>/gi, '\n')
    .replace(/<a[^>]*href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/gi, (_, href, label) => {
      const clean = ENTITY_DECODED(label.replace(/<[^>]+>/g, '')).trim();
      if (!clean) return '';
      if (/^(#|javascript:|mailto:)/i.test(href)) return clean;
      return `${clean} (${href})`;
    })
    .replace(/<(td|th)[^>]*>/gi, ' | ')
    .replace(/<[^>]+>/g, ' ');

  text = ENTITY_DECODED(text)
    .replace(/[ \t\f\v]+/g, ' ')
    .replace(/ ?\n ?/g, '\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim();

  return { title, text };
}

/**
 * Fetch a URL and return readable content. Never throws for HTTP errors;
 * check `error` / `ok` in the result.
 */
export async function fetchReadable(url, {
  maxChars = 8000,
  focus = null,
  raw = false,
  timeoutMs = 20000,
  userAgent = DEFAULT_UA,
} = {}) {
  const started = Date.now();
  let controller;
  let timer;
  try {
    controller = new AbortController();
    timer = setTimeout(() => controller.abort(), timeoutMs);
    const res = await fetch(url, {
      redirect: 'follow',
      signal: controller.signal,
      headers: {
        'User-Agent': userAgent,
        Accept: 'text/html,application/xhtml+xml,application/json,text/plain,text/markdown;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
      },
    });

    const buf = Buffer.from(await res.arrayBuffer());
    const contentType = res.headers.get('content-type') || '';
    const charsetMatch = contentType.match(/charset=([^;]+)/i);
    const charset = (charsetMatch ? charsetMatch[1] : 'utf-8').trim().toLowerCase();

    let body;
    try {
      body = new TextDecoder(charset).decode(buf);
    } catch {
      body = buf.toString('utf8');
    }

    const isJson = /application\/(ld\+)?json/i.test(contentType);
    const isHtml = /text\/html|application\/xhtml/i.test(contentType) || /^\s*<(!doctype|html)/i.test(body);

    let content;
    let title = '';
    if (raw || isJson) {
      content = isJson ? body.trim() : body;
      const t = body.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
      title = t ? ENTITY_DECODED(t[1]).trim() : '';
    } else if (isHtml) {
      const parsed = htmlToMarkdown(body);
      title = parsed.title;
      content = parsed.text;
    } else {
      content = body;
    }

    // Strip non-visible compression garbage if a server ignored Accept-Encoding
    if (/^\u001f\u008b|^\x78\x9c/i.test(content.slice(0, 2))) {
      try {
        content = zlib.gunzipSync(buf).toString('utf8');
      } catch { /* leave as-is */ }
    }

    if (focus) {
      const needle = focus.toLowerCase();
      const lines = content.split('\n');
      const kept = [];
      lines.forEach((line, i) => {
        if (line.toLowerCase().includes(needle)) {
          const from = Math.max(0, i - 2);
          const to = Math.min(lines.length, i + 3);
          for (let j = from; j < to; j += 1) {
            if (!kept.includes(lines[j])) kept.push(lines[j]);
          }
          kept.push('…');
        }
      });
      content = kept.length ? kept.join('\n') : `(no lines matched "${focus}")`;
    }

    const truncated = content.length > maxChars;
    const finalContent = truncated ? `${content.slice(0, maxChars)}\n\n… [truncated at ${maxChars} chars of ${content.length}]` : content;

    return {
      ok: res.ok,
      url: res.url || url,
      status: res.status,
      contentType,
      title,
      content: finalContent,
      truncated,
      ms: Date.now() - started,
      ...(res.ok ? {} : { error: `HTTP ${res.status}` }),
    };
  } catch (e) {
    const aborted = e.name === 'AbortError';
    return {
      ok: false,
      url,
      status: 0,
      contentType: '',
      title: '',
      content: '',
      truncated: false,
      ms: Date.now() - started,
      error: aborted ? `timeout after ${timeoutMs}ms` : e.message,
    };
  } finally {
    clearTimeout(timer);
  }
}

function renderMarkdown(result) {
  const lines = [
    `### ${result.title || result.url}`,
    `URL: ${result.url}`,
    `HTTP ${result.status}${result.contentType ? ` · ${result.contentType.split(';')[0]}` : ''}${result.error ? ` · ${result.error}` : ''}`,
    '',
    result.content || '(empty body)',
  ];
  return lines.join('\n');
}

// CLI runner — only when invoked directly, never when imported.
const invoked = process.argv[1] && process.argv[1].replace(/\\/g, '/').endsWith('tools/webfetch.mjs');
if (invoked) {
  const args = process.argv.slice(2);
  const url = args.find((a) => !a.startsWith('--'));
  const opt = (name, fallback) => {
    const found = args.find((a) => a.startsWith(`--${name}=`));
    return found ? found.slice(name.length + 3) : fallback;
  };
  if (!url) {
    console.error('Usage: node tools/webfetch.mjs <url> [--max-chars=8000] [--focus=text] [--raw] [--json] [--timeout=20000]');
    process.exit(2);
  }
  const result = await fetchReadable(url, {
    maxChars: Number(opt('max-chars', 8000)) || 8000,
    focus: opt('focus', null),
    raw: args.includes('--raw'),
    timeoutMs: Number(opt('timeout', 20000)) || 20000,
    userAgent: opt('ua', DEFAULT_UA),
  });
  if (args.includes('--json')) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(renderMarkdown(result));
  }
  process.exit(result.error && result.status === 0 ? 2 : 0);
}
