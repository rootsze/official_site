import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

test('Each sector catalog page renders complete technical components', () => {
  const pages = [
    { file: 'products/electrical-systems.html', checks: ['RNMV-EI', 'RNHV', 'SZBB', 'KYN28A-12', '<table'] },
    { file: 'products/railway-equipment.html', checks: ['Haite', 'Linkage', '±0.1mm', '1435mm', '<table'] },
    { file: 'products/brake-pad-lines.html', checks: ['<video', 'outer-arc-grinder.mp4', '200T-500T', 'Turnkey'] },
    { file: 'products/special-vehicles.html', checks: ['Dongfeng', 'Refrigerated', 'Tanker', 'LHD / RHD'] }
  ];

  for (const item of pages) {
    const fullPath = path.resolve(process.cwd(), item.file);
    assert.ok(fs.existsSync(fullPath), `Missing ${item.file}`);
    const content = fs.readFileSync(fullPath, 'utf-8');
    for (const check of item.checks) {
      assert.ok(content.includes(check), `${item.file} missing expected content: ${check}`);
    }
    // Verify RFQ contact form exists
    assert.ok(content.includes('web3forms') || content.includes('contact-form'), `${item.file} must have RFQ inquiry form`);
    // Verify language switcher exists
    assert.ok(content.includes('lang-switch'), `${item.file} must have language switcher`);
  }
});
