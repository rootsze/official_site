import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

test('news.html exists, has valid template structure, active navbar, and 3 articles', () => {
  const newsPath = path.join(process.cwd(), 'news.html');
  assert.ok(fs.existsSync(newsPath), 'news.html must exist');
  const html = fs.readFileSync(newsPath, 'utf8');

  // Verify navigation has active state on News
  assert.match(html, /class="nav-link[^"]*active"[^>]*data-i18n="nav\.news"/, 'News link must be marked active');
  // Verify home link points back to index.html
  assert.match(html, /href="index\.html#home"/, 'Home link must point to index.html#home');
  // Verify category filter elements exist
  assert.match(html, /data-filter="all"/, 'Filter All must exist');
  assert.match(html, /data-filter="product"/, 'Filter Product Updates must exist');
  assert.match(html, /data-filter="industry"/, 'Filter Industry Insights must exist');
  assert.match(html, /data-filter="turnkey"/, 'Filter Turnkey Solutions must exist');
  // Verify at least 3 article cards exist
  const cardMatches = [...html.matchAll(/class="[^"]*news-card[^"]*"/g)];
  assert.ok(cardMatches.length >= 3, 'At least 3 news article cards must be present');
  // Verify news detail modal exists
  assert.match(html, /id="newsDetailModal"/, 'News detail modal must exist');
});
