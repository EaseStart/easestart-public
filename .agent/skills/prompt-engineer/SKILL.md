---
name: prompt-engineer
description: "Transforms user prompts into optimized prompts using frameworks (RTF, RISEN, Chain of Thought, RODES, Chain of Density, RACE, RISE, STAR, SOAP, CLEAR, GROW)"
---

# Prompt Optimizer

> Silently analyze user intent → select framework → generate optimized prompt. Never explain framework choice.

## Framework Selection

| Task Type | Framework | When |
|-----------|-----------|------|
| Role-based (act as expert) | **RTF** (Role-Task-Format) | Clear role + task + output format |
| Step-by-step reasoning | **Chain of Thought** | Debugging, proof, logic |
| Multi-phase projects | **RISEN** (Role-Instructions-Steps-End goal-Narrowing) | Complex deliverables |
| System design/analysis | **RODES** (Role-Objective-Details-Examples-Sense check) | Architecture, design |
| Summarization | **Chain of Density** | Compress, synthesize |
| Communication | **RACE** (Role-Audience-Context-Expectation) | Reports, presentations |
| Investigation | **RISE** (Research-Investigate-Synthesize-Evaluate) | Research, diagnosis |
| Problem-solving | **STAR** (Situation-Task-Action-Result) | Context-rich problems |
| Documentation | **SOAP** (Subjective-Objective-Assessment-Plan) | Records, technical docs |
| Goal-setting | **CLEAR** (Collaborative-Limited-Emotional-Appreciable-Refinable) | OKRs, objectives |
| Coaching | **GROW** (Goal-Reality-Options-Will) | Mentoring, growth plans |

## Blending

Combine 2-3 frameworks when task spans multiple types:
- Complex technical project → **RODES + Chain of Thought**
- Leadership decision → **CLEAR + GROW**
- Simple task → single framework, keep it short

## Process

1. **Analyze** — Detect type, complexity, clarity, domain
2. **Clarify** — Ask max 3 questions (only if critical info missing)
3. **Select** — Map to framework(s) silently
4. **Generate** — Output optimized prompt in markdown code block

## Quality Checks

- Prompt is self-contained (no external context needed)
- Task is specific and measurable
- Output format is clear
- No ambiguous language
- Complexity matches original input

## Rules

| ❌ Never | ✅ Always |
|----------|----------|
| Explain framework choice | Analyze intent first |
| Generic one-size prompts | Customize to context |
| Ask >3 clarifying questions | Include output format |
| Meta-commentary in output | Present in code block |
| Over-engineer simple tasks | Match complexity to input |

## Hard Gate (Before Submitting Optimized Prompt)

- [ ] Output chứa rõ ràng: Role + Task + Format
- [ ] Không ambiguous language
- [ ] Complexity matches original input
- [ ] Framework phù hợp đã chọn (RTF, RODES, etc.)

## Done Condition

Optimized prompt achieves higher output quality than original + gate items ✅
