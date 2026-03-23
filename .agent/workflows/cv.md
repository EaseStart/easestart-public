---
description: Full CV lifecycle — tailor content, build HTML, verify consistency, export PDF. Lucius 4-phase pipeline for Jang Trinh's multi-role CV system.
---

# CV Pipeline Workflow

4-phase pipeline modeled after Lucius theory. Each phase produces a specific artifact, loads the right skills, and requires verification before advancing.

**Pipeline:** `Research → Tailor → Build → Export`

**Entry at any phase:** If earlier artifacts already exist, start at the next phase.

---

## Phase 1: RESEARCH → Understand the Target Role

> **Trigger:** "new CV for [role]", "tailor CV for [title]", "CV cho vị trí [X]"
> **Output:** Role analysis + tailoring strategy
> **Gate:** User confirms strategy before writing content.

### Load Skills
// turbo
```bash
brv query "CV content strategy role tailoring"
```
- Read `cv-pipeline/SKILL.md` — canonical profile data, content rules, recognition items
- Read `CV-html/DS-Foundations.md` — design tokens

### World-Class Research Protocol (Lucius Neural Propagation)

> Source: Lucius theory — hướng loang ban đầu quyết định chất lượng.

| Step | Action | Output |
|------|--------|--------|
| **① Benchmark** | What does a world-class CV for this role look like? Find exemplars (FAANG hires, top consultants, recognized leaders). Not average — find the BEST | Best-in-class CV patterns + what makes them memorable |
| **② First Principles** | What does the hiring manager ACTUALLY need to see? Strip away conventions. What is the ROOT signal they're looking for? | 1-sentence hiring signal (e.g., "Proof of shipping AI at scale") |
| **③ Proven Frameworks** | What CV/content frameworks work at scale? XYZ formula? STAR? Accomplishment-based storytelling? | Framework selection + rationale |
| **④ Cross-Domain** | What can we steal from other domains? Sales pitches? Consulting proposals? Product briefs? | 1+ cross-domain insight to differentiate |
| **⑤ Trade-offs** | What do we emphasize vs de-emphasize? What experience is most vs least relevant? Deliberate framing choices. | Trade-off table: emphasize X, de-emphasize Y, because Z |
| **⑥ Executability** | Does the tailoring strategy fit within the 2-page constraint? Are all claims backed by real data from canonical profile? | Adjusted strategy within constraints |

### Actions
1. **Role Signal Analysis:** What is the ONE thing this role needs to see?
2. **Experience Reframing Map:** For each role in career history, how should bullets be reframed?
3. **Impact Banner Prioritization:** Which 10 metrics from canonical profile are most relevant?
4. **Competency Grid Design:** Which 3 columns of skills should appear?

### Anti-Patterns
- ❌ Don't fabricate metrics — only use data from `cv-pipeline/SKILL.md` Canonical Profile
- ❌ Don't skip trade-offs — you CAN'T emphasize everything equally
- ❌ Don't benchmark average CVs — find the absolute best in the target role's industry

---

## Phase 2: TAILOR → Write Markdown Content

> **Trigger:** "write markdown", "draft content", "tailor content"
> **Prerequisite:** Phase 1 strategy approved (or role is already well-understood).
> **Output:** `CV-md/Jang2026_{Role_Name}.md`
> **Gate:** User reviews markdown content.

### Load Skills
- Read `cv-pipeline/SKILL.md` — XYZ formula, FAANG power verbs, role tailoring strategy
- Check existing CVs for consistency: `grep -rn "KEY_METRIC" CV-md/`

### Actions
1. **Write summary paragraph:** Role-specific framing of career narrative (3-4 sentences max).
2. **Write experience bullets:** XYZ formula + FAANG verbs. Each bullet = verb + action + result.
3. **Order by relevance:** Most relevant experience for THIS role goes first, not chronologically.
4. **Write skills section:** Tailored to role, grouped by domain (3 groups).
5. **Write recognition section:** Same 8 items across all roles (from canonical data).

### Naming Convention
```
CV-md/Jang2026_{Role_With_Underscores}.md
```

### Anti-Patterns
- ❌ Don't copy bullets verbatim from other CVs — reframe each one for the target role
- ❌ Don't exceed 2 pages worth of content — be ruthlessly selective
- ❌ Don't use passive voice — every bullet starts with a power verb

---

## Phase 3: BUILD → Generate HTML

> **Trigger:** "build HTML", "tạo HTML", "generate page"
> **Prerequisite:** Markdown CV exists in `CV-md/`.
> **Output:** `CV-html/{role-folder}/v2-modern.html`
> **Gate:** Visual inspection in browser.

### Load Skills
- Read `cv-pipeline/SKILL.md` — design system, file registry
- Read `CV-html/DS-Foundations.md` — full token reference
- Reference an existing v2-modern HTML as template: `CV-html/principal-product-designer/ppd-v2-modern.html`

### v2-modern Layout Blueprint

```
┌──────────────── 1811px ────────────────┐
│ ████████████████████████████████████████│  ← BLACK HEADER
│ █  JANG TRINH                          │    56px DIN, uppercase
│ █  [Role Title]           [links]      │    30px SF Pro
│ ████████████████████████████████████████│
│ ████████████████████████████████████████│  ← IMPACT BANNER
│ █  [Metric] [Metric] [Metric] [×5]    │    2×5 grid, metric-card
│ █  [Metric] [Metric] [Metric] [×5]    │    44px DIN value, 18px label
│ ████████████████████████████████████████│
│                                        │
│  Summary paragraph (28px, max-w 1400)  │  ← SUMMARY SECTION
│  Core Capabilities (22px, slate)       │
│  ─────────────────────────────────── │
│                                        │
│  EXPERIENCE (56px DIN, uppercase)      │  ← EXPERIENCE
│  ● EaseUI — [subtitle]    [dates]     │    timeline-item with dots
│    │ Sub-Section Title                 │    sub-section (border-left 3px)
│    │ — Bullet point with XYZ result   │    28px body
│    │ — Bullet point with XYZ result   │
│  ● Elfie — [subtitle]     [dates]     │
│    │ Sub 1                            │
│    │ Sub 2                            │
│  ● HDBank...                          │
│  ● Home Credit...                     │
│  ─────────────────────────────────── │
│                                        │
│  CORE COMPETENCIES (56px DIN)         │  ← COMPETENCIES
│  [Col 1]      [Col 2]      [Col 3]   │    3-column grid
│  ─────────────────────────────────── │
│                                        │
│  RECOGNITION (56px DIN)               │  ← RECOGNITION
│  ★ Item 1          ★ Item 2          │    2×4 grid
│  ★ Item 3          ★ Item 4          │
│  ─────────────────────────────────── │
│                                        │
│  BSc, Computer Science · Singapore    │  ← EDUCATION FOOTER
└────────────────────────────────────────┘
```

### Folder Naming Convention
```
CV-html/{role-in-kebab-case}/v2-modern.html
```

### HTML Technical Requirements
| Requirement | Details |
|-------------|---------|
| **CDN** | Tailwind CSS via `cdn.tailwindcss.com` |
| **Fonts** | DIN Condensed via cdnfonts.com, SF Pro Display via cdnfonts.com |
| **Print CSS** | `@media print { print-color-adjust: exact; }` |
| **Max Width** | `max-w-[1811px]` on outer container |
| **Padding** | `px-[73px]` on all sections |
| **Company links** | Per canonical data in cv-pipeline skill |

### Anti-Patterns
- ❌ Don't use arbitrary colors — only #000, #FFF, #4E4B66
- ❌ Don't add shadows — flat design only
- ❌ Don't skip the Impact Banner — it's the visual anchor
- ❌ Don't change the 8-item Recognition section — it's standardized

---

## Phase 4: EXPORT → Generate PDF

> **Trigger:** "export PDF", "tạo PDF", `/export-pdf`
> **Prerequisite:** HTML file exists in `CV-html/`.
> **Output:** `CV-pdf/Jang_Trinh_{Role_Name}.pdf`
> **Gate:** PDF must be exactly 2 pages.

### Load Skills
- Read `/export-pdf` workflow — Playwright script, page sizes, troubleshooting

### Execute
// turbo-all

1. **Install dependencies** (if needed):
```bash
cd /tmp && npm install playwright && npx playwright install chromium
```

2. **Add new CV to the export script** (if not already registered):
   - v2-modern → `h: '2560px'`
   - v1-classic → `h: '2800px'`

3. **Run export**:
```bash
cd /tmp && node export-cv-pdf.mjs
```

4. **Verify page count**:
```bash
cd /Users/jang/Desktop/Jang/CV-pdf && for f in *.pdf; do echo "$f: $(mdls -name kMDItemNumberOfPages "$f" | awk '{print $3}') pages"; done
```

### Page Count Troubleshooting

| Pages | Action |
|-------|--------|
| 2 ✅ | Done |
| 3+ | Increase page height: `2560px` → `2700px` → `2800px` → `2900px` |
| 1 | Content too short — add more bullets or increase section spacing |
| Blank | Check `file://` path. Ensure HTML file exists. |

### Anti-Patterns
- ❌ Don't skip `printBackground: true` — black headers will render white
- ❌ Don't forget `document.fonts.ready` — DIN Condensed needs time to load
- ❌ Don't generate PDFs without verifying page count — ALWAYS check

---

## Quick Reference

| Phase | Trigger | Output | Skills | Gate |
|-------|---------|--------|--------|------|
| **1. Research** | "new CV for [role]" | Role analysis | cv-pipeline, DS-Foundations | User confirms strategy |
| **2. Tailor** | "tailor content" | `CV-md/Jang2026_*.md` | cv-pipeline (XYZ, verbs) | User reviews markdown |
| **3. Build** | "build HTML" | `CV-html/*/v2-modern.html` | cv-pipeline, DS-Foundations | Browser inspection |
| **4. Export** | "export PDF", `/export-pdf` | `CV-pdf/Jang_Trinh_*.pdf` | export-pdf workflow | 2-page verification |

## Batch Operations

### Update All CVs (e.g., date change, metric change)
```bash
# 1. Find all instances
grep -rn "OLD_VALUE" CV-html/ CV-md/

# 2. Replace in all HTML
find CV-html -name "*.html" -exec sed -i '' 's/OLD_VALUE/NEW_VALUE/g' {} +

# 3. Replace in all Markdown
find CV-md -name "*.md" -exec sed -i '' 's/OLD_VALUE/NEW_VALUE/g' {} +

# 4. Re-export all PDFs
cd /tmp && node export-cv-pdf.mjs

# 5. Verify
grep -rn "OLD_VALUE" CV-html/ CV-md/  # Should return nothing
```

### Add a New Role
1. Phase 1: Research → define tailoring strategy
2. Phase 2: Tailor → `CV-md/Jang2026_{Role}.md`
3. Phase 3: Build → `CV-html/{role-kebab}/v2-modern.html`
4. Phase 4: Export → add to script → `CV-pdf/Jang_Trinh_{Role}.pdf`
5. Update `cv-pipeline/SKILL.md` file registry

---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Research | Target role analysis + JD parsing | Role brief + keyword map | Clear role requirements understood |
| **2** Tailor | Content writing (XYZ formula + FAANG verbs) | Markdown CV file | Content aligns with role keywords |
| **3** Build | HTML generation from design system | HTML CV page | Matches `DS-Foundations.md` tokens |
| **4** Verify | Consistency + cross-reference check | Verification report | No contradictions across formats |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | Content tailored + HTML matches design system + no contradictions | → Ready for /export-pdf |
| **MEDIUM** | Content good but minor formatting issues | → Binary: A) Export as-is, B) Fix formatting |
| **LOW** | Role requirements unclear or content generic | → Stop, return to Phase 1 research |

### Anti-Patterns
- ❌ Generic bullets without XYZ formula (did X, measured by Y, achieved Z)
- ❌ Same CV for all roles — each role needs tailored content
- ❌ HTML that doesn't match design system tokens — visual consistency matters
- ❌ Contradicting metrics across CV versions (e.g., "3M downloads" in one, "2M" in another)
