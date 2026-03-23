---
description: "Community engagement workflow — find relevant posts, generate replies, publish via browser. $0 API cost."
---

# /marketing-engage — Community Engagement Automation

> Find relevant posts in target communities → generate authentic replies → publish via browser.
> Focus: build reputation first, brand awareness second.

---

## Overview

| Property | Value |
|----------|-------|
| **Cost** | $0 (uses Antigravity LLM + browser) |
| **Platforms** | Twitter/X, Reddit |
| **Agent** | marketing-agent |
| **Philosophy** | Help first. Build trust. Let the brand follow naturally. |

## Prerequisites

- Logged into target platforms in browser
- Read `prompts/marketing/brand.yaml` for mention strategy
- Read platform-specific reply/comment templates

---

## Phase 1: FIND — Discover Engagement Opportunities

> **Output:** List of posts worth engaging with
> **Skills:** marketing strategy
> **Gate:** Relevant posts identified

### Actions

1. **Use Antigravity `browser_subagent` to browse target communities:**

   **Twitter/X:**
   ```
   Task: Search Twitter for recent tweets about [design systems, component libraries,
   solo founder, build-in-public, React UI]. Find 5-10 tweets with good engagement
   (10+ likes) that Jang could add genuine value to. Return: author handle, tweet text,
   tweet URL, engagement count.
   ```

   **Reddit:**
   ```
   Task: Browse r/webdesign, r/SaaS, r/IndieHackers, r/reactjs. Find 3-5 posts from
   the last 48 hours asking questions or discussing topics where a senior designer/
   engineer could add value. Return: subreddit, title, post text, URL, comment count.
   ```

2. **Filter for quality:**
   - Post is asking a genuine question OR sharing a relatable experience
   - Post has enough engagement (not talking to the void)
   - Topic matches Jang's expertise (design, engineering, startups)
   - Not a rage-bait or toxic thread
   - Not already replied by competitors or obvious brand accounts

3. **Present post list to CEO** — quick triage: which ones to engage with?

### Anti-Patterns
- ❌ Engaging with every post — quality > quantity
- ❌ Engaging with controversial/toxic threads — avoid drama
- ❌ Only engaging with posts where you can plug your product — transparent

---

## Phase 2: GENERATE — Create Replies

> **Output:** Reply text for each selected post
> **Gate:** Replies generated matching platform voice

### Actions

1. **For each selected post, generate a reply:**
   - Read the appropriate template:
     - Twitter: `prompts/marketing/twitter/reply.yaml`
     - Reddit: `prompts/marketing/reddit/comment.yaml`
   - Fill in template variables:
     - `author_handle` / `subreddit`
     - `post_text` / `post_title`
     - `reply_number` / `comment_number`
     - `should_mention`: roll against mention_rate (20% Twitter, 10% Reddit)
     - `mention_rate`: from brand.yaml
   - If available, include `winning_examples` for in-context learning

2. **Quality check each reply:**
   - Addresses the specific question/topic (not generic)
   - Matches platform voice (check against template rules)
   - Character limit respected (Twitter 280, Reddit ~300 words)
   - Mention feels natural (not forced)
   - Passes the "would a real person write this?" test

### Anti-Patterns
- ❌ Generic replies like "Great point!" — zero value
- ❌ Copy-pasting same reply structure — variety is key
- ❌ Mentioning product when it doesn't fit — credibility killer

---

## Phase 3: REVIEW — CEO Approval (HARD_GATE)

> **Output:** Approved replies
> **Gate:** HARD — CEO approves each reply before posting

### Actions

1. Present each reply with context:
   ```
   Platform: Twitter/Reddit
   Original: @author — "post text..."
   Reply: "your generated reply..."
   Mention: Yes/No (which product)
   ```

2. CEO actions: ✅ Approve · ✏️ Edit · ❌ Skip

3. Track approval rate — if <50% approved, revisit prompt templates.

---

## Phase 4: ENGAGE — Post Replies via Browser

> **Output:** Published replies with tracking
> **Gate:** Replies posted and logged

### Actions

1. **For each approved reply, use `browser_subagent`:**

   **Twitter:**
   ```
   Task: Navigate to [tweet URL] → Click reply button → Type reply text →
   Click "Reply" to post. Capture the reply URL.
   ```

   **Reddit:**
   ```
   Task: Navigate to [post URL] → Scroll to comment box → Type comment →
   Click "Comment" to post. Capture the comment permalink.
   ```

2. **Spacing:** Wait 3-5 minutes between replies on the same platform.

3. **Log to `output/marketing/engagement-log.csv`:**
   ```
   Date,Platform,Type,Original_URL,Original_Author,Reply_Preview,Reply_URL,Mention,Status
   ```

---

## Engagement Cadence

| Platform | Daily Target | Time | Best Hours (UTC+7) |
|----------|:----------:|:----:|:------------------:|
| Twitter replies | 5-10 | 20 min | 8-10am, 8-10pm |
| Reddit comments | 2-3 | 15 min | 9-11am, 7-9pm |
| **Total** | | **~35 min** | |

## Winning Examples Bank

After posting, track engagement (likes, replies, retweets) and add high-performing
replies to the `winning_examples` section of future prompts. This creates a flywheel:

```
Good reply → High engagement → Added as winning example → AI learns voice → Better replies
```

Store winning examples in `output/marketing/winning-examples.json`:
```json
{
  "twitter": [
    {
      "parent_author": "designerX",
      "parent_text": "Design systems are overrated",
      "our_reply": "ngl this is a hot take but the real problem is...",
      "likes": 47,
      "retweets": 5,
      "date": "2026-03-19"
    }
  ],
  "reddit": []
}
```

---

## Lucius Compliance

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | Reply matches brand voice + adds genuine value | → Post reply |
| **MEDIUM** | Reply is on-brand but may be too promotional | → Binary: A) Post as-is, B) Soften CTA |
| **LOW** | Reply feels forced or off-topic | → Skip this post, find better opportunity |

### Anti-Patterns
- ❌ Engaging without CEO review (HARD_GATE)
- ❌ Replying to controversial topics that could damage brand
- ❌ Posting promotional replies in communities that ban self-promotion
