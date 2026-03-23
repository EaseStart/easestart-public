---
description: Automated quality gates — deterministic checks + multi-pass AI review + browser verification
---

# Review Gate Workflow

Multi-layer quality gate that runs after Phase 4 implementation. Combines deterministic scripts with focused AI skill-swap reviews.

> **Trigger:** After coding is complete, before human visual review.

---

## Step 1: Deterministic Gate (parallel, zero tokens)

// turbo
```bash
bash scripts/gate-check.sh
```

If any check fails → auto-fix retry (max 3 attempts from original code).

---

## Step 2: AI Review Passes (sequential, skill-swapping)

Load ONE skill at a time, review with a constrained prompt. Each pass outputs a score (0-10) + specific issues.

### Pass 1: Layout & Visual Hierarchy
- Load `product-designer/SKILL.md`
- Prompt: *"ONLY review layout, spacing, alignment, and visual hierarchy. Score 0-10. List specific issues."*
- Check: Grid alignment, whitespace balance, visual flow, Fitts' Law compliance

### Pass 2: Typography & Readability
- Load `baseline-ui/SKILL.md`
- Prompt: *"ONLY review typography scale, font sizes, contrast, and readability. Score 0-10. List specific issues."*
- Check: All font sizes ≥ 12px, heading hierarchy, line-height, contrast ratios

### Pass 3: Performance
- Load `web-perf/SKILL.md`
- Prompt: *"ONLY review performance metrics. Score 0-10. List specific issues."*
- Check: Bundle size, image optimization, no N+1 fetches, lazy loading

### Pass 4: Design Token Compliance
- Load `easeui-core-components/SKILL.md`
- Prompt: *"ONLY check design token usage. Score 0-10. List specific issues."*
- Check: No raw hex/rgb, all `var(--*)`, component reuse, animation tokens

---

## Step 3: Browser Visual Check (parallel with Step 2)

Use `browser_subagent` to capture screenshots at 4 breakpoints:
- **Mobile:** 375px
- **Tablet:** 768px
- **Desktop:** 1024px
- **Ultrawide:** 1440px

Check for: overflow, clipping, layout breaks, interactive element sizing.

---

## Step 4: Score Aggregation

```
avg_score = (layout + typography + performance + tokens) / 4
lowest = min(layout, typography, performance, tokens)
```

| Result | Action |
|--------|--------|
| avg ≥ 8.0 and lowest ≥ 6.0 | ✅ PASS — proceed to human visual review |
| avg < 8.0 OR lowest < 6.0 | Auto-fix the lowest-scoring area, re-run that pass only |
| After 1 retry still < 8.0 | Escalate to human with all scores + issues |

---

## Step 5: Human Visual Review (Gate 3)

Present screenshots to user with score summary:
```
Layout: 8/10  |  Typography: 9/10  |  Performance: 7/10  |  Tokens: 10/10
Average: 8.5/10 ✅
Lowest: Performance (7) — flagged for attention

📎 4 breakpoint screenshots attached.
```

Human approves → ship. Human requests changes → fix → re-run affected pass.

---

## Conflict Resolution

When passes disagree:

| Conflict | Resolution |
|----------|------------|
| Typography vs Layout on font size | Typography pass wins (domain expert) |
| Performance vs Layout on animation | Layout wins if perf ≥ 7; perf wins if < 7 |
| Two passes flag same issue | Higher severity wins |

**Rule:** Each pass is authoritative within its domain only.

---

## Skip Conditions

Not every feature needs all 4 passes:

| Feature Type | Run These Passes |
|-------------|-----------------|
| UI feature (new page/component) | All 4 passes |
| API/backend only | Skip Pass 1, 2, 4 — Run Pass 3 only |
| Bug fix (< 20 lines changed) | Skip all — run `gate-check.sh` only |
| Styling/CSS only | Skip Pass 3 — Run 1, 2, 4 |

---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Deterministic | Lint + type-check + build | Lint results | Zero errors (warnings OK) |
| **2** AI Review | 4-pass specialist review | Pass scores (1-10) | No pass scores < 4 |
| **3** Browser | Visual check at target viewport | Screenshots | Visual matches design |
| **4** Score | Aggregate all scores | Final score | Score ≥ 7.0 |
| **5** Human | Founder visual review (HARD_GATE) | Approval | Founder approves |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | Aggregate ≥ 8.0 + lint clean + browser matches | → Ready for /ship |
| **MEDIUM** | Aggregate 6.0-7.9 | → Binary: A) Ship with known issues, B) Iterate on lowest pass |
| **LOW** | Aggregate < 6.0 or lint errors | → Block, fix critical issues first |

### Anti-Patterns
- ❌ Skipping deterministic gate to save time — lint catches real bugs
- ❌ Running AI review without browser verification — rendering matters
- ❌ Overriding low scores without documenting why
