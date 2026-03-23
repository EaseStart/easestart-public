---
name: pm-tracking
description: "PM execution tracking skill — daily ops, decision management, blocker triage, sprint health. Cross-cutting knowledge for PM agent."
---

# PM Tracking Skill

> Provides PM agent with knowledge data, search configuration, and execution protocols for daily operations, decision management, blocker tracking, and sprint health monitoring.

---

## Data Sources

| Domain | File | Rows | Search Columns |
|--------|------|------|----------------|
| **PM Frameworks** | `data/pm/pm-frameworks.csv` | 26 | Name, Category, When_To_Use, How_It_Works, Keywords |
| **PM Templates** | `data/pm/pm-templates.csv` | 14 | Name, Type, Sections, Stage |
| **PM Anti-Patterns** | `data/pm/pm-anti-patterns.csv` | 25 | Category, Anti_Pattern, Why_Bad, Instead, Source |

**Total:** 65 rows across 3 PM knowledge domains.

---

## Search Configuration

```python
PM_CONFIG = {
    "pm-frameworks": {
        "file": "data/pm/pm-frameworks.csv",
        "search_cols": ["Name", "Category", "When_To_Use", "How_It_Works", "Keywords"],
    },
    "pm-templates": {
        "file": "data/pm/pm-templates.csv",
        "search_cols": ["Name", "Type", "Sections", "Stage"],
    },
    "pm-anti-patterns": {
        "file": "data/pm/pm-anti-patterns.csv",
        "search_cols": ["Category", "Anti_Pattern", "Why_Bad", "Instead", "Source"],
    },
}
```

---

## Skill Loading Protocol

```
PM Agent activated:
1. ALWAYS load pm-frameworks.csv FIRST → understand available frameworks
2. ALWAYS load pm-anti-patterns.csv → enforce guardrails
3. IF daily ops → load pm-templates.csv → "Daily Standup" template
4. IF decision → load pm-templates.csv → "Decision Record" template
5. IF retro → load pm-templates.csv → "Weekly Retro (4Ls)" template
6. IF blocker → load pm-templates.csv → "Blocker Report" template
7. IF health → load pm-templates.csv → "Health Check" template
8. IF prioritization needed → search pm-frameworks.csv → category="prioritization"
9. IF planning needed → search pm-frameworks.csv → category="planning"
```

---

## Workflows

| Workflow | Trigger | Output |
|----------|---------|--------|
| `/daily-ops` | Daily standup capture | Daily log with momentum score |
| `/weekly-retro` | End of week reflection | 4Ls retro + next week plan + momentum trend |
| `/decide` | Significant decision needed | ADR-format decision record |

---

## Naming Conventions (Naming-as-API)

| Note Type | Pattern | Example |
|-----------|---------|---------|
| Daily | `pm/daily/{YYYY-MM-DD}.md` | `pm/daily/2026-03-13.md` |
| Decision | `pm/decisions/{project}/{YYYY-MM-DD}-{slug}.md` | `pm/decisions/easeui/2026-03-13-auth-provider.md` |
| Blocker | `pm/blockers/{project}/{YYYY-MM-DD}-{slug}.md` | `pm/blockers/easeui/2026-03-13-stripe-webhook.md` |
| Retro | `pm/retros/{YYYY}-W{WW}.md` | `pm/retros/2026-W11.md` |
| Momentum | Embedded in daily/weekly | Section within parent doc |

---

## Cross-Agent Integration

PM agent is cross-cutting (Stage 0-6). It interacts with ALL specialist agents:

```
Query about tools → route to mvp-agent, BUT log decision via pm-agent
Query about growth → route to growth-agent, BUT track metrics via pm-agent
Query about hiring → route to ops-agent, BUT track blocker via pm-agent
```

PM agent does NOT make technical or strategic decisions. It:
- ✅ Tracks execution and progress
- ✅ Manages decision records
- ✅ Escalates blockers
- ✅ Scores momentum
- ❌ Does NOT choose tech stacks (→ mvp-agent)
- ❌ Does NOT decide pricing (→ growth-agent)
- ❌ Does NOT assess PMF (→ validation-agent)

---

## Lucius Compliance

| Layer | Implementation |
|-------|---------------|
| **L1 Neural Propagation** | Cross-agent backlinks, naming-as-API for glob queries |
| **L2 Gated Pipeline** | 4-phase workflows with measurable gates per phase |
| **L3 Research Grounding** | 65-row CSV knowledge base, cite source per recommendation |
| **L4 Anti-Patterns** | 25 PM anti-patterns + per-phase anti-patterns in workflows |
| **L5 Confidence** | 0-100% scoring, binary choices at 40-69%, escalation at <40% |
