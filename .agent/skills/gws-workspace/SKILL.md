---
name: gws-workspace
description: "Google Workspace CLI integration — enables EaseStart agents to execute actions on Calendar, Tasks, Sheets, Gmail, Drive, Docs, Slides, and Chat."
---

# Google Workspace CLI Skill

> Gives EaseStart agents hands — not just advice, but direct execution on Google Workspace via `gws` CLI.

---

## Prerequisites

```bash
# Install
npm install -g @googleworkspace/cli
# OR
brew install googleworkspace-cli

# Auth (select only needed scopes)
gws auth login -s drive,gmail,sheets,calendar,tasks,slides,docs

# Verify
gws calendar +agenda --today
```

> ⚠️ Personal Gmail: max ~25 OAuth scopes for unverified apps. Use selective `-s` flag.

---

## Command Quick Reference

| Service | Read (Safe) | Write (Confirm First) |
|---------|------------|----------------------|
| **Calendar** | `gws calendar +agenda` | `gws calendar +insert` |
| **Tasks** | `gws tasks tasks list --params '{"tasklist":"@default"}'` | `gws tasks tasks insert --params '{"tasklist":"@default"}' --json '{"title":"..."}'` |
| **Sheets** | `gws sheets +read --spreadsheet ID --range "A1:D"` | `gws sheets +append --spreadsheet ID --values "a,b,c"` |
| **Gmail** | `gws gmail +triage --max 5` | `gws gmail +send --to X --subject Y --body Z` |
| **Drive** | `gws drive files list --params '{"pageSize":5}'` | `gws drive +upload ./file.md` |
| **Docs** | `gws docs documents get --params '{"documentId":"ID"}'` | `gws docs +write --title "T" --body "B"` |
| **Slides** | `gws slides presentations get --params '{"presentationId":"ID"}'` | `gws slides presentations create --json '{"title":"T"}'` |
| **Chat** | — | `gws chat +send --space spaces/ID --text "msg"` |

## Cross-Service Workflows

| Workflow | What It Does | Read/Write |
|----------|-------------|------------|
| `gws workflow +standup-report` | Today's meetings + open tasks | Read-only |
| `gws workflow +weekly-digest` | Week summary: meetings + unread count | Read-only |
| `gws workflow +meeting-prep` | Next meeting: agenda, attendees, docs | Read-only |
| `gws workflow +email-to-task` | Convert Gmail → Google Task | Write |
| `gws workflow +file-announce` | Announce Drive file in Chat space | Write |

---

## Security Rules

1. **Read-only commands** (`+agenda`, `+triage`, `+read`, `+standup-report`) → safe to execute
2. **Write commands** (`+send`, `+insert`, `+append`, `+upload`) → **always confirm with founder first**
3. Use `--dry-run` before destructive operations
4. Use `--sanitize` for PII/content safety screening
5. **Never** output tokens or API keys

---

## Agent ↔ gws Persona Mapping

| EaseStart Agent | gws Persona | Primary Services |
|----------------|-------------|-----------------|
| `pm-agent` | `persona-project-manager` | Calendar, Tasks, Sheets |
| `ops-agent` | `persona-team-lead` | Drive, Docs, Chat, Calendar |
| `marketing-agent` | `persona-content-creator` | Docs, Drive, Gmail, Chat |
| `fundraising-agent` | `persona-sales-ops` | Slides, Sheets, Calendar, Gmail |
| `validation-agent` | — | Forms, Sheets, Calendar |
| `finance-agent` | — | Sheets, Drive |
| `wellness-agent` | `persona-exec-assistant` | Calendar |

---

## Shell Tips (zsh)

```bash
# Sheet ranges with ! — use double quotes
gws sheets +read --spreadsheet ID --range "Sheet1!A1:D10"

# JSON params — wrap in single quotes
gws drive files list --params '{"pageSize": 5}'

# Pipe JSON output to jq for filtering
gws gmail +triage --format json | jq '.[].subject'
```

---

## Anti-Patterns

- ❌ Requesting all scopes (`gws auth login` without `-s`) — will exceed Gmail's 25-scope limit
- ❌ Auto-sending emails without founder approval — always confirm writes
- ❌ Storing Sheet IDs or API keys in agent notes — use environment variables
- ❌ Polling Calendar every minute — use `events +subscribe` for realtime when needed
- ❌ Ignoring `--dry-run` for batch operations — preview before executing

---

## Lucius Compliance

| Layer | Implementation |
|-------|---------------|
| **L1 Neural Propagation** | Cross-agent execution mapping: 7 agents mapped to specific `gws` personas, standardizing workspace actions. |
| **L2 Gated Pipeline** | Enforced via explicit confirmation gates for all `write` operations. `/gws-setup` is a strict 4-phase pipeline. |
| **L3 Research Grounding** | Grounded in official Google Workspace CLI documentation and structured JSON outputs. |
| **L4 Anti-Patterns** | 5 gws-specific execution anti-patterns documented, plus workspace-specific boundary rules. |
| **L5 Confidence** | Binary execution scoring: Read Operations = Auto-run (High Confidence). Write Operations = Require Founder Approval (Zero-trust/Gate). |
