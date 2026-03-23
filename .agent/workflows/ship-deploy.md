---
description: "Phase 3 of dev pipeline — deploy with L5 confidence scoring + auto-update docs. Produces release-notes.md artifact."
---

# /ship — Deploy Pipeline

> Source: gstack `/ship` (test → review → deploy → docs) + Lucius L5 confidence + L2 gated pipeline.
> **Pipeline position:** Phase 3 of 4 → `/code-review` → `/qa` → **`/ship`** → `/dev-retro`

---

## Trigger

- "ship", "deploy", "push to production", "release"
- After `/qa` gate passes

## Prerequisite

```
Gate check: qa-test-report.md must exist and show PASS verdict.
If not found → "Run /qa first. Shipping without testing = shipping bugs to users."

If /code-review also not done → "Full pipeline required: /code-review → /qa → /ship"
```

## Protocol: Confidence → Test → Deploy → Document

### Step 1: L5 Confidence Check (Lucius)

Before ANY deploy action, evaluate confidence:

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | ≥70% | ✅ Ship autonomously — all gates passed, tests green, review done |
| **MEDIUM** | 40-69% | ⚠️ Binary choice: "A) Ship with known issue [X]. B) Fix [X] first (~{time})" |
| **LOW** | <40% | ❌ Stop — test coverage gap, review incomplete, or critical bug open |
| Same gate fails 2× | — | Auto-escalate — full status report, ask founder for direction |

**Confidence factors:**
- Code review passed? (+20%)
- QA passed? (+20%)
- All tests green? (+15%)
- No open P0/P1 bugs? (+15%)
- Analytics tracking verified? (+10%)
- Docs up to date? (+10%)
- Previously deployed successfully? (+10%)

### Step 2: Test Suite

```bash
# Run full test suite
python3 scripts/test_core.py           # Core unit tests
python3 scripts/test_guardrails.py     # Guardrail enforcement
python3 scripts/simulate.py            # Persona simulations

# Show coverage delta
echo "Tests: {before} → {after} (+{new} new)"
```

### Step 3: Deploy

```bash
# Sync with main
git pull origin main --rebase

# Push changes
git add -A
git commit -m "{conventional commit message}"
git push origin {branch}

# If direct deploy:
# vercel deploy --prod (or equivalent)
```

### Step 4: Document-on-Ship (Auto)

> Source: gstack `/document-release` — auto-update docs on every release.

After successful deploy:

```
1. Cross-reference diff vs README.md:
   - New features mentioned in code but not in README? → Update
   - README claims something the code no longer does? → Fix drift
   
2. Cross-reference diff vs CHANGELOG.md:
   - Add entry: "## {date} — {version/release summary}"
   
3. Cross-reference diff vs architecture docs:
   - New files/modules not documented? → Add to ARCHITECTURE.md
   - Removed files still referenced? → Clean up

4. Flag drift:
   "📋 Docs drift detected: README says 'supports 3 payment methods' 
    but code shows 5. Auto-updated."
```

### Step 5: Post-Ship Verification

```
1. Is the deployed URL accessible?
2. Core flow still works in production?
3. Analytics events firing?
4. No error spikes in first 5 minutes?
```

## Gate

```
Output: release-notes.md
  - Version/release: {identifier}
  - Changes: {summary}
  - Tests: {passed}/{total} ({new} new)
  - Confidence: {score}% ({level})
  - Docs updated: {list}
  - Post-ship verification: PASS/FAIL

Gate: Confidence ≥ MEDIUM + tests green + deployed successfully
      → If PASS: log to pm/STATE.md, update shipping streak
      → If FAIL: rollback + diagnose
```

## Artifact: release-notes.md

```markdown
# Release Notes — {date}

## What Shipped
- {feature/fix 1}
- {feature/fix 2}

## Confidence
- Score: {N}% ({HIGH/MEDIUM/LOW})
- Code review: ✅ / ❌
- QA: ✅ / ❌
- Tests: {passed}/{total}

## Docs Updated
- README.md: {what changed}
- CHANGELOG.md: entry added
- {other docs}

## Post-Ship Verification
- URL accessible: ✅ / ❌
- Core flow works: ✅ / ❌
- Analytics firing: ✅ / ❌
- Errors: none / {count}
```

## Anti-Patterns
- ❌ Shipping without running test suite — tests exist for a reason
- ❌ Shipping with LOW confidence — fix blockers first
- ❌ Skipping docs update — docs drift compounds fast
- ❌ Shipping without post-deploy verification — "it works locally" ≠ "it works in production"
- ❌ Shipping without analytics — you won't know if it's working or broken
