---
description: "Validate a startup idea end-to-end — UX psychology-driven flow from Founder Intake through DOV scoring to behavioral validation."
---

# /validate-idea Workflow (Build-Ship-Measure)

> Full validation pipeline using UX psychology principles:
> **Intake → DOV → Market → Build → Observe → Interview → Decision**
>
> Psychology-driven design: Progressive Disclosure, IKEA Effect, Peak-End Rule, Zeigarnik Effect

## Prerequisites
- Founder has identified at least 1 problem area
- Willingness to build and ship fast

---

## 🧭 Progress Map

```
░░░░ Phase 0: INTAKE    — Know the founder (30 seconds)
████ Phase 1: DOV       — Deep Origin Validation (5 minutes)
████ Phase 2: MARKET    — Market reality check (10 minutes)
████ Phase 3: BUILD     — Ship & measure (1-2 weeks)
████ Phase 4: DECISION  — Go / Iterate / Pivot
```

> Show this progress map to the founder at the start. Update ░→█ as they advance.
> **Zeigarnik Effect:** Incomplete progress bars create psychological tension to complete.

---

## Phase 0: FOUNDER INTAKE (30 seconds)

> **Psychology:** Self-Determination Theory — autonomy, competence, relatedness.
> The founder must feel HEARD before being assessed.

> 🔴 **MANDATORY:** Do NOT skip this phase. Do NOT jump to scoring.
> This is the fix for the Cold Start Problem.

### Step 0.1: Idea Description

```
ASK: "Mô tả idea 1 câu: Bạn đang xây dựng cái gì, cho ai?"
EXTRACT: {idea}, {target_audience}, {industry}
```

### Step 0.2: Founder-Opportunity Fit (IdeaValidator §1.1)

```
ASK 3 QUESTIONS (batch — ask all at once):

  1. "Bạn có kinh nghiệm/kiến thức chuyên môn gì trong lĩnh vực {industry}?"
     → Maps to: Specific Knowledge

  2. "Bạn có hiểu rõ quy trình hiện tại mà khách hàng đang dùng để giải quyết vấn đề này không?"
     → Maps to: Domain Expertise

  3. "Bạn có mạng lưới (khách hàng, chuyên gia, đối tác) trong lĩnh vực này không?"
     → Maps to: Relationships

SCORE Founder-Opportunity Fit:
  3/3 (all YES)  → 18-20/20 (Strong Fit)
  2/3            → 13-17/20 (Moderate — need advisor/co-founder)
  1/3            → 8-12/20  (Weak — high risk, needs partner)
  0/3            → 0-7/20   (Red Flag — reconsider domain)
```

### Step 0.3: Customer Zero Check (Giantiny ①)

```
ASK: "Bạn có đang GẶP vấn đề này không? Nó ảnh hưởng đến bạn thế nào?"
IF YES → Record as Customer Zero ✅ (emotional connection detected)
IF NO  → "⚠️ Validation sẽ khó hơn 3x. Cân nhắc chọn vấn đề mà bạn tự trải qua."
```

### Step 0.4: Urgency Filter (Do-Nothing Scenario)

```
ASK: "Nếu KHÔNG AI xây dựng giải pháp này, chuyện gì xảy ra trong 6 tháng tới?"
     "Thiệt hại ước tính bao nhiêu tiền/thời gian?"

IF answer is vague → Nice-to-have ⚠️ (proceed with caution)
IF answer is concrete + measurable → Must-solve ✅ (strong signal)
```

> **IKEA Effect:** Founder just articulated their own Do-Nothing cost.
> They now FEEL the urgency — it's their words, not AI's analysis.

### Phase 0 Gate

```
COMPILE Founder Profile:
  Idea:                 {idea}
  Target:               {target_audience}
  Industry:             {industry}
  Founder-Fit Score:    {X}/20
  Customer Zero:        ✅/⚠️
  Urgency:              Must-solve / Nice-to-have
  Do-Nothing Cost:      {founder's own estimate}

IF Founder-Fit = 0/3 AND Customer Zero = ⚠️:
  → WARN: "Red flags: no domain expertise + not Customer Zero."
  → Binary: A) Proceed anyway (aware of risks), B) Pivot to personal problem
ELSE:
  → Auto-proceed to Phase 1
```

---

## Phase 1: DOV — Deep Origin Validation (5 minutes)

> **Psychology:** Progressive Disclosure — DOV tests the CORE before investing in full canvas.
> IKEA Effect — Founder does the analysis, system validates + enriches.

> **Source:** IdeaValidator Stage 1 — Monkey Problem, Weakchain, 4-Dimension Impact.

### Step 1.0: Knowledge Quality Gate (autoresearch)

> 🔬 **Auto-trigger:** Before DOV, verify knowledge base quality.

// turbo
```bash
python3 autoresearch/evaluate.py 2>&1 | grep "^score:\|^coverage:"
```

```
IF score < 90 OR coverage < 80:
  → SUGGEST: "Knowledge base has gaps. Run /autoresearch first for better insights."
  → Binary: A) Run /autoresearch sprint (5 min), B) Proceed anyway
IF score ≥ 90:
  → Auto-proceed to DOV
```

### Step 1.1: JTBD Statement (Founder writes)

> **IKEA Effect:** Founder writes it. System refines it.

```
ASK: "Viết 1 câu Jobs-to-be-Done theo cấu trúc:
      'Khi tôi [Context] nhưng [Barrier] → Giúp tôi [Goal] để [Outcome]'"

EXAMPLE: "Khi tôi MUA NHÀ nhưng KHÔNG HIỂU PHÁP LÝ → Giúp tôi KIỂM TRA RỦI RO để TRÁNH MẤT TIỀN"

SEARCH: frameworks --query "jobs to be done"
VALIDATE: Does JTBD cover functional + emotional jobs?
REFINE: Suggest improvements to founder's JTBD if needed
```

### Step 1.2: Monkey Problem (Founder identifies)

> **Information Gap:** Create curiosity before revealing.

```
TEASE: "Trong ngành {industry}, 80% startup thất bại vì không giải quyết được
        MỘT biến số quyết định. Monkey Problem = biến số đó."

ASK: "Theo bạn, đâu là biến số KHÓ NHẤT mà nếu không giải quyết được,
      toàn bộ JTBD sẽ thất bại?"

SEARCH: frameworks --query "monkey problem critical assumption"
VALIDATE: Is the founder's answer really the hardest variable?
ENRICH: Add context from KB if founder is close but not precise

🎢 PEAK MOMENT: "Monkey Problem của bạn là: ___. 
   Nếu không giải quyết được điều này, TẤT CẢ sẽ thất bại.
   Nhưng nếu giải quyết được — bạn có unfair advantage."
```

### Step 1.3: Weakchain (Founder maps)

> **IKEA Effect:** Founder maps the customer journey. System finds the break.

```
ASK: "Liệt kê 5-7 bước mà khách hàng hiện tại phải làm để giải quyết vấn đề này.
      Đánh dấu bước nào GÂY KHÓ CHỊU NHẤT."

EXAMPLE (BDS Law):
  1. Tìm nhà trên Batdongsan.com ✅
  2. Xem nhà, thương lượng ✅  
  3. Kiểm tra pháp lý ← 🔴 WEAKCHAIN (thuê luật sư 5-15tr, chờ 2 tuần)
  4. Ký hợp đồng, công chứng
  5. Sang tên sổ đỏ

SEARCH: frameworks --query "weakchain process friction entry point"
VALIDATE: Is the founder's marked step really the weakest?
IDENTIFY: What makeshift solution do customers currently use at this step?

OUTPUT: "Weakchain = Step {N}: {description}. Đây là điểm MVP nên bắt đầu."
```

### Step 1.4: 4-Dimension Impact Scoring

```
SCORE (using founder's context + KB data):
  Functional:       /10 (giải quyết JTBD nhanh hơn bao nhiêu?)
  Emotional:        /10 (giảm lo lắng, tăng tự tin?)
  Breakthrough UX:  /10 (so với giải pháp tạm bợ hiện tại?)
  Market Scale:     /10 (đủ người sẵn sàng trả tiền?)

SEARCH: frameworks --query "4 dimension impact assessment"
```

### DOV Scorecard (IdeaValidator 100-point system)

```
┌──────────────────────────────────────────────┐
│  📊 DOV SCORECARD                            │
│                                              │
│  Founder-Opportunity Fit:  {X}/20  {bar}     │  ← from Phase 0
│  Core Difficulty (Monkey): {X}/20  {bar}     │
│  Market Friction (Weak):   {X}/20  {bar}     │
│  Urgency & Reality:        {X}/20  {bar}     │  ← founder's Do-Nothing cost
│  Value Potential (4-D):    {X}/20  {bar}     │
│  ────────────────────────────────────        │
│  TOTAL:                    {X}/100           │
│                                              │
│  Benchmark: Average = 55 · Top 30% = 72+    │
│                                              │
│  Verdict: {Red Flag / Need Iteration / Go}   │
└──────────────────────────────────────────────┘

🎢 PEAK MOMENT: Show scorecard with benchmark comparison.
```

### Phase 1 Gate (Progressive Disclosure)

```
IF DOV < 50 (Red Flag):
  → "Ý tưởng có lỗ hổng ở tầng cốt lõi. Cần quay lại tìm vấn đề khác."
  → Binary: A) Pivot — explore different problem, B) Iterate — improve weakest pillar
  → ⛔ Do NOT proceed to Lean Canvas

IF DOV 50-69 (Need Iteration):
  → "Tiềm năng có, nhưng mắt xích chưa chặt. Trụ cột yếu nhất: {pillar}."
  → Binary: A) Iterate on weakest pillar, B) Proceed to market check (risky)
  → Only unlock: Problem + Customer + UVP blocks of Lean Canvas

IF DOV ≥ 70 (Validated to Start):
  → "✅ DOV passed. Idea tốt ở tầng cốt lõi. Phase 2: kiểm tra thị trường."
  → Unlock full Lean Canvas + Market Research
  → 🎢 CLIFFHANGER: "DOV = {score}. Nhưng thị trường có đồng ý không? Phase 2 sẽ cho biết..."
```

---

## Phase 2: MARKET VALIDATION + CANVAS (10 minutes)

> **Psychology:** Zeigarnik Effect — cliffhanger from Phase 1 pulls founder forward.
> Progressive Disclosure — canvas blocks unlock based on DOV score.

### Step 2.1: Lean Canvas (ideation-agent)

```
IF DOV ≥ 70:
  → Guide through ALL 9 blocks (full canvas)
IF DOV 50-69:
  → Guide through 3 blocks only: Problem, Customer Segments, UVP
  → "Strengthen these 3 before expanding to full canvas."

SEARCH: frameworks --query "lean canvas"
ACTION: Guide through blocks (pre-filled with Phase 0-1 data)

PRE-FILL from Phase 0-1:
  Problem:            → JTBD + Monkey Problem + Weakchain
  Customer Segments:  → {target_audience} from intake
  UVP:                → Solving {Monkey Problem} for {target} 
  Solution:           → Fix {Weakchain} using {approach}

OUTPUT: lean-canvas-v1.md
GATE: Required blocks filled → proceed
```

### Step 2.2: Counter-Position Check (Giantiny ②)

```
TEASE: "Có 1 câu hỏi phân biệt startup sống sót và startup chết:
        liệu đối thủ lớn có thể copy bạn không?"

ASK: "Nếu Google/đối thủ lớn nhất build cái này, họ có cần THAY ĐỔI
      mô hình kinh doanh hiện tại theo cách tự hại chính họ không?"

IF YES → Counter-positioned ✅
IF NO  → "Iterate trên business model cho đến khi tìm ra counter-position."

SEARCH: frameworks --query "counter-positioning structural anchors"
SEARCH: positioning --query "counter-positioning {industry}"

🎢 PEAK MOMENT: "Counter-position của bạn: {description}.
   Đây là lý do {competitor} KHÔNG THỂ copy bạn."
```

### Step 2.3: Market Sizing (TAM→F1→F2)

```
SEARCH: positioning --query "TAM bottom-up drill-down"
SEARCH: industries --query "{industry}"

ACTION: Guide founder through:
  TAM: Total industry size
  F1:  Sub-market (geography/demo/behavior filter)
  F2:  Niche where founder can be #1 immediately

VALIDATE: F2 estimated via bottom-up (customers × ARPU)
```

### Step 2.4: Market Timing — Why Now?

```
SEARCH: frameworks --query "market timing why now enabler"

CHECK 3 enablers:
  Technology:  What new tech makes this 10x cheaper/faster?
  Behavior:    What consumer habit changed recently?
  Regulatory:  What new law forces customers to act?

VERIFY: Google Trends + funding signals (if data available)
```

### Step 2.5: Cross-Agent Validation (Lucius L5)

```
ACTION: Run parallel evaluation

  IDEATION-AGENT evaluates:
    Market opportunity score    /100
    Problem severity score      /100
    Founder-market fit score    /100
    → Weighted average: {N}/100

  VALIDATION-AGENT evaluates:
    Market evidence score       /100
    Competitive landscape score /100
    Execution feasibility score /100
    → Weighted average: {M}/100

  GAP ANALYSIS (if |N - M| > 20):
    Show disagreement areas + recommendation
    Binary: A) Proceed with ideation's framing, B) Address validation's concerns first

GATE:
  Gap ≤ 20 → AUTO-proceed (agents agree)
  Gap > 20 → Show report, founder chooses A or B
  Both scores < 50 → BLOCK — pivot recommended
```

### Phase 2 Gate

```
IF DOV ≥ 70 AND Counter-Position found AND F2 validated:
  → "✅ Thị trường confirmed. Phase 3: Build & Ship."
  → 🎢 CLIFFHANGER: "Lý thuyết xong. Giờ thị trường THẬT sẽ phản hồi. Phase 3 = build + deploy."

IF Missing counter-position OR F2 too small:
  → Binary: A) Iterate on business model, B) Pivot to different market
```

---

## Phase 3: BUILD & VALIDATE (1-2 weeks)

> **Psychology:** The builder phase. Founder transitions from analysis to action.

### Step 3.1: Grand Slam Offer Design (IdeaValidator Stage 3)

```
SEARCH: pricing --query "grand slam offer value equation"

GUIDE founder through:
  1. Dream Outcome: What does the customer ultimately want?
  2. Perceived Likelihood: Why should they believe YOU?
  3. Time Delay: How fast do they see results?
  4. Effort & Sacrifice: What must THEY do?

  Value = (Dream Outcome × Likelihood) ÷ (Time Delay × Effort)

ASK: "List ALL problems your customer faces (from Monkey + Weakchain)."
ACTION: For each problem → specific solution → delivery method (self-serve/done-with-you/done-for-you)
OUTPUT: Grand Slam Offer with outcome-focused name + value-based pricing
```

### Step 3.2: Build & Deploy (mvp-agent + data-agent)

```
ACTION: AI-assisted build sprint (1-3 days)
  1. Tech stack selection (mvp-agent) — HARD_GATE: CEO approves
  2. Build core action (1 feature that proves value — the Weakchain fix)
  3. Deploy to production (public URL)
  4. Install PostHog with 5 P0 events (data-agent)
OUTPUT: Deployed product with analytics tracking
GATE: Product live + events firing → proceed
```

### Step 3.3: Distribute to Real Users

```
ACTION: Post on 2+ relevant communities
SEARCH: mkt_channels --query "community launch organic"
OUTPUT: Post URLs with UTM tracking
GATE: ≥50 real visitors (not friends/family) → proceed
WAIT: 48-72 hours for data collection
```

### Step 3.4: Behavioral Validation (data-agent + validation-agent)

```
ACTION: Analyze PostHog data
CHECK:
  Activation rate (core action completion): ≥30% = pass
  D7 return rate: ≥15% = pass
  Feature concentration: 1 feature = 80%+ usage = clear value
GATE: Behavioral data reviewed → proceed to interviews
```

### Step 3.5: Post-Deploy Interviews (validation-agent)

```
ACTION: Interview 15 users who ACTUALLY TRIED the product
  5 power users (3+ sessions) → WHY keep coming back?
  5 one-time users → WHY didn't they return?
  5 bounce users → WHY didn't they try core action?

RULES:
  ✅ Ask about ACTUAL experience (not hypothetical)
  ✅ Cross-reference interviews with behavioral data
  ❌ Never interview people who haven't tried the product

OUTPUT: validation-report.md
GATE: ≥10 interviews + cross-reference with analytics data
```

---

## Phase 4: DECISION (Peak Moment)

> **Psychology:** Peak-End Rule — this is the END of the journey.
> Make it memorable, clear, and actionable.

### Step 4.1: PMF Readiness Score

```
CALCULATE:
  Founder-Opportunity Fit        [from Phase 0]  /20
  DOV Score                      [from Phase 1]  /20
  Market Validation              [from Phase 2]  /20
  Behavioral data (activation)  [from Phase 3]   /20
  Post-deploy interviews        [from Phase 3]   /20
  TOTAL: /100
```

### Step 4.2: Final Scorecard

```
🎢 PEAK MOMENT #3 — The End (make it memorable):

┌──────────────────────────────────────────────┐
│  🏆 VALIDATION SCORECARD                     │
│                                              │
│  Founder Fit:        {X}/20  ████░░  {level} │
│  Idea Core (DOV):    {X}/20  █████░  {level} │
│  Market Reality:     {X}/20  ████░░  {level} │
│  User Behavior:      {X}/20  ███░░░  {level} │
│  User Interviews:    {X}/20  ████░░  {level} │
│  ─────────────────────────────────           │
│  TOTAL:              {X}/100                 │
│                                              │
│  📊 Benchmark: Average founder = 48/100      │
│               Top 30% = 72+  · Top 10% = 88+ │
│                                              │
│  Your ranking: Top {N}% of ideas on EaseStart│
└──────────────────────────────────────────────┘
```

### Step 4.3: Decision Gate

```
IF ≥ 72 (Top 30%):
  → "✅ GO — Strong validation. Ready for growth."
  → 🔗 Diderot: "Next: /sprint-growth or /generate-report for Intel Memo"

IF 50-71 (Average):
  → "⚡ ITERATE — Promising but needs work."
  → Show weakest pillar + specific improvement action
  → 🔗 Diderot: "Next: /deep-research on {weakest domain} or re-run /validate-idea"

IF < 50 (Below Average):
  → "🔄 PIVOT — Evidence suggests a different approach."
  → Show specific reasons from data
  → 🔗 Diderot: "Next: /validate-idea with a different problem, or /deep-research to find better angles"
```

---

## Anti-Patterns

```
❌ Skipping Phase 0 (Founder Intake) — leads to guessing Founder-Fit
❌ AI doing ALL analysis without founder input — no IKEA Effect = no ownership
❌ 9-block Canvas immediately — overwhelms founder (use Progressive Disclosure)
❌ Flat progression without peaks — forgettable experience
❌ Ending without next action — violates Diderot Effect  
❌ Interviewing hypothetical users before deploying product
❌ Surveys as primary validation (observe behavior first)
❌ Building for months without shipping to real users
❌ Trusting self-reports over behavioral data when they conflict
❌ Counting friends/family as "real users"
```

## UX Psychology Principles Applied

| Principle | Where Applied |
|---|---|
| **Self-Determination** (Deci & Ryan) | Phase 0: Founder feels heard before assessed |
| **Cognitive Load** (Sweller) | Progressive Disclosure: DOV → Canvas (not 9 blocks immediately) |
| **IKEA Effect** (Norton) | Steps 1.1-1.3: Founder writes JTBD, maps Weakchain, quantifies Do-Nothing |
| **Information Gap** (Loewenstein) | Steps 1.2, 2.2: Tease insight before revealing |
| **Peak-End Rule** (Kahneman) | 3 peaks: Monkey Problem, Counter-Position, Final Scorecard |
| **Zeigarnik Effect** | Progress map + cliffhangers between phases |
| **Diderot Effect** | Step 4.3: Every outcome links to a natural next workflow |

## Output Artifacts

- `founder-profile.md` (from Phase 0)
- `dov-scorecard.md` (from Phase 1)
- `lean-canvas-v1.md` (from Phase 2)
- `grand-slam-offer.md` (from Phase 3)
- `validation-report.md` (behavioral + interview cross-reference)
- `final-scorecard.md` (from Phase 4)
- `output/{slug}/index.html` (HVS-style validation report — auto-generated)

## Phase 4.5: GENERATE REPORT (Auto-trigger)

> **Trigger:** When Phase 4 verdict is GO (score ≥ 72) or founder says "build"
> **Skip if:** Founder chose PIVOT or KILL

### Step 4.5.1: Generate HVS-style Validation Report

// turbo
```bash
python3 scripts/generate_validation_report.py "{idea}" --industry {industry} --open
```

This generates a single-page HTML report with auto-research:
- **Reframe** — Pain vs Feature, benchmarks, frameworks, 3 approaches
- **DOV Validation** — Founder fit, JTBD, problem anatomy, scorecard
- **Market Intel** — TAM, competitors, timing (auto-researched from KB)
- **Grand Slam Offer** — Value equation, pricing (auto-researched)
- **Digital Validation** — Reddit + HN pain signals (live scraping)
- **Roadmap** — Timeline with phases

> The script auto-researches all gaps (30+ KB domains + Reddit/HN). Use `--skip-research` for faster generation without live data.

### Step 4.5.2: AI Enrichment (Optional)

If founder wants deeper content, create `enrichment.json` with AI-synthesized data:

```bash
python3 scripts/generate_validation_report.py "{idea}" --data enrichment.json --open
```

### Anti-Patterns
- ❌ Generating report before Phase 4 verdict — premature
- ❌ Skipping auto-research — sections will have generic placeholders
- ❌ Not opening in browser for founder review

## Time Estimate: 1-2 weeks (AI-era compressed)

---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **0** Intake | Founder profile + Customer Zero | Founder profile | All 4 questions answered |
| **1** DOV | Problem anatomy + JTBD + scoring | DOV scorecard | Score ≥ 50 to proceed |
| **2** Market | Canvas + Counter-position + TAM | Lean Canvas + Market report | Counter-position found |
| **3** Build | Deploy + observe + interview | Validation report | ≥10 interviews + data |
| **4** Decision | Final scoring + recommendation | Final scorecard | Founder chooses Go/Iterate/Pivot |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | DOV ≥ 72 + Customer Zero ✅ + Counter-position found | → Proceed to build |
| **MEDIUM** | DOV 50-71 + some concerns | → Binary: A) Build anyway (low cost), B) More research |
| **LOW** | DOV < 50 or no Customer Zero + no counter-position | → Pivot or kill the idea |

### Anti-Patterns
- ❌ Validating an idea you don't personally use (no Customer Zero)
- ❌ Skipping Founder Intake — the system MUST know founder context
- ❌ Skipping competitive research — someone is already doing this
- ❌ Perfect Lean Canvas syndrome — v1 is always wrong, and that's OK
- ❌ Scoring without founder input — never guess what you can ask
