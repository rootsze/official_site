# Special Purpose Vehicles Accordion Expand/Collapse Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the "Expand All" and "Collapse All" functionality in `products/special-vehicles.html` so that all 4 vehicle categories (28 models) can be expanded or collapsed simultaneously, while allowing independent manual toggling of each category.

**Architecture:** Remove Bootstrap's `data-parent="#spvAccordion"` mutual exclusion attribute from all category collapse elements in `products/special-vehicles.html` and the Python generator script `scripts/sync_spv_i18n.py`. This allows Bootstrap 4 Collapse to operate in independent panel mode where jQuery's `.collapse('show')` and `.collapse('hide')` apply to all categories simultaneously without triggering sibling closing events.

**Tech Stack:** HTML5, Bootstrap 4, jQuery, Python 3, Node.js (`node:test`).

**Spec:** [docs/superpowers/specs/2026-11-13-spv-accordion-expand-collapse-fix-design.md](file:///Users/brainzhang/work/rootze/landingpage/docs/superpowers/specs/2026-11-13-spv-accordion-expand-collapse-fix-design.md)

## Global Constraints
- Do not modify vehicle card layouts, specifications, image URLs, or RFQ modal bindings.
- All category headers must retain their data-toggle and data-target bindings so manual clicking continues to work seamlessly.
- Generator script `scripts/sync_spv_i18n.py` must stay in complete parity with `products/special-vehicles.html`.
- All Node.js tests in `tests/*.test.mjs` must pass.

## Review Focus
- Clicking "Expand All" must expand all 4 categories without closing any preceding categories.
- Clicking "Collapse All" must collapse all 4 categories.
- Re-running `python3 scripts/sync_spv_i18n.py` must not reintroduce `data-parent="#spvAccordion"`.
- Clicking any individual category header must toggle that category without affecting the expansion state of other categories.
- Existing i18n translation keys (`catalog.spv.btn_expand_all`, `catalog.spv.btn_collapse_all`) must continue working in both English and Chinese.

---

### Task 1: Automated Unit/Structure Test for SPV Accordion Behavior

**Files:**
- Create: `tests/spv-accordion.test.mjs`

**Interfaces:**
- Consumes: `products/special-vehicles.html`, `scripts/sync_spv_i18n.py`, `js/main.js`
- Produces: automated test suite ensuring all 4 categories exist, absence of `data-parent="#spvAccordion"`, and existence of click bindings in `js/main.js`.

- [ ] **Step 1: Write the failing test in `tests/spv-accordion.test.mjs`**

```javascript
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test tests/spv-accordion.test.mjs`
Expected: FAIL due to presence of `data-parent="#spvAccordion"` in `products/special-vehicles.html` and `scripts/sync_spv_i18n.py`.

- [ ] **Step 3: Commit the test**

```bash
git add tests/spv-accordion.test.mjs
git commit -m "test: add test suite for spv accordion expand/collapse behavior"
```

---

### Task 2: Remove `data-parent` from `products/special-vehicles.html` and `scripts/sync_spv_i18n.py`

**Files:**
- Modify: `products/special-vehicles.html:150-1100`
- Modify: `scripts/sync_spv_i18n.py:1320-1340`

**Interfaces:**
- Consumes: `products/special-vehicles.html`, `scripts/sync_spv_i18n.py`
- Produces: HTML and Python generator template without `data-parent="#spvAccordion"`

- [ ] **Step 1: Modify `scripts/sync_spv_i18n.py`**

In `generate_catalog_section_html()` around line 1330:
Change:
```python
<div id="{cat['collapse_id']}" class="collapse {is_show}" aria-labelledby="{cat['heading_id']}" data-parent="#spvAccordion">
```
To:
```python
<div id="{cat['collapse_id']}" class="collapse {is_show}" aria-labelledby="{cat['heading_id']}">
```

- [ ] **Step 2: Modify `products/special-vehicles.html`**

Remove ` data-parent="#spvAccordion"` from all 4 category collapse elements:
1. `id="collapse-tanker-trucks"`
2. `id="collapse-tanker-semis"`
3. `id="collapse-reefer"`
4. `id="collapse-engineering"`

- [ ] **Step 3: Run the test to verify it passes**

Run: `node --test tests/spv-accordion.test.mjs`
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add products/special-vehicles.html scripts/sync_spv_i18n.py
git commit -m "fix(products): remove data-parent on special vehicles accordion to enable expand-all"
```

---

### Task 3: Generator Sync, End-to-End Test Suite, and Verification

**Files:**
- Verify: `scripts/sync_spv_i18n.py`
- Verify: `products/special-vehicles.html`
- Verify: `tests/*.test.mjs`

**Interfaces:**
- Consumes: `scripts/sync_spv_i18n.py`, test suite
- Produces: Verified synchronized codebase passing all regression checks

- [ ] **Step 1: Run generator test run or sync check**

Run: `python3 scripts/sync_spv_i18n.py`
Verify that `git diff products/special-vehicles.html` introduces no unintended regressions and does not re-add `data-parent`.

- [ ] **Step 2: Run all test suites**

Run: `node --test tests/*.test.mjs`
Expected: All suites PASS.

- [ ] **Step 3: Commit any sync changes (if any)**

```bash
git add -u
git commit -m "chore: synchronize special vehicles accordion template and verify regression tests"
```
