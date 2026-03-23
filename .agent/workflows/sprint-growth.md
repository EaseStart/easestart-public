---
description: 4-week growth sprint (Stage 3→5) — chains growth, marketing, and finance agents with dependency gates.
---

# /sprint-growth — Growth Sprint

> One command launches a full growth sprint. 3 steps, 3 agents, dependency-gated.

---

## Overview

| Property | Value |
|----------|-------|
| **Duration** | 4 weeks |
| **Stages** | 3 → 5 |
| **Agents** | growth → marketing → finance |
| **Tasks** | 3, dependency-chained |

## Task Chain

```
✅ T1: Channel selection + PMF confirmation (growth-agent)
   └→ T2: Content + acquisition strategy (marketing-agent) ← blocked by T1
      └→ T3: Unit economics + pricing optimization (finance-agent) ← blocked by T2
```

---

### Auto-Research: Marketing Data Check (autoresearch)

> 🔬 **Auto-trigger:** Before growth sprint, verify marketing knowledge quality.

// turbo
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from core import load_csv
for d in ['mkt_channels', 'mkt_growth', 'mkt_launch', 'mkt_sales']:
    rows, _ = load_csv(d)
    status = '✅' if len(rows) >= 5 else '⚠️ LOW'
    print(f'  {d}: {len(rows)} rows {status}')
"
```

```
IF any marketing domain < 5 rows:
  → SUGGEST: "Some marketing domains have limited data. Run /autoresearch first."
  → Binary: A) Enrich marketing domains (5 min), B) Proceed anyway
```

## Step 1: Channel Selection (growth-agent)

**Agent:** `growth-agent`
**Deliverable:** Top 2 channels + Bullseye Framework analysis

### Actions
1. Confirm PMF ≥ 40% (hard gate — cannot proceed without)
2. Run Bullseye Framework (19 channels → test 3 → double down on 1-2)
3. Search marketing channels domain for stage-appropriate options
4. Apply Giantiny ④ check: profit margin positive before scaling?
5. Define growth experiment plan (2-week test per channel)

### Gate — `HARD_GATE` (CEO must approve channels)
- [ ] PMF ≥ 40% confirmed
- [ ] Bullseye Framework completed
- [ ] Top 2 channels selected with reasoning
- [ ] Budget allocated per channel (Giantiny: lean)
- [ ] Giantiny ④ profit check passed

### Agent Note Output
→ Write `pm/agent-notes/growth-agent-output.md` with:
- Selected channels + reasoning
- Experiment plan + success criteria
- Budget breakdown

---

## Step 2: Content + Acquisition Strategy (marketing-agent) ← blocked by Step 1

**Agent:** `marketing-agent`
**Deliverable:** Content calendar + landing page + email sequence

### Actions
1. Read growth-agent's channel selection
2. Create 30-day content calendar for selected channels
3. Optimize landing page (CTA, above-the-fold, social proof)
4. Design onboarding email sequence (5 emails)
5. Set up community strategy (if applicable)

### Gate — `SOFT_GATE` (auto-unblock finance → notify CEO)
- [ ] Content calendar for 30 days
- [ ] Landing page copy reviewed
- [ ] Email sequence drafted (5 onboarding emails)
- [ ] Founder notified (auto-proceeds to Step 3)

### Agent Note Output
→ Write `pm/agent-notes/marketing-agent-output.md` with:
- Content calendar summary
- Key messaging / positioning
- Channel-specific tactics

---

## Step 3: Unit Economics (finance-agent) ← blocked by Step 2

**Agent:** `finance-agent`
**Deliverable:** Unit economics dashboard + pricing optimization

### Actions
1. Read growth + marketing outputs
2. Calculate CAC per channel
3. Calculate LTV (based on current retention data)
4. Compute LTV:CAC ratio (target ≥3:1)
5. Run pricing sensitivity analysis
6. Project 12-month runway at current burn rate

### Gate — `HARD_GATE` (CEO must review financials)
- [ ] CAC calculated per channel
- [ ] LTV estimated with retention data
- [ ] LTV:CAC ≥ 3:1 (or plan to improve)
- [ ] 12-month cash flow projection
- [ ] Founder reviews financials

### Agent Note Output
→ Write `pm/agent-notes/finance-agent-output.md` with:
- Unit economics summary (CAC, LTV, ratio)
- Burn rate + runway
- Pricing recommendation

---

## Sprint Completion

When all 3 steps complete:

1. Update `pm/agent-notes/_state.json`:
   - Set stage to 4 or 5 (based on metrics)
   - Update all agent_outputs

2. Decision point:
   - If profitable → Continue bootstrapping (Giantiny ④)
   - If need capital → Suggest `/fundraise` workflow
   - If team needed → Suggest ops-agent consultation

3. Track metrics: MRR, CAC, LTV, LTV:CAC ratio, monthly burn

---

## Anti-Patterns (Lucius L4)

- ❌ Starting growth sprint without PMF ≥ 40% confirmed — hard gate
- ❌ Spreading budget across 5+ channels — focus on 1-2 channels max
- ❌ Scaling before unit economics positive — profit > growth (Giantiny ④)
- ❌ Content calendar without channel data — match content to proven channel
- ❌ Revenue projection without customer interview data backing — evidence-based only
- ❌ Sprint without gate approval at each step — CEO decides, not agent
- ❌ Completing sprint without updating `_state.json` — breaks context chain

---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Channels | Identify + rank growth channels (Bullseye) | Channel ranking doc | Top 3 channels identified |
| **2** Test | Run experiments on top channels | Experiment results | CAC + conversion data collected |
| **3** Double Down | Scale winning channel | Scaling plan | Channel shows positive ROI |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | PMF confirmed + channel data clear + ROI positive | → Scale the channel |
| **MEDIUM** | Channel promising but data limited | → Binary: A) Test more, B) Try next channel |
| **LOW** | No channel showing results after 3+ experiments | → Re-evaluate PMF before more growth |

### Anti-Patterns
- ❌ Growth before PMF confirmed (Stage < 4)
- ❌ Spreading budget across 5+ channels — focus on 1-2
- ❌ Copying competitor channels without testing fit
