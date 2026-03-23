---
description: "Generate HVS-style single-page validation report with auto-research — deep KB search + Reddit/HN pain signals."
---

# /generate-validation-report — HVS-style Validation Report

> Single-page HTML report with auto-research. Runs after `/validate-idea` passes or on-demand.

---

## When to Use

- After `/validate-idea` scores ≥ 72 (GO verdict)
- When founder says "build report" or "generate report"
- When sharing validation results with co-founders/investors
- As final deliverable before starting MVP development

## Prerequisites

- Startup idea (one sentence)
- Industry (auto-detected if omitted)
- Optional: enrichment JSON with AI-synthesized content

---

## Phase 1: GENERATE (Auto-research + Build)

> The script auto-researches all data gaps from 30+ KB domains + Reddit/HN.

// turbo
```bash
python3 scripts/generate_validation_report.py "{idea}" --open
```

### With specific industry:

// turbo
```bash
python3 scripts/generate_validation_report.py "{idea}" --industry {industry} --open
```

### With AI enrichment data:

// turbo
```bash
python3 scripts/generate_validation_report.py "{idea}" --data enrichment.json --open
```

### Skip auto-research (faster, less data):

// turbo
```bash
python3 scripts/generate_validation_report.py "{idea}" --skip-research --open
```

### Via validate_idea.py:

// turbo
```bash
python3 scripts/validate_idea.py "{idea}" --report
```

---

## What Gets Generated

```
output/{ascii-slug}/
├── index.html    ← Full single-page report
└── shared.css    ← HVS design system
```

### Report Sections

| Section | Content | Auto-researched? |
|---------|---------|:---:|
| **Hero** | Title, DOV score, stage, classification badge, verdict | ✅ |
| **Phase 0 — Reframe** | Pain vs Feature, benchmarks, frameworks, cross-domain, 3 approaches | ✅ |
| **Stage 1 — DOV Validation** | Founder-opportunity fit, JTBD, problem anatomy, DOV scorecard | ✅ |
| **Digital Validation** | Reddit + HN pain signals, top quotes | ✅ (live) |
| **Stage 2 — Market Intel** | TAM/SAM/SOM, competitors, market timing | ✅ |
| **Stage 3 — Grand Slam Offer** | Value equation, problem→solution, pricing, guarantee | ✅ |
| **Roadmap** | Phase-based timeline with milestones | ✅ |
| **Sources** | All data sources used (KB + Digital + Auto-research) | ✅ |

### Auto-Research Pipeline

```
_auto_research(idea, industry, stage)
  ├── Reframe: 3 queries × benchmarks, frameworks, cross-domain
  ├── DOV: 3 queries × anti-patterns
  ├── Market: 2 queries × TAM + 3 queries × timing
  ├── Offer: 3 queries × pricing strategies
  └── Digital: Reddit (3 subs) + Hacker News → pain analysis
```

---

## Phase 2: VERIFY

### 2a. Check output exists

// turbo
```bash
ls -la output/{slug}/index.html output/{slug}/shared.css
```

### 2b. Content check

```
VERIFY:
  1. Hero section shows correct DOV score
  2. Benchmark table has real company names (not empty cells)
  3. Framework table has descriptions (not truncated)
  4. DOV scorecard bars render correctly
  5. Digital validation section shows pain signal data (if available)
  6. Sidebar navigation links work (smooth scroll)
  7. Sources section lists all data origins
```

---

## Phase 3: DELIVER

```
TELL FOUNDER:
  "Validation Report generated: output/{slug}/

   📊 DOV Score: {score}/100 — {classification}
   🔬 Auto-researched: benchmarks, frameworks, market data, pricing
   📡 Digital validation: {n} posts scanned for pain signals

   Open index.html in your browser to review."
```

---

## Enrichment JSON Schema (Optional)

For AI agents enriching the report, provide a JSON file with this structure:

```json
{
  "title": "Custom Report Title",
  "subtitle": "Custom subtitle",
  "reframe": {
    "founder_says": "What the founder literally said",
    "agent_hears": "What the AI agent interprets",
    "root_problem": "The deep underlying problem",
    "benchmarks": [{"name": "Company", "location": "HQ", "what": "Why they're #1"}],
    "frameworks": [{"name": "Framework", "applied": "How it applies here"}],
    "cross_domain": [{"from": "Source industry", "insight": "Transferable insight"}],
    "tradeoffs": [{"choose": "A", "sacrifice": "B", "why": "Reason"}],
    "approaches": [{"label": "Tag", "name": "Approach Name", "desc": "Description"}]
  },
  "dov": {
    "jtbd": "When I [situation], I want to [motivation], so I can [outcome]",
    "founder_fit": {"specific_knowledge": 8, "domain_expertise": 7, "network": 6},
    "monkey": {"title": "Critical risk", "desc": "Description"},
    "weakchain": {"title": "Process bottleneck", "desc": "Description"},
    "do_nothing": {"title": "Inaction scenario", "desc": "Description"},
    "impact": {"Functional": 8, "Emotional": 7, "Breakthrough UX": 9, "Billion+ Market": 6}
  },
  "market": {
    "tam": [{"level": "TAM", "market": "Category", "size": "$50B"}],
    "competitors": [{"name": "Competitor", "weakness": "Gap", "exploit": "Our advantage"}],
    "timing": [{"driver": "Trend", "evidence": "Why now"}]
  },
  "offer": {
    "value_equation": "Dream Outcome × Perceived Likelihood / Time × Effort",
    "problems_solutions": [{"problem": "Pain point", "solution": "Our answer"}],
    "offer_name": "Product Name",
    "offer_tagline": "One-liner",
    "pricing": [{"tier": "Plan", "target": "Who", "includes": "What", "price": "$X/mo"}],
    "guarantee": "Money-back guarantee details"
  },
  "roadmap": {
    "phases": [{"name": "Phase 1", "items": [{"time": "Week 1", "action": "Do this"}]}]
  }
}
```

---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Artifact | Gate |
|:-----:|----------|------|
| **1** Generate | `output/{slug}/index.html` | Script exits 0, both files exist |
| **2** Verify | Content checklist | All 7 checks pass |
| **3** Deliver | Founder notification | Founder opens and reviews |

### L5 Confidence Protocol

| Condition | Action |
|-----------|--------|
| Auto-research fills all sections | Deliver report directly |
| Some sections have fallback data | Deliver with note: "Market data needs manual research" |
| Digital validation fails (API error) | Deliver without digital section, note in sources |

### Anti-Patterns
- ❌ Generating before validation is complete
- ❌ Skipping auto-research and delivering empty sections
- ❌ Not opening in browser — founder must see visual output
- ❌ Using Vietnamese characters in output folder slug
