# Design: Special Purpose Vehicles Accordion Expand/Collapse Fix

## 1. Intent & Context
In `products/special-vehicles.html` (the Commercial Special Purpose Vehicles catalog), the "Expand All" (`#btnExpandAll`) and "Collapse All" (`#btnCollapseAll`) buttons fail to expand all categories simultaneously. Clicking "Expand All" only keeps one category open instead of expanding all four categories.

Root cause:
Each category's collapse element (`#collapse-tanker-trucks`, `#collapse-tanker-semis`, `#collapse-reefer`, `#collapse-engineering`) contains the Bootstrap attribute `data-parent="#spvAccordion"`.
Bootstrap's collapse plugin enforces strict mutual exclusivity when `data-parent` is present: invoking `.collapse('show')` on an item automatically hides any open siblings in the same accordion container. Consequently, jQuery's sequential loop in `js/main.js` (`$('#spvAccordion .collapse').collapse('show')`) causes each opened section to immediately close the preceding section, leaving only the final item visible.

## 2. Goals & Non-Goals
- **Goals**:
  - Enable "Expand All" (`#btnExpandAll`) to open all 4 categories simultaneously so users can browse all 28 vehicle models at once.
  - Enable "Collapse All" (`#btnCollapseAll`) to close all categories simultaneously.
  - Ensure individual category header clicks continue to toggle their respective section smoothly.
  - Ensure arrow icon states (down/up or standard indicator) and ARIA attributes behave cleanly.
  - Synchronize both `products/special-vehicles.html` and the generator script `scripts/sync_spv_i18n.py`.
- **Non-Goals**:
  - Do not alter vehicle card structures, images, spec badges, or RFQ modal triggers.
  - Do not change styling or layout of the accordion headers.

## 3. Approaches Considered & Decision
- **Approach 1 (Chosen - Independent Collapsible Panels)**:
  - Remove `data-parent="#spvAccordion"` from the category collapse containers in `products/special-vehicles.html` and `scripts/sync_spv_i18n.py`.
  - In `js/main.js`, keep or enhance `#btnExpandAll` and `#btnCollapseAll` calls to trigger `.collapse('show')` and `.collapse('hide')`.
  - *Tradeoffs*: Without `data-parent`, each category operates independently. This is ideal for a multi-category product catalog because users can open and compare multiple vehicle categories side by side, and both "Expand All" and "Collapse All" work reliably using standard Bootstrap APIs without hacks or state race conditions.
- **Approach 2 (Strict Accordion Mutex with Expand-All Override via Custom JS)**:
  - Remove HTML `data-parent`, but simulate single-open mutual exclusivity via custom JS listeners during individual clicks, with an override flag when clicking "Expand All".
  - *Tradeoffs*: Adds stateful JS logic and event coordination for minimal practical benefit, while restricting users from viewing multiple categories simultaneously. Rejected in favor of Approach 1.

## 4. Implementation Details
1. **`products/special-vehicles.html`**:
   - Remove `data-parent="#spvAccordion"` from:
     - `#collapse-tanker-trucks`
     - `#collapse-tanker-semis`
     - `#collapse-reefer`
     - `#collapse-engineering`
2. **`scripts/sync_spv_i18n.py`**:
   - Update line ~1330 in `generate_catalog_section_html()`:
     Remove `data-parent="#spvAccordion"` from `<div id="{cat['collapse_id']}" class="collapse {is_show}" aria-labelledby="{cat['heading_id']}">`.
3. **`js/main.js`**:
   - Verify `#btnExpandAll` and `#btnCollapseAll` event listeners:
     ```javascript
     $('#btnExpandAll').on('click', function() {
       $('#spvAccordion .collapse').collapse('show');
     });
     $('#btnCollapseAll').on('click', function() {
       $('#spvAccordion .collapse').collapse('hide');
     });
     ```
   - (Optional/Check) Ensure `aria-expanded` attributes on card headers update accordingly.

## 5. Verification Plan
- Inspect `products/special-vehicles.html` to confirm no `data-parent="#spvAccordion"` attributes remain on `.collapse` elements.
- Verify running `python3 scripts/sync_spv_i18n.py` generates consistent HTML without re-introducing `data-parent`.
- Verify test suites (`node --test tests/i18n.test.mjs` and related checks).
- In browser or DOM simulation, confirm clicking `#btnExpandAll` shows all 4 categories, clicking `#btnCollapseAll` hides all 4 categories, and clicking an individual header toggles only that section.
