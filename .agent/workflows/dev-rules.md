---
description: Development standards and conventions. File naming, code quality, pre-commit rules, and implementation guidelines.
---

# Development Rules

**IMPORTANT:** Analyze the skills catalog and activate the skills that are needed for the task during the process.

## General
- **File Naming**: Use kebab-case for file names with a meaningful name that describes the purpose of the file
- **File Size Management**: Keep individual code files under 200 lines
  - Split large files into smaller, focused components/modules
  - Extract utility functions into separate modules
- Follow the codebase structure and code standards in `./docs` during implementation
- Do not simulate or mock — always implement real code

## Code Quality Guidelines
- No syntax errors — code must be compilable
- Prioritize functionality and readability over strict style enforcement
- Use try-catch error handling and cover security standards

## Pre-commit Rules
- Run linting before commit
- Run tests before push (DO NOT ignore failed tests)
- Keep commits focused on actual code changes
- **DO NOT** commit confidential information (dotenv, API keys, credentials)
- Use conventional commit format

## Code Implementation
- Write clean, readable, maintainable code
- Follow established architectural patterns
- Handle edge cases and error scenarios
- Update existing files directly — do NOT create "enhanced" copies
---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Audit | Read existing codebase conventions | Convention analysis | Existing patterns documented |
| **2** Define | Write/update dev rules | `DEV_RULES.md` or equivalent | Rules cover naming, quality, pre-commit |
| **3** Enforce | Apply rules to codebase | Lint configs + pre-commit hooks | All files pass lint |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | Rules align with existing codebase + no breaking changes | → Apply rules |
| **MEDIUM** | Some existing code violates new rules | → Binary: A) Grandfather old code, B) Fix violations |
| **LOW** | Rules conflict with existing conventions | → Stop, discuss trade-offs with founder |

### Anti-Patterns
- ❌ Defining rules without reading existing codebase patterns
- ❌ Rules so strict that all existing code fails lint
- ❌ Not setting up automated enforcement (lint + pre-commit)
