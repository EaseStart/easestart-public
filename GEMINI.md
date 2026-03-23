# EaseStart — Project Ground Rules

> These rules are ALWAYS active. Every agent, every workflow, every code change must comply.

---

## Project Context

EaseStart is a CLI-based startup validation system that generates Founder's Intel Memo reports.
Stack: Python scripts + CSV knowledge base + HTML/CSS report output.

## Ground Rules

### 1. Monochrome Design System

All report output uses monochrome design tokens. No exceptions.

| Token | Value | Usage |
|-------|-------|-------|
| `--black` | #000000 | Headings, borders, active states, copy block bg |
| `--white` | #FFFFFF | Body bg, copy block text, button hover |
| `--slate` | #4E4B66 | Secondary text, labels |
| `--border` | #E0E0E0 | Dividers |
| `--bg-muted` | #FAFAFA | Muted backgrounds |
| `--accent` | #22C55E | Scorecard total bar ONLY |

**Forbidden:** green/red for do/don't, colored backgrounds, purple, gradients, shadows, border-radius.

### 2. No Emojis in Report HTML

All labels use **UPPERCASE TEXT**. Emojis are ONLY allowed inside copy template content (social media posts).

### 3. Everything is Personalized

All content must use the founder's specific idea, target audience, and industry. No generic advice.

Variables: `{short}` (idea name), `{target}` (audience), `{ind}` (industry), `{problem}` (derived problem).

No bracket placeholders like `[the problem]` — derive from context.

### 4. Everything is Actionable

Every recommendation includes ready-to-execute deliverables:
- Step-by-step instructions (personalized)
- DO THIS / AVOID THIS (concrete, not abstract)
- Platform-ready copy templates (Reddit, Twitter, Discord, Email, etc.)
- COPY button on every template block

### 5. CEO is the Reader

Non-technical founders are the primary audience:
- Zero jargon (translate all internal codes)
- Every score has explanation + benchmark
- Every insight has a concrete next step
- Max 3 concepts per section

### 6. Skill Loading

Any work on reports MUST load `@[skills/easestart-report]` first.

---

## Key Files

| File | Purpose |
|------|---------|
| `scripts/generate_report.py` | Report generator |
| `output/shared.css` | Design system tokens |
| `.agent/skills/easestart-report/SKILL.md` | Full design rules |
| `.agent/workflows/generate-report.md` | Generation workflow |
| `.agent/agents/easestart-orchestrator.md` | Master orchestrator |

## Communication

- User communicates in **Vietnamese**
- Code, content, and variables in **English**

---

## 🎯 Skill Selection Gate (MANDATORY)

> 🔴 Before starting ANY task, identify and load the relevant skill(s).

**Protocol:**

```
1. Receive user request
2. SCAN skills below for matches
3. READ the matching SKILL.md
4. For report work → ALWAYS load `easestart-report` first
5. ONLY THEN proceed to coding
```

| Task Domain | Required Skill(s) |
|---|---|
| **Report generation/design** | `easestart-report` (ALWAYS) + `product-designer` |
| **Landing page / Web** | `frontend-design` + `product-designer` |
| **SEO / Growth** | `seo-fundamentals` + `geo-fundamentals` |
| **Research / Content** | `founder-knowledge` + `brainstorming` |
| **Bug fix** | `clean-code` only |
| **Prompt tuning** | `prompt-engineer` |
| **Browser testing** | `playwright-skill` |

**🔴 HARD CAP: MAX 3 skills per task. No exceptions.**
(Research-backed: 2-3 skills = +18.6% success. 4+ = diminishing returns.)

---

## 🗣️ Communication Protocol (MANDATORY)

1. **Never ask open-ended questions.** Present binary choices with a recommendation:
   - ❌ *"Nên làm gì với layout?"*
   - ✅ *"Dùng A (grid) hay B (flex)? Mình recommend A vì match pattern hiện tại."*
2. **Rate confidence 0-100%** before each quality gate.
3. **Batch questions.** 3 câu hỏi → hỏi 1 lần, đừng interrupt 3 lần.
4. **Timeout rule:** Confidence 40-69% → proceed with best guess.
5. **Ask vs Research — NEVER GUESS.**
   - **Cần context từ founder** (kinh nghiệm, mạng lưới, ý định, preferences) → **HỎI**. Không bao giờ đoán.
   - **Có thể tự research** (thị trường, đối thủ, pháp lý, data) → **Trigger research** tự động (autoresearch/web search/KB search).
   - ❌ Đoán Founder-Problem Fit mà không hỏi = **BUG**
   - ✅ Tự research TAM/SAM/SOM mà không cần hỏi = **ĐÚNG**

---

## 🔴 Self-Challenge (MANDATORY — Before Implementing)

Before committing to an approach, state:
1. **1 risk** — why this approach could fail
2. **1 alternative** — another viable approach considered

If risk > 40%, reconsider.

---

## Permission Defaults

| Permission | Default |
|------------|---------|
| Create new file | ✅ If needed |
| Delete file | ❌ Ask user first |
| Modify database/CSV schema | ❌ Ask user first |
| Install new dependency | ❌ Ask user first |
| Modify GEMINI.md / skills | ❌ Ask user first |

### 🚀 Effort is Not a Constraint (AI-Powered Development)

> 🔴 **Since all development is AI-assisted, effort is NEVER a valid reason to cut scope or simplify.**

**Always ship the complete, high-quality version:**
- Full test coverage — not "we'll add tests later"
- Comprehensive error handling — not "happy path only"
- Complete documentation — not "we'll document it later"
- Proper refactoring — not "it works, ship it"
- All edge cases handled — not "most users won't hit this"

**Only cut scope for REAL constraints:**
- Hard deadline from business/client
- Technical impossibility (not difficulty)
- User experience concern (too complex for the user, not for the AI)

**Failure Condition:**
- ❌ Saying "to save effort" or "for simplicity" = **PROTOCOL VIOLATION** — the AI handles the effort, not you.

---

## 🧠 Context Discipline Protocol (MANDATORY)

> 200K context windows degrade after ~100K tokens. These rules prevent that.

### Rule 1: One Phase Per Conversation
- Large features should split phases across conversations.
- At end of each phase: `brv curate` → suggest new conversation.
- **Exception:** Small fixes can stay in one conversation.

### Rule 2: ByteRover Handoff
```
START: brv query "{feature} {topic}" → load existing knowledge
END:   brv curate "{what was done}" -f {changed files} → save for next conversation
```

### Rule 3: Outline-First, Always
- Files < ~150 lines → read whole.
- Larger files: outline first → read only the relevant section.

### Rule 4: Lazy Skill Loading
- **NEVER** read all SKILL.md files at start.
- Only read a skill when the current task requires it.

### Rule 5: Token-Aware Reading
- Never read more than ~200 lines in a single `view_file` call for large files.
- Use `StartLine`/`EndLine` to target specific ranges.

### Rule 6: Write to Filesystem, Not Context
- Command output > 50 lines → save to `/tmp/` and reference the path.

### Rule 7: Checkpoint and Break at High Usage
- Long conversation → `brv curate` progress → suggest breakpoint.

### Rule 8: Session Awareness (No Re-Reading)
- Don't re-read content already shown in the same conversation.
- Saves ~15-25% of tool calls.

### Rule 9: Always Curate After Every Task

> 🔴 After completing ANY task — big or small — run `brv curate` before moving on.

```
DONE → brv curate "{what was done and why}" -f {changed files}
```

### Context Budget Summary

| Action | Token Cost | Alternative | Savings |
|--------|-----------|-------------|--------|
| Read 800-line file | ~4,000 | Outline + targeted read | **70%** |
| Read all SKILL.md files | ~8,000 | Read only 1-2 needed | **75%** |
| Keep test output in context | ~3,000 | Write to `/tmp/` | **90%** |
| Re-read seen definitions | ~1,500 | Session awareness | **100%** |
