---
description: Design in-person courses & workshops using the AI-proof Skills/Knowledge framework. Covers curriculum architecture, session design, content creation, and delivery methodology.
---

# /course-design — In-Person Course Design Workflow

> Methodology for designing in-person courses that teach **human-centric skills & knowledge** — the things AI cannot replace. Built from the 4-Group Skills/Knowledge Framework.

> **Lucius:** L2 (Phase→Artifact→Gate) · L5 (learning objective coverage check)
> **Owner:** ops-agent

---

## PREREQUISITES

Before starting, ensure you have:
- [ ] Clear **target audience** (role, experience level, industry)
- [ ] **Course goal** — which skills/knowledge to develop
- [ ] **Duration** — half-day, full-day, multi-day, or multi-week
- [ ] **Class size** — impacts exercise design (optimal: 8-16 for skill-building)
- [ ] Reference: This workflow's knowledge base (Section 7)

---

## PHASE 1: CURRICULUM ARCHITECTURE

### 1.1 — Map Learning Objectives to the 4-Group Framework

Every course must target skills/knowledge from one or more of these groups:

| Group | Focus | Core Question |
|-------|-------|---------------|
| **A: Đọc Người** | Read people — emotions, culture, org dynamics | "Can participants accurately read unspoken context?" |
| **B: Ra Quyết Định** | Decide under ambiguity — framing, tradeoffs, prioritization | "Can participants make good decisions with incomplete info?" |
| **C: Nhìn Hệ Thống** | Systems thinking — synthesis, patterns, taste | "Can participants see connections others miss?" |
| **D: Orchestrate** | Create results through others — facilitate, negotiate, coach | "Can participants move a group toward outcomes?" |

**Action:**
1. List 3-5 specific learning objectives
2. Tag each objective to a Group (A/B/C/D)
3. For each objective, identify the **sub-skills** from the decomposition list (Section 7.3)
4. Verify at least 60% of objectives target **Tier 2-3** skills (AI-resistant)

> 🔴 **Rule:** Never design a course that only teaches Tier 1 (AI-replaceable) content. If content is Tier 1, it should be pre-work or reference material — not live instruction time.

### 1.2 — Determine the AI Replaceability Tier Mix

| Tier | Role in Course | Time Allocation |
|------|---------------|-----------------|
| **Tier 1** (AI-replaceable) | Pre-work, reference handouts, AI-demo during class | 0-10% of live time |
| **Tier 2** (Hard to replace) | Structured exercises, guided practice, case studies | 40-50% of live time |
| **Tier 3** (Elite-only) | Live scenarios, immersive simulations, mentor observation | 40-50% of live time |

### 1.3 — Design the Skill Progression Arc

```
Session Flow:
AWARENESS → UNDERSTANDING → PRACTICE → INTEGRATION → REFLECTION

1. AWARENESS: "I didn't know I was missing this"
   - Show the gap between what AI can do and what humans must do
   - Demo AI strengths → reveal where it fails → that's what we'll learn

2. UNDERSTANDING: "Now I see the components"
   - Decompose the skill into sub-skills (from Section 7.3)
   - Participants self-assess: which sub-skills do I already have?

3. PRACTICE: "I'm trying it in a safe space"
   - Structured exercises with immediate feedback
   - Pair work, small group, role-play

4. INTEGRATION: "I'm combining multiple skills in realistic scenarios"
   - Complex case studies or live simulations
   - Cross-group skill application (e.g., Read People + Decide)

5. REFLECTION: "I know what to practice next"
   - Personal action plan
   - Peer feedback synthesis
```

---

## PHASE 2: SESSION DESIGN

### 2.1 — Session Blueprint Template

For each session block (60-90 min), use this structure:

```markdown
## Session: [Title]
**Group:** A / B / C / D
**Tier:** 2 / 3
**Duration:** __ min

### Learning Objective
[One specific, observable outcome]

### Opening Hook (5-10 min)
[Story, provocative question, or AI demo that creates tension]

### Core Concept (10-15 min)
[Minimum viable theory — decomposed sub-skills, framework, or model]
[Use visual frameworks, not lecture]

### Practice Exercise (25-40 min)
[Structured activity — see Exercise Design patterns below]
**Format:** Individual / Pair / Small Group / Full Class
**Materials:** [List needed materials]
**Debrief questions:** [3-5 questions for reflection]

### Integration Bridge (5-10 min)
[Connect this session to the next, or to real-world application]
[Personal commitment: "One thing I'll try this week"]
```

### 2.2 — Exercise Design Patterns by Group

> **Data:** 20 exercise patterns across 4 groups → [`data/exercise-patterns.csv`](data/exercise-patterns.csv)
>
> Columns: `group`, `pattern`, `description`, `best_for`
>
> Filter by `group` (A/B/C/D) to find exercises matching your target skill group.

### 2.3 — Time Block Templates

**Half-day (4 hours):**
```
09:00 - 09:30  Opening + AI vs Human frame-setting
09:30 - 10:30  Session 1: Core skill (Group __)
10:30 - 10:45  Break
10:45 - 12:00  Session 2: Practice + integration exercise
12:00 - 12:30  Reflection + personal action plan
```

**Full-day (8 hours):**
```
09:00 - 09:45  Opening + self-assessment + AI demo
09:45 - 11:00  Session 1: Group A or C skill (foundation)
11:00 - 11:15  Break
11:15 - 12:30  Session 2: Group B skill (decision-making layer)
12:30 - 13:30  Lunch
13:30 - 15:00  Session 3: Group D skill (orchestration layer)
15:00 - 15:15  Break
15:15 - 16:30  Integration exercise (combines all groups)
16:30 - 17:00  Reflection + peer feedback + action plan
```

**Multi-week (4 weeks × 1 session/week):**
```
Week 1: Group A — Read People (foundation for everything else)
Week 2: Group C — See Systems (build the "lens")
Week 3: Group B — Decide (use A + C to make better decisions)
Week 4: Group D — Orchestrate (put it all together through others)

Between-session assignments: real-world observation tasks
```

---

## PHASE 3: CONTENT CREATION

### 3.1 — Slide/Material Design Rules

1. **No wall of text** — use visuals, frameworks, before/after comparisons
2. **Show, don't tell** — video clips, real examples, live demos over theory
3. **AI contrast** — for every skill taught, show what AI CAN do (Tier 1) then what it CAN'T (Tier 2-3). This creates the "why this matters" motivation
4. **Decomposition visual** — always show the sub-skill breakdown so learners know exactly WHAT to practice
5. **Real examples from 4 industries** — Agriculture, Hospitality, Product Design, PM — rotate examples so every audience finds relevance

### 3.2 — Handout Templates

Each session should have a **1-page handout** with:
- Skill name + tier level
- Sub-skill decomposition (3-5 bullets)
- Self-assessment scale (1-5 for each sub-skill)
- "Practice this week" prompt
- Recommended observation/exercise to do alone

### 3.3 — Pre-work Design

Pre-work should cover **Tier 1 content** so live time focuses on Tier 2-3:
- Reading: frameworks, models, case studies (AI can generate/summarize these)
- Self-assessment: rate yourself on the sub-skills we'll cover
- Observation task: "Before class, spend 15 min in a coffee shop and note 3 things about the service flow"

---

## PHASE 4: DELIVERY METHODOLOGY

### 4.1 — Instructor Principles

These are meta-skills the instructor must embody (all Tier 3):

| Principle | Application |
|-----------|-------------|
| **Model, don't lecture** | Demonstrate the skill live — read the room, facilitate, synthesize in real-time |
| **Create productive discomfort** | Push participants just past their comfort zone, not into panic zone |
| **Name what you're doing** | "Notice how I just reframed that question? That's the skill we're learning" |
| **Debrief > Exercise** | The exercise creates experience; the debrief creates learning |
| **Honor tacit knowledge** | Participants already have experience — surface it, don't overwrite it |

### 4.2 — Energy & Pacing

```
Energy arc for a full-day session:

HIGH   ████                    ████
MED    ██████████         ███████████████
LOW                 █████                  ████
       |Morning|  |Break| |Afternoon|  |Close|

- Morning: Build energy gradually, peak before lunch
- After lunch: Start with movement/interaction (NOT lecture)
- Late afternoon: Integration exercise creates its own energy
- Close: Reflective, calm, forward-looking
```

### 4.3 — Feedback & Assessment

| Method | When | Purpose |
|--------|------|---------|
| **Self-assessment** | Before + after course | Measure perceived growth |
| **Peer observation** | During exercises | Real-time skill feedback |
| **Facilitator notes** | During exercises | Identify individual growth areas |
| **1-week follow-up** | Post-course | Check real-world application |
| **Before/after comparison** | End of course | Show concrete progress on sub-skill ratings |

---

## PHASE 5: POST-COURSE

### 5.1 — Follow-up Design
- [ ] Send 1-page summary + personal action plan reminder (Day 1)
- [ ] "Practice prompt" challenge — one sub-skill to practice per week (Week 1-4)
- [ ] Group check-in call or chat (Week 2)
- [ ] Optional 1:1 coaching session (Week 4)
- [ ] Alumni community access for ongoing practice

### 5.2 — Course Iteration
- [ ] Collect feedback: what exercises landed, what fell flat
- [ ] Review personal action plans: what participants actually did
- [ ] Update exercise database with new scenarios from real participant stories
- [ ] Adjust tier balance if participants were more/less advanced than expected

---

## SECTION 6: COURSE PROPOSAL TEMPLATE

When pitching a course to a client or student, use this structure:

```markdown
# [Course Title]

## Vấn đề
[What AI can now do in their field — and what it CAN'T]
[The gap: skills that matter more than ever but aren't taught]

## Kết quả sau khóa học
[3-5 specific, observable outcomes — tied to Tier 2-3 skills]

## Ai nên tham gia
[Target audience, experience level, prerequisites]

## Cấu trúc
[Duration, format, session overview]

## Phương pháp
[How we teach: 70% practice, 20% framework, 10% theory]
[What makes this different: skill decomposition, AI-contrast, real-world exercise]

## Về giảng viên
[Credentials that prove instructor has Tier 3 skills in these areas]
```

---

## SECTION 7: KNOWLEDGE BASE — Skills & Knowledge Reference

> This section is the source of truth for curriculum content. Reference when selecting learning objectives and designing exercises.

### 7.1 — AI Replaceability Tiers

| Tier | Definition | Course Role |
|------|-----------|-------------|
| **Tier 1** — Dễ bị AI thay thế | AI does 70-90% as well as humans. Improving fast. | Pre-work only. Don't waste live time. |
| **Tier 2** — Khó bị AI thay thế | Needs real context, judgment, or human interaction. AI assists but can't replace. | Core curriculum. Structured practice. |
| **Tier 3** — Elite, khó thay thế | Rare even among humans. Top 5-10% in the field. Years of accumulation. | Advanced sessions. Mentor modeling. Immersive scenarios. |

### 7.2 — The 4 Groups

```
         ┌─────────────┐
         │  A: ĐỌC     │ ← Input: Read people, emotions,
         │   NGƯỜI     │   culture, organizations
         └──────┬──────┘
                │ feeds into
    ┌───────────┼───────────┐
    ▼                       ▼
┌──────────┐         ┌──────────┐
│ B: RA    │         │ C: NHÌN  │
│ QUYẾT    │◄───────►│ HỆ       │ ← Lens: See systems,
│ ĐỊNH     │         │ THỐNG    │   patterns, connections
└──────┬───┘         └────┬─────┘
       │                  │
       └────────┬─────────┘
                ▼
         ┌─────────────┐
         │ D: ORCHESTR-│ ← Output: Create results
         │   ATE       │   through other people
         └─────────────┘
```

**Group A → B + C → D** (train in this order for multi-week courses)

### 7.3 — Skill & Knowledge Decomposition

> **Data:** 32 skills/knowledge items across 4 groups → [`data/skills-knowledge.csv`](data/skills-knowledge.csv)
>
> Columns: `group` (A/B/C/D), `type` (skill/knowledge), `name`, `tier` (2/3), `sub_components`
>
> - Filter by `group` to find skills for a specific curriculum area
> - Filter by `tier` to check AI-replaceability level
> - Use `sub_components` as the basis for exercise design and self-assessment rubrics

### 7.4 — Industry Application Matrix

> **Data:** AI vs Human strengths across 4 domains → [`data/industry-matrix.csv`](data/industry-matrix.csv)
>
> Columns: `domain`, `ai_strongest`, `human_wins`
>
> Use when selecting examples: each session should rotate examples across industries for relevance.

---

## SECTION 8: QUICK START CHECKLIST

```
// turbo-all
```

1. Define audience + goal → Pick target Groups (A/B/C/D) and Tier mix
2. List 3-5 learning objectives → Tag each to Group + decomposed sub-skills
3. Choose course format (half-day / full-day / multi-week)
4. Design sessions using the Session Blueprint Template (Phase 2.1)
5. Select exercises from Exercise Design Patterns (Phase 2.2)
6. Create pre-work covering Tier 1 content
7. Build 1-page handouts per session (Phase 3.2)
8. Write course proposal using template (Section 6)
9. Deliver → Debrief → Collect feedback → Iterate (Phase 5)

---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Curriculum | Learning objectives → 4-Group Framework | Curriculum map + skill matrix | All objectives mapped to AI tier |
| **2** Session Design | Blueprint per session | Session blueprints (markdown) | Each session has hook + concept + practice + reflection |
| **3** Content | Exercises + case studies + rubrics | Content files | All exercises are hands-on, not theoretical |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | All sessions have blueprints + exercises + clear AI-proof justification | → Course ready |
| **MEDIUM** | Some sessions lack exercises or rubrics | → Binary: A) Ship with gaps noted, B) Complete missing content |
| **LOW** | Learning objectives unclear or wrong AI tier assignment | → Stop, return to Phase 1 |

### Anti-Patterns
- ❌ Teaching AI-replaceable skills without acknowledging it — course loses value
- ❌ All theory, no practice — adults learn by doing
- ❌ Sessions without opening hooks — attention lost in first 5 minutes
- ❌ No reflection/debrief phase — learning doesn't consolidate
