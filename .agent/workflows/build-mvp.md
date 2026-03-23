---
description: "Build and launch an MVP — from scope definition through tech stack selection to first 100 users."
---

# /build-mvp Workflow

> MVP pipeline: Scope → Stack → Build → Launch → First 100 Users

## Prerequisites
- Lean Canvas v1 finalized
- Counter-position identified (Giantiny ②)
- Build plan ready (AI-assisted sprint)

## Steps

### Step 1: Core Loop Definition
```
ASK: "What is the ONE thing your product does?"
ASK: "Describe the simplest user workflow in 1 sentence."
OUTPUT: core-loop.md (single paragraph)
GATE: Core loop defined in ≤ 3 sentences → proceed
CONFIDENCE:
  ≥90% clear → Auto-proceed to feature cut
  70-89% → Proceed but note ambiguity
  <70% → Ask clarifying questions until loop is crisp
```

### Step 2: Feature Ruthless Cut
```
ACTION: List ALL features founder wants
CLASSIFY each as:
  ✅ CORE — needed for core loop to work
  ⚠️ NICE — helpful but not essential  
  ❌ CUT — absolutely not in MVP

RULE: MVP = CORE features only
GATE: ≤ 3 core features identified → proceed
CONFIDENCE:
  ≥90% scope tight → Auto-proceed to stack selection
  70-89% → Proceed with watchlist of nice-to-haves
  <70% → Founder is not cutting enough. Force "pick only 1 feature" exercise
```

### Step 3: Tech Stack Selection (Giantiny ③)
```
ASK: "What's your strongest programming language?"
ASK: "Are you the sole developer?"

SEARCH: tools --query "solo founder tech stack" --stage 3

RECOMMEND based on profile:
  Full-stack → Next.js + Supabase + Stripe + Vercel
  Frontend   → Next.js + Supabase (BaaS)
  Non-tech   → Webflow/Framer + Stripe

CHECK: "Can 1 person operate this stack?" 
  IF NO → "Pick simpler stack"

OUTPUT: tech-stack-decision.md
```

### Step 4: Build Sprint (4 weeks)
```
Week 1: Project Setup
  - [ ] Repo created
  - [ ] Auth configured (Supabase/Clerk)
  - [ ] Main page shell built
  - [ ] Deploy pipeline working (Vercel)

Week 2: Core Feature
  - [ ] Core loop functional end-to-end
  - [ ] Happy path works without errors
  - [ ] Data persistence working

Week 3: Polish + Payment
  - [ ] Stripe Checkout integrated (if charging)
  - [ ] Basic onboarding flow
  - [ ] Mobile-responsive check
  - [ ] Error handling for critical paths

Week 4: Analytics + Launch Prep
  - [ ] PostHog/Mixpanel installed
  - [ ] Key events tracked (signup, activation, core action)
  - [ ] Landing page live with value proposition
  - [ ] 10 beta invitations sent
```

### Step 5: Pre-Launch Checklist
```
REQUIRED:
  - [ ] Core loop works end-to-end ✅
  - [ ] Analytics tracking live ✅
  - [ ] Landing page with clear UVP ✅
  - [ ] Payment tested (real transaction) ✅
  - [ ] 10 beta users invited from relevant communities ✅

GIANTINY ③ MEDIA:
  - [ ] First "build in public" post published ✅
  - [ ] Product story/narrative written ✅
```

### Step 6: Launch Execution
```
Day 1: Soft Launch
  - Post on relevant communities (Reddit, Discord)
  - Post on Indie Hackers
  - Share on personal social media

Day 2-3: Community Launch
  - Post on relevant Reddit communities
  - Submit to Hacker News (if technical)
  - Share in relevant Slack/Discord communities

Day 7: Product Hunt (optional)  
  - Only if B2C or developer tool
  - Prepare assets: logo, screenshots, tagline
  
SEARCH: tools --query "launch platforms startup"
```

### Step 7: First 100 Users Tracking
```
SETUP Dashboard:
  Daily Active Users (DAU)
  Week 1 Retention (D7)
  Activation Rate (% completing core action)
  
GATE: 
  100+ signups → ✅ proceed to retention analysis
  < 100 after 2 weeks → iterate on distribution, not product
CONFIDENCE:
  ≥90% (100+ signups + activation >30%) → Auto-proceed to Stage 4
  70-89% (50-100 signups) → Continue distribution push
  <70% (<50 signups) → Revisit launch channels and value proposition
```

### Step 8: Post-Launch Decision
```
IF retention > 20% WoW → "Strong signal. Proceed to Stage 4 (PMF)."
IF retention 10-20% → "OK signal. Improve onboarding, then remeasure."
IF retention < 10% → "Weak. Return to validation — might be product-problem mismatch."

CONFIDENCE:
  ≥90% (retention >25% + activation >40%) → Auto-advance to growth-agent
  70-89% (retention 15-25%) → Proceed but monitor weekly
  50-69% (retention 10-15%) → Onboarding optimization first
  <50% (retention <10%) → Escalate to founder. Possible pivot needed.

SEARCH: reasoning --query "low retention after launch"
```

## Output Artifacts
- `core-loop.md`
- `tech-stack-decision.md`
- `build-sprint-tracker.md`
- `launch-plan.md`
- `post-launch-report.md`

## Time Estimate: 2-4 weeks (AI-era: 1-2 weeks)

---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Stack | Tech stack selection | Stack decision doc | CEO approves (HARD_GATE) |
| **2** Build | Implement MVP features | Working code | Core user flow functional |
| **3** Test | Unit + integration tests | Test results | Tests pass |
| **4** Deploy | Ship to production | Live URL + analytics | Product accessible to real users |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | Stack proven + core flow works + tests pass + deployed | → MVP complete |
| **MEDIUM** | Deployed but edge cases or minor bugs | → Binary: A) Proceed to validate, B) Fix first |
| **LOW** | Core flow broken or can't deploy | → Stop, debug root cause |

### Anti-Patterns
- ❌ Over-engineering at MVP stage — ship ugly, ship fast
- ❌ Building 10 features instead of 1 core flow
- ❌ No analytics setup — deploying blind
