---
description: Quarterly review of all 13 EaseStart agents for staleness, accuracy, and relevance. Run every 3 months or after major changes.
---

# /agent-review — Periodic Agent Review

> Prevent drift. Keep agents sharp. Run quarterly.

---

## When to Use

- Every 3 months (quarterly cadence)
- After significant EaseStart architecture changes
- When agents give noticeably stale recommendations
- When new CSV data domains are added

## Review Checklist

Run this for **each** of the 13 agents:

### Per-Agent Checks

```markdown
## Agent: {agent-name}

### 1. Instructions Relevance
- [ ] Agent description still accurate?
- [ ] Trigger conditions still correct?
- [ ] Stage assignments still make sense?
- [ ] All referenced CSV domains still exist?

### 2. Data Currency
- [ ] CSV data sources agent uses — are they up to date?
- [ ] Anti-patterns list — any new ones to add?
- [ ] Case studies — are examples still relevant?
- [ ] Tools recommended — any discontinued or better alternatives?

### 3. Verification Checklist Quality
- [ ] Verification checks still catching real issues?
- [ ] Any new failure modes to add?
- [ ] Giantiny pillar references still aligned?

### 4. Integration Health
- [ ] Inter-agent triggers still firing correctly?
- [ ] NotebookLM integration (if applicable) still working?
- [ ] Deep research workflow connection (if applicable) current?

### Verdict: {PASS | UPDATE NEEDED | MAJOR REWRITE}
```

### System-Level Checks

```markdown
## System Health
- [ ] Orchestrator routing — run 5 test queries, all route correctly?
- [ ] Handoff workflow — load test with sample HANDOFF.md?
- [ ] autoresearch evaluate.py — score stable or improving?
- [ ] Workflow count — any new workflows needed based on usage patterns?
- [ ] data/sessions/ — cleanup old handoff files (> 30 days)?
```

## Output

Create report: `data/sessions/AGENT-REVIEW-{YYYY-Q#}.md`

## Cadence

| Month | Action |
|-------|--------|
| January | Q1 Review |
| April | Q2 Review |
| July | Q3 Review |
| October | Q4 Review |

---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Audit | Review agent performance data | Performance report | Data collected |
| **2** Evaluate | Score against criteria | Evaluation scorecard | All agents scored |
| **3** Improve | Recommend changes | Improvement plan | CEO approves changes |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | Clear performance data + consistent patterns | → Recommend changes |
| **MEDIUM** | Limited data or mixed signals | → Binary: A) Accept assessment, B) Gather more data |
| **LOW** | Insufficient data to evaluate | → Stop, run more sessions first |

### Anti-Patterns
- ❌ Evaluating agents without performance data
- ❌ Changing agent roles without CEO approval
- ❌ Ignoring cross-agent dependency impacts
