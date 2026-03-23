---
description: "Structured decision making — ADR-style records with Lucius confidence scoring. Lucius 4-phase pipeline."
---

# Decide Workflow

> PM Agent workflow for structured decision making.
> Sources: ADR (Architecture Decision Records), Two-Way Door (Amazon), Lucius L5 Confidence Protocol, Pre-Mortem.

---

## Phase 1: CONTEXT — Define the Problem

> **Output:** Problem statement with constraints
> **Skills:** pm-tracking (pm-frameworks.csv → ADR, Pre-Mortem)
> **Gate:** Problem statement ≤ 2 sentences

### Actions

1. What specific problem are we solving? (not "what should we build?")
2. What constraints are real? (budget, time, tech stack, skills)
3. What constraints are assumed? (challenge these)
4. Who is affected by this decision?
5. Is this a one-way door (irreversible) or two-way door (reversible)?

### Anti-Patterns
- ❌ Starting with solutions — "Should we use X?" before defining the problem
- ❌ Problem statement > 3 sentences — if you can't be concise, you don't understand it
- ❌ Confusing assumed constraints with real ones — "We can't change the DB" vs "We don't WANT to change the DB"

---

## Phase 2: OPTIONS — List Alternatives

> **Output:** Options table with pros/cons
> **Skills:** pm-tracking (pm-templates.csv → Decision Record)
> **Gate:** Each option has ≥ 1 pro and ≥ 1 con. Minimum 2 options.

### Actions

1. List ≥ 2 alternatives (minimum: doing it vs not doing it)
2. For each option:
   - What are the pros? (be specific, not generic)
   - What are the cons? (be honest, not dismissive)
   - What's the effort? (time, cost, complexity)
   - What's the risk? (what could go wrong)
3. Identify the "do nothing" option — sometimes it's the right one
4. If only 1 option seems viable → you haven't explored enough

### Anti-Patterns
- ❌ Only 1 option listed — confirmation bias, not decision-making
- ❌ Straw man alternatives — listing bad options to make preferred one look good
- ❌ Pros-only analysis — every option has trade-offs, be honest

---

## Phase 3: DECIDE — Choose with Confidence

> **Output:** Decision with confidence score and rationale
> **Skills:** pm-tracking (pm-frameworks.csv → Two-Way Door, Lucius L5)
> **Gate:** Confidence ≥ 40% to proceed

### Actions

1. Rate confidence 0-100%:
   - **≥ 70%** → Proceed autonomously. Document and ship.
   - **40-69%** → Present binary choice with recommendation to founder
   - **< 40%** → STOP. Ask founder for specific input. Don't guess.
2. State the decision clearly: "We will {X} because {Y}"
3. For two-way doors: decide fast — if wrong, we can reverse
4. For one-way doors: take an extra day to review

### Confidence Calibration

| Evidence Type | Confidence Boost |
|--------------|-----------------|
| Direct user feedback | +20% |
| Production data | +15% |
| Similar prior decision that worked | +10% |
| Team consensus | +10% |
| Industry best practice | +5% |
| Gut feeling only | +0% (baseline) |

### Anti-Patterns
- ❌ Deciding with < 40% confidence without asking for help
- ❌ Treating all decisions equally — two-way doors should be fast
- ❌ "Let's revisit this later" without new information — re-litigation
- ❌ Decision by committee — one person owns the call (DACI: Approver)

---

## Phase 4: RECORD — Document the ADR

> **Output:** Decision record in ADR format
> **Skills:** pm-tracking (pm-templates.csv → Decision Record)
> **Gate:** Decision linked to relevant project docs

### Actions

1. Write ADR in standard format:
   ```markdown
   ## DR-{YYYY-MM-DD}-{slug}

   **Status:** accepted
   **Context:** {problem in 1-2 sentences}
   **Confidence:** {score}%

   ### Options Considered
   | Option | Pros | Cons |
   |--------|------|------|
   | A: {name} | {pros} | {cons} |
   | B: {name} | {pros} | {cons} |

   ### Decision
   {What we chose and WHY}

   ### Consequences
   - ✅ {positive outcome expected}
   - ⚠️ {trade-off we're accepting}

   ### Links
   - Related: {linked docs, blockers, other decisions}
   ```
2. Link ADR to project index
3. If superseding a previous decision → mark old one as "superseded"
4. Notify relevant agents if decision affects their domain

### Anti-Patterns
- ❌ Decision without record — institutional memory = zero
- ❌ ADR that doesn't explain WHY — future you won't remember context
- ❌ Superseding without linking to original — broken decision chain
- ❌ ADR with no consequences section — every choice has trade-offs
