# 📊 EaseStart — Knowledge Graph Ontology

> Schema definitions for all 29+ CSV domains in the EaseStart knowledge graph.
> **1110 rows | 29+ domains | 6 pillars | 15 guardrails**

---

## Ontology Overview

```
StartupStage (7)     ──has_actions──▶  Action
    │                                    │
    ├──tracks──▶ Metric                  ├──uses──▶ Tool (96)
    │                                    │
    ├──recommends──▶ Tool                └──references──▶ Resource
    │
    └──prerequisite──▶ StartupStage

Framework (20+)      ──defines──▶ Concept ──relates_to──▶ Concept

Program (50+)        ──applicable_to──▶ StartupStage

PlaybookRule (38)    ──applies_at──▶ StartupStage

ReasoningRule (30)   ──decides_for──▶ Industry × Stage

MarketingData (59)   ──channels + content + email + landing + community──▶ Growth

FinanceData (22)     ──bookkeeping + unit_economics──▶ Sustainability

LegalData (22)       ──contracts + security──▶ Compliance
```

---

## Core Domains (8)

### 1. `stages.csv` — Startup Journey

| Column | Type | Description |
|--------|------|-------------|
| `No` | int | Order (0-6) |
| `Stage` | string | Stage name |
| `Keywords` | string | Search keywords (comma-separated) |
| `Exit_Criteria` | string | Required completions (pipe-separated) |
| `Key_Metrics` | string | Metrics to track |
| `Actions` | string | Recommended next actions |
| `Recommended_Tools` | string | Tool names |
| `Frameworks` | string | Applicable frameworks |
| `Duration_Weeks` | string | Typical duration |
| `Agent` | string | Primary agent |
| `AI_Era_Timeline` | string | Compressed timeline when using AI-assisted development (2026+) |
| `AI_Methodology` | string | Build-Ship-Measure methodology notes for AI-era stage compression |

---

### 2. `tools.csv` — Startup Tools

| Column | Type | Description |
|--------|------|-------------|
| `No` | int | ID |
| `Name` | string | Tool name |
| `URL` | string | Website URL |
| `Category` | string | Primary category |
| `Subcategory` | string | Subcategory |
| `Keywords` | string | Search keywords |
| `Pricing_Model` | string | free/freemium/paid/enterprise |
| `Free_Tier` | string | Free tier details |
| `Startup_Program` | string | Startup credits/deals |
| `Applicable_Stages` | string | Stages where useful |
| `Best_For` | string | Use case description |
| `Alternatives` | string | Alternative tools |
| `Quality_Score` | int | 1-10 rating |
| `Last_Verified` | date | Link verification date |

---

### 3. `frameworks.csv` — Startup Methodologies

| Column | Type | Description |
|--------|------|-------------|
| `No` | int | ID |
| `Name` | string | Framework name |
| `Author` | string | Creator |
| `Type` | string | canvas/methodology/framework/mental-model |
| `Keywords` | string | Search keywords |
| `Key_Concepts` | string | Core concepts (pipe-separated) |
| `Applicable_Stages` | string | Relevant stages |
| `Steps` | string | How to use |
| `Output_Template` | string | Deliverable template name |
| `Best_For` | string | When to use |
| `Source_URL` | string | Original source |

---

### 4. `resources.csv` — Books, Essays, Courses

| Column | Type | Description |
|--------|------|-------------|
| `No` / `Title` / `Author` / `Type` / `URL` / `Keywords` / `Topics` / `Applicable_Stages` / `Key_Takeaways` / `Quality_Score` / `Read_Time_Min` | various | Standard resource fields |

### 5. `programs.csv` — Startup Credits & Deals

| Column | Type | Description |
|--------|------|-------------|
| `No` / `Name` / `Provider` / `Category` / `Keywords` / `Credits_Value` / `Eligibility` / `Duration` / `Application_URL` / `Best_For` / `Last_Verified` | various | Standard program fields |

### 6. `playbook.csv` — Do/Don't Rules (38 rules)

| Column | Type | Description |
|--------|------|-------------|
| `No` / `Stage` / `Category` / `Rule` / `Keywords` / `Do` / `Dont` / `Example_Good` / `Example_Bad` / `Severity` / `Source` | various | Standard playbook fields |
| `Impact_Preview` | string | Projected outcome: cost, timeline, expected result (Agentic OS: Business Impact Simulation) |
| `Reversibility` | enum | `reversible` \| `partially` \| `irreversible` — can this action be undone? |

### 7. `reasoning/_SCHEMA.csv` — Decision Engine (30 rules)

| Column | Type | Description |
|--------|------|-------------|
| `No` / `Stage` / `Context` / `Keywords` / `Decision_Rules` (JSON) / `Anti_Patterns` / `Recommended_Action` / `Agent` / `Severity` | various | Conditional branching logic |
| `Validity_Period` | enum | `evergreen` \| `180_days` \| `90_days` \| `30_days` — how long this rule stays relevant (Agentic OS: Context Decay) |
| `Decay_Note` | string | Why this rule may expire and when to re-evaluate |

### 8. `industries/*.csv` — Context Specialization

| Column | Type | Description |
|--------|------|-------------|
| `No` / `Stage` / `Guideline` / `Keywords` / `Do` / `Dont` / `Tools` / `Metrics` / `Severity` | various | Industry-specific guidance |

---

## Marketing Domains (5)

### 9. `marketing/channels.csv` — 15 channels

| Column | Type |
|--------|------|
| `No` / `Channel` / `Keywords` / `Type` / `Cost` / `Time_Per_Week` / `ROI_Timeline` / `Best_For` / `Stage` / `Giantiny_Fit` / `Description` / `Do` / `Dont` / `Anti_Pattern` / `Giantiny_Note` | various |

### 10. `marketing/content-playbook.csv` — 12 content types

| Column | Type |
|--------|------|
| `No` / `Content_Type` / `Keywords` / `Stage` / `Platform` / `Frequency` / `Time_Per_Piece` / `SEO_Value` / `Conversion_Value` / `Example` / `Template` / `Anti_Pattern` / `Giantiny_Note` | various |

### 11. `marketing/email-sequences.csv` — 10 sequences

| Column | Type |
|--------|------|
| `No` / `Sequence` / `Keywords` / `Day` / `Subject_Line_Template` / `Body_Framework` / `CTA` / `Tracking_Metric` / `Stage` / `Anti_Pattern` | various |

### 12. `marketing/landing-page.csv` — 12 elements

| Column | Type |
|--------|------|
| `No` / `Element` / `Keywords` / `Category` / `Description` / `Do` / `Dont` / `Conversion_Impact` / `Example_Good` / `Example_Bad` / `Source` | various |

### 13. `marketing/community.csv` — 10 patterns

| Column | Type |
|--------|------|
| `No` / `Pattern` / `Keywords` / `Stage` / `Category` / `Description` / `Do` / `Dont` / `Platform` / `Effort` / `Impact` / `Giantiny_Note` / `Example` | various |

---

## Finance Domains (2)

### 14. `finance/bookkeeping.csv` — 10 tasks

| Column | Type |
|--------|------|
| `No` / `Task` / `Keywords` / `Category` / `Stage` / `Frequency` / `Time_Required` / `Tool` / `Description` / `Do` / `Dont` / `Giantiny_Note` | various |

### 15. `finance/unit-economics.csv` — 12 metrics

| Column | Type |
|--------|------|
| `No` / `Metric` / `Keywords` / `Formula` / `Category` / `Healthy_Range` / `Warning_Range` / `Danger_Range` / `Why_It_Matters` / `How_To_Improve` / `Anti_Pattern` / `Giantiny_Note` | various |

---

## Operations Domains (2)

### 16. `operations/support.csv` — 10 patterns

| Column | Type |
|--------|------|
| `No` / `Topic` / `Keywords` / `Stage` / `Category` / `Description` / `Do` / `Dont` / `Tool` / `SLA` / `Solo_Fit` / `Giantiny_Note` | various |

### 17. `operations/automation.csv` — 10 workflows

| Column | Type |
|--------|------|
| `No` / `Workflow` / `Keywords` / `Category` / `Trigger` / `Action` / `Tool_Free` / `Tool_Paid` / `Time_Saved` / `Stage` / `Complexity` / `Giantiny_Note` | various |

---

## Legal Expansion Domains (2)

### 18. `legal/contracts.csv` — 10 types

| Column | Type |
|--------|------|
| `No` / `Contract_Type` / `Keywords` / `Stage` / `Priority` / `Key_Clauses` / `DIY_Template` / `Lawyer_Needed` / `Cost` / `Risk_If_Missing` / `Giantiny_Note` | various |

### 19. `legal/security.csv` — 12 items

| Column | Type |
|--------|------|
| `No` / `Area` / `Keywords` / `Stage` / `Priority` / `Description` / `Implementation` / `Tool` / `Cost` / `Verification` / `Risk_If_Ignored` / `Giantiny_Note` | various |

### 20. `analytics/event-taxonomy.csv` — 15 events

| Column | Type | Description |
|--------|------|-------------|
| `No` | int | Order |
| `Event_Name` | string | PostHog/Mixpanel event name (snake_case) |
| `Category` | string | Core Action / Engagement / Revenue / Acquisition |
| `Stage` | string | Valid 2-5 range |
| `Priority` | string | P0 (must-have) / P1 (should-have) / P2 (nice-to-have) |
| `Properties` | string | Event properties to capture (pipe-separated) |
| `Why_Track` | string | Business rationale for tracking this event |
| `Tool` | string | Recommended analytics tool |
| `Anti_Pattern` | string | What NOT to do with this event |
| `Giantiny_Note` | string | Giantiny philosophy check |

### 21. `analytics/funnel-templates.csv` — 8 funnels

| Column | Type | Description |
|--------|------|-------------|
| `No` | int | Order |
| `Funnel_Name` | string | AARRR / Activation / Retention / Revenue / Viral |
| `Product_Type` | string | SaaS / Marketplace / DevTool / Consumer |
| `Stage` | string | Valid 2-5 range |
| `Steps` | string | Funnel steps (→ separated) |
| `Key_Metric_Per_Step` | string | What to measure at each step |
| `Healthy_Range` | string | Benchmark ranges per step |
| `Warning_Range` | string | Ranges that indicate problems |
| `Fix_If_Broken` | string | Specific fix recommendations |
| `Source` | string | Source citation (Reforge, ProfitWell, etc.) |
| `Giantiny_Note` | string | Giantiny philosophy check |

### 22. `analytics/analytics-tools.csv` — 8 tools

| Column | Type | Description |
|--------|------|-------------|
| `No` | int | Order |
| `Tool` | string | Tool name |
| `Category` | string | Product Analytics / Session Replay / CDP |
| `Stage` | string | Valid 2-6 range |
| `Pricing` | string | Free tier + paid pricing |
| `Self_Hosted` | boolean | Whether self-hosting is available |
| `Key_Features` | string | Core capabilities (pipe-separated) |
| `Best_For` | string | Who should use this tool |
| `Alternatives` | string | Competing tools |
| `Anti_Pattern` | string | When NOT to use this tool |
| `Giantiny_Note` | string | Giantiny philosophy check |

---

## Guardrails-as-Code (`data/guardrails.json`)

> Inspired by Agentic OS Policy-as-Code Engine. Hard enforcement rules that agents MUST check before recommending actions.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique ID (G-NNN format) |
| `type` | enum | `BLOCK` (hard stop) or `WARN` (warning) |
| `domain` | string | Which domain this rule applies to |
| `condition` | string | Pseudo-code condition for triggering |
| `message` | string | User-facing message shown when triggered |
| `severity` | enum | `CRITICAL` / `HIGH` / `MEDIUM` / `LOW` |
| `rationale` | string | Why this guardrail exists |

**15 rules** covering: stage-gating (G-001–G-004), budget protection (G-005), PMF enforcement (G-006), irreversible action warnings (G-007), channel concentration (G-008–G-009), equity protection (G-010), validation completeness (G-011), launch readiness (G-012), runway emergencies (G-013–G-014), context decay (G-015).

---

## Decision Impact Rules (`reasoning/impact-rules.csv`)

| Column | Type | Description |
|--------|------|-------------|
| `Decision_Type` / `Keywords` / `Upstream_Areas` / `Downstream_Needs` / `Risk_Level` / `Stage_Warning` / `Anti_Pattern` | various | Impact analysis fields |
| `Reversibility` | enum | `reversible` \| `partially` \| `irreversible` — can this decision be undone? |

---

## Marketing Channels (`marketing/channels.csv`)

| Column | Type | Description |
|--------|------|-------------|
| Standard channel fields | various | Channel, Type, Cost, etc. |
| `Impact_Preview` | string | Projected reach, cost, and timeline for this channel |
| `Reversibility` | enum | `reversible` \| `partially` \| `irreversible` |

---

## Data Quality Gates (Lucius L4)

| Rule | Applies To | Violation = |
|------|-----------|------------|
| `Keywords` MUST be filled | ALL CSVs | Search blind spot |
| `Giantiny_Note` in new CSVs | marketing, finance, ops, legal | Missing philosophy alignment |
| `Anti_Pattern` or `Dont` | ALL CSVs | No mistake prevention |
| `Stage` MUST use valid 0-6 | ALL CSVs | Wrong agent routing |
| `Decision_Rules` valid JSON | reasoning | Engine crash |
| `Reversibility` MUST be filled | playbook, channels, impact-rules | Missing risk awareness |
| `Validity_Period` MUST be filled | reasoning | Context decay blind spot |
| Guardrail IDs unique + G-NNN | guardrails.json | Engine crash |
