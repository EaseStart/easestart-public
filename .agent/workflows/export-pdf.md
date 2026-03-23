---
description: Export HTML CV files to PDF using Playwright + Chromium. Ensures 2-page output with correct fonts, backgrounds, and layout.
---

# PDF Export Guidelines for HTML CVs

> Automated PDF generation from HTML CVs using Playwright + Chromium.

## Prerequisites

// turbo-all

```bash
cd /tmp && npm install playwright && npx playwright install chromium
```

## Page Size Reference

| Layout Type | Width | Height | Files |
|-------------|-------|--------|-------|
| **v2-modern** (single-column) | `1811px` | `2560px` | All new role CVs |
| **v1-classic** (2-column, 2-page HTML) | `1811px` | `2800px` | `ppd-v1-classic`, `aipm-v1-classic` |

> **Why 1811px?** Matches the `max-w-[1811px]` constraint in all CV HTML files.
> **Why different heights?** v1-classic files have denser 2-column layouts with more vertical content.

## Export Script

Save as `/tmp/export-cv-pdf.mjs`:

```javascript
import { chromium } from 'playwright';
import { resolve } from 'path';
import { mkdir } from 'fs/promises';

const BASE = '/Users/jang/Desktop/Jang/CV-html';
const PDF_DIR = '/Users/jang/Desktop/Jang/CV-pdf';

// ── File Registry ──────────────────────────────────
// Add new CVs here. Use h: '2800px' for v1-classic layouts.
const files = [
  { html: 'principal-product-designer/ppd-v1-classic.html', pdf: 'Jang_Trinh_Principal_Product_Designer_v1.pdf', h: '2800px' },
  { html: 'principal-product-designer/ppd-v2-modern.html', pdf: 'Jang_Trinh_Principal_Product_Designer_v2.pdf', h: '2560px' },
  { html: 'ai-product-manager/aipm-v1-classic.html', pdf: 'Jang_Trinh_AI_Product_Manager_v1.pdf', h: '2800px' },
  { html: 'ai-product-manager/aipm-v2-modern.html', pdf: 'Jang_Trinh_AI_Product_Manager_v2.pdf', h: '2560px' },
  { html: 'product-design-consultant/v2-modern.html', pdf: 'Jang_Trinh_Product_Design_Consultant.pdf', h: '2560px' },
  { html: 'ux-research-lead/v2-modern.html', pdf: 'Jang_Trinh_UX_Research_Lead.pdf', h: '2560px' },
  { html: 'cx-strategist/v2-modern.html', pdf: 'Jang_Trinh_CX_Strategist.pdf', h: '2560px' },
  { html: 'workshop-facilitator/v2-modern.html', pdf: 'Jang_Trinh_Workshop_Facilitator.pdf', h: '2560px' },
  { html: 'ai-transformation-consultant/v2-modern.html', pdf: 'Jang_Trinh_AI_Transformation_Consultant.pdf', h: '2560px' },
];

async function main() {
  await mkdir(PDF_DIR, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage();

  for (const { html, pdf, h } of files) {
    const htmlPath = resolve(BASE, html);
    const pdfPath = resolve(PDF_DIR, pdf);

    // Set viewport to match page dimensions
    await page.setViewportSize({ width: 1811, height: parseInt(h) });

    console.log(`📄 ${html} → ${pdf}`);

    // Load with networkidle to ensure CDN resources (Tailwind, fonts) are loaded
    await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle', timeout: 30000 });

    // Wait for web fonts to fully render
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(2000);

    await page.pdf({
      path: pdfPath,
      width: '1811px',
      height: h,
      printBackground: true,       // CRITICAL: renders black headers
      preferCSSPageSize: false,     // Use our dimensions, not @page CSS
      margin: { top: 0, right: 0, bottom: 0, left: 0 },
    });

    console.log(`  ✅ Saved`);
  }

  await browser.close();
  console.log(`\n🎉 All ${files.length} PDFs generated in ${PDF_DIR}`);
}

main().catch(e => { console.error(e); process.exit(1); });
```

## Run

```bash
cd /tmp && node export-cv-pdf.mjs
```

## Verify Page Count

```bash
cd /Users/jang/Desktop/Jang/CV-pdf && for f in *.pdf; do echo "$f: $(mdls -name kMDItemNumberOfPages "$f" | awk '{print $3}') pages"; done
```

**Expected:** Every PDF = 2 pages.

## Critical Settings Explained

| Setting | Value | Why |
|---------|-------|-----|
| `printBackground: true` | Required | Without this, black header/banner renders white |
| `preferCSSPageSize: false` | Required | Ignores any `@page` CSS so our explicit dimensions take effect |
| `margin: 0` | Required | CVs have built-in padding (73px), no extra margins needed |
| `waitUntil: 'networkidle'` | Required | Ensures Tailwind CDN + Google Fonts CDN fully load |
| `document.fonts.ready` | Required | Waits for DIN Condensed and SF Pro Display font rendering |
| `waitForTimeout(2000)` | Safety net | Extra 2s buffer for slow CDN responses |

## Naming Convention

```
Jang_Trinh_{Role_Name}[_v1|_v2].pdf
```

- `_v1` = v1-classic layout (2-column Figma-style)
- `_v2` = v2-modern layout (editorial single-column)
- No suffix = only one version exists (v2-modern)

## Adding a New CV

1. Create HTML in `CV-html/{role-folder}/v2-modern.html`
2. Add entry to the `files` array in the export script
3. Use `h: '2560px'` for v2-modern, `h: '2800px'` for v1-classic
4. Run the script
5. Verify: **must be exactly 2 pages**

## Troubleshooting

| Problem | Fix |
|---------|-----|
| **3+ pages** | Increase page height (try `2700px` → `2800px` → `2900px`) |
| **Content cut off** | Reduce content in HTML, or increase page height |
| **White header** | Ensure `printBackground: true` |
| **Wrong fonts** | Check CDN URLs, increase `waitForTimeout` |
| **Blank PDF** | Check `file://` path is correct and HTML exists |

---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Validate | Check HTML exists + fonts loaded | Validation check | HTML file exists + no missing assets |
| **2** Render | Playwright Chromium → PDF | PDF file | PDF renders correctly |
| **3** Verify | Page count + visual check | Verification | Exactly 2 pages + fonts correct |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | 2 pages + fonts loaded + backgrounds correct | → PDF ready |
| **MEDIUM** | Content overflows slightly or minor font issue | → Binary: A) Accept, B) Adjust HTML spacing |
| **LOW** | Wrong page count or missing fonts/backgrounds | → Stop, debug CSS print styles |

### Anti-Patterns
- ❌ Exporting without verifying page count — 3-page CV is instant rejection
- ❌ Not checking font loading — fallback fonts look unprofessional
- ❌ Skipping background color/image verification — print CSS strips backgrounds by default
