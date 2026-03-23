---
description: "Autonomous research sprint — turbo-mode experiment loop to improve EaseStart knowledge graph. Run when research or knowledge enrichment is needed."
---

// turbo-all

# /autoresearch — Autonomous Research Sprint

> Run experiment loops to improve EaseStart's knowledge graph score.
> Based on Karpathy's autoresearch pattern, adapted for Antigravity.

---

## When to Use

- Founder asks to improve knowledge quality
- Agent detects knowledge gap during any workflow
- Before generating reports (ensure data quality)
- After deep-research produces new CSV rows
- Periodic knowledge maintenance

## Auto-Trigger Conditions

These workflows automatically invoke `/autoresearch` when relevant:

| Workflow | Trigger | Action |
|----------|---------|--------|
| `/validate-idea` | Lean Canvas step | Check relevant domain coverage |
| `/deep-research` | After CSV rows added | Verify quality via evaluate.py |
| `/sprint-validate` | Pricing hypothesis | Check pricing domain coverage |
| `/generate-report` | Before generation | Ensure overall score ≥ 90 |
| `/sprint-growth` | Channel research | Check marketing domains |
| `/feature-dev` | Brainstorm research | Feed findings into research docs |

---

## Phase 1: SCOUT — Assess Current State

// turbo
```bash
python3 autoresearch/strategies.py --analyze
```

1. Read `autoresearch/state.md` if it exists (resume mode)
2. Read `autoresearch/results.tsv` — check previous experiments
3. Run weakness analysis — identify targets
4. Check `evaluate.py` current score:

// turbo
```bash
python3 autoresearch/evaluate.py 2>&1 | tail -10
```

**Output:** List of target domains + current score baseline.

---

## Phase 2: PLAN — Generate Experiment Strategies

Based on SCOUT findings, choose strategy:

| Weakness | Strategy | Command |
|----------|----------|---------|
| Low coverage (domains < 3 rows) | Enrich | Add quality rows to gap domains |
| Low quality (>20% empty fields) | Cleanup | Fill empty columns with real data |
| Low simulation (test cases fail) | Targeted fix | Add rows matching failed test queries |
| Score already ≥ 95 | Cross-domain | Try relationship enrichment or subtraction |

**For batch mode (20+ experiments):**

// turbo
```bash
python3 autoresearch/strategies.py --generate 20 -o /tmp/strats.json
```

Then fill the generated strategies with real knowledge data.

---

## Phase 3: SPRINT — Execute Experiments

### Option A: Interactive Sprint (15-20 experiments)

For each experiment:

1. Modify CSV data (targeted, small change)
2. Commit:
// turbo
```bash
git add -A && git commit -m "experiment: {description}"
```

3. Evaluate:
// turbo
```bash
python3 autoresearch/evaluate.py 2>&1 | grep "^score:"
```

4. Decision:
   - Score improved → **KEEP** ✅
   - Score equal/worse → **DISCARD** and reset:
// turbo
```bash
git reset --hard HEAD~1
```

5. Log to results.tsv (tab-separated)

### Option B: Batch Mode (20-50 experiments)

// turbo
```bash
python3 autoresearch/run_batch.py /tmp/strats.json
```

Or auto-generate + run:

// turbo
```bash
python3 autoresearch/run_batch.py --auto 10 --dry-run
```

If dry-run looks good:

```bash
python3 autoresearch/run_batch.py --auto 10
```

---

## Phase 4: META — Review & Save State

1. Check final score:
// turbo
```bash
python3 autoresearch/evaluate.py 2>&1 | tail -10
```

2. Review results.tsv — what worked?
// turbo
```bash
cat autoresearch/results.tsv
```

3. `state.md` is auto-updated by run_batch.py. If running interactive sprint, update manually.

4. **Meta-iteration (every 10 experiments):** Review program.md itself:
   - Are the experiment strategies producing keeps or mostly discards?
   - Should we change the approach?
   - What domains are saturated (no more improvements possible)?

---

## Rules

- **Source requirement:** Every CSV row must be based on real knowledge. No fabrication.
- **Quality > Quantity:** 2 well-researched rows > 20 filler rows.
- **Simplicity criterion:** Removing bad data for equal score = WIN.
- **Never modify:** `scripts/core.py`, `autoresearch/evaluate.py`, `scripts/simulate.py`
- **Context discipline:** Redirect long output to `/tmp/`, don't flood context.

## Anti-Patterns

- ❌ Adding rows without domain knowledge (hallucination risk)
- ❌ Running 50+ experiments without reviewing intermediate results
- ❌ Ignoring the weakest component (targeted > random)
- ❌ Modifying locked files (core.py, evaluate.py)
- ❌ Skipping state.md update at end of session
