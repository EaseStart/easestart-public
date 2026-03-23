# Marketing-for-Founders — Research Summary

> **Source:** [EdoStra/Marketing-for-Founders](https://github.com/EdoStra/Marketing-for-Founders) (~1.4K ⭐)
> **Researched:** 2026-03-19
> **Pipeline:** Lucius 5-Phase (DISCOVER → SCAN → DEEP DIVE → EXTRACT → INTEGRATE)

---

## Overview

Practical marketing resource collection targeting SaaS/App/Startup founders getting their first 10/100/1000 users. 18 categories covering the full marketing stack from launch to optimization. Bootstrap-focused (no big-budget assumptions).

## Key Findings

### What This Repo Does Well
- **Comprehensive scope:** 18 marketing categories with 152+ curated resources
- **Bootstrap-first:** Every tactic designed for founders with zero budget
- **LLM SEO/AEO/GEO section:** Cutting-edge 2025 knowledge on AI search optimization
- **Actionable:** Direct links to playbooks, templates, and frameworks (not just theory)
- **Stage-appropriate:** Naturally organized from early-stage (validation) to growth

### What It Misses (Anti-Goals)
- No structured data format (markdown only, not searchable)
- No stage-gating or progression logic
- No decision rules or reasoning engine
- No industry specialization

## Patterns Extracted → EaseStart Integration

| Priority | Pattern | EaseStart Impact | Files Affected |
|----------|---------|-----------------|----------------|
| **P0** | 15 launch platforms + directories | New domain `mkt_launch` | `marketing/launch-platforms.csv` |
| **P0** | 8 sales/outreach tactics | New domain `mkt_sales` | `marketing/sales-outreach.csv` |
| **P0** | 13 growth tactics (LLM SEO, Reddit, CRO, etc.) | New domain `mkt_growth` | `marketing/growth-tactics.csv` |
| **P0** | 15 new relationship edges | Knowledge graph enrichment | `relationships.csv` |
| **P1** | Agent hierarchy for marketing (from bmad) | Inspire reasoning engine | Documented (future) |
| **P2** | Chronological checklist format (from draftdev) | Alternative UX for report | Archived for future |

## Impact Summary

| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| Grow pillar rows | 59 | 95 | **+36 rows (+61%)** |
| Grow pillar % | 11% | 16% | **+5pp** |
| Total KG rows | 554 | 590 | **+36 rows** |
| Relationship edges | 58 | 73 | **+15 edges (+26%)** |
| New domains | 0 | 3 | `mkt_launch`, `mkt_sales`, `mkt_growth` |

## Cross-References

- [RESEARCH.md](../../RESEARCH.md) — All research tracks
- [marketing/channels.csv](../../data/marketing/channels.csv) — Existing marketing channels (15 rows)
- [marketing/content-playbook.csv](../../data/marketing/content-playbook.csv) — Content types (12 rows)
- [autoresearch/repo-research.md](../../autoresearch/repo-research.md) — Research methodology
