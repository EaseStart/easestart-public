---
description: Create marketing carousel slides from JSON data using HTML templates (Royal Bold style), render to 1080×1080 PNG, with scalable output structure
---

# /slides — Marketing Carousel Pipeline

> Founder gives topic → AI handles everything → ready-to-post slides

> **Lucius:** L2 (Phase→Artifact→Gate) · L5 (confidence check before publish)
> **Owner:** marketing-agent · **LOTUS:** Tag output with layer + ion_id

// turbo-all

## Phase 0: Discovery (Socratic Gate)

**Trigger:** Founder says anything like "tạo carousel", "make slides", "marketing content về..."

**AI MUST ask these questions before proceeding:**

### Required Questions

1. **Topic/Angle:** "Nội dung chính là gì? (topic, insight, framework, tip list...)"
2. **Platform:** "Post ở đâu?"
   - Instagram carousel (1080×1080, 5-10 slides)
   - LinkedIn document post (1080×1080, 5-15 slides)
   - Both (same format)
3. **Style:** "Dùng style nào?"
   - `royal-bold` — Playfair Display serif, off-white bg, dark blue accents ✅ Ready
   - _(more styles to come)_
4. **Tone:** "Tone nào?" (auto-inferred from platform)
   - Instagram → Visual-first educator (from `brand.yaml → voice.per_platform`)
   - LinkedIn → Professional founder sharing real insights
5. **Slide count:** "Bao nhiêu slides?" (default: 5 — cover + 3 content + CTA)

### Optional (ask if unclear)

- Target audience, CTA goal, key insight

**Gate:** Do NOT proceed until founder confirms topic + platform + style.

---

## Phase 1: Content Generation

### Step 1a: Load Brand Context

Before writing ANY content, load these references:

```
MUST READ:
  prompts/marketing/brand.yaml         → Founder persona, voice DNA, credentials
  prompts/marketing/visual-styles.yaml  → Design tokens for chosen style

PLATFORM-SPECIFIC:
  prompts/marketing/instagram/carousel.yaml  → If Instagram
  prompts/marketing/linkedin/post.yaml       → If LinkedIn (for caption writing)
```

Key rules from `brand.yaml`:
- **Numbers over adjectives**: "172 signups in 3 days" > "amazing traction"
- **Frameworks over advice**: "Here's the framework" > "You should..."
- **Sentence style**: "Short. Punchy. Breathe. Then detail."
- **Mention strategy**: Only ~20% of posts mention EaseUI. Never an ad.
- **NEVER use**: "Excited to announce", "Game-changer", "Thoughts?", generic motivation

### Step 1b: Generate Slides Content

Use `instagram/carousel.yaml` system prompt as content guidelines, then map to template JSON:

| Carousel Prompt Output | → Maps to Template |
|------------------------|--------------------|
| `cover.heading` | `cover` → `hero-title` |
| `cover.subtitle` | `cover` → `intro-text` |
| `slides[].heading` | `content` → `section-heading` |
| `slides[].body` | `content` → `body-content` |
| Final slide | `cta` → `cta-heading` |
| `caption` | Save for posting (not rendered) |
| `hashtags` | Save for posting (not rendered) |

### Step 1c: Write slides.json

```json
[
  {
    "template": "cover",
    "data": {
      "intro-text": "Subtitle (who is this for)",
      "hero-title": "Main <span class='highlight'>key</span> title",
      "author-name": "Jang Trịnh"
    }
  },
  {
    "template": "content",
    "data": {
      "number-tag": "#1",
      "section-heading": "One clear takeaway",
      "body-content": "<p class='t-body'>Explanation text.</p>",
      "prompt-wrap": true,
      "prompt-label": "Try this:",
      "prompt-text": "Actionable prompt"
    }
  },
  {
    "template": "bridge",
    "data": {
      "large-statement": "Big <span class='highlight'>statement</span>",
      "illustration-img": "illustration-topic.png",
      "body-text": "Supporting line"
    }
  },
  {
    "template": "cta",
    "data": {
      "cta-heading": "Found this useful?",
      "cta-author": "Jang Trịnh",
      "cta-caption": "Follow for daily insights →"
    }
  }
]
```

### Also generate: Post metadata

```json
{
  "caption": "Instagram/LinkedIn caption (100-300 chars)",
  "hashtags": ["designsystems", "uidesign", "productdesign"],
  "mention_easeui": false,
  "platform": "instagram"
}
```

Save both to `/tmp/{slug}-slides.json` and `/tmp/{slug}-meta.json`.

---

## Phase 2: Illustrations (Optional)

If any slide uses `bridge` template, generate illustration.

### Method 1: Antigravity `generate_image` (PREFERRED ✅)

> **Use this first!** Built into Antigravity subscription — $0 extra cost, no API key needed.

Call the `generate_image` tool with this prompt pattern for royal-bold style:

```
Prompt: "Hand-drawn illustration of [TOPIC], two-tone blue (#1900AC) outlines
and green (#00D47E) fills, white background, simple line art style, very few
elements, clean and minimal, large centered, filling 80% of canvas"

ImageName: "illustration_[slug]"
```

Then copy the generated artifact image to the template folder:

```bash
cp /path/to/generated/image.png \
   easestart/templates/marketing/royal-bold/illustration-[slug].png
```

### Method 2: Gemini API (Fallback)

Only use if Antigravity `generate_image` is unavailable or result is unsatisfactory.

```bash
cd /Users/jang/Desktop/Jang
python3 .agent/skills/ai-multimodal/scripts/gemini_batch_process.py \
  --task generate \
  --prompt "Hand-drawn illustration of [TOPIC], two-tone blue (#1900AC) outlines and green (#00D47E) fills, white background, simple line art style, very few elements, clean and minimal, large centered, filling 80% of canvas" \
  --model imagen-4.0-generate-001 \
  --aspect-ratio 1:1 \
  --output easestart/templates/marketing/royal-bold/illustration-[slug].png
```

### Image Generation Model Guide

| Model | Provider | Cost | Best For |
|-------|----------|------|----------|
| `generate_image` (Antigravity) | Built-in | **$0 (included)** | ✅ Default for all illustrations |
| `imagen-4.0-generate-001` | Google API | Free tier | Production quality, fallback |
| `imagen-4.0-ultra-generate-001` | Google API | Paid | Ultra quality when needed |
| `gemini-2.5-flash-image` | Google API | Free 500/day | Quick drafts |
| `gemini-3-pro-image-preview` | Google API | ~$0.13/img | Text in images, 4K (Nano Banana Pro) |
| `gemini-3.1-flash-image` | Google API | TBD | Nano Banana 2 (not yet available) |

> 🔴 **Priority:** Antigravity built-in → Imagen 4 free → Flash Image → Paid models

### Illustration Quality Rules

| Rule | Why |
|------|-----|
| "very few elements, clean and minimal" | Prevents over-detailed cluttered illustrations |
| "large centered, filling 80% of canvas" | Prevents tiny illustrations with excess whitespace |
| Keep two-tone blue + green fills | This is the royal-bold brand style. Don't deviate. |
| "simple line art style" | Matches the hand-drawn aesthetic of reference PDFs |

> **If illustration looks too detailed or busy:** Re-generate with "fewer elements" and "bolder strokes" in prompt. Less is more.

### Post-Processing

Remove white background for clean compositing:

```bash
cd /Users/jang/Desktop/Jang/easestart
python3 scripts/remove_bg.py \
  templates/marketing/royal-bold/illustration-[slug].png \
  templates/marketing/royal-bold/illustration-[slug].png \
  --white-bg --composite
```

For product photos/mockups with shadows:

```bash
python3 scripts/remove_bg.py photo.png photo-clean.png --extract-shadow
# → photo-clean.png (subject) + photo-clean-shadow.png (shadow layer)
```

> **Modes:** `--white-bg` (threshold, best for illustrations) vs AI (default, best for photos).
> render.py auto-removes white bg when `"remove-bg": true` in slides.json.

---

## Phase 3: Render

```bash
cd /Users/jang/Desktop/Jang/easestart
python3 scripts/render.py --slides /tmp/{slug}-slides.json --slug {slug}
```

**Output structure:**
```
output/marketing/carousels/{date}-{slug}/
  slides.json       ← input copy (reproducibility)
  metadata.json     ← style, date, slug, file list
  slide_01_cover.png ... slide_NN_cta.png
```

---

## Phase 4: Review & Iterate

1. Show all rendered slides to founder
2. Ask: "Có cần chỉnh gì không?"
3. When approved:
   - Confirm output path for download
   - Share caption + hashtags for posting
   - Remind: log to `output/marketing/content-log.csv` for tracking

---

## Content Rules (from brand.yaml)

### Writing DNA

| Rule | Example |
|------|---------|
| Numbers > adjectives | "172 signups in 3 days" not "amazing traction" |
| Frameworks > advice | "Here's the 3-step framework" not "You should..." |
| Short sentences | "Short. Punchy. Breathe. Then detail." |
| Show don't tell | Screenshots, metrics, demos > promises |
| 0-1 emoji per slide | Never forced, only when natural |

### Content Domains

From `brand.yaml → content_pillars`:
- Design Systems & Design Tokens
- AI in Design (EaseUI's space)
- UX Patterns backed by data
- Build-in-Public (metrics, decisions, trade-offs)
- Career advice for designers
- Engineering for designers

### Mention Strategy

- Only ~20% of carousels mention EaseUI/EaseStart
- When mentioning: "Built with learnings from EaseUI" — always natural
- NEVER: "Check out", "Try our tool", "Sign up" — never ad copy

---

## Files & Cross-References

| What | Path | Purpose |
|------|------|---------|
| **Brand identity** | `prompts/marketing/brand.yaml` | Founder persona, voice, credentials |
| **Instagram prompt** | `prompts/marketing/instagram/carousel.yaml` | Content generation guidelines |
| **LinkedIn prompt** | `prompts/marketing/linkedin/post.yaml` | Caption/post voice |
| **Visual styles** | `prompts/marketing/visual-styles.yaml` | Design tokens per style |
| **Templates** | `templates/marketing/royal-bold/` | HTML/CSS implementation |
| **Render script** | `scripts/render.py` | Playwright renderer |
| **Output** | `output/marketing/carousels/{date}-{slug}/` | Rendered slides |
| **Content log** | `output/marketing/content-log.csv` | Publishing tracker |
| **Marketing data** | `data/marketing/` | Channels, content playbook, growth tactics |

---

## Available Templates

| Template | Purpose | Key Fields | ⚠️ Notes |
|----------|---------|------------|----------|
| `cover` | Hero opening | `intro-text`, `hero-title`, `author-name` | Title 120px for long text. Use `<span class='highlight'>` for keyword. |
| `content` | Numbered content | `number-tag`, `section-heading`, `body-content` | Max ~8 body lines. Use `<br>` in prompt-text. **No emoji.** |
| `bridge` | Illustration divider | `large-statement`, `illustration-img`, `body-text` | Illustration must be two-tone royal-bold style. Place max 2 content slides between bridges. |
| `cta` | Call-to-action | `cta-heading`, `cta-author`, `cta-caption` | Heading 88px. Use `<br>` to separate title and tagline in caption. |

## Design System (Royal Bold)

| Token | Value |
|-------|-------|
| Canvas | 1080×1080px |
| Padding | 120px |
| Background | #FFFBF8 |
| Primary | #1900AC |
| Body text | 32px, SF Pro Rounded / Inter |
| Cover title | 120px Playfair Display (was 155px — too large for long titles) |
| Section heading | 72px |
| CTA heading | 88px (was 120px — too large for multi-word metrics) |
| Illustration heading | 96px |
| Highlight | #FFD254, marker-underline 35% |
| Bridge illustration | `flex: 0 0 50%` — fills top half, image at `max: 95%` |

---

## Quality Rules — Lessons Learned

> 🔴 **MANDATORY.** These rules come from real production feedback. Violating them = rejected slides.

### 1. No Emoji. Ever.

Emoji look cheap and unprofessional in carousel slides. Use text characters instead.

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| 🟢 Safe → auto-publish | `•` Safe → auto-publish |
| 💡 Key insight | Styled callout box (no emoji) |
| 🔥 Hot take | Bold text or highlight span |

Also: Remove default `💡` from `content.html` callout template.

### 2. Content Overflow Prevention

Each slide is 1080×1080px with 120px padding. Content MUST fit without overflow.

| Element | Max safe lines |
|---------|---------------|
| Heading (72px) | 2 lines max |
| Body text (32px) | ~8-10 lines |
| Heading + body + prompt card | Total must fit in ~840px height |

**Rules:**
- 4+ bullet points → merge into a compact paragraph
- Body text + bullet list + prompt card = almost always overflow → cut one
- Always preview rendered PNG before delivering

### 3. Visual Rhythm — Break Monotony

Never stack 3+ content slides in a row. Use bridge slides as visual breakers.

| ❌ Bad flow | ✅ Good flow |
|-----------|------------|
| Cover → Content × 5 → CTA | Cover → Content × 2 → **Bridge** → Content → **Bridge** → Content → **Bridge** → CTA |
| 7 text-heavy slides in a row | Alternating text + illustration |

**Target:** Max 2 consecutive content slides before a bridge.

### 4. HTML Line Breaks in JSON

`\n` does NOT work in HTML rendering. Always use `<br>` for line breaks in:

| Field | Use `<br>` |
|-------|-----------|
| `prompt-text` | Between each question/statement |
| `cta-caption` | Between title and tagline |
| `body-content` | Between bullet items (use `<br>` inside `<p>`) |

### 5. Illustration Style Discipline

All illustrations MUST follow the royal-bold two-tone style. No exceptions.

| ✅ Correct | ❌ Wrong |
|-----------|---------|
| Blue (#1900AC) outlines + green (#00D47E) fills | Multi-color, rainbow, gradient |
| Simple line art, few elements | Detailed, busy, cluttered |
| Clean hand-drawn aesthetic | Realistic, 3D, photographic |
| Fills 80%+ of canvas | Tiny icon lost in whitespace |

**Prompt template:**
```
"Hand-drawn illustration of [TOPIC], two-tone blue (#1900AC) outlines
and green (#00D47E) fills, white background, simple line art style,
very few elements, clean and minimal, large centered, filling 80% of canvas"
```

**If result is too busy:** Add "fewer elements" and "bolder strokes".
**If result is too small:** Add "filling 90% of canvas" and "zoomed in".

### 6. Font Size Calibration

Text size must match content length. Long text at large sizes = overflow.

| Element | Short text (≤3 words) | Long text (4+ words) |
|---------|----------------------|---------------------|
| Cover title | 155px OK | **120px** (reduced) |
| CTA heading | 120px OK | **88px** (reduced) |
| Bridge statement | 96px OK | 80px if 3+ lines |


---

## Lucius Compliance

### Phase → Artifact → Gate Mapping

| Phase | Steps | Artifact | Gate |
|:-----:|-------|----------|------|
| **0** Discovery | Socratic questions | Clarity on topic + audience | Founder approves direction |
| **1** Content | Brand load → generate → JSON | `slides.json` | JSON validates, content matches brand voice |
| **2** Illustrations | Image generation + processing | PNG illustrations | Visual quality check |
| **3** Render | HTML → PNG pipeline | `output/*.png` files | All slides render at 1080×1080 |
| **4** Review | CEO review + iterate | Approved carousel set | CEO approves for publishing |

### L5 Confidence Protocol

| Confidence | Score | Decision |
|:----------:|:-----:|----------|
| **HIGH** | Brand alignment ✅ + visuals ✅ + JSON valid ✅ | → Proceed to render autonomously |
| **MEDIUM** | 1 concern (e.g. illustration quality) | → Binary choice: A) Publish as-is, B) Regenerate weak slide |
| **LOW** | Brand voice mismatch or wrong audience | → Stop, re-run Phase 0 Socratic gate |

### Anti-Patterns
- ❌ Skipping Phase 0 Socratic gate — content without audience clarity = wasted slides
- ❌ Using placeholder images — every slide must have real illustrations
- ❌ Publishing without CEO review (Phase 4 is HARD_GATE)
- ❌ More than 10 slides per carousel — attention drops after 7-8
