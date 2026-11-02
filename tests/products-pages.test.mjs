import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

test('Each sector catalog page renders complete technical components, unique titles, and working RFQ form contract', () => {
  const pages = [
    { file: 'products/electrical-systems.html', title: 'Industrial Electrical Systems', checks: ['RNMV-EI', 'RNHV', 'SZBB', 'KYN28A-12', '<table'] },
    { file: 'products/railway-equipment.html', title: 'Railway Track Equipment', checks: ['Haite', 'Linkage', '±0.1mm', '1435mm', '<table'] },
    { file: 'products/brake-pad-lines.html', title: 'Turnkey Brake Pad Lines', checks: ['<video', 'outer-arc-grinder.mp4', '200T-500T', 'Turnkey'] },
    { file: 'products/special-vehicles.html', title: 'Special Purpose Vehicles', checks: ['Dongfeng', 'Refrigerated', 'Tanker', 'LHD / RHD'] }
  ];

  for (const item of pages) {
    const fullPath = path.resolve(process.cwd(), item.file);
    assert.ok(fs.existsSync(fullPath), `Missing ${item.file}`);
    const content = fs.readFileSync(fullPath, 'utf-8');
    
    // 1. Verify specific content
    for (const check of item.checks) {
      assert.ok(content.includes(check), `${item.file} missing expected content: ${check}`);
    }

    // 2. Verify unique title
    assert.ok(content.includes(`<title>${item.title}`), `${item.file} should have unique page title starting with ${item.title}`);

    // 3. Verify RFQ form contract matches main.js expectations
    assert.ok(content.includes('id="inquiryForm"'), `${item.file} missing id="inquiryForm"`);
    assert.ok(content.includes('id="inqName"'), `${item.file} missing id="inqName"`);
    assert.ok(content.includes('id="inqCompany"'), `${item.file} missing id="inqCompany"`);
    assert.ok(content.includes('id="inqContact"'), `${item.file} missing id="inqContact"`);
    assert.ok(content.includes('id="inqCategory"'), `${item.file} missing id="inqCategory"`);
    assert.ok(content.includes('id="inqMessage"'), `${item.file} missing id="inqMessage"`);
    assert.ok(content.includes('id="inqSubmitBtn"'), `${item.file} missing id="inqSubmitBtn"`);
    assert.ok(content.includes('id="inqSubmitBtnText"'), `${item.file} missing id="inqSubmitBtnText"`);
    assert.ok(content.includes('id="inquirySuccessModal"'), `${item.file} missing #inquirySuccessModal`);

    // 4. Verify navbar contains All Sectors Overview
    assert.ok(content.includes('All Sectors Overview'), `${item.file} navbar dropdown should link to All Sectors Overview`);

    // 5. Verify language switcher exists
    assert.ok(content.includes('lang-switch'), `${item.file} must have language switcher`);
  }
});
