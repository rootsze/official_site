import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

test('CSS rules in css/rootze.css enforce equal height & flex structure for contact section', () => {
  const cssPath = path.resolve(process.cwd(), 'css/rootze.css');
  assert.ok(fs.existsSync(cssPath), 'Missing css/rootze.css');
  const css = fs.readFileSync(cssPath, 'utf-8');

  // Must define .contact-form-card with flex column & height: 100%
  assert.match(css, /\.contact-form-card\s*\{[^}]*display:\s*flex;/s, 'contact-form-card must have display: flex');
  assert.match(css, /\.contact-form-card\s*\{[^}]*flex-direction:\s*column;/s, 'contact-form-card must have flex-direction: column');
  assert.match(css, /\.contact-form-card\s*\{[^}]*height:\s*100%;/s, 'contact-form-card must have height: 100%');

  // Must define .contact-info-card with flex column & height: 100%
  assert.match(css, /\.contact-info-card\s*\{[^}]*display:\s*flex;/s, 'contact-info-card must have display: flex');
  assert.match(css, /\.contact-info-card\s*\{[^}]*flex-direction:\s*column;/s, 'contact-info-card must have flex-direction: column');
  assert.match(css, /\.contact-info-card\s*\{[^}]*height:\s*100%;/s, 'contact-info-card must have height: 100%');

  // Must define .form-group-message with flex-grow
  assert.match(css, /\.form-group-message\s*\{[^}]*display:\s*flex;/s, 'form-group-message must have display: flex');
  assert.match(css, /\.form-group-message\s*\{[^}]*flex-grow:\s*1;/s, 'form-group-message must have flex-grow: 1');
  assert.match(css, /\.form-group-message\s+textarea\s*\{[^}]*flex-grow:\s*1;/s, 'form-group-message textarea must have flex-grow: 1');
  assert.match(css, /\.form-group-message\s+textarea\s*\{[^}]*min-height:\s*140px;/s, 'form-group-message textarea must have min-height: 140px');
});

test('Contact section in partial and index.html implements strict equal-height layout contracts', () => {
  const files = [
    path.resolve(process.cwd(), 'src/partials/08-contact.html'),
    path.resolve(process.cwd(), 'index.html')
  ];

  for (const filePath of files) {
    assert.ok(fs.existsSync(filePath), `Missing ${filePath}`);
    const html = fs.readFileSync(filePath, 'utf-8');

    // 1. Row has align-items-stretch
    assert.match(html, /class="[^"]*row\s+block-9[^"]*align-items-stretch[^"]*"/, `${filePath} row must include align-items-stretch`);

    // 2. col-md-8 has d-flex and mb-4 mb-md-0 (no mb-md-5)
    assert.match(html, /class="[^"]*col-md-8\s+d-flex\s+mb-4\s+mb-md-0[^"]*"/, `${filePath} left column must have d-flex mb-4 mb-md-0`);
    assert.doesNotMatch(html, /class="[^"]*col-md-8[^"]*mb-md-5[^"]*"/, `${filePath} left column must not have mb-md-5`);

    // 3. Form has contact-form-card & submit wrapper has mt-auto
    assert.match(html, /<form[^>]*class="[^"]*contact-form-card[^"]*"/, `${filePath} form must include contact-form-card`);
    assert.match(html, /<div[^>]*class="[^"]*form-group[^"]*mt-auto[^"]*"[^>]*>\s*<button[^>]*type="submit"/s, `${filePath} submit button wrapper must have mt-auto`);

    // 4. Message group has form-group-message and textarea has rows="6"
    assert.match(html, /class="[^"]*form-group\s+form-group-message[^"]*"/, `${filePath} message group must include form-group-message`);
    assert.match(html, /<textarea[^>]*id="inqMessage"[^>]*rows="6"/, `${filePath} inqMessage must have rows="6"`);

    // 5. Right column has d-flex and contact-info-card
    assert.match(html, /class="[^"]*col-md-4\s+d-flex\s+mb-4\s+mb-md-0[^"]*"/, `${filePath} right column must have d-flex mb-4 mb-md-0`);
    assert.match(html, /class="[^"]*contact-info-card[^"]*"/, `${filePath} right column inner container must include contact-info-card`);
  }
});

test('E2E Layout: Submit button bottom aligns with WhatsApp card bottom in rendered browser', async () => {
  const { spawn } = await import('node:child_process');
  const chromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  if (!fs.existsSync(chromePath)) {
    return; // Skip on environments without Chrome
  }

  const port = 9520 + Math.floor(Math.random() * 50);
  const chrome = spawn(chromePath, [
    '--headless=new',
    `--remote-debugging-port=${port}`,
    '--disable-gpu',
    '--window-size=1200,900'
  ]);

  try {
    for (let i = 0; i < 20; i++) {
      await new Promise(r => setTimeout(r, 200));
      try {
        const res = await fetch(`http://127.0.0.1:${port}/json/version`);
        if (res.ok) break;
      } catch {}
    }
    const targetUrl = `file://${path.resolve(process.cwd(), 'index.html')}`;
    const newTabRes = await fetch(`http://127.0.0.1:${port}/json/new?${targetUrl}`, { method: 'PUT' });
    const target = await newTabRes.json();
    const ws = new WebSocket(target.webSocketDebuggerUrl);
    await new Promise(r => ws.onopen = r);

    let id = 1;
    function send(method, params = {}) {
      return new Promise(resolve => {
        const curId = id++;
        const handler = (event) => {
          const data = JSON.parse(event.data);
          if (data.id === curId) {
            ws.removeEventListener('message', handler);
            resolve(data.result);
          }
        };
        ws.addEventListener('message', handler);
        ws.send(JSON.stringify({ id: curId, method, params }));
      });
    }

    await send('Page.enable');
    await send('Emulation.setDeviceMetricsOverride', { width: 1200, height: 900, deviceScaleFactor: 1, mobile: false });
    await new Promise(r => setTimeout(r, 400));

    const evalRes = await send('Runtime.evaluate', {
      expression: `(() => {
        const textarea = document.querySelector("#inqMessage");
        const submitBtn = document.querySelector("#inqSubmitBtn");
        const greenCard = document.querySelector(".contact-info-card .p-3");
        
        const sRect = submitBtn.getBoundingClientRect();
        const gRect = greenCard.getBoundingClientRect();
        const tRect = textarea.getBoundingClientRect();
        return {
          textareaHeight: Math.round(tRect.height),
          submitBottom: Math.round(sRect.bottom),
          greenBottom: Math.round(gRect.bottom),
          diff: Math.round(sRect.bottom - gRect.bottom),
          gap: Math.round(sRect.top - tRect.bottom)
        };
      })()`,
      returnByValue: true
    });

    const metrics = evalRes.result.value;
    assert.ok(metrics.textareaHeight >= 140, `Textarea height (${metrics.textareaHeight}px) should be >= 140px`);
    assert.equal(metrics.diff, 0, `Submit button bottom (${metrics.submitBottom}px) must exactly align with green card bottom (${metrics.greenBottom}px)`);
    assert.ok(metrics.gap <= 24, `Gap between textarea and submit button (${metrics.gap}px) should be standard form gap <= 24px`);
  } finally {
    chrome.kill();
  }
});

