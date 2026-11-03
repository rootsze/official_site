import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

test('README.md adheres to bilingual brand and technical documentation contracts', () => {
  const root = process.cwd();
  const readmePath = path.join(root, 'README.md');
  assert.ok(fs.existsSync(readmePath), 'README.md must exist at repository root');

  const content = fs.readFileSync(readmePath, 'utf8');

  // 1. Bilingual Top-Level Sections & Reciprocal Anchors
  assert.match(
    content,
    /^# Rootze Global\s+[—–-]\s+Factory-Backed Industrial & Vehicle Export Portal/m,
    'README must have English top-level title'
  );
  assert.match(
    content,
    /^# 襄阳如志进出口有限公司\s+[—–-]\s+全球工业装备与专用汽车出海门户/m,
    'README must have Chinese top-level title'
  );

  assert.ok(
    content.includes('[🇨🇳 Switch to Chinese Document / 中文版本](#-襄阳如志进出口有限公司---全球工业装备与专用汽车出海门户)'),
    'English section must have direct markdown anchor jump to Chinese section'
  );
  assert.ok(
    content.includes('[🌐 Back to English / 返回英文版本](#rootze-global--factory-backed-industrial--vehicle-export-portal)'),
    'Chinese section must have direct markdown anchor jump to English section'
  );

  // 2. Corporate Identity
  assert.ok(content.includes('Xiangyang Ruzhi Import & Export Co., Ltd.'), 'English company name must be present');
  assert.ok(content.includes('襄阳如志进出口有限公司'), 'Chinese company name must be present');
  assert.ok(content.includes('Rootze Global'), 'Brand name Rootze Global must be present');

  // 3. Official Channels & Domains
  assert.ok(content.includes('https://rootzeglobal.com'), 'Official website domain must be present');
  assert.ok(content.includes('+86 15168203740') || content.includes('+8615168203740'), 'Official WhatsApp number must be present');
  assert.ok(content.includes('sales@rootzeglobal.com'), 'Official email sales@rootzeglobal.com must be present');
  assert.ok(content.includes('Web3Forms'), 'Web3Forms RFQ integration must be explained');

  // 4. Product Catalog Subpages & News Portal Links
  const requiredProductLinks = [
    'products/electrical-systems.html',
    'products/railway-equipment.html',
    'products/special-vehicles.html',
    'products/brake-pad-lines.html',
    'news.html'
  ];

  for (const link of requiredProductLinks) {
    assert.ok(content.includes(link), `README must reference relative page: ${link}`);
    assert.ok(fs.existsSync(path.join(root, link)), `Referenced file must exist on disk: ${link}`);
  }

  // 5. Design Philosophy & Device Adaptation
  assert.match(content, /factory-backed|equity-backed/i, 'English section must document factory-backed supply model');
  assert.match(content, /直系工厂|实体工厂|股权合作/i, 'Chinese section must document factory-direct export model');
  assert.match(content, /responsive/i, 'English section must describe responsive layout');
  assert.match(content, /响应式/i, 'Chinese section must describe responsive layout');
  assert.match(content, /mobile|scroll/i, 'English section must document mobile optimization / no horizontal scroll');
  assert.match(content, /横向滚动|免滚动|卡片化/i, 'Chinese section must document no horizontal scroll / card view optimization');

  // 6. Engineering & Verification Commands
  assert.ok(content.includes('scripts/build.py'), 'Must document build script scripts/build.py');
  assert.ok(content.includes('preview.sh'), 'Must document preview script preview.sh');
  assert.ok(content.includes('tests/*.test.mjs'), 'Must document automated test command');

  // 7. No Obsolete Headline
  assert.doesNotMatch(
    content,
    /^# RootZe — Global New Energy Battery & EV Distribution/m,
    'Obsolete prototype title must be replaced'
  );
});
