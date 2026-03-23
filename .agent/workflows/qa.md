---
description: "Phase 2 of dev pipeline — browser-based QA on staging. Produces qa-test-report.md artifact."
---

# /qa — Browser QA Testing

> Source: gstack `/qa` (Playwright-based browser QA) + Lucius L2 gated pipeline.
> **Pipeline position:** Phase 2 of 4 → `/code-review` → **`/qa`** → `/ship` → `/dev-retro`

---

## Trigger

- "test app", "qa staging", "qa https://..."
- After `/code-review` gate passes
- Before any `/ship` workflow

## Prerequisite

```
Gate check: code-review-report.md must exist and show PASS verdict.
If not found → "Run /code-review first. QA without review = testing bugs you could have caught."
```

## Protocol: Test Real Flows in Real Browser

### Step 1: Environment Check

```
1. What's the staging URL? (ask founder if not known)
2. Does the app require authentication? If yes, get test credentials.
3. What's the core user flow? (signup → core action → outcome)
```

### Step 2: Core Flow Testing

Test the **core loop** end-to-end in a real browser:

```
For each core flow:
  1. Open browser → navigate to URL
  2. Complete the flow as a real user would
  3. Note: page load time, visual bugs, broken links, error states
  4. Screenshot key states (before/after)
  5. Test on mobile viewport (375px) if web app
```

### Step 3: Edge Case Testing

| Category | What to Test |
|----------|-------------|
| **Empty states** | No data, no users, first-time experience |
| **Error states** | Invalid input, network offline, unauthorized |
| **Boundary** | Very long text, special characters, large files |
| **Mobile** | Touch interactions, viewport overflow, scroll |

### Step 4: Bug → Fix → Verify Loop

```
For each bug found:
  1. Document: what happened, expected vs actual
  2. Severity: P0 (blocks user) / P1 (annoying) / P2 (cosmetic)
  3. If P0 or P1 and fix < 15 min → fix immediately
  4. Re-test after fix → confirm resolved
  5. Generate regression test for the fix
```

### Step 5: Regression Test Generation

```
For each fix applied:
  → Write a Playwright test that would catch this regression
  → Save to tests/ directory
  → Format: test("{flow}: {what was fixed}", async () => { ... })
```

## Gate

```
Output: qa-test-report.md
  - Core flows tested: {count}
  - Bugs found: {count} (P0: {n}, P1: {n}, P2: {n})
  - Bugs fixed: {count}
  - Regression tests added: {count}
  - Mobile tested: yes/no

Gate: Zero P0 bugs remaining. All core flows pass.
      → If PASS: proceed to /ship
      → If FAIL: fix P0s and re-test (max 3 rounds)
```

## Artifact: qa-test-report.md

```markdown
# QA Test Report — {date}

## Environment
- **URL:** {staging URL}
- **Browser:** Chromium via Playwright
- **Viewports:** Desktop (1440px) + Mobile (375px)

## Core Flows Tested
| # | Flow | Result | Notes |
|---|------|--------|-------|
| 1 | {flow description} | ✅ / ❌ | {notes} |

## Bugs Found
| # | Severity | Description | Status | Fix Time |
|---|----------|-------------|--------|----------|
| 1 | P0/P1/P2 | {description} | Fixed / Open | {time} |

## Regression Tests Added
- {test file}: {count} tests

## Verdict: PASS / FAIL
```

## Anti-Patterns
- ❌ Testing only the happy path — edge cases ARE the product quality
- ❌ Skipping mobile testing — most users are on mobile
- ❌ Fixing bugs without adding regression tests — same bug WILL return
- ❌ Running QA without code review first — review catches logical bugs, QA catches UX bugs

---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Environment | Verify prod-like setup | Environment check | Server running + DB seeded |
| **2** Core Flows | Test happy paths in real browser | Flow test results | All core flows pass |
| **3** Edge Cases | Test error states + boundaries | Edge case results | No crashes on invalid input |
| **4** Bug Fix | Fix → verify → iterate loop | Bug fixes committed | All found bugs resolved |
| **5** Regression | Generate regression tests | New test files | Tests prevent re-introduction |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | All core flows pass + edge cases handled + regression tests added | → PASS verdict, proceed to /ship |
| **MEDIUM** | Core flows pass but edge cases have known issues | → Binary: A) Ship with known issues documented, B) Fix first |
| **LOW** | Core flow fails or critical bug found | → FAIL verdict, block /ship |

### Anti-Patterns
- ❌ Testing only happy path — edge cases cause production bugs
- ❌ Finding bugs without fixing them — QA without action is observation
- ❌ Skipping regression test generation — same bug will return
- ❌ Testing against mock data instead of real browser
