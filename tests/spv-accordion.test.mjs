import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

test('special-vehicles.html accordion elements do not have data-parent mutual exclusion', () => {
  const htmlPath = path.join(process.cwd(), 'products/special-vehicles.html');
  assert.ok(fs.existsSync(htmlPath), 'products/special-vehicles.html must exist');
  const html = fs.readFileSync(htmlPath, 'utf8');

  // Verify all 4 category collapse IDs exist
  const expectedCollapseIds = [
    'collapse-tanker-trucks',
    'collapse-tanker-semis',
    'collapse-reefer',
    'collapse-engineering'
  ];

  for (const id of expectedCollapseIds) {
    assert.ok(html.includes(`id="${id}"`), `Element with id="${id}" must exist in HTML`);
  }

  // Verify that data-parent="#spvAccordion" is NOT present on any collapse element
  assert.ok(
    !html.includes('data-parent="#spvAccordion"'),
    'products/special-vehicles.html must not contain data-parent="#spvAccordion" so categories can be independently and simultaneously expanded'
  );

  // Verify expand and collapse all buttons exist
  assert.ok(html.includes('id="btnExpandAll"'), 'btnExpandAll button must exist');
  assert.ok(html.includes('id="btnCollapseAll"'), 'btnCollapseAll button must exist');
});

test('scripts/sync_spv_i18n.py template does not include data-parent="#spvAccordion"', () => {
  const scriptPath = path.join(process.cwd(), 'scripts/sync_spv_i18n.py');
  assert.ok(fs.existsSync(scriptPath), 'scripts/sync_spv_i18n.py must exist');
  const scriptContent = fs.readFileSync(scriptPath, 'utf8');

  assert.ok(
    !scriptContent.includes('data-parent="#spvAccordion"'),
    'scripts/sync_spv_i18n.py generator template must not contain data-parent="#spvAccordion"'
  );
});

test('js/main.js wires #btnExpandAll and #btnCollapseAll to #spvAccordion .collapse', () => {
  const mainJsPath = path.join(process.cwd(), 'js/main.js');
  assert.ok(fs.existsSync(mainJsPath), 'js/main.js must exist');
  const jsContent = fs.readFileSync(mainJsPath, 'utf8');

  assert.match(jsContent, /#btnExpandAll/, 'js/main.js must reference #btnExpandAll');
  assert.match(jsContent, /#btnCollapseAll/, 'js/main.js must reference #btnCollapseAll');
  assert.match(jsContent, /#spvAccordion\s+\.collapse.*collapse\(['"]show['"]\)/, 'btnExpandAll must trigger collapse show');
  assert.match(jsContent, /#spvAccordion\s+\.collapse.*collapse\(['"]hide['"]\)/, 'btnCollapseAll must trigger collapse hide');
});
