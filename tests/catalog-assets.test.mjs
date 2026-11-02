import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

test('Product catalog assets exist and meet size constraints', () => {
  const requiredImages = [
    'images/products/electrical/rnmv-softstarter.jpg',
    'images/products/electrical/rnhv-inverter.jpg',
    'images/products/electrical/szbb-compensation.jpg',
    'images/products/electrical/kyn28-switchgear.jpg',
    'images/products/railway/haite-digital-gauge.jpg',
    'images/products/railway/linkage-tamper.jpg',
    'images/products/railway/linkage-cutter.jpg',
    'images/products/brakelines/grinder-driller.jpg',
    'images/products/brakelines/video-poster.jpg',
    'images/products/vehicles/refrigerated-truck.jpg',
    'images/products/vehicles/fuel-tanker.jpg'
  ];

  for (const img of requiredImages) {
    const fullPath = path.resolve(process.cwd(), img);
    assert.ok(fs.existsSync(fullPath), `Required image missing: ${img}`);
    const stat = fs.statSync(fullPath);
    assert.ok(stat.size > 1000, `Image too small or empty: ${img}`);
    assert.ok(stat.size < 500000, `Image exceeds 500KB limit: ${img} (${stat.size} bytes)`);
  }

  const videoPath = path.resolve(process.cwd(), 'videos/brakelines/outer-arc-grinder.mp4');
  assert.ok(fs.existsSync(videoPath), 'Brake line video missing');
  assert.ok(fs.statSync(videoPath).size > 10000, 'Video file empty');
});
