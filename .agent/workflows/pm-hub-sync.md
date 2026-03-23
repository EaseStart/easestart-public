---
description: Auto-update PM Hub after any feature development work — keeps the Kanban board current without human intervention
---

# PM Hub Auto-Sync Protocol

> **Trigger:** Run this after ANY feature development, spec writing, or implementation work.
> **Purpose:** Keep `plans/specs/*/STATUS.md` and `plans/specs/README.md` in sync so PM Hub board reflects reality.
> **User role:** VIEW ONLY. All updates are AI-driven.

---

## When to Trigger This Workflow

Run the PM Hub sync steps whenever you:
- ✅ **Implement a use case** (partially or fully)
- ✅ **Ship a feature** (all UCs done)
- ✅ **Start work on a feature** (status change: backlog → in-progress)
- ✅ **Create new spec documents** (brainstorm, usecases, blueprint)
- ✅ **Add or modify key implementation files**
- ✅ **Drop or descope a use case**

---

## Step 1: Update STATUS.md for the Feature

**File:** `plans/specs/{feature-id}/STATUS.md`

### 1a. Update Use Case Checkboxes

After implementing a UC, check it off:
```diff
-- [ ] UC-01: Generate a Complete Multi-Page Site
+- [x] UC-01: Generate a Complete Multi-Page Site
```

If a UC is dropped, mark and annotate:
```diff
-- [ ] UC-05: Voice Command Support
+- [ ] UC-05: Voice Command Support — **DROPPED** (deferred to Phase 4)
```

### 1b. Update YAML Frontmatter Status

| When | Change |
|------|--------|
| Starting work | `status: backlog` → `status: in-progress` |
| All UCs complete | `status: in-progress` → `status: shipped` + add `shipped_date: YYYY-MM-DD` |
| Work paused | `status: in-progress` → `status: paused` |

// turbo
### 1c. Update Key Files Table

After creating or modifying implementation files, add them:
```markdown
## Key Files

| Area | File |
|------|------|
| Main component | `app/src/components/editor/command-center.tsx` |
| Action registry | `app/src/lib/action-registry.ts` |
```

// turbo
### 1d. Update Implementation Audit

Move items from "What Does NOT Exist Yet" to "What Exists" as they are built:
```diff
 ### What Exists
 | Component | File | Status | Note |
 |-----------|------|--------|------|
+| Command Center | `app/src/components/editor/command-center.tsx` | ✅ | 280 lines — cmdk-based palette with fuzzy search |

 ### What Does NOT Exist Yet
-- ❌ cmdk integration
+- ~~cmdk integration~~ ✅ Done
```

### 1e. Update Notes

Add significant implementation decisions, dropped scope, or known issues.

---

## Step 2: Update README.md Dashboard

**File:** `plans/specs/README.md`

// turbo
### 2a. Update Status Column

When a feature's status changes:
```diff
-| `command-center/` | 1 | 📋 Specced | brainstorm, usecases, STATUS |
+| `command-center/` | 1 | 🔨 In Progress | brainstorm, usecases, STATUS |
```

Status icons:
- ✅ Shipped
- 🔨 In Progress
- 📋 Specced
- ⬜ Backlog
- ⏸ Paused

// turbo
### 2b. Update Documents Column

When new spec artifacts are created:
```diff
-| `command-center/` | 1 | 🔨 In Progress | brainstorm, usecases, STATUS |
+| `command-center/` | 1 | 🔨 In Progress | brainstorm, blueprint, usecases, STATUS |
```

---

## Step 3: ByteRover Curate

// turbo
After updating STATUS.md, curate the changes:
```bash
brv curate "Implemented UC-01 for {feature}: {brief description}" -f plans/specs/{feature}/STATUS.md
```

---

## Quick Reference: File Touch Map

| Action | Files to Update |
|--------|----------------|
| Implement a UC | `STATUS.md` (checkbox + key files + audit) |
| Ship a feature | `STATUS.md` (status + shipped_date), `README.md` (status icon) |
| Start a feature | `STATUS.md` (status), `README.md` (status icon) |
| Create a new spec doc | `README.md` (documents column) |
| Drop a UC | `STATUS.md` (checkbox + notes) |
| Add implementation file | `STATUS.md` (key files + audit) |

---

## Example: Full Sync After Shipping Command Center

```bash
# 1. STATUS.md — all UCs checked, status changed
# plans/specs/command-center/STATUS.md
# ---
# status: shipped
# shipped_date: 2026-03-15
# ---
# - [x] UC-01: Open Command Palette and Execute an Action
# - [x] UC-02: Quick Navigation via Command Palette
# - [ ] UC-03: AI-Powered Command — **DEFERRED to Phase CC3**

# 2. README.md — status icon updated
# | `command-center/` | 1 | ✅ Shipped | brainstorm, usecases, STATUS |

# 3. brv curate
brv curate "Shipped Command Center (UC-01, UC-02). UC-03 deferred to CC3." -f plans/specs/command-center/STATUS.md
```

---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Feature Status | Update STATUS.md (checkboxes, YAML, files, audit) | Updated STATUS.md | All sections reflect actual state |
| **2** Dashboard | Update README.md dashboard table | Updated README.md | Status + docs columns accurate |
| **3** Knowledge | ByteRover curate | Updated .brv context | `brv curate` success |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | Feature code matches STATUS.md + README dashboard current | → Sync complete |
| **MEDIUM** | Some checkboxes uncertain (feature partially done) | → Binary: A) Mark as partial, B) Verify with tests first |
| **LOW** | Can't determine feature state from code alone | → Stop, ask founder to clarify scope |

### Anti-Patterns
- ❌ Updating STATUS.md without checking actual code state
- ❌ Marking features as "done" without verifying all use cases
- ❌ Skipping ByteRover curate — context goes stale
- ❌ Not updating README dashboard — PM Hub becomes unreliable
