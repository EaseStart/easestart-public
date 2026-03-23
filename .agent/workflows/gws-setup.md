---
description: "Setup Google Workspace CLI (gws) for EaseStart — interactive step-by-step guide. Agent walks user through each phase."
---

# Google Workspace Setup

> One-time workflow to connect EaseStart agents to Google Workspace.
> **Skills:** gws-workspace
> **Estimated time:** ~10 minutes

---

## How This Workflow Works

> Agent guides the user step-by-step. At each phase, the agent:
> 1. Explains what this step does (1 sentence)
> 2. Asks the user for any required input
> 3. Runs the automated part
> 4. Confirms success before moving on

---

## Phase 1: INSTALL gws CLI

> **What:** Install the Google Workspace command-line tool.
> **Automated:** ✅ Yes — no user input needed.

```bash
npm install -g @googleworkspace/cli
gws --version
```

**Gate:** `gws --version` returns a version number → proceed.

---

## Phase 2: CHOOSE Google Account

> **What:** Decide which Google account will connect to EaseStart.
> **User Input Required:** ✋

### Ask User:
```
Bạn muốn dùng Google account nào để kết nối với EaseStart?
(Ví dụ: yourname@gmail.com hoặc email công ty)
```

### After user provides email:
```bash
gcloud auth login USER_EMAIL
gcloud config set account USER_EMAIL
```

**Gate:** `gcloud auth list` shows the correct account as ACTIVE → proceed.

---

## Phase 3: CREATE GCP Project

> **What:** Create a Google Cloud project to host the API credentials.
> **User Input Required:** ✋ (optional — can use default name)

### Ask User:
```
Tôi sẽ tạo một project trên Google Cloud để lưu credentials.
Bạn muốn đặt tên gì? (Enter để dùng mặc định: "easestart-gws")
```

### After user confirms:
```bash
gcloud projects create PROJECT_ID --name="PROJECT_NAME" --set-as-default
```

**Gate:** `gcloud config get project` returns the project ID → proceed.

---

## Phase 4: ENABLE APIs

> **What:** Bật 8 Google APIs cần thiết cho EaseStart agents.
> **Automated:** ✅ Yes — no user input needed.

```bash
gcloud services enable \
  calendar-json.googleapis.com \
  drive.googleapis.com \
  sheets.googleapis.com \
  gmail.googleapis.com \
  docs.googleapis.com \
  slides.googleapis.com \
  tasks.googleapis.com \
  chat.googleapis.com
```

**Gate:** All 8 services enabled → proceed.

---

## Phase 5: CONFIGURE OAuth (Manual — Browser Required)

> **What:** Tạo OAuth credentials trên Google Cloud Console.
> **User Input Required:** ✋ — cần thao tác trên browser.

### Give User These Instructions:

```
Bước này cần làm trên browser (khoảng 3 phút). Tôi sẽ hướng dẫn từng bước:

📋 BƯỚC 5A — OAuth Consent Screen:
1. Mở link: https://console.cloud.google.com/apis/credentials/consent?project=PROJECT_ID
2. Chọn "External" → Click "Create"
3. App name: gws CLI
4. User support email: chọn email của bạn
5. Developer contact: nhập email của bạn
6. Click "SAVE AND CONTINUE" qua 3 trang (Scopes → Test users → Summary)

⚠️ QUAN TRỌNG — Thêm Test User:
7. Quay lại tab "Test users" → Click "+ ADD USERS"
8. Nhập email của bạn: USER_EMAIL
9. Click "SAVE"
(Bỏ bước này sẽ bị lỗi 403 khi login!)

📋 BƯỚC 5B — Tạo OAuth Client:
1. Mở link: https://console.cloud.google.com/apis/credentials?project=PROJECT_ID
2. Click "+ CREATE CREDENTIALS" → "OAuth client ID"
3. ⚠️ Application type: chọn "Desktop app" (KHÔNG phải Web application)
4. Name: gws CLI
5. Click "CREATE"
6. Click "DOWNLOAD JSON" trong popup

Xong rồi cho tôi biết nhé! Hoặc paste path file JSON đã tải về.
```

### After user confirms download:

```bash
mkdir -p ~/.config/gws
mv ~/Downloads/client_secret_*.json ~/.config/gws/client_secret.json

# Verify correct format
python3 -c "import json; d=json.load(open('$HOME/.config/gws/client_secret.json')); assert 'installed' in d, 'ERROR: Wrong type! Need Desktop app, not Web application'"
```

### Known Pitfalls
- ❌ Chọn "Web application" → JSON có key `"web"` → gws không nhận → phải tạo lại
- ❌ Quên thêm Test User → lỗi `403: access_denied` khi login
- ❌ Quên download JSON → gws không tìm thấy credentials

**Gate:** File exists with `"installed"` key → proceed.

---

## Phase 6: LOGIN & VERIFY

> **What:** Kết nối gws CLI với Google account.
> **Semi-automated:** Agent chạy lệnh, user approve trên browser.

```bash
gws auth login -s drive,gmail,sheets,calendar,tasks,slides,docs,chat
```

### Tell User:
```
Browser sẽ mở lên. Bạn hãy:
1. Chọn account USER_EMAIL
2. Nếu thấy "Google hasn't verified this app" → click "Advanced" → "Go to gws CLI (unsafe)"
3. Click "Allow" cho tất cả permissions
4. Khi thấy "Success" → nhắn tôi!
```

### After user confirms:
```bash
# Verify all services
gws calendar +agenda --today        # Calendar ✓
gws tasks tasklists list             # Tasks ✓
gws gmail +triage --max 3           # Gmail ✓
```

**Gate:** All 3 commands return data → ✅ **SETUP COMPLETE!**

---

## Automation Summary

| Phase | Automated? | Future Automatable? |
|-------|:---:|:---:|
| 1. Install | ✅ | ✅ |
| 2. Choose account | ✋ Ask user | ✋ Always manual |
| 3. Create project | ✅ after input | ✅ |
| 4. Enable APIs | ✅ | ✅ |
| 5. OAuth setup | ✋ Browser | ❌ GCP Console only |
| 6. Login | ⚠️ Browser approve | ⚠️ First time only |

**Phases 1, 3, 4 = fully scriptable.** Target: `easestart setup gws` automates these 3, then guides user through 2, 5, 6 interactively.

---

## Post-Setup Quick Reference

```bash
# Check auth status
gws auth status

# Daily standup (PM agent)
gws workflow +standup-report

# Create calendar event
gws calendar events insert --params '{"calendarId":"primary"}' \
  --json '{"summary":"Event","start":{"dateTime":"..."},"end":{"dateTime":"..."}}'

# Add a task
gws tasks tasks insert --params '{"tasklist":"@default"}' \
  --json '{"title":"My Task"}'

# Read emails
gws gmail +triage --max 5

# Set tracking Sheet ID (add to .zshrc)
export EASESTART_SHEET_ID="your-sheet-id-here"
```

---

## Lucius Compliance

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | Auth success + all services accessible | → GWS ready |
| **MEDIUM** | Auth works but some services limited | → Binary: A) Proceed with available services, B) Fix permissions |
| **LOW** | Auth failed or tokens invalid | → Stop, re-run auth setup |

### Anti-Patterns
- ❌ Storing credentials in code — use environment variables
- ❌ Skipping service verification after auth
