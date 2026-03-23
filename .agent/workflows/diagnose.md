---
description: "Self-assessment diagnostic — helps founders identify their current stage and get routed to the right agent/data."
---

# /diagnose — Founder Stage Diagnostic

> Run this when a founder doesn't know where they are or what to do next.

## Protocol

### Step 1: Rapid Assessment (5 questions)

Ask each question and record YES / NO:

```
Q1: "Do you have a specific problem you personally experience?"
    YES → at least Stage 0
    NO  → Pre-Stage 0 (need problem discovery)

Q2: "Have you filled out a Lean Canvas with testable hypotheses?"
    YES → at least Stage 1
    NO  → Stage 0 (needs ideation)

Q3: "Have you deployed a product and observed real user behavior?"
    YES → at least Stage 2
    NO  → Stage 1 (build and deploy first)

Q4: "Do you have a working product with real users?"
    YES → at least Stage 3
    NO  → Stage 2 (needs MVP)

Q5: "Have you measured Sean Ellis PMF score ≥40%?"
    YES → at least Stage 4
    NO  → Stage 3 (needs PMF)
```

### Step 2: Determine Stage

| Q1 | Q2 | Q3 | Q4 | Q5 | Stage | Agent |
|----|----|----|----|----|-------|-------|
| NO | - | - | - | - | **Pre-0** | ideation-agent |
| YES | NO | - | - | - | **0** | ideation-agent |
| YES | YES | NO | - | - | **1** | mvp-agent (build first) |
| YES | YES | YES | NO | - | **2** | validation-agent + data-agent |
| YES | YES | YES | YES | NO | **3** | growth-agent |
| YES | YES | YES | YES | YES | **4+** | growth-agent or ops-agent |

### Step 3: Sub-Stage Assessment

Once stage is determined, check exit criteria from `stages.csv`:

```
SEARCH: stages --stage {determined_stage}
SHOW: exit criteria for current stage
ASK: "Which of these have you completed?"
DETERMINE: exact sub-stage position
```

### Step 4: Generate Action Plan

```
Based on stage assessment:
1. LIST uncompleted exit criteria (these are your TODOs)
2. SEARCH relevant domain for each TODO:
   - playbook --stage {stage} (rules)
   - reasoning --stage {stage} (decisions)
   - tools --stage {stage} (recommended tools)
   - templates (output artifacts to create)
3. PRIORITIZE: most impactful uncompleted item first
4. DELIVER: "Your #1 action this week is: {action}"
```

### Step 5: Wellness Check (Optional but Recommended)

```
ASK: "Before we dive in — how are you feeling about your energy?"

IF any burnout signals detected:
  RUN: wellness-agent monthly self-assessment
  BEFORE: proceeding with action plan
  
REASON: A burned-out founder makes bad decisions.
        Wellness check first, execution second.
```

## Cross-Domain Triggers

After diagnosis, automatically search related domains:

| If Stage | Auto-Search |
|----------|------------|
| 0-1 | frameworks (Lean Canvas, ICE) + casestudies (similar companies) |
| 1-2 | tools (recommended stack) + analytics_tools (PostHog) + legal (when to incorporate?) |
| 2-3 | analytics_funnels (funnel analysis) + analytics_events (what to track) + metrics (what to measure) |
| 3 | pricing (how to charge) + metrics (Sean Ellis) + casestudies (PMF examples) |
| 4 | pricing + fin_economics (unit economics) + mkt_channels (growth) |
| 5-6 | playbook (growth rules) + psychology (burnout check) + team_equity (first hire) |

## Anti-Patterns

- ❌ Doing pre-deploy interviews when you could deploy and observe real behavior
- ❌ Self-diagnosing as Stage 4 when you've never surveyed users
- ❌ Using this diagnostic to procrastinate instead of executing
- ❌ Ignoring wellness check ("I'm fine, let's just build")

---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Gather | Collect founder context + data | Context brief | Enough info to assess |
| **2** Analyze | Evaluate stage + blockers | Diagnostic report | Stage identified + blockers listed |
| **3** Route | Recommend next workflow/agent | Routing recommendation | Founder confirms direction |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | Clear stage + clear blockers + data supports | → Route to specialist |
| **MEDIUM** | Stage clear but blockers ambiguous | → Binary: A) Route with caveats, B) Gather more data |
| **LOW** | Can't determine stage from available info | → Stop, ask Socratic discovery questions |

### Anti-Patterns
- ❌ Diagnosing without asking founder context questions
- ❌ Routing to wrong-stage agent based on assumptions
- ❌ Skipping stage detection protocol
