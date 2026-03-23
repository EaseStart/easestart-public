---
description: Generate a handoff document at session end to preserve context for the next session. Use when finishing a long session or switching topics.
---

# /handoff — Session Handoff Document

> Preserve context between sessions. Solve the #1 bottleneck of one-man-company: context loss.

---

## When to Use

- End of a long session (> 30 min or > 70% context used)
- Switching to a different topic or agent
- End of day/week
- Before `/clear` or starting fresh conversation
- Orchestrator detects context > 70% → auto-suggest this workflow

## Protocol

### Step 1: Gather Context

Silently review the current session and identify:

1. **Stage:** What startup stage is the founder currently at?
2. **Agents used:** Which specialist agents were activated?
3. **Decisions made:** What was decided during this session?
4. **Open questions:** What was discussed but not resolved?
5. **Blockers:** What is preventing progress?
6. **Next steps:** What should the next session focus on?

### Step 2: Confirm Context

Before writing, ask the founder:

```
"Before I create the handoff doc, a quick check:
1. Has anything changed since we last discussed [current direction]?
2. Any decisions you've reconsidered?
3. Anything I should flag for the next session?"
```

> ⚠️ **Lucius guard:** Prevents "false continuity" — handoff doc reflecting old direction when founder has changed their mind.

### Step 3: Write Handoff Document

Create file: `data/sessions/HANDOFF-{YYYY-MM-DD}.md`

Format:

```markdown
# Session Handoff — {Date}

## Current State
- **Stage:** {N} — {Stage Name}
- **Focus area:** {What we worked on}
- **Agents activated:** {list}

## Decisions Made
1. {Decision 1} — Reasoning: {why}
2. {Decision 2} — Reasoning: {why}

## Open Questions
- {Question that needs answers next time}

## Blockers
- {What's blocking progress}

## Next Steps (Priority Order)
1. {Most important next action}
2. {Second priority}
3. {Third priority}

## Context Notes
{Any additional context the next session should know — key data points, URLs, specific numbers discussed}
```

### Step 4: Confirm with Founder

```
"Handoff doc saved at data/sessions/HANDOFF-{date}.md
Next session: just mention 'load handoff' and I'll pick up where we left off."
```

## Rules

- **Keep it concise:** Max 500 words. Compression > completeness.
- **Decisions > discussions:** Record WHAT was decided, not the debate.
- **Actionable next steps:** Each next step should be executable without extra context.
- **One file per session:** Don't append to old handoffs — create new file per day.
- **Auto-suggest:** Orchestrator should suggest `/handoff` when context > 70%.

---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Capture | Summarize session decisions + context | HANDOFF-{date}.md | All decisions captured |
| **2** Write | Structure handoff document | Formatted handoff file | Covers stage, focus, blockers, context |
| **3** Verify | Cross-check with session history | Verified handoff | No contradictions with STATE.md |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | All decisions captured + stage confirmed | → Save handoff |
| **MEDIUM** | Some decisions may be incomplete | → Ask founder to confirm key points |
| **LOW** | Session was exploratory, no clear decisions | → Write brief note instead of full handoff |

### Anti-Patterns
- ❌ Handoff without capturing stage transitions
- ❌ Overwriting previous handoff instead of creating new one
- ❌ Not updating STATE.md alongside handoff
