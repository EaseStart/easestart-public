---
description: "Generate a multi-page HTML Intel Memo report — CEO-grade idea validation with tailored content per startup stage (0-6). Lucius 4-Phase compliant."
---

# /generate-report — Founder's Intel Memo

> Generate a beautiful multi-page HTML report with stage-specific insights, citations, interactive detail drawer, and confidence scores.

---

## When to Use

- After completing a validation session with any agent
- After a `/validate-idea` workflow completes (Step 9)
- When founder asks to "see my report" or "export results"
- At end of session when orchestrator auto-suggests (Session Closing Protocol 2d)
- When founder wants to share progress with co-founders/advisors

## Prerequisites

- Founder has identified their startup idea (even rough)
- Industry detected or specified

---

## Phase 1: COLLECT → Gather Inputs (Lucius L2)

> Output: idea + industry confirmed
> Gate: Both inputs available

```
REQUIRED: idea (one sentence describing the startup)
OPTIONAL: industry (auto-detected if omitted)

ASK: "What's your startup idea in one sentence?"
IF industry unknown → Auto-detect from idea text
```

### Anti-Patterns (Lucius L4)
- ❌ Generating report without confirming idea text with founder
- ❌ Assuming industry without checking auto-detection result
- ❌ Generating before any validation work has been done (Stage 0 with no sessions)

---

## Phase 2: GENERATE → Build Report (Lucius L2)

> Output: output/{YYYY-MM-DD}-{slug}/ (9 files)
> Skills: core.py (BM25 search), validate_idea.py (scoring)
> Gate: All 9 files generated without errors

### Auto-Research Quality Gate (autoresearch)

> 🔬 **Auto-trigger:** Before generating, verify knowledge quality for report accuracy.

// turbo
```bash
python3 autoresearch/evaluate.py 2>&1 | grep "^score:\|^coverage:"
```

```
IF score < 90:
  → WARNING: "Knowledge base score is {score}. Report quality may be affected."
  → Binary: A) Run /autoresearch sprint first (recommended), B) Generate anyway
IF score ≥ 90:
  → Auto-proceed to generation
```

// turbo
```bash
python3 scripts/generate_report.py "{idea}" --industry {industry} --open
```

### What Gets Generated

```
output/{YYYY-MM-DD}-{slug}/
├── index.html              ← Hub (overview + 7 stage cards + methodology)
├── shared.css              ← Workshop design tokens
└── stages/
    ├── stage-0-pre-idea.html   ← psychology, reasoning, frameworks
    ├── stage-1-ideation.html   ← casestudies, industries, reasoning
    ├── stage-2-validation.html ← playbook, landing, content, resources
    ├── stage-3-mvp.html        ← tools, anti-patterns, templates, pricing
    ├── stage-4-pmf.html        ← metrics, pricing, channels, playbook
    ├── stage-5-growth.html     ← channels, community, email, content, ops
    └── stage-6-scale.html      ← team, equity, contracts, legal, finance
```

### Report Features

| Feature | Description |
|---------|-------------|
| **Sidebar navigation** | Fixed left nav linking all 7 stages + Hub |
| **Stage indicator bar** | Clickable 7-dot bar, active stage highlighted |
| **Knowledge Coverage** | Domain table with BM25 search results per stage |
| **Stage Questions** | 3 tailored questions per stage (not generic) |
| **Anti-patterns** | Stage-specific warnings from knowledge base |
| **Scorecard** | 5-dimension confidence score with progress bars |
| **Citations** | Numbered `(1) (2)...` markers next to conclusions |
| **Detail Drawer** | Click citation → right panel with full source data |
| **Sources section** | Bottom-of-page citation index with domains + confidence |
| **Bottom nav** | ← Previous Stage / Next Stage → |

### Citation System (Lucius L5 — Source Attribution)

Every data point includes:
- **Citation marker** `(n)` — black circle, clickable
- **Source domain** — which CSV the data comes from
- **Confidence level** — HIGH/MEDIUM/LOW based on BM25 score
- **Full data fields** — all columns from the CSV row
- **Query** — the exact search query that found this result

> ⚠️ **Lucius guard:** Reports without citations violate L5 (always cite source). The CitationRegistry class enforces this automatically.

---

## Phase 3: VERIFY → Quality Check (Lucius L5)

> Gate: Report passes ALL verification checks before delivery.

### 3a. File Integrity

```
VERIFY:
  1. All 9 files exist in output/{YYYY-MM-DD}-{slug}/
  2. Each stage page has ≥3 citations
  3. Hub page shows correct avg score
  4. Sidebar navigation works (all links valid)
  5. Stage bar highlights correct active stage
  6. Citation drawer opens and closes correctly
```

### 3b. Ground Rules Verification (MANDATORY)

> Run these checks EVERY time a report is generated. If any fail, fix before delivery.

// turbo
```bash
OUT="output/{YYYY-MM-DD}-{slug}"

echo "=== 1. NO GENERIC PLACEHOLDERS ==="
grep -rn '\[the problem\]\|\[problem\]\|\[pain point\]\|\[desired outcome\]\|\[specific\]\|\[name\]' "$OUT/stages/" | wc -l
# MUST be 0. If > 0 → fix in get_question_guides()

echo "=== 2. NO 'ANSWER THIS YOURSELF' ==="
grep -rn "Answer this yourself" "$OUT/stages/" | wc -l
# MUST be 0. Every question needs an AI-generated insight.

echo "=== 3. PERSONALIZATION (idea appears in output) ==="
grep -c "{idea_keyword}" "$OUT/stages/stage-0-*.html"
# MUST be > 0. Content must reference the founder's actual idea.

echo "=== 4. NO EMOJIS IN HTML LABELS ==="
grep -Pn '✅|❌|📋|💡|🔗' "$OUT/stages/stage-0-*.html" | grep -v 'dlv-copy-block' | wc -l
# MUST be 0. Emojis only allowed INSIDE copy template blocks.

echo "=== 5. COPY BUTTONS PRESENT ==="
for s in 0 1 2 3 4 5 6; do
  f=$(ls "$OUT/stages/stage-${s}-"*.html)
  copies=$(grep -c 'dlv-copy-btn' "$f")
  echo "  Stage $s: $copies copy buttons"
done
# Stages with copy templates must have ≥1 copy button.

echo "=== 6. BUTTON TEXT CONSISTENT ==="
grep -rn "How do I do this" "$OUT/" | wc -l
# MUST be 0. All buttons should say "Actionable Template".

echo "=== 7. CONTENT COVERAGE ==="
for s in 0 1 2 3 4 5 6; do
  f=$(ls "$OUT/stages/stage-${s}-"*.html)
  steps=$(grep -c 'dlv-steps' "$f")
  pairs=$(grep -c 'dlv-pair' "$f")
  insights=$(grep -c 'q-insight' "$f")
  echo "  Stage $s: steps=$steps do-dont=$pairs insights=$insights"
done
# Every stage MUST have: steps ≥ 3, do-dont ≥ 3, insights ≥ 3
```

### 3c. Design System Check

| Check | Expected | Fail Action |
|-------|----------|-------------|
| Colors only from DS tokens | `--black`, `--white`, `--slate`, `--border`, `--bg-muted` | Remove any hardcoded colors |
| No emojis in labels | Uppercase text only | Replace with text |
| No border-radius | Only on copy buttons | Remove |
| No shadows | Zero `box-shadow` | Remove |
| Copy blocks use `var(--black)` bg | Dark bg, white text, mono font | Fix in shared.css |
| COPY button visible | Top-right, absolute positioned | Fix z-index/position |

### 3d. Confidence Protocol

| Condition | Action |
|-----------|--------|
| ≥90% knowledge coverage | Auto-deliver to founder |
| 70-89% coverage | Deliver with caveat: "Some stages have limited data" |
| <70% coverage | Stop — inform founder KB may be incomplete |

---

## Phase 4: DELIVER → Present to Founder

```
TELL FOUNDER:
  "Intel Memo generated: output/{folder-name}/
   
   What's inside:
   • 7 stage pages — every question answered by AI with personalized insights
   • Actionable Templates — step-by-step + ready-to-copy content for Reddit, Twitter, Discord, email
   • COPY button on every template — click to copy, paste and post
   • Click numbered citations (1)(2)(3) for source details
   
   Open index.html in your browser to start at your current stage."
```

### Anti-Patterns (Lucius L4)
- Generating report and NOT telling founder about copy templates
- Delivering report without mentioning which stage the founder should start at
- Showing "Answer this yourself" instead of providing an AI-generated insight
- Using emojis in report labels
- Leaving generic `[placeholder]` brackets in copy content
- Not offering to re-run after founder has done more work

---

## Giantiny Philosophy Lens (Pillar Check)

Each report automatically checks against 5 Giantiny pillars:

| Pillar | How Report Addresses It |
|--------|----------------------|
| ① Customer Zero | Stage 0-1 questions ask "Is this YOUR problem?" |
| ② Counter-Positioning | Stage 1-2 questions ask competitive differentiators |
| ③ Code + Media Leverage | Stage 3 domains include tools, anti-patterns for 1-person ops |
| ④ Profit > Growth | Stage 4-5 ask unit economics before growth channels |
| ⑤ Micro-MOATs | Stage 6 guides toward network effects, data moats, brand |

---

## UX Psychology Rules (MANDATORY)

> Non-technical CEOs are the primary readers. Every element must be immediately understandable.

### 3 Core Principles

| Principle | Application |
|-----------|-------------|
| **Information Gap** (Loewenstein) | Every score MUST have explanation + benchmark. CEO needs to know "why?" and "compared to what?" |
| **Cognitive Load** (Sweller) | Zero jargon. All internal codes translated to plain language. Max 3 concepts per section. |
| **Action Paralysis** (Schwartz) | Every insight MUST have a concrete next step. Never show a problem without a solution. |

### 12 UX Rules for Report Content

| # | Rule | Implementation |
|:-:|---|---|
| 1 | **No codenames in UI** | `domain_label()` translates: `mkt_landing` → "Landing Pages", `fin_economics` → "Unit Economics" |
| 2 | **Every question has action steps** | `Actionable Template ▾` expandable with specific numbered steps |
| 3 | **Scores have "Why?" explanation** | `score_explanations{}` dict provides reason + action per dimension |
| 4 | **Benchmark context for scores** | Bottom of scorecard shows: "Average founder: 62/100 · Top 10%: 88+" |
| 5 | **Citations hint they're clickable** | Hover tooltip: "Click for source" via CSS `::after` |
| 6 | **Drawer uses readable field names** | `FIELD_LABELS` map: `Dont` → "Avoid This", `Example_Good` → "Good Example" |
| 7 | **Insights have plain explanations** | `.q-explain` shows "Counter-Positioning: creating models big players can't copy" |
| 8 | **Stage bar explains progression** | `.stage-note`: "Stages are sequential. Complete exit criteria before advancing." |
| 9 | **Warnings section = CEO language** | "Common mistakes at this stage" not "Anti-patterns for Stage 2" |
| 10 | **Sources have intro text** | "These are the data sources behind every recommendation above." |
| 11 | **Questions section has guidance** | Subtitle: 'Click "How do I do this?" for action steps.' |
| 12 | **Knowledge table = "Source" not "Domain"** | Column header says "Source" not "Domain", "Top Finding" not "Top Result" |

### Adding New Questions (Template)

When adding questions to `stage_questions{}`, each tuple MUST have 4 elements:

```python
(label, question, insight_query, deliverable_query)
#  ↑        ↑          ↑              ↑
#  Short   The CEO    Query for      Query for build_deliverable()
#  name    question   insight line   → pulls Steps/Do/Don't/Examples from KB
```

Example:
```python
("Revenue Model", "How will you make money?",
 "pricing strategy revenue model",        # → insight
 "pricing strategy subscription freemium")  # → deliverable template
```

### Actionable Deliverables Rule

> **Principle: Everything we suggest = actionable items. CEO copies and executes.**

`build_deliverable()` automatically:
1. Searches KB with `deliverable_query` (top 3 results)
2. Extracts: Steps → Do/Don't → Examples → Key Concepts → URLs
3. Personalizes: `{short}`, `{target}`, `{ind}` → founder's actual idea/industry
4. Deduplicates: `seen_content` set prevents repeats
5. Falls back to `get_question_guides()` if KB gaps exist
6. Renders platform-ready copy templates where applicable

Output structure:
```
Actionable Template ▾
├── Step-by-Step (numbered, personalized to idea)
├── DO THIS / AVOID THIS (side-by-side bordered grid)
├── Real Examples: Good vs Bad (black/slate left-border)
├── Key Concepts (bullet list)
├── Source Link
└── [Platform] — READY TO COPY (black code block + COPY button)
```

### Platform-Ready Copy Templates

10 questions include `copy` field with pre-written content optimized per platform:

| Stage | Templates |
|-------|----------|
| 0 (Pre-Idea) | Reddit post, Twitter/X thread, Discord message, Interview script |
| 1 (Ideation) | TAM calculator template |
| 2 (Validation) | Landing page headline+CTA, Community validation post |
| 3 (MVP) | User research DM |
| 4 (PMF) | Churn interview email, Sean Ellis survey email, Unit economics tracker |
| 5 (Growth) | Discord welcome message |
| 6 (Scale) | Job post template |

Copy blocks render as:
- `.dlv-copy-block`: `var(--black)` background, `var(--white)` text, `var(--mono)` font
- `.dlv-copy-btn`: COPY button top-right, inverts on hover
- Label: `{platform} — READY TO COPY` (uppercase)

### Adding New Score Dimensions

When modifying `build_scorecard()`, every dimension MUST have:
```python
"Dimension Name": {
    "low": ("Why it's low (description)", "What to do about it (action)"),
    "high": ("Why it's high (description)", "What to do next"),
}
```

---

## Report Design Rules (MANDATORY)

> Every visual element must adhere to these rules. No exceptions.

### Rule 1: Monochrome Only

| Token | Value | Usage |
|-------|-------|-------|
| `var(--black)` | #000000 | Headings, borders, active states, copy block bg |
| `var(--white)` | #FFFFFF | Body bg, copy block text, button hover |
| `var(--slate)` | #4E4B66 | Secondary text, labels, "AVOID THIS" column |
| `var(--border)` | #E0E0E0 | Row dividers, grid borders |
| `var(--bg-muted)` | #FAFAFA | Muted backgrounds (bad example, expand content) |
| `var(--bg-code)` | #F5F5F5 | Code/mono backgrounds |
| `var(--accent)` | #22C55E | Scorecard total bar only (nowhere else) |

**Forbidden:** No green/red for do/don't. No colored backgrounds (except `--bg-muted`). No purple. No gradients.

### Rule 2: No Emojis in Rendered HTML

All labels use **uppercase text**, never emojis:

| Wrong | Correct |
|-------|---------|
| ✅ Do This | **DO THIS** |
| ❌ Avoid This | **AVOID THIS** |
| 📋 Actionable Template | Actionable Template |
| 💡 insight | insight (no prefix) |
| 🔗 Link | Link (underline only) |
| 📋 Copy | **COPY** → **COPIED** |

**Exception:** Emojis are allowed ONLY inside copy template content (social media posts need them for platform optimization).

### Rule 3: Typography System

| Element | Font | Size | Weight | Transform |
|---------|------|------|--------|-----------|
| Page title | `var(--heading)` Barlow Condensed | 56px | 700 | UPPERCASE |
| Section heading | `var(--heading)` | 36px | 700 | UPPERCASE |
| Sub-heading | System | 22px | 700 | — |
| Section label | System | 14px/11px | 700 | UPPERCASE + letter-spacing 2px |
| Body text | `var(--sf)` SF Pro Rounded | 20px | 400 | — |
| Data/table text | `var(--sf)` | 18px | 400 | — |
| Small labels | `var(--sf)` | 13px | 400 | — |
| `dlv-label` | `var(--sf)` | 11px | 700 | UPPERCASE + letter-spacing 2px |
| Copy blocks | `var(--mono)` SF Mono | 13px | 400 | — |

### Rule 4: Component Patterns

**Do/Don't Grid (`.dlv-pair`)**
- Two-column grid, no gap, single `var(--border)` border
- DO column: `var(--black)` label, right border divider
- AVOID column: `var(--slate)` label, no background
- Labels are `<strong>` with 11px uppercase

**Examples (`.dlv-example`)**
- Good: 3px left-border `var(--black)`, white background
- Bad: 3px left-border `var(--slate)`, `var(--bg-muted)` background
- No emoji prefixes, no colored backgrounds

**Copy Blocks (`.dlv-copy-block`)**
- Background: `var(--black)`, Text: `var(--white)`
- Font: `var(--mono)`, Size: 13px, Line-height: 1.7
- `padding-right: 80px` to make room for COPY button
- Max-height: 320px with overflow scroll
- COPY button: absolute top-right, transparent bg, `var(--white)` border/text
- Button hover: `var(--white)` bg, `var(--black)` text
- Click: text changes to COPIED, resets after 1.5s

**Expand Button (`.expand-btn`)**
- Dashed border, `var(--slate)` text
- Hover: solid `var(--black)` border + text
- Inside text: "Actionable Template ▾" (no emoji)

**Section Borders**
- Major sections: `3px solid var(--black)` (scorecard, stage-bar, sources)
- Data rows: `1px solid var(--border)`
- Citations: black circle `20×20px`, `var(--mono)` number

### Rule 5: Personalization

All content in `get_question_guides(idea, industry)` uses f-strings:
- `{short}` → idea name (before "for"): e.g., "AI startup advisor"
- `{target}` → target audience (after "for"): e.g., "overwhelmed solo founders"
- `{ind}` → industry title: e.g., "Devtools"

Every step, do/don't, and example must reference the founder's specific idea. No generic advice.

### Rule 6: Layout Constraints

- Sidebar: 240px fixed, `var(--black)` background
- Main: `margin-left: 240px`, `max-width: 1000px`, `padding: 50px 73px`
- Section gaps: 48px (h2 margin-top)
- No border-radius except copy block buttons (subtle)
- No shadows anywhere
- No animations except transitions (0.15s)

---

## Output Artifacts

- `output/{YYYY-MM-DD}-{slug}/index.html` — Hub page
- `output/{YYYY-MM-DD}-{slug}/shared.css` — Design system (copied)
- `output/{YYYY-MM-DD}-{slug}/stages/stage-{0-6}-{name}.html` — Stage pages
