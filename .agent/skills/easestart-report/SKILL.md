---
name: easestart-report
description: "Intel Memo report design system, personalization rules, copy template protocol, and UX psychology rules. MANDATORY for any report generation or modification."
---

# EaseStart Report Skill

> Rules for generating and modifying the Founder's Intel Memo HTML report.
> Any code change to `generate_report.py` or `shared.css` MUST follow these rules.

---

## 1. Design System — Monochrome Only

| Token | Value | Usage |
|-------|-------|-------|
| `var(--black)` | #000000 | Headings, major borders, active states, copy block bg |
| `var(--white)` | #FFFFFF | Body bg, copy block text, button hover fill |
| `var(--slate)` | #4E4B66 | Secondary text, labels, AVOID THIS column |
| `var(--border)` | #E0E0E0 | Row dividers, grid borders |
| `var(--bg-muted)` | #FAFAFA | Muted bg (bad examples, expand content) |
| `var(--bg-code)` | #F5F5F5 | Code/mono backgrounds |
| `var(--accent)` | #22C55E | Scorecard total bar ONLY |

**FORBIDDEN:**
- No green/red for do/don't columns
- No colored backgrounds (except `--bg-muted`)
- No purple, no gradients, no shadows
- No border-radius (except subtle on buttons)
- No animations (only `transition: 0.15s`)

---

## 2. No Emojis in Rendered HTML

All labels use **uppercase text**. Never use emojis in the report HTML.

| Wrong | Correct |
|-------|---------|
| ✅ Do This | **DO THIS** |
| ❌ Avoid This | **AVOID THIS** |
| 📋 Actionable Template | Actionable Template |
| 💡 insight | insight (no prefix) |
| 🔗 Link | Link (underline only) |
| 📋 Copy / ✅ Copied! | **COPY** → **COPIED** |

**Exception:** Emojis ARE allowed inside copy template content only (social media posts need them for platform optimization).

---

## 3. Typography System

| Element | Font | Size | Weight | Transform |
|---------|------|------|--------|-----------|
| Page title | `var(--heading)` Barlow Condensed | 56px | 700 | UPPERCASE |
| Section heading (h2) | `var(--heading)` | 36px | 700 | UPPERCASE |
| Sub-heading (h3) | System | 22px | 700 | — |
| Section label (h4) | System | 14-16px | 700 | UPPERCASE + letter-spacing 2px |
| Body text (p) | `var(--sf)` | 20px | 400 | — |
| Data/table text | `var(--sf)` | 18px | 400 | — |
| Small labels | `var(--sf)` | 13px | 400 | — |
| `dlv-label` | `var(--sf)` | 11px | 700 | UPPERCASE + letter-spacing 2px |
| Copy blocks | `var(--mono)` SF Mono | 13px | 400 | — |

---

## 4. Component Patterns

### Do/Don't Grid (`.dlv-pair`)
- Two-column grid, no gap, single `var(--border)` border
- DO column: `var(--black)` label, right border divider
- AVOID column: `var(--slate)` label, no background
- Labels: `<strong>` 11px uppercase

### Examples (`.dlv-example`)
- Good: 3px left-border `var(--black)`, white bg
- Bad: 3px left-border `var(--slate)`, `var(--bg-muted)` bg
- No emoji prefixes. No colored backgrounds.

### Copy Blocks (`.dlv-copy-block`)
- Background: `var(--black)`, Text: `var(--white)`
- Font: `var(--mono)`, 13px, line-height 1.7
- `padding-right: 80px` for COPY button clearance
- Max-height: 320px, `overflow-y: auto`
- COPY button: absolute top-right, transparent bg, `var(--white)` border/text
- Hover: inverts to `var(--white)` bg, `var(--black)` text
- Click: "COPY" → "COPIED" (1.5s reset)

### Expand Button (`.expand-btn`)
- Dashed border, `var(--slate)` text
- Hover: solid `var(--black)` border + text
- Text: "Actionable Template ▾" (no emoji)

### Section Borders
- Major: `3px solid var(--black)` (scorecard, stage-bar, sources)
- Rows: `1px solid var(--border)`
- Citations: black circle 20×20px, `var(--mono)` number

---

## 5. Personalization Protocol

All content in `get_question_guides(idea, industry)` uses f-strings with derived variables:

```python
short   = idea.split(" for ")[0]       # "AI startup advisor"
target  = idea.split(" for ")[1]       # "overwhelmed solo founders"
ind     = industry.title()             # "Devtools"
problem = f"not having a reliable {short.lower()}"  # derived problem
```

### Rules
- Every step, do/don't, and example MUST reference `{short}`, `{target}`, or `{problem}`
- No generic advice: "your product" → `{short}`, "your users" → `{target}`
- Copy template content must be ready-to-use, not placeholder-filled
- Only acceptable brackets: `[your-carrd-url]`, `[your-email]`, `[your name]`, `[rate]`, `[hours]` — things only the founder knows

### Fallback Priority
1. Search KB with `deliverable_query` → use top 3 results
2. If KB gaps → fill from `get_question_guides()` (personalized)
3. Never show empty deliverables

---

## 6. Platform-Ready Copy Templates

10 questions include `copy` field with content optimized per platform:

| Stage | Copy Templates |
|-------|---------------|
| 0 Pre-Idea | Reddit post, Twitter/X thread, Discord message, Interview script |
| 1 Ideation | TAM calculator spreadsheet template |
| 2 Validation | Landing page headline+CTA, Community validation post |
| 3 MVP | User research DM |
| 4 PMF | Churn interview email, Sean Ellis PMF survey, Unit economics tracker |
| 5 Growth | Discord community welcome message |
| 6 Scale | Job post template |

### Adding New Copy Templates
```python
"copy": [
    ("Platform Name", f"""Content here using {short}, {target}, {problem}.
Line 2 with more content.
All variables are f-string interpolated."""),
]
```

Content must be:
- Platform-optimized (Reddit = question format, Twitter = thread with hooks, Discord = casual)
- Complete — founder copies and posts immediately
- Personalized — uses `{short}`, `{target}`, `{problem}`, `{ind}`

---

## 7. UX Psychology (CEO Reader)

Non-technical founders are the primary audience. Apply these principles:

| Principle | Application |
|-----------|-------------|
| **Information Gap** (Loewenstein) | Every score has explanation + benchmark |
| **Cognitive Load** (Sweller) | Zero jargon. All codes → plain language. Max 3 concepts/section |
| **Action Paralysis** (Schwartz) | Every insight has a concrete next step |

### 12 UX Rules

1. No codenames — `domain_label()` translates internal codes
2. Every question has expandable action steps
3. Scores have "Why?" explanations
4. Benchmarks show average vs top 10% founders
5. Citations show hover tooltip "Click for source"
6. Drawer uses readable field names
7. Insights have plain-language explanations
8. Stage bar explains sequential progression
9. Warnings use CEO language ("Common mistakes", not "Anti-patterns")
10. Sources section has introductory sentence
11. Questions section has guidance subtitle
12. Knowledge table uses "Source" not "Domain"

---

## 8. Layout Constraints

- Sidebar: 240px fixed, `var(--black)` background
- Main: `margin-left: 240px`, `max-width: 1000px`, `padding: 50px 73px`
- Section gaps: 48px (h2 margin-top)
- No border-radius (except copy block buttons)
- No shadows anywhere
- No animations except `transition: 0.15s`
- Responsive: sidebar hidden at ≤900px

---

## Quick Reference

| File | Purpose |
|------|---------|
| `scripts/generate_report.py` | Report generator: all HTML, scoring, KB search |
| `output/shared.css` | Design tokens + all component styles |
| `get_question_guides()` | Personalized fallback content (21 questions) |
| `build_deliverable()` | KB search + fallback + copy template rendering |
| `build_scorecard()` | 5-dimension scoring with explanations |
| `CitationRegistry` | Source tracking + drawer data |
