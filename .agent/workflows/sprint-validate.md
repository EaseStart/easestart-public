---
description: Sprint Validate — post-deploy validation via behavioral data + user interviews (Stage 2→3 in 1-2 weeks)
---

# /sprint-validate — Validation Sprint (Build-Ship-Measure)

> Validate deployed product through real user behavior + post-deploy interviews.
> **Prerequisite:** sprint-build completed (product deployed + tracking active).

---

## Overview

| Property | Value |
|----------|-------|
| **Duration** | **1-2 weeks** |
| **Stages** | 2 → 3 |
| **Agents** | data-agent → validation-agent → growth-agent → orchestrator |
| **Tasks** | 5, dependency-chained |

## Task Chain

```
✅ T1: Behavioral data review (data-agent) [SOFT_GATE]
   └→ T2: Funnel analysis + fixes (data-agent) [SOFT_GATE]
      └→ T3: Post-deploy interviews (validation-agent) [SOFT_GATE]
         └→ T4: Pricing hypothesis (growth-agent) [HARD_GATE]
            └→ T5: Stage decision (orchestrator) [HARD_GATE]
```

---

## T1: Behavioral Data Review — SOFT_GATE

**Owner:** `data-agent` | **Prerequisite:** ≥50 visitors

1. Pull PostHog: visitors, template selections, core actions
2. Calculate: activation rate, D7 return, feature concentration

**Gate:**
- [ ] ≥50 visitors tracked
- [ ] Core metrics calculated
- [ ] Auto-advance to T2

→ `pm/agent-notes/data-agent-output.md`

---

## T2: Funnel Analysis — SOFT_GATE

**Owner:** `data-agent` | **Blocked by:** T1

1. Search `analytics_funnels` for product-type template
2. Map data to funnel steps
3. Identify worst drop-off
4. Recommend fix

**Gate:**
- [ ] Funnel mapped with rates
- [ ] Worst drop-off identified
- [ ] Auto-advance to T3

---

## T3: Post-Deploy Interviews — SOFT_GATE

**Owner:** `validation-agent` | **Blocked by:** T2

1. Segment users: power (3+ sessions), one-time, bounce
2. Interview 5 per segment (15 total)
3. Modified Mom Test — about ACTUAL product experience
4. Cross-reference interviews with behavioral data
   - Trust behavior over self-reports when they conflict

**Gate:**
- [ ] ≥10 interviews completed
- [ ] All 3 segments represented
- [ ] Interview data cross-referenced with analytics
- [ ] Auto-advance to T4

→ `pm/agent-notes/validation-agent-output.md`

---

### Auto-Research: Pricing Data Check (autoresearch)

> 🔬 **Auto-trigger:** Before pricing hypothesis, verify pricing domain coverage.

// turbo
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from core import load_csv
rows, _ = load_csv('pricing')
print(f'pricing domain: {len(rows)} rows')
if len(rows) < 5: print('⚠️ Low pricing data — consider /autoresearch enrichment')
"
```

## T4: Pricing Hypothesis — HARD_GATE

**Owner:** `growth-agent` | **Blocked by:** T3

1. Read validation data (behavioral + interviews)
2. Search `pricing` domain
3. Propose 2-3 pricing tiers
4. Run Giantiny ④ (Profit > Growth)

**Gate:**
- [ ] Pricing backed by real usage data
- [ ] Competitor pricing researched
- [ ] **CEO approves pricing model**

→ `pm/agent-notes/growth-agent-output.md`

---

## T5: Stage Decision — HARD_GATE

**Owner:** `orchestrator` | **Blocked by:** T4

Present CEO:

```
📊 Validation Summary:
  Activation: {X}% (≥30% = pass)
  D7 Retention: {Y}% (≥15% = pass)
  Interviews: {N} done
  Revenue signal: {fake door click rate}%

🎯 Decision:
  A) STAGE 3 → Metrics pass. Scale distribution.
  B) ITERATE → Fix {worst drop-off}. Stay Stage 2.
  C) PIVOT → Kill signals. Back to Stage 1.
```

**Gate:**
- [ ] All metrics + interview summary presented
- [ ] **CEO decides: continue / iterate / pivot**

→ Broadcast: `[orchestrator] Sprint Validate: {decision} — {X}% activation, {Y}% D7 | Sprint: sprint-validate`

---

## Timeline

| Task | Duration |
|------|----------|
| T1-T2 | 3 hours (data exists) |
| T3 | 1 week (interviews) |
| T4 | 2 hours |
| T5 | 1 hour |
| **Total** | **1-2 weeks** |

## Anti-Patterns
- ❌ Interviewing hypothetical users (not product users)
- ❌ Skipping behavioral data → going straight to interviews
- ❌ Trusting interviews over analytics when they conflict
- ❌ Moving to Stage 3 without measuring activation + retention
- ❌ Pricing without real usage data

---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Setup | Deploy + configure analytics | Live product with tracking | Events firing correctly |
| **2** Observe | Collect behavioral data (≥50 users) | Behavioral data report | Sufficient sample size |
| **3** Interview | Post-deploy interviews (15+) | Interview insights | Patterns identified |
| **4** Score | PMF measurement + decision | PMF scorecard | Pivot/persevere/iterate decision |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | ≥50 users + 15 interviews + PMF ≥40% | → Proceed to growth |
| **MEDIUM** | Data collected but signals mixed | → Binary: A) Iterate features, B) More user testing |
| **LOW** | <50 users or <15 interviews | → Stop, not enough data to decide |

### Anti-Patterns
- ❌ Interviewing before deploying — ask about REAL experience, not hypothetical
- ❌ Trusting self-reports over behavioral data
- ❌ Declaring PMF without ≥40% "very disappointed" score
