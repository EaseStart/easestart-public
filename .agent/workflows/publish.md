---
description: Publish marketing content to Facebook Page + Threads with golden hour scheduling
---

# /publish — Social Media Auto-Publish Pipeline

Publish content from `output/marketing/` to Facebook Page (UX Hacker) and Meta Threads.
Supports text, image, and video posts with preview/confirm flow and golden hour scheduling.

## Prerequisites

1. `.env` file configured with Meta API tokens (see `.env.example`)
2. `requests` package installed (`pip install requests`)
3. Optional: `python-dotenv` for auto-loading `.env` (`pip install python-dotenv`)

## Quick Start

```bash
# Preview only (no publish)
// turbo
easestart publish output/marketing/video/repo-trend-radar/facebook-post.md --dry-run

# Publish to Facebook only
easestart publish output/marketing/video/repo-trend-radar/facebook-post.md -p facebook

# Publish to Threads only
easestart publish output/marketing/video/repo-trend-radar/facebook-post.md -p threads

# Publish to both platforms
easestart publish output/marketing/video/repo-trend-radar/facebook-post.md -p all

# Post immediately (skip golden hour wait)
easestart publish output/marketing/video/repo-trend-radar/facebook-post.md --now

# Attach video/image
easestart publish output/marketing/video/repo-trend-radar/facebook-post.md --media output/marketing/video/repo-trend-radar/final-linkedin-16x9.mp4

# Skip confirmation (auto-yes)
easestart publish output/marketing/video/repo-trend-radar/facebook-post.md --now --yes
```

## Full Pipeline Flow

```
1. Generate content     → Use prompts/marketing/{platform}/post.yaml
2. Review content file  → Edit output/marketing/.../post.md
3. Dry run preview      → easestart publish <file> --dry-run
4. Real publish         → easestart publish <file> -p all
5. Confirm preview      → Terminal shows formatted post + scheduling info
6. Wait for golden hour → Auto-waits (or --now to skip)
7. Published!           → Post URLs printed
8. Auto-logged          → output/marketing/content-log.csv updated
```

## Golden Hours (VN Timezone)

| Platform | Window 1    | Window 2    | Window 3    |
|----------|-------------|-------------|-------------|
| Facebook | 11:00-13:00 | 19:00-21:00 | —           |
| Threads  | 07:00-09:00 | 12:00-14:00 | 18:00-20:00 |

## Content File Formats

### Markdown (.md)
Expected structure (like `facebook-post.md` or `linkedin-post.md`):
```markdown
# Title

## Post (copy & paste)

Your post body here...

#hashtag1 #hashtag2

---

## Publishing Notes
- **Attach:** `video-file.mp4`
```

### Plain Text (.txt)
Just the post body with optional hashtags at the end.

## Standalone Usage (without CLI)

```bash
// turbo
python scripts/publish.py output/marketing/video/repo-trend-radar/facebook-post.md --dry-run
```

## Multi-Image Carousel Post

Facebook supports attaching multiple images via `attached_media`:

```python
import requests, json

# Step 1: Upload each image as unpublished
media_fbids = []
for img_path in image_files:
    with open(img_path, 'rb') as f:
        r = requests.post(f'https://graph.facebook.com/v25.0/{page_id}/photos',
            data={'published': 'false', 'access_token': page_token},
            files={'source': (filename, f, 'image/png')})
        media_fbids.append(r.json()['id'])

# Step 2: Create post with all images
attached = [{'media_fbid': fbid} for fbid in media_fbids]
requests.post(f'https://graph.facebook.com/v25.0/{page_id}/feed', data={
    'message': full_text,
    'attached_media': json.dumps(attached),
    'access_token': page_token,
})
```

## Editing a Live Post

```python
# Update text without re-publishing (keeps images + engagement)
requests.post(f'https://graph.facebook.com/v25.0/{post_id}', data={
    'message': updated_text,
    'access_token': page_token,
})
```

---

## Facebook Setup Guide (First Time)

### Step 1: Create Meta App

1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Create or select an App (ours: **"Marketing"**)
3. App type: **Business**

### Step 2: Get App Credentials

1. **App Dashboard → Settings → Basic**
2. Copy **App ID** → `META_APP_ID`
3. Click **Show** next to App Secret → `META_APP_SECRET`

### Step 3: Enable Page Permissions

> ⚠️ **CRITICAL:** This step is often missed and causes 403 errors.

1. **App Dashboard → Use Cases**
2. Find **"Manage everything on Page"** (PAGES_API) → click **Customize**
3. Add these permissions:
   - `pages_show_list` ✅
   - `pages_read_engagement` ✅
   - `pages_manage_posts` ✅ ← **MUST HAVE for publishing**

### Step 4: Generate Page Access Token

1. Go to [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Select your App (e.g., "Marketing")
3. **User or Page** dropdown → select your page (e.g., "UX Hacker")
4. In **Permissions**, ensure all 3 are checked + `pages_manage_posts`
5. Click **Generate Access Token** → authorize
6. Copy the token → `FB_PAGE_ACCESS_TOKEN`

### Step 5: Get Page ID

```bash
# Option A: From Graph API Explorer
GET /me/accounts → find your page → copy "id"

# Option B: Direct
GET /{page-name}?fields=id
```

### Step 6: Configure `.env`

```bash
cp .env.example .env
# Fill in:
# META_APP_ID=...
# FB_PAGE_ID=...
# FB_PAGE_ACCESS_TOKEN=...
```

### Step 7: Verify

```bash
// turbo
easestart publish output/marketing/video/repo-trend-radar/facebook-post.md --dry-run -p facebook
```

### Token Notes

| Type | How to get | Lifespan |
|------|-----------|----------|
| Short-lived User Token | Graph API Explorer "Generate" | ~1 hour |
| Long-lived User Token | Exchange via `/oauth/access_token` | ~60 days |
| Page Token (from long-lived User) | `GET /me/accounts` | **Never expires** ✅ |

**Get a never-expiring Page token:**
```bash
# 1. Exchange short-lived → long-lived user token
curl "https://graph.facebook.com/v25.0/oauth/access_token?\
grant_type=fb_exchange_token&\
client_id={APP_ID}&client_secret={APP_SECRET}&\
fb_exchange_token={SHORT_TOKEN}"

# 2. Get Page token from long-lived user token
curl "https://graph.facebook.com/v25.0/me/accounts?access_token={LONG_TOKEN}"
# → Page token from this response NEVER expires
```

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| Missing env vars | Copy `.env.example` to `.env` and fill values |
| `requests` not found | `pip install requests` |
| Facebook 403 `pages_manage_posts` | App Dashboard → Use Cases → Customize → Add `pages_manage_posts` → re-generate token |
| Facebook 403 general | Token is User type, not Page type. Use `GET /{page_id}?fields=access_token` to get Page token |
| Threads 403 | App Review may be pending for `threads_content_publish` |
| Video upload fails | Try `--now` flag; video may be too large for direct upload |
| Token expired | Re-generate or use never-expiring Page token (see Token Notes above) |


---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **1** Prepare | Load content + select platform | Content ready for publish | Content passes brand safety |
| **2** Review | CEO approves content (HARD_GATE) | Approval | Explicit CEO "yes" |
| **3** Publish | Browser automation → post | Published URL | Post visible on platform |
| **4** Log | Record to content-log.csv | Log entry | Entry recorded |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | Content approved + platform tested + brand aligned | → Publish |
| **MEDIUM** | Content good but timing uncertain | → Binary: A) Publish now, B) Schedule for optimal time |
| **LOW** | Content quality or brand safety concern | → Stop, revise content |

### Anti-Patterns
- ❌ Publishing without CEO review (HARD_GATE, no exceptions)
- ❌ Publishing same content to multiple platforms without adaptation
- ❌ Not logging published content to content-log.csv
