---
name: brainstorming
description: "Dynamic Scope Challenge + Socratic questioning protocol. MANDATORY for complex requests, new features, or unclear requirements. Merges GStack '10-star thinking' with Lucius neural propagation."
allowed-tools: Read, Glob, Grep
---

# Brainstorming & Dynamic Scope Challenge

> **MANDATORY:** Use for complex/vague requests, new features, architecture decisions.
> **Philosophy:** "Planning is not review. Founder taste is not engineering rigor. If you blur all of that together, you get a mediocre blend." — Explicit cognitive gears.

---

## 🛑 SOCRATIC GATE (ENFORCEMENT)

### When to Trigger

| Pattern | Action |
|---------|--------|
| "Build/Create/Make [thing]" without details | 🛑 Run Dynamic Scope Challenge |
| Complex feature or architecture | 🛑 Full 6-part challenge |
| Update/change request | 🛑 Confirm scope + Mode Selection |
| Vague requirements | 🛑 Premise Challenge first |
| Bug fix / hotfix | 🛑 Lightweight — Steps 0A + 0D (HOLD mode) only |

### 🚫 MANDATORY: Dynamic Scope Challenge Before Implementation

1. **STOP** — Do NOT start coding
2. **RUN** the 6-part challenge below
3. **WAIT** — Get user response before proceeding
4. **COMMIT** — Once mode is selected, execute faithfully. No drift.

---

## 🧠 STEP 0: Dynamic Scope Challenge

> Source: GStack Nuclear Scope Challenge + Lucius L1 Neural Propagation.
> Principle: Hướng loang ban đầu quyết định chất lượng. Start wrong → everything compounds wrong.

### 0A. Premise Challenge

> "Is this the right problem to solve?"

Ask these **before** discussing solutions:

1. **Right problem?** Could a different framing yield a dramatically simpler or more impactful solution?
2. **Real outcome?** What is the actual user/business outcome? Is this plan the most direct path, or are we solving a proxy problem?
3. **Do-nothing test:** What happens if we do nothing? Real pain point or hypothetical one?

> If the answer to #3 is "nothing much" → challenge whether this should be built at all.

### 0B. 10-Star Product Thinking

> "What is the product actually for?"

Do NOT take the request literally. Ask a more important question first:

- **What's the 10x version?** 10x more ambitious, 10x more value, for only 2x the effort?
- **What's the real job-to-be-done?** "Photo upload" is not the feature — "help sellers create listings that actually sell" is.
- **What would make a user say "oh nice, they thought of that"?**

Example reframe:
```
User says: "Add photo upload"
Weak AI: File picker + save image
10-Star: Auto-identify product → pull specs → draft title/description → suggest hero image → detect bad photos
```

### 0C. Dream State Mapping

> Lucius L1 — visualize the trajectory before deciding

```
CURRENT STATE              THIS PLAN                12-MONTH IDEAL
[describe where we are] → [describe what changes] → [describe target state]
```

**Ask:** Does this plan move toward the 12-month ideal or away from it? If it solves today's problem but creates next quarter's nightmare, say so explicitly.

### 0D. Scope Mode Selection

> Commit to one mode. Do NOT silently drift.

Present three options:

| Mode | When | Posture |
|------|------|---------|
| **🔥 EXPANSION** | Greenfield, user says "go big" | Build the cathedral. Push scope UP. "What's 10x better for 2x effort?" |
| **🔒 HOLD** | Bug fix, refactor, hotfix | Make it bulletproof. Exact scope, maximum rigor. No expansion, no reduction. |
| **✂️ REDUCTION** | Plan > 15 files, overbuilt | Surgery. Find the minimum that ships value. Cut everything else. |

**Context-dependent defaults:**
- Greenfield feature → suggest EXPANSION
- Bug fix or hotfix → default HOLD
- Refactor → default HOLD
- Plan touching > 15 files → suggest REDUCTION

**CRITICAL:** Once selected, COMMIT fully. Do not silently drift toward a different mode. Raise concerns once here — after that, execute the chosen mode faithfully.

### 0E. Cross-Domain Insight

> Lucius L1 — neural propagation across domains.

- Ý tưởng xuất sắc thường đến từ ngành khác
- "How does [gaming / healthcare / finance / logistics] solve this same problem?"
- Find 1+ cross-domain insight that could transform the approach

### 0F. Trade-off Table

> Every decision has a cost. Make it explicit.

```
| Decision | Choose | Sacrifice | Accept Because |
|----------|--------|-----------|----------------|
| [Tradeoff 1] | X | Y | Z |
| [Tradeoff 2] | X | Y | Z |
```

> ❌ Never present a solution as "all upside, no downside" — surface the real cost.

---

## ✨ DELIGHT OPPORTUNITIES (EXPANSION mode only)

After the Scope Challenge, identify **5+ bonus chunks** (< 30 min each) that would make users think "oh nice, they thought of that."

For each one:
- **What:** One-line description
- **Why it delights:** User emotion it triggers
- **Effort:** S/M estimate

Present as individual questions — never batch:
- **A)** Add to backlog
- **B)** Skip
- **C)** Build it now

---

## 📊 Question Format (MANDATORY)

> ⛔ NEVER use static templates. Questions must be dynamic and context-specific.

```markdown
### [PRIORITY] **[DECISION POINT]**

**Question:** [Clear question]

**Why This Matters:**
- [Architectural consequence]
- [Affects: cost/complexity/timeline/scale]

**Options:**
| Option | Pros | Cons | Best For |
|--------|------|------|----------|
| A | [+] | [-] | [Use case] |

**If Not Specified:** [Default + rationale]
```

### Question Generation Process

```
1. Parse request → Extract domain, features, scale indicators
2. Identify decision points → Blocking vs. deferable
3. Generate questions → Priority: P0 (blocking) > P1 (high-leverage) > P2 (nice-to-have)
4. Format with trade-offs → What, Why, Options, Default
```

### Core Principles

| Principle | Meaning |
|-----------|---------|
| **Questions Reveal Consequences** | Each question connects to an architectural decision |
| **Context Before Content** | Understand greenfield/feature/refactor/debug context first |
| **Minimum Viable Questions** | Each question must eliminate implementation paths |
| **Generate Data, Not Assumptions** | Don't guess — ask with trade-offs |
| **Binary Choices + Recommendation** | Never open-ended "What should I do?" (Lucius L5) |

---

## 📢 Progress Reporting

**PRINCIPLE:** Transparency builds trust. Status must be visible and actionable.

### Status Board Format

| Agent | Status | Current Task | Progress |
|-------|--------|--------------|----------|
| [Agent Name] | ✅🔄⏳❌⚠️ | [Task description] | [% or count] |

### Status Icons

| Icon | Meaning |
|------|---------|
| ✅ | Completed |
| 🔄 | Running |
| ⏳ | Waiting / Blocked |
| ❌ | Error |
| ⚠️ | Warning |

---

## ⚠️ Error Handling

**PRINCIPLE:** Errors are opportunities for clear communication.

### Error Response Pattern

```
1. Acknowledge the error
2. Explain what happened (user-friendly)
3. Offer specific solutions with trade-offs (binary choices)
4. Ask user to choose or provide alternative
```

| Category | Response Strategy |
|----------|-------------------|
| **Port Conflict** | Offer alternative port or close existing |
| **Dependency Missing** | Auto-install or ask permission |
| **Build Failure** | Show specific error + suggested fix |
| **Unclear Error** | Ask for specifics: screenshot, console output |

---

## ✅ Completion Message

```
1. Success confirmation (celebrate briefly)
2. Summary of what was done (concrete)
3. How to verify/test (actionable)
4. Next steps suggestion (proactive)
```

---

## 🚫 Anti-Patterns (AVOID)

| Anti-Pattern | Why |
|--------------|-----|
| Jumping to solutions before understanding | Wastes time on wrong problem |
| Assuming requirements without asking | Creates wrong output |
| Over-engineering first version | Delays value delivery |
| Taking request literally without challenging | Misses the real product |
| "I think" phrases | Uncertainty → Ask instead |
| Silently drifting scope mode | Undermines the commitment |
| Presenting "all upside" solutions | Hides real trade-offs |
| Batching questions | Ask one at a time per decision |
| Open-ended "What should I do?" | Always binary choice + recommendation |

---
