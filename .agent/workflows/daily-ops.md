---
description: "Daily execution tracking — standup, blocker triage, priority setting, and EOD wrap. Lucius 4-phase pipeline."
---

# Daily Ops Workflow

> PM Agent workflow for daily execution tracking. Solo founder accountability system.
> Sources: PM-Kit `/daily`, 3-Question Standup, Linear Method momentum, Shape Up appetite.

---

## Phase 1: CAPTURE — Daily Standup

> **Output:** Updated daily log entry
> **Skills:** pm-tracking, `gws-workspace`
> **Gate:** All active projects reported

### Actions

0. **Auto-Pull Context:** Run `gws workflow +standup-report` to read today's meetings and tasks, plus `gws gmail +triage` for urgent inboxes.
1. For each active project, capture (using context from step 0):
   - ✅ **Shipped:** What completed since last daily?
   - 🔄 **WIP:** What's in progress? (track day count)
   - ❌ **Blocked:** What's stuck? (auto-create blocker if new)
2. Check yesterday's WIP → flag items carried for 3+ days
3. Calculate shipped count vs yesterday's plan

### Anti-Patterns
- ❌ Daily without blocked section — honesty over comfort
- ❌ Listing 5+ WIP items — WIP limit is 3 (Kanban)
- ❌ Copy-pasting yesterday's daily — lazy capture = no value

---

## Phase 2: TRIAGE — Blocker Review

> **Output:** Blocker status updates, new blocker records
> **Skills:** pm-tracking, `gws-workspace`
> **Gate:** Critical blockers have owner + due date + action plan

### Actions

1. Review all open blockers across active projects
2. For each new blocker:
   - Assign severity (Critical/High/Medium/Low)
   - Assign owner (default: founder)
   - Set due date based on severity matrix
   - **Action:** Run `gws tasks insert` to push to Google Tasks for cross-device visibility.
3. Check escalation rules: blocker > 2× response time → escalate severity
4. Resolve any blockers that are actually done

### Anti-Patterns
- ❌ Blocker without owner — no accountability = no resolution
- ❌ Critical blocker with "will handle later" — critical = TODAY
- ❌ 5+ active blockers — stop and do root cause analysis

---

## Phase 3: PRIORITIZE — Today's Focus

> **Output:** Max 3 priorities for today with appetite check
> **Skills:** pm-tracking (pm-frameworks.csv → Appetite Check, Eisenhower)
> **Gate:** Max 3 items, each scoped to ≤ half day

### Actions

1. List candidate tasks from WIP + backlog
2. Apply Eisenhower filter: urgent+important first
3. Appetite check: how long should each take?
4. Select top 3 — commit to completing at least 1
5. If carrying from yesterday: explain WHY it's still priority

### Anti-Patterns
- ❌ 5+ priorities today — that's a wish list, not a plan
- ❌ All items marked "important" — if everything is priority, nothing is
- ❌ Priority without appetite — "build checkout" is not a task, it's a project

---

## Phase 4: REFLECT — EOD Wrap-up

> **Output:** End of day summary with momentum update
> **Skills:** pm-tracking, `gws-workspace`
> **Gate:** Carried items have explanation

### Actions

1. Review today's 3 priorities: what shipped, what carried?
2. For carried items: why? blocked? scope too big? avoided?
3. Update momentum score (shipped vs planned).
4. **Action:** Run `gws sheets +append` to log metrics (Shipped, Carried, Blockers, Momentum) into the central tracking Sheet.
5. Preview tomorrow: what's the one thing that would make tomorrow a win?

### Anti-Patterns
- ❌ Skipping wrap-up — no closure = no learning
- ❌ "I'll finish it tomorrow" without why it didn't finish today
- ❌ EOD without momentum check — tracking without reflection = noise
