---
description: Sprint Build — AI-era rapid build-and-deploy workflow (Stage 1→2 in 2-4 days)
---

# /sprint-build — Build-Ship-Measure Sprint

> From idea to deployed product with tracking and first users. 6 tasks, 4 agents, 2-4 days.

---

## Overview

| Property | Value |
|----------|-------|
| **Duration** | **2-4 days** (AI-era compressed) |
| **Stages** | 1 → 2 |
| **Agents** | mvp-agent → data-agent → marketing-agent → orchestrator |
| **Tasks** | 6, dependency-chained |

## Task Chain

```
✅ T1: Tech stack selection (mvp-agent) [HARD_GATE]
   └→ T2: Core product build (mvp-agent) [SOFT_GATE]
      └→ T3: Deploy to production (mvp-agent) [SOFT_GATE]
         └→ T4: Analytics setup (data-agent) [SOFT_GATE]
            └→ T5: First distribution (marketing-agent) [SOFT_GATE]
               └→ T6: Sprint review — 48h metrics (orchestrator) [HARD_GATE]
```

---

## T1: Tech Stack Selection — HARD_GATE

**Owner:** `mvp-agent`

1. Search `tools` domain for stage-appropriate stack
2. Apply Giantiny ③: can 1 person operate?
3. Anti-pattern: no Rust+WASM+microservices for unvalidated idea

**Gate:**
- [ ] Familiar tech (not trendy-for-trending)
- [ ] Deployable to Vercel/Railway in <1 day
- [ ] Free tier sufficient
- [ ] **CEO approves**

→ `pm/agent-notes/mvp-agent-output.md`

---

## T2: Core Product Build — SOFT_GATE

**Owner:** `mvp-agent` | **Blocked by:** T1

1. Build core action (1 feature proves value)
2. No auth for first use
3. Mobile-responsive

**Gate:**
- [ ] Core action works end-to-end
- [ ] <3s load time
- [ ] Auto-advance to T3

---

## T3: Deploy — SOFT_GATE

**Owner:** `mvp-agent` | **Blocked by:** T2

**Gate:**
- [ ] Public URL live, HTTPS
- [ ] OG meta tags set
- [ ] Auto-advance to T4

---

## T4: Analytics Setup — SOFT_GATE

**Owner:** `data-agent` | **Blocked by:** T3

1. Install PostHog
2. 5 P0 events from `analytics_events`
3. Create first funnel

**Gate:**
- [ ] 5 events tracking
- [ ] Funnel created
- [ ] Events verified live
- [ ] Auto-advance to T5

→ `pm/agent-notes/data-agent-output.md`

---

## T5: First Distribution — SOFT_GATE

**Owner:** `marketing-agent` | **Blocked by:** T4

1. Post on 2+ communities (Reddit, HN, Discord)
2. UTM params for attribution

**Gate:**
- [ ] Posted on 2+ communities
- [ ] UTM params set
- [ ] Auto-advance to T6

---

## T6: Sprint Review — HARD_GATE

**Owner:** `orchestrator` | **Blocked by:** T5 + 48h data

1. Review PostHog after 48h
2. Present metrics to CEO

**Gate:**
- [ ] ≥10 visitors
- [ ] Analytics shows real data
- [ ] Core action completion rate measured
- [ ] **CEO decides: continue / iterate / pivot**

→ Broadcast: `[orchestrator] Sprint Build complete: {product} at {URL}, {N} visitors | Sprint: sprint-build`

---

## Timeline

| Task | Duration |
|------|----------|
| T1 | 1 hour |
| T2 | 1-3 days (AI) |
| T3-T5 | 2 hours |
| T6 | 48h wait |
| **Total** | **3-5 days** |

## Anti-Patterns
- ❌ Building 2 weeks without deploying
- ❌ Deploying without analytics
- ❌ Posting without UTM tracking
- ❌ Sprint review without 48h data minimum

---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Stack | Select tech stack + architecture | Tech stack decision doc | CEO approves stack (HARD_GATE) |
| **2** Build | Implement core features | Working code + tests | Core loop functional |
| **3** Deploy | Ship to production | Live URL | Accessible + analytics firing |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | Stack proven + core loop works + tests pass + deployed | → Sprint complete |
| **MEDIUM** | Deployed but minor issues | → Binary: A) Proceed to validate, B) Fix issues |
| **LOW** | Core loop broken or deploy failed | → Stop, debug before moving on |

### Anti-Patterns
- ❌ Over-engineering architecture before core loop works
- ❌ Building without analytics setup — flying blind
- ❌ Choosing trendy tech over familiar tech at speed-critical stage
