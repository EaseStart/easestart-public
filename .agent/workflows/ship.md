---
description: Automated ship pipeline — merge main, test, review, version bump, commit, push, PR. For ready branches, not for deciding what to build.
---

# /ship — Automated Release Pipeline

> Source: GStack Ship Workflow + Lucius L2 Gated Pipeline.
> Philosophy: "Branches die when only boring release work is left. AI should not procrastinate."

**When to use:** Branch is ready. Product thinking done. Architecture done. Review done. Just needs to land.

**When NOT to use:** Still deciding what to build → use `/feature-dev` instead.

---

## Step 1: Pre-flight

// turbo
```bash
git branch --show-current
```

1. If on `main` → **ABORT**: "You're on main. Ship from a feature branch."
2. Run `git status` — uncommitted changes are always included.
3. Run `git diff main...HEAD --stat` and `git log main..HEAD --oneline` — understand what's being shipped.

**Report summary:**
```
📦 Shipping: [branch-name]
   [N] commits, [+X/-Y] lines, [Z] files changed
   Latest: [last commit message]
```

---

## Step 2: Merge origin/main

// turbo
```bash
git fetch origin main && git merge origin/main --no-edit
```

- **If conflicts (simple):** Try auto-resolve (VERSION, CHANGELOG ordering).
- **If conflicts (complex):** STOP and show them to user.
- **If up to date:** Continue silently.

---

## Step 3: Run Tests

Run project-specific test suite:

```bash
# Detect and run appropriate tests
if [ -f "package.json" ]; then
  npm test 2>&1 | tee /tmp/ship_tests.txt
fi

if [ -f "Makefile" ]; then
  make test 2>&1 | tee /tmp/ship_tests.txt
fi

if [ -f "pytest.ini" ] || [ -f "pyproject.toml" ]; then
  python -m pytest 2>&1 | tee /tmp/ship_tests.txt
fi
```

- **If any test fails:** Show failures and **STOP**. Do not proceed.
- **If all pass:** Note counts briefly and continue.
- **If no test suite:** Note "No tests found" and continue with warning.

---

## Step 4: Pre-Landing Review

> Integrates with existing `/review-gate` workflow.

1. Check if `/review-gate` workflow exists → run it
2. If not, run manual review:
   - `git diff origin/main` — get full diff
   - Apply 2-pass review:
     - **Pass 1 (CRITICAL, blocking):** Security issues, race conditions, trust boundary violations
     - **Pass 2 (INFORMATIONAL, non-blocking):** Dead code, magic numbers, test gaps

**Output format:**
```
Pre-Landing Review: N issues (X critical, Y informational)

CRITICAL (blocking /ship):
- [file:line] Problem → Fix: [suggestion]

Issues (non-blocking, included in PR body):
- [file:line] Problem → Fix: [suggestion]
```

- **If CRITICAL issues found:** STOP. Ask user per issue: A) Fix now, B) Acknowledge, C) Skip.
- **If only informational:** Continue — include in PR body.
- **If no issues:** `Pre-Landing Review: No issues found.`

---

## Step 5: Version Bump (auto-decide)

Detect versioning strategy from project:

| Signal | Version Type |
|--------|-------------|
| `feat:` commits present | Minor bump |
| Only `fix:` / `chore:` | Patch bump |
| `BREAKING CHANGE` in commits | Major bump |
| No versioning file found | Skip this step |

```bash
# Common version file locations:
# package.json → npm version [patch|minor|major]
# VERSION file → update manually
# pyproject.toml → update version field
```

---

## Step 6: Commit (conventional commits)

> Uses the `commit` skill for Sentry-convention commits.

1. Stage all changes: `git add -A`
2. Create bisectable commits — group by type/scope
3. Follow conventional commit format: `feat(scope): description`

> **Bisectable rule:** Each commit should be independently revertable. Don't mix unrelated changes.

---

## Step 7: Push

// turbo
```bash
git push origin HEAD
```

- If push fails (rejected) → `git pull --rebase origin HEAD && git push origin HEAD`
- If still fails → STOP and report.

---

## Step 8: Create PR

Create or update PR with structured body:

```markdown
## Summary
[Auto-generated from commit messages]

## Changes
[File stats from git diff --stat]

## Pre-Landing Review
[Paste review findings from Step 4]

## Test Results
[Pass/fail summary from Step 3]
```

---

## Confidence Protocol (Lucius L5)

| Step | If Score < 40% |
|------|----------------|
| Step 2 (merge conflicts) | STOP — show conflicts |
| Step 3 (test failures) | STOP — show failures |
| Step 4 (critical issues) | STOP — ask per issue |
| Step 5 (version type) | Ask: "Minor or patch?" |

> ❌ Never auto-proceed past a CRITICAL gate failure.

---

## Quick Reference

```
/ship = Pre-flight → Merge main → Test → Review → Version → Commit → Push → PR
         Step 1      Step 2       Step 3  Step 4   Step 5   Step 6   Step 7  Step 8
```

---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Pre-flight | Branch check + diff analysis | Ship summary | On feature branch, changes clear |
| **2** Merge | Merge origin/main | Clean merge | No unresolved conflicts |
| **3** Test | Run full test suite | Test results | All tests pass |
| **4** Review | Pre-landing review (2-pass) | Review report | No CRITICAL issues |
| **5** Version | Auto-detect version bump | Version file updated | Correct semver bump |
| **6** Commit | Conventional commits | Clean commits | Bisectable, well-formatted |
| **7** Push + PR | Push + create PR | PR on GitHub | PR body includes review + tests |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | Tests pass + review clean + merge clean | → Ship autonomously |
| **MEDIUM** | Non-blocking issues found | → Include in PR body, ship with caveats |
| **LOW** | Test failures or CRITICAL review issues | → STOP, do not ship |

### Anti-Patterns
- ❌ Shipping from main branch — always use feature branches
- ❌ Force-pushing to resolve conflicts — merge properly
- ❌ Shipping without running tests — "it works on my machine" is not QA
