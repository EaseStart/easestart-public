---
name: easestart-knowledge
description: "EaseStart knowledge graph search — BM25 hybrid search across 29+ CSV domains with L5 confidence scoring."
---

# EaseStart Knowledge Skill

Search the EaseStart CSV knowledge graph for startup advice, frameworks, tools, and case studies.

## Usage

```python
# Basic search
results = search(query="pricing strategy for SaaS", domain="pricing")

# Stage-weighted search
results = search(query="validate idea", domain="stages", stage=2)
```

## Result Fields

| Field | Type | Description |
|-------|------|-------------|
| `_score` | float | BM25 relevance score |
| `_confidence` | HIGH/MEDIUM/LOW | Lucius L5 confidence |
| `_domain` | string | Source CSV domain |
| `_anti_pattern_warning` | string | ⚠️ if anti-pattern triggered |

## Confidence Protocol (L5)

| Level | BM25 Score | Action |
|:-----:|:----------:|--------|
| HIGH | ≥ 3.0 | Proceed autonomously, cite source |
| MEDIUM | 1.0 – 2.99 | Present binary choice |
| LOW | < 1.0 | Stop, ask founder for context |
