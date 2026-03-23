---
description: Autonomous deep research on market, competitors, or channels. Output feeds back into CSV knowledge base (data flywheel). Use for market sizing, competitor analysis, channel viability.
---

# /deep-research — Research-as-Agent Workflow

> Autonomous research loop. Output = structured report + CSV data rows that feed back into the knowledge base.

---

## When to Use

- Founder asks about market size or competitors
- Growth agent needs channel viability data
- Ideation agent needs competitive landscape
- Validation agent needs industry benchmarks
- Any agent says "I need more data on..."

## Trigger Conditions

- Orchestrator detects research-heavy question
- Agent explicitly flags knowledge gap
- Founder asks "research X for me" or "find data on X"

---

## Research Protocol

### Step 1: Define Research Scope

```
Ask: "What specific question are you trying to answer?"
Ask: "What decisions will this research inform?"
Ask: "What would a USEFUL answer look like?"
```

**Output:** Single research question + success criteria.

Example:
- Question: "What channels work for bootstrapped B2B SaaS with <$1K MRR?"
- Criteria: "3+ real examples with specific numbers"

### Step 2: Execute Research

**Method hierarchy (use highest available):**

1. **NotebookLM AI Research** (preferred — deep, multi-source)
   ```bash
   notebooklm create "{topic} Research"
   notebooklm source add-research "{topic}" --mode deep --import-all
   notebooklm generate report --format briefing-doc --wait
   ```

2. **Web search** (fallback — fast, surface-level)
   - Search for case studies, data points, industry reports
   - Prioritize: first-party data > blog posts > opinions

3. **Knowledge base search** (supplement — check what we already know)
   ```python
   search(query="{topic}", domain="casestudies")
   search(query="{topic}", domain="resources")
   ```

### Step 3: Structure Output

Write report to `output/{company}/research/{topic-slug}.md`:

```markdown
# Research: {Topic}

## Question
{Specific research question}

## Key Findings
1. {Finding with source + data point}
2. {Finding with source + data point}
3. {Finding with source + data point}

## Data Points
| Metric | Value | Source | Confidence |
|--------|-------|--------|------------|

## Implications for {Company}
- {What this means for founder's decision}

## Sources
- [{Title}]({URL}) — {why relevant}

## Confidence: {HIGH/MEDIUM/LOW}
{Reasoning for confidence level}
```

### Step 4: Feed Back into Knowledge Base (DATA FLYWHEEL)

> 🔴 **CRITICAL:** Research is NOT complete until data feeds back into CSVs.

**Identify which CSV domain(s) the research enriches:**

| Research Topic | Target CSV | What to Add |
|---------------|-----------|-------------|
| Competitor analysis | `data/casestudies/startups.csv` | New case study rows |
| Channel research | `data/marketing/content-playbook.csv` | Channel tactics with data |
| Tool discovery | `data/tools/*.csv` | New tools with reviews |
| Framework insight | `data/frameworks/*.csv` | Framework details |
| Pricing data | `data/pricing/*.csv` | Pricing models + examples |
| Industry data | `data/industries/*.csv` | Industry-specific insights |

**CSV row quality rules (from autoresearch):**
- Every row must be based on real knowledge (no fabrication)
- Fewer high-quality rows > many low-quality rows
- Include source attribution in appropriate column
- All search columns must have content (quality check)

### Step 4.5: Autoresearch Verify (auto-trigger)

> 🔬 **Auto-trigger:** After new rows added, verify knowledge quality.

// turbo
```bash
python3 autoresearch/evaluate.py 2>&1 | tail -10
```

```
IF score dropped from baseline:
  → Review added rows — specific rows may have broken existing queries
  → Consider: remove rows that hurt score, refine keywords
IF score improved:
  → ✅ Keep rows, log result to autoresearch/results.tsv
```

### Step 5: L4 Data Quality Gate (Lucius)

> 🔴 **MANDATORY:** Before inserting rows into CSVs, validate against ONTOLOGY.md quality rules.

**Every new CSV row MUST pass ALL checks:**

| Check | Rule | If Missing |
|-------|------|-----------|
| `Keywords` | Must be filled (comma-separated) | → Search engine can't find this row |
| `Stage` | Must be valid 0-6 range | → Wrong agent routing |
| `Anti_Pattern` or `Dont` | Must have mistake prevention | → No guardrail for this data |
| `Giantiny_Note` | Required for marketing/finance/ops/legal domains | → Missing philosophy lens |
| Source attribution | Must cite real URL or reference | → Unverifiable → hallucination risk |

```
For each new row:
  1. Validate all required columns per _SCHEMA.csv
  2. Check Keywords are populated
  3. Check Stage is valid (0-6 or stage range)
  4. If domain has Anti_Pattern column → must be filled
  5. ❌ If ANY check fails → DO NOT INSERT. Fix row first.
  ✅ If ALL pass → Insert row and proceed to evaluation.
```

### Step 6: Verify Quality

```bash
# Run evaluation to ensure data quality didn't degrade
python3 autoresearch/evaluate.py
```

- If score improved or stable → ✅ Keep data
- If score dropped → Review added rows, fix or discard

### Step 7: Report to Founder

```
"Research complete. Key findings:
1. {Top finding}
2. {Top finding}
3. {Top finding}

I've also added {N} new data rows to the knowledge base.
This means future questions about {topic} will get better answers."
```

---

## Rules

- **Source requirement:** Every finding must cite a real source. No fabrication.
- **Confidence scoring:** Be honest. "I'm only 60% confident" > "I think..."
- **Scope discipline:** Answer the SPECIFIC question. Don't scope creep into adjacent topics.
- **Flywheel mandatory:** Research without data-back = one-off, no compound value.
- **Time-box:** Max 1 research round per question. Don't rabbit-hole.

## Research Quality Checklist

Before presenting findings:
- [ ] Every claim has a source URL or reference?
- [ ] Data points are specific (numbers, dates, names) not vague?
- [ ] Findings directly answer the original question?
- [ ] At least 1 CSV row added to knowledge base?
- [ ] `evaluate.py` score stable or improved?
- [ ] Confidence level explicitly stated?

## Anti-Patterns

- ❌ Research without specific question → becomes rabbit hole
- ❌ Findings without sources → hallucination risk
- ❌ Research without feeding back into CSVs → zero compound value
- ❌ Spending > 30 min on one research question → diminishing returns
- ❌ Accepting blog opinions as evidence (prefer first-party data)
- ❌ Research as procrastination → founder should be BUILDING, not researching
