<img src="https://capsule-render.vercel.app/api?type=waving&color=0:000000,100:1a1a2e&height=180&section=header&text=EaseStart&fontSize=52&fontColor=ffffff&animation=fadeIn&fontAlignY=34&desc=Your%20AI%20Startup%20Co-Pilot&descAlignY=54&descSize=18&descColor=cccccc" width="100%" />

<div align="center">

<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.demolab.com?font=Inter&weight=500&size=22&duration=4000&pause=1200&color=888888&center=true&vCenter=true&multiline=false&repeat=true&width=500&height=30&lines=Stop+Googling+startup+advice.+Start+building.;Stage-gated+AI+for+solo+founders.;1110+knowledge+rows+%C2%B7+14+agents+%C2%B7+22+workflows" alt="Typing SVG" /></a>

<br />

[![License: PolyForm Shield 1.0.0](https://img.shields.io/badge/License-PolyForm_Shield_1.0.0-000000.svg?style=flat-square)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-000000.svg?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Knowledge Rows](https://img.shields.io/badge/Knowledge_Rows-1110-000000.svg?style=flat-square)](data/_REGISTRY.md)
[![Agents](https://img.shields.io/badge/Agents-14-000000.svg?style=flat-square)](docs/ARCHITECTURE.md)
[![Workflows](https://img.shields.io/badge/Workflows-22-000000.svg?style=flat-square)](.agent/workflows/)
[![Industries](https://img.shields.io/badge/Industries-30-000000.svg?style=flat-square)](data/industries/_SCHEMA.csv)
[![Zero Deps](https://img.shields.io/badge/Core_Deps-0-000000.svg?style=flat-square)](#zero-dependency-core)
[![Tests](https://img.shields.io/badge/Tests-143%2F143-000000.svg?style=flat-square)](#quality-assurance)

**Works with any AI coding IDE:**

[![IDE Skills](https://skillicons.dev/icons?i=vscode&theme=dark)](https://antigravity.dev)

[**Antigravity**](https://antigravity.dev) · [**Claude Code**](https://claude.ai) · [**Gemini CLI**](https://ai.google.dev/gemini-api/docs/gemini-cli) · [**Cursor**](https://cursor.com) · [**Windsurf**](https://windsurf.com) · [**Open Code**](https://github.com/nicepkg/OpenCode)

[Quick Start](#-quick-start) · [User Guide](docs/USER-GUIDE.md) · [Architecture](docs/ARCHITECTURE.md) · [Philosophy](docs/PHILOSOPHY.md) · [Contributing](#-contributing)

</div>

---

## Table of Contents

- [The Problem](#-the-problem)
- [How EaseStart Works](#-how-easestart-works)
- [Quick Start](#-quick-start)
- [The 7-Stage Model](#-the-7-stage-model)
- [14 Specialist Agents](#-14-specialist-agents)
- [Knowledge Graph](#-knowledge-graph-554-rows--29-domains)
- [Embedded Tools](#-embedded-tools)
- [Workflows](#-workflows-15)
- [CLI](#-cli)
- [MCP Server](#-mcp-server)
- [Intel Memo Reports](#-intel-memo-reports)
- [Philosophy: Giantiny Biz](#-philosophy-giantiny-biz)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Quality Assurance](#-quality-assurance)
- [Documentation](#-documentation)
- [Standing on the Shoulders of Giants](#-standing-on-the-shoulders-of-giants)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 The Problem

You're a solo founder. It's 2am. You're staring at a blank screen, Googling _"how to validate my startup idea"_.

ChatGPT gives you a 5-paragraph essay that sounds smart but says **nothing specific** to your situation. You read 3 Medium articles, 2 Reddit threads, and a Twitter thread. Still confused. Still stuck.

**The real problem isn't advice — it's the wrong advice at the wrong time.**

A Stage 0 founder doesn't need growth hacking. A Stage 3 founder shouldn't be rewriting their Lean Canvas. Generic AI assistants don't know this. They give you everything, everywhere, all at once.

> **EaseStart is different.** It knows which stage you're in, what you should be doing _right now_, and what mistakes will kill your startup if you make them at this stage.
>
> **1110 curated knowledge rows · 14 specialist agents · 22 workflows · 30 industries · 0 dependencies.**

---

## 🧠 How EaseStart Works

Clone the repo → open your AI coding IDE → your AI assistant is now a **startup co-pilot** with 14 specialist agents, 1110 rows of curated knowledge, and anti-pattern detection built in.

```
You:   "I have 200 users but no revenue. What pricing model fits?"

AI:    → Orchestrator detects Stage 4 (PMF)
       → Routes to growth-agent
       → Searches pricing domain (15 strategies)
       → ⚠️  Anti-pattern: "Don't launch freemium before 1,000 users"
       → Recommends value-based pricing with 3 tiers
       → Cites: strategies.csv row 7 (BM25 score: 4.2, HIGH confidence)
```

### How It's Different

| | Generic AI (ChatGPT, Claude) | EaseStart |
|---|---|---|
| **Context** | Knows nothing about your stage | **Stage-gated** — knows where you are, gives specific next steps |
| **Knowledge** | Trained on the internet | **1110 curated rows** from YC, Lean Startup, JTBD, real companies |
| **Search** | Keyword matching, no structure | **BM25 + domain routing** with confidence scoring |
| **Agents** | One generalist | **14 specialists** enforcing proven frameworks |
| **Industries** | Generic advice | **30 industries** from AgriTech to SpaceTech |
| **Anti-patterns** | No guardrails | **Stage-specific warnings** that prevent the mistakes killing 90% of startups |
| **Execution** | Advice only | **Agents propose plans. CEO approves. Agents deliver.** |

---

## 🚀 Quick Start

### 1. Clone

```bash
git clone https://github.com/EaseStart/easestart.git
cd easestart
```

### 2. Verify (instant — zero dependencies)

```bash
python3 scripts/search.py "freemium vs subscription SaaS"
```

> **That's it.** No `pip install`. No API keys. No database. Works immediately.

### 3. Connect Your AI IDE

<table>
<tr>
<td width="200"><strong>Antigravity<br>Claude Code</strong></td>
<td>

Open your IDE in the `easestart/` folder. Agents load automatically via `.agent/` directory.

</td>
</tr>
<tr>
<td><strong>Gemini CLI</strong></td>
<td>

Open your IDE in the `easestart/` folder. `GEMINI.md` and `.agent/` configure routing automatically.

</td>
</tr>
<tr>
<td><strong>Cursor<br>Windsurf</strong></td>
<td>

```bash
python3 cli/main.py init
# Auto-detects your IDE → installs MCP server
```

</td>
</tr>
</table>

### 4. Start Building

Open your AI IDE and try:

```
I want to build a personal finance app for Gen Z in Vietnam.
Help me create a Lean Canvas and evaluate this idea.
```

The **orchestrator** detects Stage 0–1 → routes to **ideation-agent** → generates Lean Canvas + Idea Score + counter-positioning analysis.

> 📖 **Full walkthrough:** [User Guide](docs/USER-GUIDE.md) — day-by-day from Idea → Validation → MVP → PMF → Growth

---

## 🗺️ The 7-Stage Model

Every startup goes through 7 stages. EaseStart knows where you are and **only gives stage-appropriate advice**.

| Stage | Name | Goal | Key Metric | Exit Criteria | Primary Agent |
|:-----:|------|------|------------|---------------|:-------------:|
| **0** | Pre-Idea | Find problems worth solving | Problems identified | ≥3 problems listed + 1 selected | `ideation` |
| **1** | Ideation | Evaluate & score ideas | Lean Canvas score | Canvas score ≥ 60 | `ideation` |
| **2** | Validation | Talk to customers + deploy | Sean Ellis ≥ 40% | 15 interviews + product deployed | `validation` |
| **3** | MVP | Build & measure first version | DAU, D7 retention | Activation ≥ 30%, D7 ≥ 15% | `mvp` |
| **4** | PMF | Find product-market fit | 40%+ "very disappointed" | PMF survey score ≥ 40% | `growth` |
| **5** | Growth | Scale acquisition channels | MRR, CAC, LTV | Unit economics positive | `growth` |
| **6** | Scale | Team + fundraise (if needed) | Revenue, headcount | SOPs documented, MOAT identified | `ops` |

> **Stage-gating is enforced.** An agent will **not** give growth advice to a Stage 1 founder. It will redirect you to what you actually need.

---

## 🤖 14 Specialist Agents

Every agent has a defined scope, anti-patterns it enforces, and stage boundaries it respects.

```
                            ┌─────────────────────┐
                            │    ORCHESTRATOR      │
                            │  Stage Detection     │
                            │  Query Routing       │
                            │  Quality Gates       │
                            └─────────┬───────────┘
                                      │
          ┌───────────┬───────────┬───┴───┬───────────┬───────────┐
          │           │           │       │           │           │
     ┌────▼───┐ ┌────▼───┐ ┌────▼──┐ ┌──▼────┐ ┌───▼────┐ ┌───▼────┐
     │ideation│ │validate│ │  mvp  │ │growth │ │fundrais│ │  ops   │
     │ 0 — 1  │ │ 1 — 2  │ │ 2 — 3 │ │ 3 — 5 │ │ 4 — 6  │ │ 5 — 6  │
     └────────┘ └────────┘ └───────┘ └───────┘ └────────┘ └────────┘
          │           │           │       │           │           │
     ┌────▼───┐ ┌────▼───┐ ┌────▼──┐ ┌──▼────┐ ┌───▼────┐ ┌───▼────┐
     │cofoundr│ │  legal │ │  data │ │market │ │finance │ │wellness│
     │ 0 — 4  │ │ 1 — 6  │ │ 2 — 3 │ │ 2 — 6 │ │ 2 — 6  │ │ 0 — 6  │
     └────────┘ └────────┘ └───────┘ └───────┘ └────────┘ └────────┘
                                      │
                                ┌─────▼─────┐
                                │    pm     │
                                │  0 — 6    │
                                │ Sprints   │
                                │ Decisions │
                                │ Tracking  │
                                └───────────┘
```

<details>
<summary><strong>View All 14 Agents with Details</strong></summary>

| # | Agent | Stages | Domain | Core Deliverables |
|:-:|-------|:------:|--------|-------------------|
| 1 | **orchestrator** | 0–6 | Routing + stage detection | Stage assessment, agent dispatch, quality gates |
| 2 | **ideation** | 0–1 | Ideas + Lean Canvas | Problem list, Canvas v1, idea scoring, counter-positioning |
| 3 | **validation** | 1–2 | Behavioral validation | Post-deploy interviews, PMF score, Sean Ellis survey |
| 4 | **mvp** | 2–3 | Tech stack + build | Tech recommendation, sprint plan, launch checklist |
| 5 | **data** | 2–3 | Analytics + tracking | Event taxonomy, funnel templates, PostHog setup |
| 6 | **growth** | 3–5 | Channels + pricing | GTM strategy, pricing model, metrics dashboard |
| 7 | **fundraising** | 4–6 | VC + bootstrap | Pitch deck outline, financial model, term sheet review |
| 8 | **ops** | 5–6 | Hiring + SOPs | Org chart, tool recommendations, MOAT building |
| 9 | **cofounder** | 0–4 | Team + equity | Equity split, 21-day trial protocol, conflict resolution |
| 10 | **legal** | 1–6 | Legal + compliance | Contract checklist, incorporation guide, security audit |
| 11 | **marketing** | 2–6 | Content + SEO + email | Channel strategy, content calendar, email sequences |
| 12 | **finance** | 2–6 | Bookkeeping + tax | P&L template, unit economics, cash flow projections |
| 13 | **wellness** | 0–6 | Burnout + resilience | Energy budget, burnout signals, self-assessment |
| 14 | **pm** | 0–6 | Sprint + taskboard | Sprint coordination, daily standups, decision logs |

</details>

### Anti-Pattern Engine

Every agent enforces anti-patterns — **preventing common mistakes before they happen**.

```
User:   "Let's start growth hacking, I have 50 beta users"

Agent:  ⚠️ ANTI-PATTERN DETECTED
        "Growth before PMF confirmed" (growth-agent rule #3)
        
        You're at Stage 3. Before growth, you need:
        ✓ Activation rate ≥ 30%
        ✓ D7 retention ≥ 15%
        ✓ 40%+ users "very disappointed" without your product
        
        → Redirecting to validation-agent for PMF measurement.
```

<details>
<summary><strong>View Anti-Pattern Rules by Agent</strong></summary>

| Agent | Anti-Patterns Enforced |
|-------|----------------------|
| **orchestrator** | Routing before stage detection · Allowing stage-skip without exit criteria · Open-ended questions |
| **ideation** | Recommending tools before defining problem · Scoring without competitive analysis · Canvas without persona |
| **validation** | Interviewing before deploying · Trusting self-reports over behavioral data · Leading questions |
| **mvp** | Over-engineering infrastructure · Trendy tech over familiar tech · Building without analytics |
| **growth** | 5+ channels simultaneously · Copying competitors · Growth before PMF · Vanity metrics |
| **fundraising** | Raising without traction · Raising too early/much · Pitch before data room · Ignoring term sheet flags |
| **ops** | Hiring before documentation · Over-hiring before PMF · No SOPs · Scaling before unit economics positive |

</details>

---

## 📊 Knowledge Graph (1110 Rows · 29+ Domains)

Every row is **factually grounded** — sourced from real books, real tools, real companies. Not AI-generated filler. Doubled from 554 to 1110 rows with marketing, finance, legal, ops, psychology, and team domains.

### 6 Pillars

| Pillar | Domains | Rows | Coverage |
|--------|---------|-----:|:--------:|
| **Build** | stages, tools, anti-patterns, frameworks, resources, templates | 186 | ██████████████████░░ 34% |
| **Operate** | playbook, reasoning, metrics, support, automation, industries | 143 | ██████████████░░░░░░ 26% |
| **Money** | pricing, bookkeeping, unit economics, programs | 62 | ██████░░░░░░░░░░░░░░ 11% |
| **Grow** | channels, content, email, landing, community | 59 | ██████░░░░░░░░░░░░░░ 11% |
| **People** | team, equity, psychology, case studies | 57 | ██████░░░░░░░░░░░░░░ 10% |
| **Protect** | legal, contracts, security | 47 | █████░░░░░░░░░░░░░░░ 8% |

### 30 Industries

<details>
<summary><strong>View All 30 Industries</strong></summary>

| Category | Industries |
|----------|-----------|
| **Tech** | SaaS B2B · SaaS B2C · Developer Tools · AI/ML · Cybersecurity · Web3/Blockchain · Quantum |
| **Commerce** | E-Commerce/DTC · Marketplace · FoodTech · Local Services |
| **Vertical** | AgriTech · PropTech · ConstructionTech · LegalTech · HRTech · InsurTech |
| **Life** | Health & Wellness · EdTech · Creator Economy · PetTech · Travel · Gaming |
| **Deep Tech** | BioTech · CleanTech · Robotics · SpaceTech |
| **Impact** | FinTech · LogiTech · Nonprofit |

**Each industry includes:** TAM estimate · stage-specific challenges · recommended tools · counter-positioning angles · key metrics · revenue model · example companies.

</details>

### Data Sources

All knowledge is sourced from battle-tested frameworks and real-world data:

| Source | What We Extracted |
|--------|------------------|
| **Y Combinator** | Startup School curriculum, batch learnings, stage definitions |
| **Lean Startup** | Build-Measure-Learn, MVP patterns, pivot criteria |
| **Jobs-to-be-Done** | Customer interview scripts, demand-side thinking |
| **The Mom Test** | Non-leading interview questions, validation protocols |
| **Hamilton Helmer** | 7 Powers framework, counter-positioning theory |
| **Naval Ravikant** | Specific knowledge, code + media leverage |
| **Basecamp / Shape Up** | Fixed-time scoping, profit-first operations |
| **Pieter Levels** | Solo-founder model, proprietary niche data |

---

## 🛠️ Embedded Tools

Pre-built tools that run **locally**. Your AI IDE deploys them for you — zero cloud, zero cost.

| Tool | Command | What It Does | Dependencies |
|------|---------|-------------|:------------:|
| **Search** | `python3 scripts/search.py "query"` | BM25 + domain routing with confidence scoring | None |
| **Digital Validation** | `python3 scripts/digital_validate.py "idea"` | Reddit + HN mining — validate ideas without interviews | None |
| **Metrics Tracker** | `python3 scripts/metrics.py` | SQLite tracker + ASCII trend charts + stage suggestions | None |
| **Semantic Search** | `python3 scripts/embed.py` | ChromaDB embeddings — understands meaning, not just keywords | `chromadb` |
| **Dashboard** | `python3 scripts/dashboard.py` | Visual dashboard at `localhost:5050` | `flask` |
| **Reports** | `python3 scripts/report.py` | Weekly markdown/PDF reports from PM data | None |
| **Intel Memo** | `python3 scripts/generate_report.py` | Multi-page HTML report with citations + interactive drawers | None |
| **Simulation** | `python3 scripts/simulate.py` | 10-persona simulation suite — tests agent routing accuracy | None |
| **Stress Test** | `python3 scripts/stress_test.py` | 102-case routing accuracy test across 29 domains | None |
| **Impact Analysis** | `python3 scripts/impact.py` | Decision impact analysis with cross-domain tracing | None |

### Zero-Dependency Core

The core engine (`scripts/core.py`) runs on **Python 3 standard library only**. No external packages required.

```bash
# Optional — only install what you need
pip install -r requirements-tools.txt  # For dashboard, semantic search, PDF export
```

### Digital Validation

Can't schedule 10 Mom Test interviews? Mine real founder pain from Reddit and Hacker News instead:

```bash
python3 scripts/digital_validate.py "your startup idea"
python3 scripts/digital_validate.py "AI tool for founders" \
    --queries "solo founder help,startup advice" \
    --output report.json
```

Scores your idea across 5 dimensions:

| Dimension | What It Measures |
|-----------|-----------------|
| Pain Prevalence | How common is the problem? |
| Pain Intensity | How painful is it? |
| Active Solving | Are people actively seeking solutions? |
| Market Awareness | Do people know the problem exists? |
| Engagement | How much discussion does it generate? |

**Score interpretation:** ≥70 → Proceed · 50–70 → Dig deeper · <50 → Consider pivoting

---

## 📋 Workflows (38)

Run these inside your AI IDE. Each follows the **Lucius 4-Phase Pipeline**: Phase → Artifact → Gate → Advance.

### 🏃 Compound Sprint System

EaseStart's killer feature: **multi-agent sprint chains** that compress months of startup work into days. Each sprint chains 3–4 specialist agents with dependency gates — an agent can't start until the previous one passes its exit criteria.

```
/sprint-build (2-4 days)                    /sprint-validate (1-2 weeks)
Stage 1 → 2                                 Stage 2 → 3
┌──────────┐   ┌──────────┐   ┌────────┐   ┌──────────────┐   ┌──────────────┐
│ mvp-agent│──▶│data-agent│──▶│mktg    │   │validate-agent│──▶│  orchestrator│
│ Tech pick│   │ Analytics│   │1st dist│   │ Interviews   │   │  Stage gate  │
│ Build    │   │ Setup    │   │        │   │ PMF score    │   │              │
│ Deploy   │   │          │   │        │   │ Behavioral   │   │              │
└──HARD────┘   └──SOFT────┘   └─SOFT───┘   └───HARD───────┘   └───HARD──────┘

/sprint-growth (4 weeks)
Stage 3 → 5
┌────────────┐   ┌────────────┐   ┌──────────────┐
│growth-agent│──▶│ mktg-agent │──▶│ finance-agent │
│ Channel    │   │ Content    │   │ Unit econ     │
│ selection  │   │ Acquisition│   │ Pricing opt   │
│ PMF check  │   │ Strategy   │   │               │
└───GATED────┘   └───GATED────┘   └───GATED──────┘
```

> **What this means:** Type `/sprint-build` and the AI orchestrates 4 agents over 2–4 days — picks your tech stack, builds the product, deploys it, sets up analytics, acquires first users, and reviews 48h metrics. All gated — if tech selection fails, nothing else starts.

### 🔧 Dev Pipeline (3-Phase Gated)

Three workflows that chain together as a complete deployment pipeline. Each phase produces an artifact and **gates the next phase** — you can't ship without QA, and you can't QA without code review.

```
/code-review ──────▶ /qa ──────▶ /ship
   Phase 1              Phase 2       Phase 3
   Fix-first audit      Browser QA    L5 confidence
   → report.md ✓        → report.md ✓ → release-notes.md ✓
```

| Phase | Workflow | What It Does | Gate |
|:-----:|----------|-------------|------|
| 1 | `/code-review` | Auto-fix obvious issues, surface ambiguous ones for human decision | `code-review-report.md` must show PASS |
| 2 | `/qa` | Playwright-based browser testing on staging URL | `qa-test-report.md` must show PASS |
| 3 | `/ship` | L5 confidence scoring → test → deploy → auto-update docs | Produces `release-notes.md` |

### 📣 $0 Marketing Engine

Generate and publish content across 7 platforms using **zero API cost** — powered by your AI IDE's LLM + browser automation.

| Workflow | Platforms | What It Does |
|----------|----------|-------------|
| `/marketing-publish` | Twitter/X, LinkedIn, Reddit | Generate content from YAML prompts → publish via browser |
| `/marketing-engage` | Reddit, Hacker News | Find relevant posts → generate authentic replies |
| `/publish` | Facebook, Threads | Carousel + post publishing with golden hour scheduling |

> Built on a **YAML prompt architecture** (`prompts/marketing/`) — brand voice, visual styles, deep storytelling, and platform-specific content strategies. All customizable.

### 🔬 Core Journey & Operations

| Workflow | Stage | What It Does |
|----------|:-----:|-------------|
| `/startup-journey` | 0–6 | Full 7-stage guided experience — auto-routes through all stages with gate enforcement |
| `/diagnose` | — | Self-assessment diagnostic — detect current stage + route to right agent/data |
| `/validate-idea` | 1–2 | End-to-end idea validation — Lean Canvas → AI build → Mom Test → PMF measurement |
| `/build-mvp` | 2–3 | Scope → tech stack → sprint plan → deploy → launch checklist |
| `/daily-ops` | 0–6 | PM standup — blocker triage, priority setting, EOD wrap |
| `/weekly-retro` | 0–6 | 4Ls retrospective + momentum scoring + next cycle planning |
| `/decide` | 0–6 | ADR-style decision records with Lucius confidence scoring |

### 🧠 Intelligence & Reports

| Workflow | What It Does |
|----------|-------------|
| `/deep-research` | Autonomous research loop — output feeds back into CSV knowledge base (**data flywheel**) |
| `/generate-report` | CEO-grade multi-page HTML Intel Memo with citations + interactive detail drawers |
| `/notebooklm-pipeline` | Audio content generation via NotebookLM |
| `/agent-review` | Quarterly audit of all 14 agents for staleness and accuracy |
| `/handoff` | Session-end context preservation for next session continuity |
| `/gws-setup` | Google Workspace MCP integration setup |

### 🎬 Content Production Pipeline

End-to-end content creation workflows — from visual assets to video teasers. Built for founders who need to ship content fast, not just write copy.

| Workflow | What It Does |
|----------|-------------|
| `/slides` | Marketing carousel generator — JSON data → HTML templates → 1080×1080 PNG. Royal Bold style with quality rules (no emoji, overflow prevention, visual rhythm) |
| `/video` | AI video production — cinematic storyboard → multi-clip generation (Veo 3 / Seedance 2.0) → stitching → platform-ready export |
| `/style-extract` | Analyze reference visuals (PDFs, screenshots, URLs) → build complete HTML template systems. Reference → pixel-perfect in one session |
| `/github-readme` | GitHub Profile & Project READMEs — dynamic stats, badges, typing SVG, capsule render, snake animations, 3D graphs |

### ⚙️ Design & Dev Standards

Production-grade development workflows — from design systems to retrospectives.

| Workflow | What It Does |
|----------|-------------|
| `/design` | UI/UX design orchestrator — coordinates product-designer, core-components, and ux-psychology skills |
| `/design-init` | Initialize/refresh project design system — extract tokens, inventory components, generate guidelines, setup Storybook |
| `/feature-dev` | Elite feature development (Amazon/Stripe/Basecamp/Linear patterns) — from spec to production |
| `/dev-rules` | Development standards enforcement — file naming, code quality, pre-commit rules |
| `/review-gate` | Automated quality gates — deterministic checks + multi-pass AI review + browser verification |
| `/ship` | Ship pipeline — merge, test, review, version bump, commit, push, PR. For ready branches |
| `/retro` | Engineering retrospective — git data analysis, productivity metrics, session detection, shipping streaks |
| `/pm-hub-sync` | Auto-update PM Hub after feature work — keeps Kanban board current without human intervention |

### 🎓 Education & Brand

Workflows for founders who also teach, mentor, or build personal brands.

| Workflow | What It Does |
|----------|-------------|
| `/workshop` | End-to-end workshop creation — research → content design → HTML build → multi-modal content (TTS, podcasts, video, quiz, flashcards) → deploy |
| `/course-design` | Design in-person courses using the AI-proof Skills/Knowledge framework — curriculum architecture, session design, delivery methodology |
| `/cv` | Full CV lifecycle — tailor content, build HTML, verify consistency, export PDF |
| `/export-pdf` | HTML → PDF export via Playwright + Chromium with correct fonts, backgrounds, and layout |

---

## ⌨️ CLI

For terminal use outside the AI IDE:

```bash
# Setup & diagnostics
python3 cli/main.py init                  # Setup IDE + MCP server
python3 cli/main.py doctor                # 14 health checks

# Knowledge exploration
python3 cli/main.py search "query"        # Search knowledge graph
python3 cli/main.py skills list           # List all 29 domains
python3 cli/main.py skills info pricing   # Domain deep-dive
python3 cli/main.py update                # Update knowledge base
```

```bash
# Direct search (no CLI needed)
python3 scripts/search.py "pricing strategy for SaaS" --domain pricing
python3 scripts/search.py "agritech market size" --domain industries
python3 scripts/search.py --stats                           # Knowledge stats
```

---

## 🔌 MCP Server

For IDEs that support [Model Context Protocol](https://modelcontextprotocol.io):

```json
{
  "mcpServers": {
    "easestart": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/easestart/mcp-server", "python", "server.py"]
    }
  }
}
```

**Available tools:**

| Tool | Description |
|------|-------------|
| `search` | Full knowledge graph search with BM25 + domain routing |
| `diagnose_stage` | Detect founder's current startup stage |
| `get_playbook` | Stage-specific playbook with next actions |
| `get_reasoning` | Decision rules for a given context |
| `get_stats` | Knowledge graph statistics |

---

## 📄 Intel Memo Reports

Generate multi-page HTML reports with a **citation system** and **interactive detail drawers**.

```bash
python3 scripts/generate_report.py --idea "AI tool for founders" --stage 2
```

**Output:** A beautiful, multi-page HTML report with:
- Stage-specific knowledge coverage with `(n)` citation markers
- Click any citation → interactive right-panel drawer shows source data
- 5-dimension confidence scorecard
- Personalized recommendations (no generic advice)
- Monochrome design system (Barlow Condensed + SF Pro Rounded)

```
output/{YYYY-MM-DD}-{slug}/
├── index.html            ← Hub page with 7 stage cards
├── shared.css            ← Design system tokens
└── stages/stage-{0-6}.html  ← Stage pages with citations
```

---

## 💡 Philosophy: Giantiny Biz

EaseStart isn't a tool dump. It's a **thinking system** built on 5 pillars that every agent enforces.

| # | Pillar | Principle | Agent Rule |
|:-:|--------|-----------|------------|
| **0** | CEO = Agent Manager | You decide, agents execute | All agents require CEO approval before execution |
| **1** | Specific Knowledge | You are Customer Zero — build what you know | `ideation-agent` asks "Are you Customer Zero?" |
| **2** | Counter-Positioning | Build what giants can't copy | `validation-agent` checks "Can competitors copy this?" |
| **3** | Code + Media Leverage | 1 person = infinite scale | `mvp-agent` prioritizes 1-person-operable stacks |
| **4** | Profit > Growth | Financial fat > hypergrowth | `growth-agent` runs profit margin check first |
| **5** | 3 Micro-MOATs | Templates + Data + Brand | `ops-agent` guides MOAT building by Stage 5 |

> _"Nobody can compete with you at being you."_ — Naval Ravikant

<details>
<summary><strong>EaseUI = Living Proof (Dogfooding)</strong></summary>

EaseStart is dogfooded by [EaseUI](https://easeui.design) — the living proof of Giantiny Biz philosophy:

| Pillar | EaseUI Evidence |
|--------|----------------|
| Customer Zero | Jang = designer who needed a better tool |
| Counter-position | AI-native design ≠ Figma (can't copy without rebuilding) |
| Code + Media | 1 founder → 172 waitlist signups → 11+ countries → 3 days |
| Profit > Growth | Bootstrap, zero VC, lean operations |
| Micro-MOAT | Community + proprietary design data |

</details>

---

## 🏗️ Architecture

```
┌───────────────────────────────────────────────────────────────────┐
│  L4: User Interface                                               │
│  AI IDE (Antigravity/Claude/Gemini/Cursor) · CLI · MCP · Reports │
├───────────────────────────────────────────────────────────────────┤
│  L3: Agent Layer                                                  │
│  Orchestrator → 14 Specialist Agents                              │
│  • Stage detection + routing        • Anti-pattern enforcement    │
│  • Progress tracking + exit gates   • Cross-agent collaboration   │
├───────────────────────────────────────────────────────────────────┤
│  L2: Retrieval Layer                                              │
│  BM25 Search Engine + Auto-Domain Routing                         │
│  • Keyword scoring + confidence     • Stage-weighted ranking      │
│  • Min-score threshold (0.5)        • Anti-pattern warning scan   │
├───────────────────────────────────────────────────────────────────┤
│  L1: Knowledge Graph                                              │
│  CSV Databases + Ontology + Decision Rules                        │
│  • 29+ domain files (1110 rows)      • 6 pillars                  │
│  • Relationships graph              • JSON decision rules         │
├───────────────────────────────────────────────────────────────────┤
│  L0: Data Ingestion                                               │
│  Autoresearch Module + Quality Scoring                            │
│  • Web crawl → LLM extract → CSV   • Link health verification    │
│  • Quality scoring pipeline         • Autonomous improvement loop │
└───────────────────────────────────────────────────────────────────┘
```

### Confidence Protocol

Search results include confidence levels mapped from BM25 scores:

| Confidence | BM25 Score | Agent Action |
|:----------:|:----------:|-------------|
| **HIGH** | ≥ 3.0 | Proceed autonomously — cite data source |
| **MEDIUM** | 1.0 – 2.99 | Present binary choice with recommendation |
| **LOW** | < 1.0 | Stop and ask — request founder context |

> 📖 **Full architecture:** [ARCHITECTURE.md](docs/ARCHITECTURE.md) — system design, agent routing, search engine internals, workflow engine

---

## 📁 Project Structure

```
easestart/
├── .agent/
│   ├── agents/              ← 14 specialist agent definitions
│   ├── skills/              ← Domain-specific knowledge modules
│   └── workflows/           ← 15 automated workflows
│
├── cli/                     ← 5-command CLI (init, search, doctor, skills, update)
│
├── data/                    ← 554-row CSV knowledge graph
│   ├── stages/              ← 7-stage model definitions
│   ├── tools/               ← 96 tools + 25 anti-patterns
│   ├── frameworks/          ← 18 startup frameworks
│   ├── industries/          ← 30 industry profiles
│   ├── marketing/           ← 5 marketing domain CSVs
│   ├── finance/             ← Bookkeeping + unit economics
│   ├── legal/               ← Checklists + contracts + security
│   ├── reasoning/           ← 30 decision rules
│   ├── psychology/          ← Burnout signals + resilience
│   ├── relationships.csv    ← Cross-domain knowledge links
│   └── _REGISTRY.md         ← Auto-generated domain index
│
├── scripts/
│   ├── core.py              ← BM25 search engine (zero deps, ~480 lines)
│   ├── search.py            ← Direct search CLI
│   ├── digital_validate.py  ← Digital Mom Test (Reddit + HN mining)
│   ├── generate_report.py   ← Intel Memo report generator
│   ├── dashboard.py         ← Local web dashboard (Flask)
│   ├── metrics.py           ← SQLite metrics tracker
│   ├── embed.py             ← Semantic search (ChromaDB)
│   ├── simulate.py          ← 10-persona simulation suite
│   ├── stress_test.py       ← 102-case routing accuracy test
│   ├── impact.py            ← Decision impact analysis
│   └── test_core.py         ← Unit tests
│
├── mcp-server/              ← MCP server for IDE integration (5 tools)
├── autoresearch/            ← Autonomous knowledge improvement loop
├── docs/                    ← User guide, architecture, philosophy, ontology
├── pm/                      ← PM agent state + daily logs
├── output/                  ← Generated reports + artifacts
├── templates/               ← Reusable content templates
├── plans/                   ← Feature specs + archived ideas
│
├── pyproject.toml           ← Package configuration
├── requirements-tools.txt   ← Optional tool dependencies
├── CHANGELOG.md             ← Release history
├── LICENSE                  ← PolyForm Shield 1.0.0
└── GEMINI.md                ← AI IDE configuration
```

---

## ✅ Quality Assurance

| Metric | Result |
|--------|:------:|
| Unit tests | **19/19** ✅ |
| Simulation (10 personas) | **10/10** ✅ |
| Stress test (102 routing cases) | **102/102** ✅ |
| Knowledge evaluation | **100/100** ✅ |
| Agent boundary tests | **12/12** ✅ |
| Digital validation score | **70.9/100** (STRONG) |
| External dependencies (core) | **0** |
| Knowledge rows | **554** |
| Industries covered | **30** |
| Python compatibility | **3.9 — 3.13** |

```bash
# Run all tests
python3 scripts/test_core.py                    # Unit tests
python3 scripts/simulate.py                     # 10-persona simulation
python3 scripts/stress_test.py                  # 102-case routing test
python3 autoresearch/evaluate.py                # Knowledge evaluation
```

---

## 📚 Documentation

| Document | Description |
|----------|------------|
| **[User Guide](docs/USER-GUIDE.md)** | **Start here** — full walkthrough from idea to scale |
| [Architecture](docs/ARCHITECTURE.md) | System design, agent routing, search engine internals |
| [Ontology](docs/ONTOLOGY.md) | Knowledge graph schemas for all 29 domains |
| [Philosophy](docs/PHILOSOPHY.md) | Giantiny Biz — the 5-pillar theory behind everything |
| [Design System](docs/DESIGN-SYSTEM.md) | Visual design tokens for reports |
| [Research](docs/RESEARCH.md) | Market research + competitive analysis |
| [CEO SOUL](docs/CEO_SOUL.md) | Self-evolving leadership profile |
| [Resolution](RESOLUTION.md) | Strategic direction — mission, architecture, plan |
| [Changelog](CHANGELOG.md) | Release history |

---

## 🗓️ Roadmap

- [ ] **Web dashboard** — visual knowledge explorer + stage tracker
- [ ] **Community templates** — user-contributed Lean Canvases, pitch decks
- [ ] **Multi-language** — Vietnamese, Spanish, Portuguese support
- [ ] **Plugin system** — custom agents + knowledge domains
- [ ] **Cloud sync** — optional sync for PM data across devices
- [ ] **AI voice assistant** — voice-first startup coaching via NotebookLM pipeline

> 💡 Have an idea? [Open an issue](https://github.com/EaseStart/easestart/issues) or submit a PR.

---

## 🙏 Standing on the Shoulders of Giants

EaseStart didn't emerge from a vacuum. We studied, learned from, and applied patterns from some of the most impactful open-source projects in the AI and developer tools ecosystem. Credit where credit is due.

| Project | What We Learned | What We Applied |
|---------|----------------|----------------|
| [**founders-kit**](https://github.com/avinash201199/founders-kit) | 500+ curated startup resources across 7 categories. Showed the _demand_ for structured founder knowledge, but lacked stage-awareness and actionability. | CSV-based structuring of all resources with stage columns, link health verification, and actionable metadata. EaseStart's entire data layer was born from rethinking this project. |
| [**ClaudeKit**](https://github.com/anthropics/claude-code) | Production-grade CLI architecture with multi-phase pipelines, health diagnostics (`ck doctor`), and skills management system. | CLI architecture (`init`, `doctor`, `skills`, `update` commands), 3-phase pipeline for `init`, RECONCILE→EXECUTE→REPORT pattern for `update`, protected files system, and skills domain management. |
| [**ui-ux-pro-max**](https://github.com/nicepkg/ui-ux-pro-max) | CSV + BM25 search is _optimal_ for knowledge bases under 5K entries — zero infrastructure, instant queries, spreadsheet-editable. Domain-faceted architecture with auto-detection. | Core search engine architecture (CSV + BM25 + auto-domain detection), multi-layer columns (searchable + actionable + implementation), JSON decision rules, zero-dependency design, and multi-platform IDE distribution. |
| [**GoClaw**](https://github.com/goclaw/agent-teams) | Agent teams with shared task boards, atomic claiming, auto-unblock gates, broadcast protocol, and immutable skill versioning. 4-Layer Security model. | Shared task board (`pm/taskboard.json`), auto-unblock gates for dependency resolution, broadcast protocol for cross-agent communication (`pm/agent-notes/_broadcast.md`), immutable skill versioning concept, and self-evolution architecture (CEO_SOUL). |
| [**ClawTeam**](https://github.com/clawteam/swarm) | Swarm intelligence patterns — agents sharing context through an inbox system, task dependency chains, and compound sprint workflows. | Agent Notes system (`pm/agent-notes/`) for inter-agent context sharing, task dependency protocol with `blocked_by` chains in PM agent, 3 compound sprint workflows (`/sprint-validate`, `/sprint-build`, `/sprint-growth`), and Output Protocol footer on all 14 agents. |
| [**GitNexus**](https://github.com/gitnexus/core) | Decision impact analysis that traces upstream/downstream effects across a knowledge graph. Auto-generated playbooks from structured data. Relationship-aware search. | Impact analysis script (`scripts/impact.py`) for cross-domain tracing, auto-generated playbooks (`scripts/playbook_gen.py`), relationship graph (`data/relationships.csv`) linking domains, and V2 MCP tools with relationship-aware search. |

### Patterns We Absorbed

```
founders-kit        → Data layer foundation (what to structure)
ui-ux-pro-max       → Search architecture (how to retrieve)
ClaudeKit           → CLI & developer experience (how to deliver)
GoClaw              → Agent coordination (how agents work together)
ClawTeam            → Swarm intelligence (how agents share context)
GitNexus            → Knowledge intelligence (how to reason across domains)
```

> _"We stand on the shoulders of giants — not to see further, but to build faster."_
>
> These projects taught us that the best AI systems aren't built in isolation. They're built by studying what works, understanding _why_ it works, and applying those lessons with intention. If you're building something similar, start by studying these repos.

---

## 🤝 Contributing

Contributions are welcome! Whether it's fixing a typo, adding knowledge rows, or building a new agent.

### Quick Contribution Guide

```bash
# 1. Fork & clone
git clone https://github.com/YOUR_USERNAME/easestart.git
cd easestart

# 2. Make changes (add/improve CSV data in data/)

# 3. Run tests
python3 scripts/test_core.py         # Unit tests pass?
python3 scripts/simulate.py          # All 10 personas pass?
python3 autoresearch/evaluate.py     # Knowledge score maintained?

# 4. Submit a PR
```

### Data Quality Rules

| Rule | Why |
|------|-----|
| Every row must be **factually grounded** | Real books, real tools, real companies — no AI-generated filler |
| At least **2 search columns** filled per row | Ensures findability via BM25 search |
| Include **Keywords** column | Powers domain routing |
| Cite sources | Maintains trust and verifiability |

### Ways to Contribute

- **Knowledge** — Add rows to existing domains or propose new domains
- **Agents** — Improve agent rules, add anti-patterns, refine stage boundaries
- **Workflows** — Create new workflows or improve existing ones
- **Tools** — Build new scripts or enhance existing ones
- **Docs** — Improve documentation, add examples, fix typos
- **Industries** — Add industry profiles with TAM, challenges, and tool recommendations

---

## 📄 License

[PolyForm Shield 1.0.0](LICENSE) — use it, fork it, build on it; just don't resell it or ship a competing product from it.

---

<div align="center">

**Built by [Jang Trịnh](https://linkedin.com/in/jangtrinh)** — Founder & Chief Product Engineer @ [EaseUI](https://easeui.design) · Ex-Head of Design @ [Elfie](https://elfie.co)

_Built by a solo founder, for solo founders._
_Dogfooded by EaseUI — the living proof of Giantiny Biz philosophy._

---

**If EaseStart helps you build something, [let us know](https://linkedin.com/in/jangtrinh) ✦**

</div>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:000000,100:1a1a2e&height=100&section=footer" width="100%" />
