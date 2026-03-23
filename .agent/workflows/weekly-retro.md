---
description: "Weekly retrospective — collect week data, reflect with 4Ls, plan next cycle, score momentum. Lucius 4-phase pipeline."
---

# Weekly Retro Workflow

> PM Agent workflow for weekly retrospective + sprint planning.
> Sources: 4Ls Retrospective, Shape Up appetite, Linear Method momentum, Fake Investor Update.

---

## Phase 1: COLLECT — Aggregate Week Data

> **Output:** Week summary document
> **Skills:** pm-tracking, `gws-workspace`
> **Gate:** ≥ 5 daily entries exist for the week

### Actions

0. **Auto-Pull Data:** Run `gws workflow +weekly-digest` for meetings/tasks summary and `gws sheets +read` to fetch the momentum trend for the week.
1. Aggregate all daily logs for the week
2. Count: shipped items, carried items, new blockers, resolved blockers
3. List all decisions made this week
4. Pull momentum scores from each daily (cross-check with Sheets data)

### Anti-Patterns
- ❌ Running retro with < 3 dailies — insufficient data to reflect
- ❌ Only counting shipped — carried items and blockers are equally important
- ❌ Retro without including decision count — decisions are shipped too

---

## Phase 2: REFLECT — 4Ls Analysis

> **Output:** 4Ls reflection document
> **Skills:** pm-tracking (pm-frameworks.csv → 4Ls Retrospective)
> **Gate:** At least 1 item per L category

### Actions

1. **Liked:** What went well? What should we keep doing?
2. **Learned:** What new insight emerged this week?
3. **Lacked:** What was missing? Tools, time, clarity, skills?
4. **Longed For:** What do we wish we had? Features, processes, people?
5. Compare with last week's 4Ls — are patterns repeating?

### Anti-Patterns
- ❌ All items in "Liked" — if nothing lacked, you're not being honest
- ❌ Same "Lacked" item for 3+ weeks — it's not a retro item, it's a blocker
- ❌ "Longed For" without action plan — wishes without plans are daydreams

---

## Phase 3: PLAN — Next Cycle Priorities

> **Output:** Next week plan with appetite estimates
> **Skills:** pm-tracking, `gws-workspace`
> **Gate:** ≤ 5 priorities, each with appetite estimate

### Actions

1. Review project roadmaps and outstanding items
2. Appetite check per priority: 1 day / 1 week / 2 weeks?
3. If anything > 2 weeks → needs re-shaping (too big, split it)
4. Select ≤ 5 priorities for next week
5. **Action:** Run `gws calendar +insert` to create Time Blocks for the top 3 priorities on the calendar.
6. Set success criteria: "Week is a win if we ship {X}"

### Anti-Patterns
- ❌ 10+ priorities for next week — that's a backlog, not a plan
- ❌ Priority without appetite — "build feature X" without time estimate
- ❌ Planning without reviewing this week's carry-overs — ignoring debt
- ❌ No success criteria — how do you know if the week was good?

---

## Phase 4: MOMENTUM — Score Sprint Health

> **Output:** Momentum report with trend analysis
> **Skills:** pm-tracking (pm-frameworks.csv → Momentum Scoring)
> **Gate:** Score explained with evidence from week's data

### Actions

1. Calculate momentum score:
   ```
   Momentum = (Shipped × 30) + (Decisions × 20) + (Blockers Resolved × 20)
            - (Blockers Open × 15) - (Carried × 10) - (Skipped Dailies × 5)
   ```
2. Compare with last 3 weeks: trend ↑ or ↓?
3. Health assessment: 🟢 (80+) / 🟡 (60-79) / 🟠 (40-59) / 🔴 (<40)
4. If 🔴: STOP — do not plan new work. Diagnose first.
5. Optional: Write "Fake Investor Update" monthly for accountability

### Anti-Patterns
- ❌ Ignoring declining momentum trend for 3+ weeks — systemic issue
- ❌ Momentum < 40 without pause — shipping while sinking
- ❌ Celebrating high score without checking quality — velocity ≠ value
- ❌ Comparing momentum across different projects — each has its own rhythm

---

## Phase 5: DEV STATS — Engineering Health (Stage 3+)

> Source: gstack `/retro` — git-based engineering metrics.
> **Skip if:** Founder is pre-Stage 3 (no code yet).

### Actions

1. **Git Stats** (auto-collect from repo):
   ```bash
   # Lines added/removed this week
   git log --since="1 week ago" --numstat --pretty="%H" | awk 'NF==3 {add+=$1; del+=$2} END {print "+" add " / -" del}'
   
   # Commits this week
   git log --since="1 week ago" --oneline | wc -l
   
   # Files changed
   git log --since="1 week ago" --name-only --pretty=format: | sort -u | wc -l
   ```

2. **Test Coverage Trend:**
   ```
   Last week: {N} tests passing
   This week: {M} tests passing
   Delta: +{M-N} new tests
   Trend: ↑ improving / → stable / ↓ declining
   ```

3. **Shipping Streak:**
   ```
   Consecutive days with successful deploys: {N}
   Record: {max} days
   🔥 if streak > 3 days
   ```

4. **Time-to-Ship:**
   ```
   Average: idea → production = {N} days this week
   vs last week: {comparison}
   ```

5. **Dev Pipeline Health:**
   ```
   /code-review runs this week: {N}
   /qa runs this week: {N}
   /ship runs this week: {N}
   Pipeline skip rate: {%} (lower is better)
   ```

### Dev Stats Report Format

```
┌─────────────────────────────────────────┐
│  DEV STATS — Week of {date}            │
│                                          │
│  📊 LOC: +{add} / -{del}               │
│  📦 Commits: {N}                        │
│  🧪 Tests: {passed}/{total} ({trend})   │
│  🔥 Ship streak: {N} days              │
│  ⏱️  Time-to-ship: {N} days avg        │
│  🔄 Pipeline: {N} full runs            │
└─────────────────────────────────────────┘
```

### Anti-Patterns
- ❌ Celebrating LOC without checking test coverage — more code + fewer tests = more bugs
- ❌ Ship streak obsession — shipping garbage daily is worse than shipping quality weekly
- ❌ Skipping dev stats pre-Stage 3 — no code = no stats needed


---

## Lucius Compliance

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | Full week of data + clear patterns + actionable insights | → Present retro |
| **MEDIUM** | Partial data but some insights | → Present with data limitations noted |
| **LOW** | < 3 days of data or no meaningful patterns | → Skip retro, note for next week |

### Anti-Patterns
- ❌ Retro without actionable next steps — observation without improvement is wasted
- ❌ Running retro on < 3 days of data — not enough signal
- ❌ Not comparing to previous retros for trend detection
