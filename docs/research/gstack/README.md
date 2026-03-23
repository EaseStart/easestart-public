# Research: garrytan/gstack

> **Repo:** [github.com/garrytan/gstack](https://github.com/garrytan/gstack)
> **Date:** 2026-03-19
> **Pipeline:** Lucius 5-Phase (SCAN → DEEP DIVE → EXTRACT → INTEGRATE)

## Summary

gstack is an open-source "software factory" by Garry Tan (YC CEO) that turns Claude Code into a virtual engineering team via 21 slash commands. It structures work as a sprint pipeline: Think → Plan → Build → Review → Test → Ship → Reflect.

## Key Findings

| # | Finding | Applicability | Priority |
|:-:|---------|:------------:|:--------:|
| 1 | **Reframe Before Build** — `/office-hours` listens to pain, reframes entire problem before building | P0 — Direct Apply | 🔥🔥🔥 |
| 2 | **Fix-First Review** — `/review` auto-fixes obvious issues, surfaces ambiguous for human | P0 — Direct Apply | 🔥🔥🔥 |
| 3 | **Gated Ship Pipeline** — test → review → deploy → docs in structured sequence | P1 — Adapt | 🔥🔥🔥 |
| 4 | **Safety Guardrails** — `/careful` warns destructive commands, `/freeze` locks scope | P1 — Adapt | 🔥🔥 |
| 5 | **Stage Readiness Dashboard** — visual check before advancing | P1 — Adapt | 🔥🔥 |
| 6 | **Cross-Model Review** — `/codex` gets second AI opinion on code | P2 — Inspire | 🔥 |
| 7 | **Document-on-Ship** — auto-update docs on every release | P1 — Adapt | 🔥🔥 |
| 8 | **Session ELI16** — simplify comms when ≥3 parallel sessions | P2 — Inspire | 🔥 |

## Lucius Theory Gaps

4 corrections identified when reviewing through Lucius lens:
1. **L1:** Reframe needs full 6-step hướng loang (cross-domain missing in gstack)
2. **L2:** Dev workflows need Phase → Artifact → Gate structure
3. **L5:** Ship decisions need confidence scoring protocol
4. **L5:** Cross-agent debate needs structured scoring + binary choices

## See Also

- [Full Research Report](../../../.gemini/antigravity/brain/80f70195-3b17-42bf-afcd-e70b144c3bba/gstack-research.md)
- [Applicability Analysis](../../../.gemini/antigravity/brain/80f70195-3b17-42bf-afcd-e70b144c3bba/gstack-apply-easestart.md)
- [Lucius Review](../../../.gemini/antigravity/brain/80f70195-3b17-42bf-afcd-e70b144c3bba/gstack-lucius-review.md)
