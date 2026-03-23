# 🏗️ EaseStart — System Architecture

> Technical architecture for EaseStart — 14 agents, 29+ domain knowledge graph, BM25 search, and 38 workflows.
> **1110 rows | 29+ domains | 14 agents | 38 workflows | 15 skills | Build-Ship-Measure methodology**

---

## Layer Architecture

```
┌─────────────────────────────────────────────┐
│  L4: User Interface                         │
│  CLI / IDE Skill / Web App (future)         │
├─────────────────────────────────────────────┤
│  L3: Agent Layer                            │
│  Orchestrator → Specialist Agents           │
│  • Stage detection                          │
│  • Task routing                             │
│  • Progress tracking                        │
├─────────────────────────────────────────────┤
│  L2: Retrieval Layer                        │
│  BM25 Search + Auto-Domain Detection        │
│  • Keyword scoring                          │
│  • Domain routing                           │
│  • Result ranking                           │
├─────────────────────────────────────────────┤
│  L1: Knowledge Graph                        │
│  CSV Databases + Ontology                   │
│  • 29+ domain files (1110 rows)         │
│  • 6 pillars: Build, Grow, Money,           │
│    People, Protect, Sustain                 │
│  • Decision rules (JSON)                    │
├─────────────────────────────────────────────┤
│  L0: Data Ingestion                         │
│  Founders Kit extraction pipeline           │
│  • Web crawl → LLM extract → CSV            │
│  • Link health verification                 │
│  • Quality scoring                          │
└─────────────────────────────────────────────┘
```

---

## Agent System

### Orchestrator Agent

```
founder-orchestrator
├── Responsibilities
│   ├── Classify user's startup stage (0-6)
│   ├── Route query to specialist agent
│   ├── Enforce stage-gated progression
│   ├── Track exit criteria completion
│   ├── Apply Giantiny philosophy lens (Customer Zero, Counter-position, Profit>Growth)
│   └── Provide cross-agent context
│
├── Input: User query + startup context
├── Output: Routed specialist response
│
└── Decision Logic:
    1. IF no context → ASK stage assessment questions
    2. IF stage known → LOAD stage-specific data
    3. IF query matches domain → ROUTE to specialist
    4. IF exit criteria met → SUGGEST next stage
    5. IF criteria not met → BLOCK with guidance
```

### Specialist Agents (14)

| Agent | Stages | Domain | Core Deliverables |
|-------|--------|--------|-------------------|
| `ideation-agent` | 0-1 | Ideas + Lean Canvas | Problem list, Lean Canvas v1 |
| `validation-agent` | 2-3 | Behavioral validation + PMF | Post-deploy interviews, PMF score |
| `mvp-agent` | 1-3 | Tech stack + build | Tech recommendation, launch plan |
| `data-agent` | 2-3 | Analytics + tracking | Event taxonomy, funnel templates |
| `growth-agent` | 3-5 | Channels + pricing | GTM strategy, metrics dashboard |
| `fundraising-agent` | 4-6 | VC + bootstrap | Pitch deck outline, financial model |
| `ops-agent` | 5-6 | Hiring + SOPs | Org chart, tool recommendations |
| `pm-agent` | 0-6 | Sprint + taskboard | Sprint coordination, task tracking |
| `cofounder-agent` | 0-4 | Team + equity | Equity split, 21-day trial protocol |
| `legal-agent` | 1-6 | Legal + compliance | Contract checklist, security audit |
| `wellness-agent` | 0-6 | Burnout + resilience | Energy budget, self-assessment |
| `marketing-agent` | 2-6 | Content + SEO + email | Channel strategy, content calendar |
| `finance-agent` | 2-6 | Bookkeeping + tax | P&L template, unit economics |
| `easestart-orchestrator` | 0-6 | Routing + stage detect | Stage assessment, agent dispatch |

### Agent Anti-Patterns (Lucius L4)

> Mỗi agent phải enforce anti-patterns — ngăn lỗi phổ biến trước khi xảy ra.

| Agent | Anti-Patterns |
|-------|--------------|
| `founder-orchestrator` | ❌ Routing trước khi detect stage · ❌ Allowing stage-skip without exit criteria met · ❌ Open-ended questions ("What do you want?") |
| `ideation-agent` | ❌ Recommending tools trước khi define problem · ❌ Scoring ideas without competitive analysis · ❌ Creating Lean Canvas without customer persona |
| `validation-agent` | ❌ Interviewing before deploying · ❌ Trusting self-reports over behavioral data · ❌ Asking leading questions ("Would you use X?") · ❌ Skipping behavioral analysis |
| `mvp-agent` | ❌ Over-engineering infrastructure · ❌ Choosing trendy tech over familiar tech · ❌ Building without analytics · ❌ Feature creep before core loop works |
| `growth-agent` | ❌ Spreading budget across 5+ channels · ❌ Copying competitor channels blindly · ❌ Growth before PMF confirmed · ❌ Vanity metrics over actionable metrics |
| `fundraising-agent` | ❌ Fundraising without traction · ❌ Raising too early or too much · ❌ Pitch deck before data room ready · ❌ Ignoring term sheet red flags |
| `ops-agent` | ❌ Hiring before process documented · ❌ Over-hiring before PMF · ❌ No SOPs → tribal knowledge · ❌ Scaling team before unit economics positive |
| `cofounder-agent` | ❌ Splitting equity 50/50 without discussion · ❌ Skipping vesting · ❌ Committing before 21-day trial · ❌ Ignoring value alignment |
| `data-agent` | ❌ Tracking 50+ events before core loop works · ❌ Analytics tool before product deployed · ❌ Vanity dashboards (pageviews ≠ activation) |
| `finance-agent` | ❌ Mixing personal/business accounts · ❌ Ignoring tax obligations · ❌ Reporting revenue before recognizing costs · ❌ No monthly close process |
| `legal-agent` | ❌ Launching without ToS/Privacy Policy · ❌ DIY contracts for \u003e$10K deals · ❌ Ignoring GDPR/data privacy · ❌ Equity changes without legal docs |
| `marketing-agent` | ❌ Selling in Heartbeat mode (LOTUS S=0%) · ❌ Copy-paste same content across platforms · ❌ Content without Ion Bank traceability · ❌ Skipping brand safety filter |
| `pm-agent` | ❌ Shipping without tests · ❌ Skipping /code-review before /ship · ❌ Sprint without taskboard.json · ❌ More than 5 active blockers unresolved |
| `wellness-agent` | ❌ Prescribing solutions without assessment · ❌ Ignoring \u003e70hr/week signals · ❌ Dismissing burnout as "normal startup pace" · ❌ Skipping energy budget |

### Skill Loading Protocol (Lucius L2)

```
easestart-orchestrator Skill Loading:
1. ALWAYS load stages.csv FIRST → detect current stage
2. ALWAYS load startup-reasoning.csv → get decision rules for context
3. IF stage 0-1 → load frameworks.csv → route to ideation-agent
4. IF stage 1-2 → load tools.csv + analytics/ → route to mvp-agent (build first)
5. IF stage 2-3 → load analytics/ + playbook.csv → route to validation-agent + data-agent
6. IF stage 3-5 → load playbook.csv + industries/ → route to growth-agent
7. IF stage 4-6 → load resources.csv → route to fundraising-agent
8. IF stage 5-6 → load tools.csv + programs.csv → route to ops-agent
9. IF stage 0-4 → load team_equity + psychology → route to cofounder-agent
10. IF stage 1-6 → load legal/ + contracts + security → route to legal-agent
11. IF stage 0-6 → load psychology + wellness → route to wellness-agent
12. IF stage 2-6 → load marketing/ (5 CSVs) → route to marketing-agent
13. IF stage 2-6 → load finance/ (2 CSVs) → route to finance-agent
14. ALWAYS load relevant industry CSV if context known
```

---

## Confidence Protocol (Lucius L5)

> Source: Lucius theory — áp dụng từ cv.md/feature-dev.md workflows.

### Agent Decision Scoring (V2)

Search results include `_confidence` level mapped from BM25 scores:

| `_confidence` | BM25 Score | Agent Action |
|--------------|------------|-------|
| **HIGH** | ≥ 3.0 | ✅ Proceed autonomously — cite data source |
| **MEDIUM** | 1.0 – 2.99 | ⁉️ Present **binary choice** with recommendation |
| **LOW** | < 1.0 | ⚠️ **Stop and ask** — request founder context |
| **Same gate fails 2×** | — | Auto-escalate regardless of score |

### Rules

- ❌ **Never** ask open-ended "What should I do?" — always binary choices with recommendation
- ❌ **Never** recommend without citing source (CSV row, framework, or resource)
- ✅ **Always** include confidence score in internal reasoning
- ✅ **Always** state which CSV/data informed the recommendation
- ✅ **Always** show `_anti_pattern_warning` to founder before recommendation

### Escalation Protocol

```
Agent stuck (LOW confidence)
  │
  ├── Has relevant CSV data? → Re-search with refined query
  │
  ├── Has reasoning rule? → Apply decision rule from startup-reasoning.csv
  │
  ├── Neither? → Escalate to orchestrator
  │
  └── Orchestrator stuck? → Ask founder with binary choice
          Max 3 escalations per workflow → STOP + full status report
```

---

## Guardrails Engine (Policy-as-Code)

> Source: Agentic OS "Policy-as-Code Engine" — adapted for EaseStart's stage-gated methodology.
> Unlike anti-patterns (advisory text), guardrails are **hard enforcement rules** that agents MUST check.

```
Agent Recommendation Flow (with Guardrails):

  Agent proposes action
      │
      ▼
  ┌──────────────────────┐
  │  Guardrails Check    │
  │  Load guardrails.json│
  │  Evaluate conditions │
  └──────────┬───────────┘
             │
     ┌───────┼───────┐
     │       │       │
     ▼       ▼       ▼
  BLOCK    WARN    PASS
  (stop)  (alert)  (ok)
     │       │       │
     ▼       ▼       ▼
  Deny +   Show    Continue
  Message  Warning  normal
```

### Rule Types

| Type | Behavior | Example |
|------|----------|---------|
| `BLOCK` | Hard stop — action denied | Growth before Stage 2 |
| `WARN` | Warning shown, CEO decides | Monthly cost >$500 |

### Coverage (15 rules)

- **Stage-gating:** G-001–G-004 (growth, ads, fundraising, hiring)
- **Budget:** G-005 (cost threshold)
- **PMF:** G-006 (scaling without PMF)
- **Irreversibility:** G-007 (cannot-undo warning)
- **Channel:** G-008–G-009 (concentration + platform risk)
- **Equity:** G-010 (no vesting = blocked)
- **Validation:** G-011 (interview minimum)
- **Launch:** G-012 (pre-Stage 3 block)
- **Runway:** G-013–G-014 (6-month warn, 3-month emergency)
- **Decay:** G-015 (expired reasoning rules)

---

## Business Impact Preview

> Source: Agentic OS "Business Impact Digital Twin" — render projected outcome before recommending.

Every recommendation in `playbook.csv` and `marketing/channels.csv` now includes:

| Field | Purpose | Example |
|-------|---------|---------|
| `Impact_Preview` | Projected cost, timeline, expected result | "5K-15K visitors day 1, $0 cost, 1 week prep" |
| `Reversibility` | Can this action be undone? | `reversible` / `partially` / `irreversible` |

**Agent Protocol:** When `Reversibility == "irreversible"`, agent MUST trigger Guardrail G-007 and show Impact Preview to CEO before proceeding.

---

## Context Decay (Temporal Awareness)

> Source: Agentic OS "Spatio-temporal Graph Memory" — strategies that worked last quarter may not apply now.

`reasoning/_SCHEMA.csv` now includes temporal metadata:

| Field | Values | Purpose |
|-------|--------|---------|
| `Validity_Period` | `evergreen` / `180_days` / `90_days` / `30_days` | How long this rule stays relevant |
| `Decay_Note` | Free text | Why the rule may expire |

**Agent Protocol:** When `Validity_Period != "evergreen"`, agent MUST note the decay risk and suggest re-evaluation if the rule may be outdated.

---

## Search Engine

### BM25 Hybrid Search (Proven Pattern)

```python
class EaseStartSearch:
    """
    BM25 search engine for startup knowledge (V2).
    Zero external dependencies. ~480 lines Python.
    Features: Stage-weighted scoring, Lucius L5 confidence, Anti-pattern warnings.
    """
    
    # 1. Base Score calculation using BM25
    bm25 = BM25().index(documents)
    scores = bm25.score(query_tokens)

    # 2. Stage-Weighted Scoring Boost
    if stage_is_known:
        scores *= STAGE_RELEVANCE_WEIGHTS[distance]

    # 3. Min-Score Threshold
    if score < 0.5:
        drop(result)

    # 4. Lucius L5 Confidence Mapping
    _confidence = "HIGH" if score >= 3.0 else "MEDIUM" if score >= 1.0 else "LOW"

    # 5. Anti-Pattern Warning Scan
    _anti_pattern_warning = _find_anti_pattern_warnings(query, domain, stage)
```

### CLI Usage

```bash
# Domain-specific search
python3 scripts/search.py "analytics tool" --domain tools

# Auto-detect domain
python3 scripts/search.py "what stage am I in"

# Industry-specific
python3 scripts/search.py "pricing strategy" --industry saas
```

---

## Workflow Engine (Lucius 4-Phase Pipeline)

> Mỗi workflow tuân theo Lucius 4-phase format: Phase → Artifact → Gate → Advance.

### Example: `/validate-idea` Workflow

```markdown
## Phase 1: ASSESS → Stage Detection
> Output: stage-assessment.md
> Skills: stages.csv, startup-reasoning.csv
> Gate: User confirms current stage is 1-2

### Actions
1. Run 5-question stage assessment
2. Load stage-specific exit criteria
3. Verify founder hasn't already validated

### Anti-Patterns
- ❌ Skipping assessment — assuming stage from user's words alone
- ❌ Allowing validation workflow for Stage 0 founder (needs ideation first)

---

## Phase 2: BUILD → Deploy Product (Build-Ship-Measure)
> Output: deployed product + analytics tracking
> Skills: tools.csv, analytics/
> Gate: Product deployed with 5 P0 events tracking

### Actions
1. AI-assisted build sprint (1-3 days)
2. Deploy to production (public URL)
3. Install PostHog with 5 P0 events (data-agent)
4. Post on 2+ communities for distribution

### Anti-Patterns
- ❌ Building for weeks without shipping
- ❌ Deploying without analytics

---

## Phase 3: OBSERVE → Behavioral Validation
> Output: behavioral-report.md + interview-synthesis.md
> Skills: analytics/, playbook.csv
> Gate: ≥50 visitors + behavioral data + 15 post-deploy interviews

### Actions
1. Observe activation rate, D7 retention, feature concentration
2. Interview 15 users who TRIED the product (post-deploy)
3. Cross-reference behavioral data with interview insights
4. Trust behavioral data over self-reports when in conflict

### Anti-Patterns
- ❌ Interviewing before deploying product
- ❌ Trusting self-reports over behavioral data

---

## Phase 4: DECIDE → Stage Gate
> Output: decision-report.md
> Skills: startup-reasoning.csv, metrics.csv
> Gate: Binary decision — Advance / Iterate / Pivot

### Decision Logic
- IF activation ≥30% + D7 ≥15% → ✅ Proceed to Stage 3
- IF mixed signals → ⚠️ Iterate on worst drop-off
- IF kill signals → ❌ Pivot (return to Phase 1)

### Anti-Patterns
- ❌ Advancing without measuring activation + retention
- ❌ Pivoting without documenting learnings
- ❌ Using pre-deploy surveys as primary validation
```

---

## Intel Memo Report System (Lucius 4-Phase)

> Multi-page HTML report generator with citation system and interactive detail drawers.

### Architecture

```
generate_report.py
├── CitationRegistry          ← Tracks all search() calls
│   ├── search_and_cite()     ← Search + register citation + return (n) marker
│   ├── to_json()             ← Export all citations as JSON for JS
│   └── build_sources_html()  ← Render Sources section at bottom
│
├── STAGE_CONFIG (7 stages)   ← Stage-specific domain maps
│   ├── focus_queries[]       ← Tailored search queries per stage
│   ├── key_question          ← The one question founder must answer
│   └── domains[]             ← Which CSV domains to query
│
├── generate_hub_page()       ← Index with 7 stage cards + methodology
├── generate_stage_page()     ← Stage page with citations + drawer
│   ├── build_domain_table()  ← Knowledge coverage with (n) markers
│   ├── build_questions_section() ← Tailored questions with (n) markers
│   ├── build_scorecard()     ← 5-dimension confidence score
│   └── DRAWER_JS             ← Right panel JS (click citation → open)
│
└── output/{YYYY-MM-DD}-{slug}/
    ├── index.html
    ├── shared.css            ← Workshop design tokens
    └── stages/stage-{0-6}.html
```

### Citation Flow (Lucius L5 — Source Attribution)

```
search(query, stage)
    ↓
CitationRegistry.search_and_cite()
    ↓ returns
(results, '<span class="cite">(n)</span>')
    ↓ embedded in HTML
User clicks (n) → DRAWER_JS reads CITATIONS[n] → populates drawer
    ↓ shows
Domain badge + Confidence badge + Score + Query + All data fields
```

### Design System (from workshop)

| Token | Value |
|-------|-------|
| Heading | Barlow Condensed, uppercase, 56px |
| Body | SF Pro Rounded (system UI fallback) |
| Palette | #000 / #FFF / #4E4B66 (monochrome) |
| Accent | Dynamic: green≥80, yellow≥60, orange≥40, red<40 |
| Drawer | 420px right panel, slides in 0.25s |

---

## Data Flow

```
User Query
  │
  ▼
┌──────────────────┐
│  Orchestrator     │
│  1. Parse query   │
│  2. Detect stage  │
│  3. Route domain  │
└────────┬─────────┘
         │
    ┌────▼────┐
    │ Search  │
    │ Engine  │
    │ (BM25)  │
    └────┬────┘
         │
     ┌────▼────────────────────────┐
     │  CSV Knowledge Graph        │
     │  29+ domains / 1110 rows    │
     │  ┌──────┐ ┌────────┐       │
     │  │tools │ │stages  │       │
     │  ├──────┤ ├────────┤       │
     │  │frames│ │analytics│      │
     │  ├──────┤ ├────────┤       │
     │  │reason│ │resource│       │
     │  ├──────┤ ├────────┤       │
     │  │market│ │finance │       │
     │  ├──────┤ ├────────┤       │
     │  │legal │ │support │       │
     │  └──────┘ └────────┘       │
     └────────┬───────────────────┘
              │
     ┌────────▼──────────────────┐
     │ 14 Specialist Agents       │
     │ + Context + Decision Rules│
     └────────┬──────────────────┘
              │
              ▼
     Actionable Response
     (with citations)
```
