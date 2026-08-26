/**
 * Tax News aggregator.
 *
 * Fetches the configured RSS feeds, normalizes every item to
 * { title, source, date, excerpt, link }, merges, dedupes, sorts newest
 * first and returns the top 20. One broken feed never takes down the rest.
 *
 * Freshness is handled by the CDN rather than by a framework: the
 * Cache-Control below is the direct equivalent of Next.js's
 * `export const revalidate = 14400` — Vercel serves a cached response for
 * four hours, then revalidates in the background while still serving the
 * stale copy, so a visitor never waits on the upstream feeds.
 *
 * Health check:  /api/tax-news?debug=1
 * Reports which feed URL answered for each source and why any failed.
 * Use it once after deploy to confirm the URLs below are live.
 */
const Parser = require('rss-parser');

const REVALIDATE_SECONDS = 14400; // 4 hours
const MAX_ITEMS = 20;
const EXCERPT_CHARS = 150;
const FETCH_TIMEOUT_MS = 8000;

/**
 * Each source lists its candidate feed URLs in order of preference; the
 * first that parses wins. Publishers move these paths around, so the
 * fallbacks keep a source alive when its primary path changes.
 *
 * Deliberately NOT included: irs.gov, whose RSS is not currently maintained.
 */
const SOURCES = [
  {
    name: 'Journal of Accountancy',
    urls: [
      'https://www.journalofaccountancy.com/feed',
      'https://www.journalofaccountancy.com/rss/all-news.xml',
      'https://www.journalofaccountancy.com/feed/',
    ],
  },
  {
    name: 'Accounting Today',
    urls: [
      'https://www.accountingtoday.com/feed?rss=true',
      'https://www.accountingtoday.com/feed',
      'https://www.accountingtoday.com/rss',
    ],
  },
  {
    name: 'CPA Practice Advisor',
    urls: [
      'https://www.cpapracticeadvisor.com/feed/',
      'https://www.cpapracticeadvisor.com/rss/',
      'https://www.cpapracticeadvisor.com/arc/outboundfeeds/rss/',
    ],
  },
  {
    name: 'Thomson Reuters Tax & Accounting',
    urls: [
      'https://tax.thomsonreuters.com/blog/feed/',
      'https://tax.thomsonreuters.com/news/feed/',
      'https://tax.thomsonreuters.com/feed/',
    ],
  },
];

const parser = new Parser({
  timeout: FETCH_TIMEOUT_MS,
  headers: { 'User-Agent': 'OCGFinancialSite/1.0 (+https://www.ocgfinancial.com/)' },
});

/** Strip tags and entities, collapse whitespace, trim to a clean word boundary. */
function toExcerpt(raw) {
  if (!raw) return '';
  var text = String(raw)
    .replace(/<[^>]*>/g, ' ')
    .replace(/&nbsp;/gi, ' ')
    .replace(/&amp;/gi, '&')
    .replace(/&quot;/gi, '"')
    .replace(/&#39;|&apos;/gi, "'")
    .replace(/&lt;/gi, '<')
    .replace(/&gt;/gi, '>')
    .replace(/&[a-z]+;/gi, ' ')
    .replace(/\s+/g, ' ')
    .trim();
  if (text.length <= EXCERPT_CHARS) return text;
  var cut = text.slice(0, EXCERPT_CHARS);
  var lastSpace = cut.lastIndexOf(' ');
  if (lastSpace > EXCERPT_CHARS * 0.6) cut = cut.slice(0, lastSpace);
  return cut.replace(/[\s,;:.\-]+$/, '') + '…';
}

function toDate(item) {
  var raw = item.isoDate || item.pubDate || item.date || null;
  if (!raw) return null;
  var d = new Date(raw);
  return isNaN(d.getTime()) ? null : d.toISOString();
}

/**
 * Summary field only — never the full article body. Feeds that ship
 * content:encoded (the whole article) are read for their short summary
 * instead, so we display a teaser and link out for the rest.
 */
function summaryOf(item) {
  return item.contentSnippet || item.summary || item.description || item.content || '';
}

function normalize(item, sourceName) {
  var title = (item.title || '').trim();
  var link = (item.link || item.guid || '').trim();
  if (!title || !link) return null;
  return {
    title: title,
    source: sourceName,
    date: toDate(item),
    excerpt: toExcerpt(summaryOf(item)),
    link: link,
  };
}

/** Try each candidate URL for a source; return items plus what happened. */
async function loadSource(source) {
  var attempts = [];
  for (var i = 0; i < source.urls.length; i++) {
    var url = source.urls[i];
    try {
      var feed = await parser.parseURL(url);
      var items = (feed.items || [])
        .map(function (it) { return normalize(it, source.name); })
        .filter(Boolean);
      if (items.length) {
        attempts.push({ url: url, ok: true, items: items.length });
        return { items: items, attempts: attempts };
      }
      attempts.push({ url: url, ok: false, error: 'parsed but returned no usable items' });
    } catch (err) {
      attempts.push({ url: url, ok: false, error: String((err && err.message) || err).slice(0, 200) });
    }
  }
  return { items: [], attempts: attempts };
}

async function getTaxNews() {
  var results = await Promise.all(SOURCES.map(function (s) {
    // Isolated per source: a rejection here can never fail the whole batch.
    return loadSource(s).catch(function (err) {
      return { items: [], attempts: [{ url: s.urls[0], ok: false, error: String(err).slice(0, 200) }] };
    });
  }));

  var merged = [];
  var diagnostics = [];
  results.forEach(function (res, idx) {
    merged = merged.concat(res.items);
    diagnostics.push({ source: SOURCES[idx].name, attempts: res.attempts, items: res.items.length });
  });

  var seen = Object.create(null);
  var deduped = merged.filter(function (item) {
    var key = item.link.split('#')[0].replace(/\/+$/, '').toLowerCase();
    if (seen[key]) return false;
    seen[key] = true;
    return true;
  });

  deduped.sort(function (a, b) {
    if (!a.date && !b.date) return 0;
    if (!a.date) return 1;
    if (!b.date) return -1;
    return b.date.localeCompare(a.date);
  });

  return { items: deduped.slice(0, MAX_ITEMS), diagnostics: diagnostics };
}

module.exports = async function handler(req, res) {
  try {
    var result = await getTaxNews();
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader(
      'Cache-Control',
      'public, s-maxage=' + REVALIDATE_SECONDS + ', stale-while-revalidate=86400'
    );
    var debug = req.query && (req.query.debug === '1' || req.query.debug === 'true');
    var body = { items: result.items, count: result.items.length, updated: new Date().toISOString() };
    if (debug) {
      body.diagnostics = result.diagnostics;
      // A health check should never be answered from cache.
      res.setHeader('Cache-Control', 'no-store');
    }
    res.status(200).json(body);
  } catch (err) {
    // Never 500 the page: an empty list renders the fallback message.
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Cache-Control', 'no-store');
    res.status(200).json({ items: [], count: 0, error: String((err && err.message) || err).slice(0, 200) });
  }
};

module.exports.getTaxNews = getTaxNews;
