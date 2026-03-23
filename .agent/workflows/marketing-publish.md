---
description: "Antigravity-native content generation + browser publishing. Generate and publish marketing content across platforms — $0 API cost."
---

# /marketing-publish — Content Generation & Publishing

> Generate marketing content using AI + publish via browser automation. Zero API cost.
> Inspired by MarketMeNow's YAML prompt architecture, powered by Antigravity.

---

## Overview

| Property | Value |
|----------|-------|
| **Cost** | $0 (uses Antigravity LLM + browser) |
| **Platforms** | Twitter/X, LinkedIn, Reddit |
| **Agent** | marketing-agent |
| **Prompt Templates** | `prompts/marketing/` |

## Prerequisites

- Brand config defined in `prompts/marketing/brand.yaml`
- Logged into target platforms in browser
- Read `prompts/marketing/brand.yaml` to understand brand voice

---

## Phase 1: GENERATE — Create Content Batch

> **Output:** Content batch (JSON) ready for review
> **Skills:** marketing strategy (content-playbook.csv)
> **Gate:** Content generated and formatted

### Actions

1. **Read brand config:**
   ```
   Read prompts/marketing/brand.yaml for brand identity, mention strategy, and content domains.
   ```

2. **Select platform + template:**
   - For Twitter threads: read `prompts/marketing/twitter/thread.yaml`
   - For Twitter replies: read `prompts/marketing/twitter/reply.yaml`
   - For LinkedIn posts: read `prompts/marketing/linkedin/post.yaml`
   - For Reddit comments: read `prompts/marketing/reddit/comment.yaml`

3. **Generate content:**
   - Use the `system` prompt from the YAML template as context
   - Fill in the `user` template variables:
     - `mention_rate`: from brand.yaml (Twitter 20%, LinkedIn 30%, Reddit 10%)
     - `should_mention`: randomly true/false based on mention_rate
     - `topic`, `context`, `count`: based on CEO's input
   - Generate content following the template's format rules

4. **Validate output:**
   - Check character limits (Twitter: 280/tweet, LinkedIn: 1000/post)
   - Verify mention_rate compliance
   - Ensure voice matches platform (check against brand.yaml → never_say list)
   - Verify JSON format is correct

### Anti-Patterns
- ❌ Publishing without CEO review — ALWAYS get approval
- ❌ Same content across platforms — each platform has its own voice
- ❌ Exceeding mention_rate — trust > awareness
- ❌ Generic content that could come from any brand

---

## Phase 2: REVIEW — CEO Approval (HARD_GATE)

> **Output:** Approved content batch
> **Gate:** HARD — CEO must approve every post before publishing

### Actions

1. Present generated content to CEO in readable format
2. For each piece of content, show:
   - Platform target
   - Content text (formatted)
   - Mention status (yes/no + which product)
   - Character count
3. CEO can: ✅ Approve, ✏️ Edit, ❌ Reject individual items
4. Loop: regenerate rejected items with CEO feedback

### Rules
- 🔴 **NEVER skip this gate.** Every post goes through CEO review.
- CEO can adjust voice, tone, or content before publishing.
- If CEO rejects >50% of batch → re-read the prompt template and adjust.

---

## Phase 3: PUBLISH — Browser Automation

> **Output:** Published posts with URLs
> **Gate:** Posts live on platforms

### Actions

1. **For each approved post, use Antigravity `browser_subagent`:**

   **Twitter/X Thread:**
   ```
   Task: Navigate to twitter.com → Click compose → Type tweet 1 → Post →
   Click "Add another tweet" → Type tweet 2 → ... → Post all
   ```

   **Twitter/X Reply:**
   ```
   Task: Navigate to the target tweet URL → Click reply → Type reply text → Post
   ```

   **LinkedIn Post:**
   ```
   Task: Navigate to linkedin.com/feed → Click "Start a post" → Type post →
   Add hashtags → Post
   ```

   **Reddit Comment:**
   ```
   Task: Navigate to the target post URL → Click comment box → Type comment → Submit
   ```

2. After each post, capture the posted URL (from browser URL bar or post link)

3. Wait 2-5 minutes between posts on the same platform (avoid rate limiting)

### Anti-Patterns
- ❌ Posting too fast — space out posts (2-5 min gap minimum)
- ❌ Not capturing URLs — we need them for tracking
- ❌ Ignoring platform login state — verify login before posting
- ❌ Bulk posting (10+ posts/hour) — looks like spam

---

## Phase 4: LOG — Record Published Content

> **Output:** Updated content log
> **Gate:** All published posts recorded

### Actions

1. **Log each published post** to `output/marketing/content-log.csv`:
   ```
   Date, Platform, Type, Content_Preview, URL, Mention, Engagement_Check_Date
   ```

2. **Set engagement check date** = publish date + 3 days

3. **Update `pm/agent-notes/marketing-agent-output.md`:**
   - What was published
   - Which platforms
   - Mention rate actual vs target
   - Any issues or learnings

### Content Log Schema

```csv
Date,Platform,Type,Content_Preview,URL,Product_Mentioned,Mention_Rate_Target,Status,Engagement_Likes,Engagement_Comments,Check_Date
2026-03-19,twitter,thread,"Design systems are not about components...",https://x.com/jangtrinh/status/123,none,20%,live,,,2026-03-22
```

---

## Quick Reference

### Content Generation Cheat Sheet

| Platform | Template | Mention Rate | Voice |
|----------|----------|:----------:|-------|
| Twitter Thread | `twitter/thread.yaml` | 20% | Opinionated builder |
| Twitter Reply | `twitter/reply.yaml` | 20% | Sharp, warm, direct |
| LinkedIn | `linkedin/post.yaml` | 30% | Professional founder |
| Reddit | `reddit/comment.yaml` | 10% | Helpful designer |

### Daily Publishing Targets

| Platform | Frequency | Time Investment |
|----------|-----------|:--------------:|
| Twitter | 1 thread + 5-10 replies | ~30 min |
| LinkedIn | 1 post | ~15 min |
| Reddit | 2-3 comments | ~15 min |
| **Total** | | **~1 hour/day** |

---

## Lucius Compliance

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | Content approved + platform tested + timing optimal | → Publish |
| **MEDIUM** | Content good but timing or platform choice uncertain | → Binary: A) Publish now, B) Schedule |
| **LOW** | Content quality or brand alignment concern | → Stop, revise content first |

### Anti-Patterns
- ❌ Publishing without CEO review (HARD_GATE)
- ❌ Same content across all platforms without adaptation
- ❌ Posting during low-engagement windows
