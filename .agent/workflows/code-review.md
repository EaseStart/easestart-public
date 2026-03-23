---
description: "Phase 1 of dev pipeline — fix-first code review before any deploy. Produces code-review-report.md artifact."
---

# /code-review — Fix-First Code Review

> Source: gstack `/review` (paranoid audit, fix-first) + Lucius L2 gated pipeline.
> **Pipeline position:** Phase 1 of 4 → `/code-review` → `/qa` → `/ship` → `/dev-retro`

---

## Trigger

- "review code", "review branch", "check before deploy"
- Before any `/ship` or `/qa` workflow
- When mvp-agent completes a build sprint

## Protocol: Fix First, Ask Second

> gstack principle: **Auto-fix everything obvious. Surface only the ambiguous for human decision.**

### Step 1: Diff Analysis

```
1. What files changed? How many lines?
2. What's the intent? (feature, bugfix, refactor, config)
3. Any new dependencies added?
```

### Step 2: Auto-Fix (Silent)

Fix these without asking — they're universally correct:

| Category | Auto-Fix |
|----------|----------|
| **Linting** | Format, whitespace, import order |
| **Dead code** | Remove unused variables, imports, functions |
| **Stale comments** | Remove "TODO" items that are done, outdated comments |
| **Console.log** | Remove debug logging (keep intentional logging) |
| **Common patterns** | `==` → `===`, missing error handling on await, unclosed resources |

### Step 3: Surface Ambiguous Issues

Present to founder with binary choice:

```
Found 3 issues that need your input:

1. 🔒 SECURITY: API key in client-side code (line 45 of api.ts)
   A) Move to environment variable  B) Accept risk (not recommended)

2. ⚡ PERFORMANCE: N+1 query in user list (line 120 of users.ts)
   A) Add eager loading (~15 min fix)  B) Skip for now (OK at <100 users)

3. 🏗️ ARCHITECTURE: Component doing 3 things (Dashboard.tsx)
   A) Split into 3 components (~30 min)  B) Leave as-is (tech debt note)
```

### Step 4: Completeness Gap Check

```
Is this an 80% solution? If finishing to 100% takes <30 min:
  → Suggest: "This is 80% done. Adding [X] would take ~20 min and complete the feature."
  → A) Complete it  B) Ship as-is
```

## Gate

```
Output: code-review-report.md
  - Files reviewed: {count}
  - Auto-fixed: {count} issues
  - Needs input: {count} issues (all resolved by founder)
  - Completeness: {%}

Gate: Zero P0 bugs remaining. All auto-fixes applied. 
      Human approved all ambiguous items.
      → If PASS: proceed to /qa
      → If FAIL: fix and re-review (max 3 rounds)
```

## Artifact: code-review-report.md

```markdown
# Code Review Report — {date}

## Summary
- **Files changed:** {count}
- **Auto-fixed:** {count} issues
- **Founder decisions:** {count} items resolved
- **P0 remaining:** {count} (must be 0 to pass gate)

## Auto-Fixes Applied
- [list of auto-fixes]

## Founder Decisions
- [issue]: chose [A/B] — [rationale]

## Completeness
- [feature]: {%} complete. [gap if any]

## Verdict: PASS / FAIL
```

## Anti-Patterns
- ❌ Asking founder about obvious fixes (linting, formatting) — auto-fix silently
- ❌ Presenting issues without binary choices — always A/B with recommendation
- ❌ Skipping security review — always check for exposed secrets, SQL injection, XSS
- ❌ Reviewing without understanding intent — ask "what changed?" first

---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Diff Analysis | Parse git diff + categorize changes | Change classification | All changes categorized |
| **2** Auto-Fix | Fix obvious issues silently | Applied fixes | No regressions introduced |
| **3** Surface | Present ambiguous issues to founder | Decision list | Founder decides on each issue |
| **4** Completeness | Check for missing tests/docs | Completeness report | `code-review-report.md` |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | No CRITICAL issues + auto-fixes clean + tests pass | → Approve for /qa |
| **MEDIUM** | Non-blocking issues found | → Binary: A) Approve with caveats, B) Fix first |
| **LOW** | CRITICAL issues (security, race condition, trust boundary) | → BLOCK — must fix before proceeding |

### Anti-Patterns
- ❌ Approving code with CRITICAL issues to save time
- ❌ Auto-fixing without running tests after
- ❌ Reviewing only the diff without understanding the context
- ❌ Skipping completeness check (missing tests = tech debt)
