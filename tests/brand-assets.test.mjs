import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

test('required brand logos and category assets exist', () => {
  const logoHorizontal = path.join(process.cwd(), 'images/logo-horizontal.png');
  const logoWhite = path.join(process.cwd(), 'images/logo-white.png');
  assert.ok(fs.existsSync(logoHorizontal), 'images/logo-horizontal.png must exist');
  assert.ok(fs.existsSync(logoWhite), 'images/logo-white.png must exist');
  assert.ok(fs.statSync(logoHorizontal).size > 1000, 'logo-horizontal.png must be non-empty');
  assert.ok(fs.statSync(logoWhite).size > 1000, 'logo-white.png must be non-empty');
});
