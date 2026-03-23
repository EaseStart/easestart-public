---
description: "Full startup journey from Stage 0 to Scale — auto-routes through all 7 stages with gate enforcement."
---

# /startup-journey Workflow

> Master workflow: orchestrates the entire 7-stage journey. Auto-routes to specialist agents at each stage.

## Steps

### Step 1: Stage Detection
```
AGENT: easestart-orchestrator
ACTION: Run stage detection protocol (8 questions)
OUTPUT: Detected stage (0-6) with confidence score
```

### Step 2: Stage-Specific Routing

| Stage | Agent | Workflow |
|-------|-------|----------|
| 0 (Pre-Idea) | ideation-agent | Problem discovery |
| 1 (Ideation) | ideation-agent | /validate-idea Step 2-3 |
| 2 (Validation) | validation-agent | /validate-idea Step 4-7 |
| 3 (MVP) | mvp-agent | /build-mvp |
| 4 (PMF) | growth-agent | PMF optimization loop |
| 5 (Growth) | growth-agent | Channel scaling |
| 6 (Scale) | ops-agent | Team + MOAT building |

### Step 3: Exit Criteria Check
```
SEARCH: stages --stage [current]
DISPLAY: Exit criteria checklist
ASK: "Which of these have you completed?"
```

### Step 4: Stage Gate
```
IF all exit criteria met → "Ready for Stage N+1. Proceeding."
IF not all met → "Focus on: [unmet criteria]. Use /[relevant-workflow]."

CONFIDENCE:
  ≥90% exit criteria met → Auto-advance to next stage agent
  70-89% → Advance with 1-2 items flagged for monitoring
  50-69% → Present decision: advance vs consolidate to founder
  <50% → Block advancement. Must complete exit criteria first.
```

### Step 5: Giantiny Philosophy Review
```
At every stage transition, check 5 pillars:
  ① Are you still Customer Zero? (or have you drifted?)
  ② Is counter-position holding? (or has competition shifted?)
  ③ Are you leveraging Code+Media? (or growing team unnecessarily?)
  ④ Is profit margin positive? (or burning cash?)
  ⑤ Is at least 1 Micro-MOAT forming? (by Stage 4+)
```

### Step 6: Context Save
```
After each stage transition:
SAVE: progress, decisions, metrics to session context
SEARCH: reasoning --query "stage transition"
```

## Time Estimate: 12-24 months (full journey)

---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Detect | Identify current startup stage (0-6) | Stage assessment | Stage confirmed by founder |
| **2** Guide | Present stage-appropriate actions | Action plan | Plan matches stage |
| **3** Track | Monitor progress via STATE.md | Updated STATE.md | State reflects reality |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | Stage clear + knowledge base has relevant data | → Route to specialist |
| **MEDIUM** | Stage likely but founder context limited | → Confirm stage with 2-3 questions |
| **LOW** | Multiple possible stages | → Run full stage detection protocol |

### Anti-Patterns
- ❌ Skipping stage detection and assuming stage
- ❌ Recommending wrong-stage actions
- ❌ Not updating STATE.md after significant sessions
