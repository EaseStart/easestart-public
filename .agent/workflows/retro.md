---
description: Weekly engineering retrospective — git data analysis, productivity metrics, session detection, shipping streaks. Run solo or team.
---

# /retro — Engineering Retrospective

> Source: GStack Retro + Lucius L3 Research Grounding.
> Philosophy: Data-driven narrative, not vibes. Decisions backed by real productivity data.

**When to use:** End of week, end of sprint, or anytime you want to reflect on work patterns.

---

## Step 1: Gather Raw Data

Identify the current user and time window:

// turbo
```bash
git config user.name
git config user.email
```

Default window: `--since="7 days ago"`. Override with `--window "14 days"` or `--since "2024-03-01"`.

Run ALL of these git commands (they are independent):

// turbo
```bash
# 1. All commits with stats
git log origin/main --since="7 days ago" --format="%H|%aN|%ae|%ai|%s" --shortstat

# 2. Per-commit file breakdown (test vs prod)
git log origin/main --since="7 days ago" --format="COMMIT:%H|%aN" --numstat

# 3. Timestamps for session detection
git log origin/main --since="7 days ago" --format="%at|%aN|%ai|%s" | sort -n

# 4. File hotspots
git log origin/main --since="7 days ago" --format="" --name-only | grep -v '^$' | sort | uniq -c | sort -rn

# 5. Per-author commit counts
git shortlog origin/main --since="7 days ago" -sn --no-merges
```

---

## Step 2: Compute Metrics

Calculate and present in a summary table:

```
| Metric | Value |
|--------|-------|
| Commits to main | N |
| Contributors | N |
| Total insertions | +N |
| Total deletions | -N |
| Net LOC | N |
| Test LOC ratio | N% |
| Active days | N |
| Detected sessions | N |
```

---

## Step 3: Commit Time Distribution

Show hourly histogram:

```
Hour  Commits  ████████████████
 08:    4      ████
 09:    7      ███████
 10:    5      █████
 ...
 22:    3      ███
 23:    1      █
```

Identify and call out:
- **Peak hours** — when you're most productive
- **Dead zones** — blocks with zero activity
- **Late-night clusters** — after 10pm (burnout signal)
- **Pattern type** — bimodal (morning/evening) or continuous

---

## Step 4: Work Session Detection

Detect sessions using **45-minute gap** threshold between consecutive commits.

For each session:
- Start/end time
- Number of commits
- Duration in minutes

Classify:
| Type | Duration | Meaning |
|------|----------|---------|
| **Deep session** | 50+ min | Focused, high-output work |
| **Medium session** | 20-50 min | Standard development |
| **Micro session** | < 20 min | Single-commit, fire-and-forget |

Calculate:
- Total active coding time
- Average session length
- LOC per hour of active time
- Deep session ratio (% of total time in deep sessions)

---

## Step 5: Commit Type Breakdown

Categorize by conventional commit prefix:

```
feat:     20  (40%)  ████████████████████
fix:      27  (54%)  ███████████████████████████
refactor:  2  ( 4%)  ██
test:      1  ( 2%)  █
```

> ⚠️ **Flag if fix ratio > 50%** — signals "ship fast, fix fast" pattern that may indicate review gaps.

---

## Step 6: Hotspot Analysis

Show top 10 most-changed files. Flag:
- Files changed **5+ times** → churn hotspot (potential refactor target)
- **Test files in hotspot** → good (tests evolving with code)
- **Config files in hotspot** → bad (unstable configuration)

---

## Step 7: Focus Score + Ship of the Week

**Focus Score:** % of commits touching the top 3 directories. High = focused. Low = scattered.

**Ship of the Week:** Largest coherent feature or fix shipped. Describe in 1-2 lines.

---

## Step 8: Save History

Save retro snapshot for trend tracking:

```bash
mkdir -p .context/retros
```

Write JSON file `.context/retros/retro-YYYY-MM-DD.json`:
```json
{
  "date": "YYYY-MM-DD",
  "window": "7 days",
  "commits": N,
  "contributors": N,
  "netLoc": N,
  "testRatio": 0.XX,
  "activeDays": N,
  "sessions": N,
  "deepSessionRatio": 0.XX,
  "focusScore": 0.XX,
  "fixRatio": 0.XX,
  "hotspots": ["file1", "file2", "file3"],
  "shipOfTheWeek": "description"
}
```

---

## Step 9: Write the Narrative

Structure the output as:

```markdown
# Engineering Retro: [date range]

## Summary
[N] commits | [N] contributors | [+/-] LOC | [N]% tests | Peak: [hour]

## Time & Session Patterns
[Histogram + session analysis]

## Shipping Velocity
[Commit type breakdown + fix ratio warning if applicable]

## Code Health
[Hotspot analysis + focus score]

## Your Week (personal deep-dive)
[Biggest ship, patterns, what went well, what to improve]

## Top 3 Wins
1. [Win]
2. [Win]
3. [Win]

## 3 Things to Improve
1. [Improvement]
2. [Improvement]
3. [Improvement]

## 3 Habits for Next Week
1. [Habit]
2. [Habit]
3. [Habit]
```

---

## Week-over-Week Trends

If previous retro exists in `.context/retros/`:

```
| Metric | Last Week | This Week | Delta |
|--------|-----------|-----------|-------|
| Commits | N | N | +/-N |
| Test Ratio | N% | N% | +/-N% |
| Deep Sessions | N | N | +/-N |
| Fix Ratio | N% | N% | +/-N% |
```

---

## Tone

- **Candid, not mean.** Name real patterns.
- **Data-driven, not vibes.** Every claim backed by a metric.
- **Actionable, not generic.** "Write tests" is useless. "Add edge case tests for upload flow (currently 0% branch coverage in `upload.ts`)" is useful.
- **Celebrate wins.** Especially shipping streaks.

---

## Important Rules

- ❌ Never fabricate metrics — only use real git data
- ❌ Never skip the JSON snapshot — trends are the real value
- ✅ Always note if test ratio < 30% (concern) or > 50% (excellent)
- ✅ Always flag fix ratio > 50% (potential review gap)
- ✅ Always identify the Ship of the Week

---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Gather | Git log + stats extraction | Raw data (commits, LOC, files) | Git data parsed successfully |
| **2** Compute | Metrics calculation | Metrics JSON | All metrics computed |
| **3** Analyze | Distribution + sessions + hotspots | Analysis report | Patterns identified |
| **4** Narrate | Human-readable retrospective | `retro-YYYY-MM-DD.md` | Narrative complete with insights |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | ≥ 50 commits in period + clear patterns | → Full retro with recommendations |
| **MEDIUM** | 10-49 commits, some patterns | → Shorter retro, flag data limitations |
| **LOW** | < 10 commits in period | → Skip detailed analysis, note low activity |

### Anti-Patterns
- ❌ Running retro on < 7 days of data — not enough signal
- ❌ Retro without actionable insights — observation without improvement plan
- ❌ Ignoring session patterns (late-night coding = burnout signal)
- ❌ Not saving history for trend comparison
