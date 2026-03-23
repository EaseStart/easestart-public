---
description: Analyze reference visual styles (PDFs, screenshots, URLs) and build complete HTML template systems. From reference → pixel-perfect templates in one session.
---

# /style-extract — Reference Style Analysis & Template Builder

> Feed reference material → AI extracts pixel-perfect specs → builds templates + CSS → ready for /slides

> **Lucius:** L2 (Phase→Artifact→Gate) · L5 (confidence on template quality)
> **Owner:** marketing-agent

// turbo-all

## When to Use

- Found a carousel/slide style you like → want to replicate it
- Downloaded reference PDFs or screenshots from social media
- Want to add a new style to `visual-styles.yaml`

## Input Requirements

Founder provides ONE OR MORE of:
- PDF files (carousel exports, slide decks)
- Screenshot images (PNG, JPG)
- URLs to reference posts (AI will screenshot)
- Brand guidelines / style guides

---

## Phase 1: Multi-Model Analysis

### Step 1a: Extract with Gemini Vision

Use `ai-multimodal` skill with the **latest Gemini model** for maximum accuracy:

```bash
cd /Users/jang/Desktop/Jang
python3 .agent/skills/ai-multimodal/scripts/gemini_batch_process.py \
  --task analyze \
  --input "[PATH_TO_REFERENCE_FILES]" \
  --model gemini-2.5-pro \
  --prompt "$(cat <<'EOF'
Analyze these slides for EXACT pixel-level design specifications. For EACH unique slide layout, extract:

## TYPOGRAPHY
- Font family (match to Google Fonts if possible)
- Font weight (exact: 400, 500, 600, 700, 900)
- Font size in px (measure against 1080px canvas)
- Line height (ratio)
- Letter spacing
- Color (hex)
- Text transform

## COLOR PALETTE
- Background color (sample from large areas, provide hex)
- Primary text/heading color
- Accent colors (highlight, tags, buttons)
- Card/container colors
- Shadow colors and opacity

## LAYOUT MEASUREMENTS
- Canvas dimensions
- Padding/margins (measure from edge to content)
- Spacing between elements
- Element sizes (cards, pills, buttons, icons)
- Alignment (left, center, justified)

## COMPONENTS
- Card styles (radius, shadow, border, padding)
- Button styles (radius, border, height, padding)
- Tag/pill styles
- Highlight/emphasis treatments
- Separator/divider styles
- Author/profile card details
- Icon styles and sizes

## SLIDE TYPES
- List ALL unique layout types found
- For each: name it, describe the visual hierarchy
- Note which elements are required vs optional

## ILLUSTRATION STYLE (if present)
- Color scheme (outline + fill colors)
- Stroke weight
- Style description (flat, hand-drawn, geometric, etc.)
- Background treatment

Be PRECISE with measurements. Estimate in px relative to a 1080x1080 canvas.
Provide HEX colors, not color names.
EOF
)" \
  --output /tmp/style-analysis-raw.md
```

### Step 1b: Cross-Validate Measurements

After Gemini analysis, **manually verify** critical measurements by:

1. Opening reference in Preview/browser at 100% zoom
2. Cross-checking: padding, font sizes, colors against analysis
3. Sampling colors with Digital Color Meter (macOS built-in)

**Known inaccuracy zones** (from Royal Bold experience):
- Padding: AI often underestimates by 20-40px
- Font weight: AI may say "Black" when it's actually "Regular" or "Bold"
- Colors: Similar shades get merged — always sample individually
- Line height: AI guesses poorly — measure baseline-to-baseline

### Step 1c: Identify Unique Layout Types

From the analysis, categorize ALL unique slide layouts:

| # | Layout Name | Description | Frequency |
|---|-------------|-------------|-----------|
| 1 | Cover | Hero headline + subtitle + author | Every carousel |
| 2 | Content | Numbered point + explanation | Most common |
| 3 | Bridge | Statement or illustration divider | Optional |
| ... | ... | ... | ... |
| N | CTA | Final call-to-action | Every carousel |

Priority: Build templates for layouts that appear in **every carousel** first.

---

## Phase 2: Build Design System

### Step 2a: Create visual-styles.yaml Entry

Add a new style entry to `easestart/prompts/marketing/visual-styles.yaml`:

```yaml
- id: {style-id}            # e.g. "royal-bold", "neo-brutalist"
  name: "{Style Name}"
  description: "{One-line description}"
  source: "{Reference file names}"
  creator_reference: "{Original creator if known}"

  typography:
    heading:
      font_family: "{Exact font name}"
      variants:
        hero_title: { size, weight, line_height, letter_spacing, color }
        section_heading: { ... }
        # ... one variant per heading use case
    body:
      font_family: "{Exact font name}"
      variants:
        body_text: { ... }
        # ... one variant per body use case

  palette:
    background: { primary, description }
    primary: { value, description }
    # ... all colors

  layout:
    canvas: { width, height }
    margins: { all_sides }
    spacing: { heading_to_body, body_paragraphs, section_breaks }

  visual_elements:
    # ... every component spec

  html_templates:
    path: "easestart/templates/marketing/{style-id}/"
    workflow: "/slides"
```

### Step 2b: Create base.css

Create `easestart/templates/marketing/{style-id}/base.css`:

**Checklist — every base.css MUST define:**

- [ ] CSS custom properties for ALL colors
- [ ] CSS custom properties for ALL spacing values
- [ ] `.slide` base (1080×1080, background, font-family, padding)
- [ ] Heading classes (`.t-hero`, `.t-section`, `.t-statement`, `.t-cta`)
- [ ] Body text classes (`.t-body`, `.t-body-emphasis`, `.t-intro`)
- [ ] Tag/pill classes (`.pill-tag`, `.pill-num`)
- [ ] Highlight class (`.highlight`)
- [ ] Card class (`.card`)
- [ ] Prompt box class (`.prompt-box`)
- [ ] Callout class (`.callout`)
- [ ] Author card class (`.author-card`)
- [ ] Button classes (action buttons, follow button, CTA pill)
- [ ] Utility classes (`.flex-grow`, spacing helpers)

### Step 2c: Create HTML Templates

For EACH layout type identified in Phase 1c, create `{layout-name}.html`.

**Template rules:**
- Link to `base.css` via `<link rel="stylesheet">`
- Every dynamic element needs a unique `id=""` for render.py injection
- Use semantic class names from base.css, NO inline styles
- Include `<link>` for Google Fonts used
- Canvas is always 1080×1080

**Required templates (minimum viable):**
1. `cover.html` — hero opening
2. `content.html` — numbered content
3. `cta.html` — final call-to-action

**Optional templates (add based on reference):**
4. `bridge.html` — statement/illustration divider
5. `statement.html` — highlighted quote/statement
6. `list-cards.html` — title + stacked cards
7. `comparison.html` — before/after or X vs Y

### Step 2d: Copy Author Avatar

```bash
cp easestart/templates/marketing/royal-bold/avatar.png \
   easestart/templates/marketing/{style-id}/avatar.png
```

---

## Phase 3: Render Test Carousel

### Step 3a: Create Test Data

Write a `/tmp/test-{style-id}.json` with 5 slides covering all template types.

### Step 3b: Render

```bash
cd /Users/jang/Desktop/Jang/easestart
python3 scripts/render.py \
  --slides /tmp/test-{style-id}.json \
  --style {style-id} \
  --slug test-{style-id}
```

### Step 3c: Compare with Reference

Open rendered slides side-by-side with reference material:

**Pixel-perfect checklist:**

- [ ] Padding matches reference (±5px tolerance)
- [ ] Font sizes match (±2px)
- [ ] Colors match (use Digital Color Meter to sample)
- [ ] Font weight is correct (not too bold/light)
- [ ] Highlight/emphasis treatment matches
- [ ] Card radius, shadow, border match
- [ ] Component spacing matches
- [ ] Content fills canvas appropriately (no excessive whitespace)
- [ ] Author/profile card placement matches

If ANY check fails → fix CSS/HTML → re-render → re-check.

---

## Phase 4: Finalize

### Step 4a: Confirm with Founder

Show rendered slides vs reference side-by-side. Ask:
- "Đã đủ giống reference chưa?"
- "Có element nào muốn thay đổi so với reference không?"

### Step 4b: Register Style

Verify the new style has ALL of:
- [ ] Entry in `visual-styles.yaml` with full specs
- [ ] `templates/marketing/{style-id}/base.css`
- [ ] At least 3 HTML templates (cover, content, cta)
- [ ] `avatar.png` in template directory
- [ ] Test render passes pixel-perfect checklist
- [ ] Listed in `/slides` workflow as available style

### Step 4c: Update /slides Workflow

Add the new style to the Available Styles table in `/slides`:

```markdown
| `{style-id}` | {description} | ✅ Ready |
```

---

## Lessons Learned (from Royal Bold)

> These are mistakes we made and fixed. Don't repeat them.

| Mistake | Lesson |
|---------|--------|
| Used AI's color guess (#3700FF) without sampling | Always use Digital Color Meter or pixel sampling |
| Set font weight to Black (900) — reference was Regular (400) | Cross-reference weight visually, not by AI description |
| Used 80px padding — reference was 120px | AI consistently underestimates padding by 30-50% |
| Full yellow highlight box covered text at large sizes | Use marker-underline (35% height gradient) for highlights |
| CTA was 3 text groups — reference had complex profile card | Analyze EVERY slide type, not just the obvious ones |
| Iterated 6 versions before getting close | Do thorough Phase 1 analysis to minimize iterations |
| Illustration had checkerboard background | Auto-flatten illustration bg with PIL in render.py |
| Output went to /tmp/ with no structure | Use `output/marketing/carousels/{date}-{slug}/` |

---

## Quick Command Reference

```bash
# Analyze reference with Gemini
python3 .agent/skills/ai-multimodal/scripts/gemini_batch_process.py \
  --task analyze --input "REFERENCE_FILES" --model gemini-2.5-pro

# Create template directory
mkdir -p easestart/templates/marketing/{style-id}

# Test render
python3 scripts/render.py --slides /tmp/test.json --style {style-id} --slug test

# Sample colors on macOS
# Spotlight → Digital Color Meter → hover over reference
```

---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Analysis | Multi-model extraction + cross-validate | `style-spec.md` (typography, colors, layout) | Spec covers all 6 categories |
| **2** Template Build | HTML + CSS generation | Template HTML files + `shared.css` | Templates render pixel-perfect |
| **3** Verify | Side-by-side comparison | Verification screenshots | Visual match ≥95% |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | All measurements verified + templates match reference | → Deliver templates |
| **MEDIUM** | Minor measurement uncertainty (e.g. font weight) | → Binary: A) Use best guess, B) Ask founder to confirm |
| **LOW** | Reference too low-res or ambiguous to extract | → Stop, request higher quality reference |

### Anti-Patterns
- ❌ Extracting from low-resolution screenshots — garbage in, garbage out
- ❌ Guessing measurements instead of cross-validating with multiple models
- ❌ Building templates without testing render at target resolution
- ❌ Ignoring font licensing — extracted fonts may not be available
