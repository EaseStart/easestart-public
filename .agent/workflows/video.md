---
description: End-to-end AI video production — cinematic storyboard, multi-clip generation (Veo 3 / Seedance 2.0), stitching, and platform-ready export.
---

# /video — AI Video Production Pipeline

> Founder gives concept → AI scripts shots → generates clips → stitches → ready-to-post video

> **Lucius:** L2 (Phase→Artifact→Gate) · L5 (confidence check before publish)
> **Owner:** marketing-agent · **LOTUS:** Tag output with layer + ion_id

// turbo-all

---

## Phase 0: Discovery (Socratic Gate)

> Output: `brief.md` (concept, platform, style, duration, references)
> Gate: Founder confirms brief before storyboard begins

**Trigger:** Founder says "tạo video", "make teaser", "video cho...", "reel about..."

**AI MUST ask these questions before proceeding:**

1. **Subject:** "Video về cái gì? (product, feature, concept, announcement)"
2. **Platform:** "Post ở đâu?"
   - Instagram Reel (9:16, 15-30s)
   - LinkedIn (16:9, 15-30s)
   - TikTok (9:16, 15-60s)
   - Twitter/X (16:9, 6-15s)
   - YouTube Shorts (9:16, <60s)
3. **Style/Mood:** "Tone nào?"
   - Cinematic epic (Villeneuve, blockbuster)
   - Tech thriller (Mr. Robot, cyber)
   - Clean minimal (Apple, MUJI)
   - Motion graphics (animated, dynamic)
   - Brand-matched (follow existing slides/design system)
4. **Duration:** "Bao lâu?" (default: 24s = 3 clips × 8s)
5. **Reference:** "Có visual reference không?" (existing slides, illustrations, brand assets)

### Anti-Patterns (Lucius L4)
- ❌ Generating video before confirming platform + format specs
- ❌ Skipping style discussion — one-line generic prompt guarantees mediocre output
- ❌ Assuming duration without checking platform sweet spot
- ❌ Ignoring existing brand assets as reference frames

---

## Phase 1: Storyboard Design

> Output: `storyboard.json` (beat outline + cinematic prompts per clip)
> Skills: `@[skills/video-production]` → Cinematic Prompt Engineering section
> Gate: Founder approves storyboard before generation begins

### 1.1 Write Beat Outline

Map the video narrative arc (minimum 2 clips, maximum 5):

```
Clip 1 (8s): HOOK — What grabs attention? (Problem/tension/question)
Clip 2 (8s): REVEAL — What's the answer? (Product/solution appears)
Clip 3 (8s): SHOWCASE — Why it matters? (System in action, key feature)
Clip 4 (8s): CTA — What do they do next? (Brand resolve, call to action)
```

### 1.2 Write Cinematic Prompts

For EACH clip, write a prompt following this MANDATORY structure:

```
[Film Style]: [genre], [camera type], [color grade], [grain/texture]
[Duration]: 8s
[Script]:

[00:00-00:03] Shot 1: [Camera Angle]. [Subject]. [Action]. [Lighting].
[00:03-00:06] Shot 2: [Camera Angle]. [Transition]. [New subject]. [Environment].
[00:06-00:08] Shot 3: [Camera Angle]. [Visual climax]. [Emotion/reveal].

[Technical Parameters]: [lens], [DOF], [motion blur], [color palette]
```

### 1.3 Save Storyboard

```bash
mkdir -p easestart/output/marketing/video/[slug]
cat > easestart/output/marketing/video/[slug]/storyboard.json << 'EOF'
{
  "project": "[project-name]",
  "platform": "[instagram-reel|linkedin|tiktok]",
  "style": "[style description]",
  "total_duration": "24s",
  "clips": [
    {
      "id": 1,
      "beat": "hook",
      "duration": "8s",
      "prompt": "[full cinematic prompt for clip 1]"
    }
  ]
}
EOF
```

### Anti-Patterns (Lucius L4)
- ❌ Writing generic one-line prompts instead of shot-by-shot scripts
- ❌ Skipping camera angle, lens, and lighting specs
- ❌ Starting generation without founder reviewing storyboard
- ❌ More than 5 clips without strong justification (attention drops)

### Confidence Gate (Lucius L5)
| Signal | Action |
|--------|--------|
| Founder says "looks good" / "LGTM" | ✅ HIGH — proceed to Phase 2 |
| Founder has questions about style/angle | ⁉️ MEDIUM — revise storyboard, re-present |
| Founder unsure about concept | ⚠️ LOW — go back to Phase 0 |

---

## Phase 2: Generate Clips

> Output: `clip_01_hook.mp4`, `clip_02_reveal.mp4`, ... (individual clips)
> Skills: `@[skills/ai-multimodal]` → Video generation
> Gate: Each clip passes visual quality check before stitching

### Option A: Veo 3 (Primary — API access)

```bash
cd /Users/jang/Desktop/Jang

# Generate each clip from storyboard
python3 .agent/skills/ai-multimodal/scripts/gemini_batch_process.py \
  --task generate-video \
  --prompt "[cinematic prompt from storyboard]" \
  --output easestart/output/marketing/video/[slug]/clip_01_hook.mp4

# Repeat for each clip in storyboard...
```

### Option B: Image-to-Video (Best for Style Consistency)

Use existing carousel slides or illustrations as reference frames:

> [!CAUTION]
> **Use `--reference-images`, NOT `--files`!** This is the #1 gotcha.
> Also: Veo 3 only supports `9:16` and `16:9` (no `1:1`). Crop after with ffmpeg.

```bash
# Step 1: Preprocess square slide → Veo-compatible aspect ratio
# (Pad with brand bg color so Veo doesn't hallucinate in margins)
ffmpeg -i slide_1080x1080.png \
  -vf "pad=1080:1920:0:(oh-ih)/2:color=#FFFBF8" \
  ref_9x16.png

# Step 2: Generate reference frame if no slide exists
python3 .agent/skills/ai-multimodal/scripts/gemini_batch_process.py \
  --task generate \
  --prompt "[scene description matching brand style]" \
  --model imagen-4.0-generate-001 \
  --output ref_frame.png

# Step 3: Animate reference frame (CORRECT way)
python3 .agent/skills/ai-multimodal/scripts/gemini_batch_process.py \
  --task generate-video \
  --reference-images ref_9x16.png \
  --prompt "Animate this illustration. Elements gently move, parallax depth..." \
  --aspect-ratio 9:16 \
  --output clip_animated.mp4

# Step 4: Crop back to 1:1 if needed (Instagram feed)
ffmpeg -i clip_animated.mp4 -vf "crop=1080:1080:0:420" -c:a copy clip_square.mp4
```

### Option C: Seedance 2.0 (Premium — manual upload)

1. Go to [Dreamina](https://dreamina.capcut.com/) or [kie.ai](https://kie.ai)
2. Paste cinematic prompt from storyboard
3. Upload reference image if using image-to-video
4. Download generated clip
5. Save to `easestart/output/marketing/video/[slug]/`

### Option D: ffmpeg Slideshow (Deterministic — from existing slides)

Best when you already have carousel slides and want guaranteed brand consistency:

```bash
# 7 slides → ~21s video with transitions
ffmpeg -y \
  -loop 1 -t 4 -i slide_01.png \
  -loop 1 -t 3 -i slide_02.png \
  ... (all slides) ... \
  -filter_complex "\
[0:v]scale=1080:1080,format=yuv420p[v0]; ... \
[v0][v1]xfade=transition=fadeslow:duration=1.0:offset=3.0[t01]; ... \
" -map "[vfinal]" -c:v libx264 -pix_fmt yuv420p -r 24 slideshow.mp4
```

> **Hybrid tip:** Use ffmpeg for text slides + Veo 3 `--reference-images` for illustration slides + screen recording for UI demos → stitch together.

### Option E: Screen Recording (Dia / Playwright — for UI Demos)

> [!IMPORTANT]
> **Rule: Real UI > AI-generated UI.** Always use actual app recordings for product demos. AI-generated dashboards look fake and reduce credibility.

```bash
# If Dia recording exists, trim to desired duration
ffmpeg -y -i Dia.mp4 -t 15 -vf "fps=24" -c:v libx264 -pix_fmt yuv420p -r 24 -an clip_demo.mp4
```

### Per-Clip Quality Check

Before advancing to Phase 3, each clip must pass:

- [ ] No morphing/melting artifacts
- [ ] Camera movement matches prompt direction
- [ ] Color palette consistent with brief
- [ ] No text garbling (if slide has text, use ffmpeg NOT Veo 3)
- [ ] Duration matches storyboard beat timing

> If a clip fails → re-generate with refined prompt. Max 3 retries per clip before escalating to founder for style decision.

### Anti-Patterns (Lucius L4)
- ❌ Stitching clips that have visible AI artifacts ("good enough" mindset)
- ❌ Using different film styles across clips (breaks visual coherence)
- ❌ Generating all clips before reviewing clip 1 (waste if style is wrong)
- ❌ Ignoring audio quality (Veo 3 generates audio — review it)
- ❌ Using `--files` instead of `--reference-images` for Veo 3 image-to-video
- ❌ Using `gemini` CLI for video generation (no native support, hangs)
- ❌ Requesting 1:1 aspect ratio from Veo 3 (only 9:16, 16:9 supported)
- ❌ **Using Veo 3 i2v on text-heavy slides** (AI garbles fonts — always static ffmpeg)
- ❌ **AI-generated UI mockups for demos** (use real screen recording — Dia/Playwright)

---

## Phase 3: Stitch & Post-Process

> Output: `final.mp4` (platform-ready video)
> Gate: Final video matches platform specs + passes full quality checklist

### 3.1 Concatenate Clips

```bash
cd easestart/output/marketing/video/[slug]

# Create clip list
ls clip_*.mp4 | sort | sed 's/^/file /' > clips.txt

# Simple concat (same codec)
ffmpeg -f concat -safe 0 -i clips.txt -c copy stitched.mp4
```

### 3.2 Add Transitions

> **RULE: Use `fadeslow` for everything.** It's smooth, professional, and Framer Motion-like.
> Cheesy transitions (`radial`, `wipeleft`, `circleopen`, `pixelize`) look like PowerPoint 2003.

```bash
# Multi-clip stitch with fadeslow (1.0-1.5s per transition)
ffmpeg -y \
  -i clip_01.mp4 -i clip_02.mp4 -i clip_03.mp4 -i clip_04.mp4 \
  -filter_complex "\
[0:v]scale=1920:1080,format=yuv420p,fps=24[v0];\
[1:v]scale=1920:1080,format=yuv420p,fps=24[v1];\
[2:v]scale=1920:1080,format=yuv420p,fps=24[v2];\
[3:v]scale=1920:1080,format=yuv420p,fps=24[v3];\
[v0][v1]xfade=transition=fadeslow:duration=1.5:offset=OFFSET1[t01];\
[t01][v2]xfade=transition=fadeslow:duration=1.5:offset=OFFSET2[t02];\
[t02][v3]xfade=transition=fadeslow:duration=1.2:offset=OFFSET3[vfinal]" \
  -map "[vfinal]" -c:v libx264 -pix_fmt yuv420p -r 24 -an stitched_no_audio.mp4
```

**Offset formula:**
```
offset_1 = clip1_duration - transition_duration
offset_2 = offset_1 + clip2_duration - transition_duration
offset_N = offset_(N-1) + clipN_duration - transition_duration
```

### 3.3 Generate Voiceover (Gemini TTS)

```bash
python3 -c "
from google import genai
from google.genai import types
import os
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
response = client.models.generate_content(
    model='gemini-2.5-flash-preview-tts',
    contents='[voiceover script ~75 words for 30s]',
    config=types.GenerateContentConfig(
        response_modalities=['AUDIO'],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Kore')
            )
        )
    )
)
for part in response.candidates[0].content.parts:
    if part.inline_data and part.inline_data.mime_type.startswith('audio'):
        with open('voiceover.wav', 'wb') as f:
            f.write(part.inline_data.data)
        break
"
ffmpeg -y -f s16le -ar 24000 -ac 1 -i voiceover.wav -c:a pcm_s16le voiceover_proper.wav
```

> **Critical:** TTS model = `gemini-2.5-flash-preview-tts` (NOT `gemini-2.5-flash`). Output is raw PCM → convert to WAV.
> **Script length:** ~75 words → ~30s. Never speed up TTS — re-write shorter script instead.

### 3.4 Generate Background Music (Veo 3)

```bash
python3 .agent/skills/ai-multimodal/scripts/gemini_batch_process.py \
  --task generate-video \
  --prompt "Ambient electronic music, minimal beats, warm synth pads" \
  --aspect-ratio 16:9 --output bgm_raw.mp4
ffmpeg -i bgm_raw.mp4 -vn -c:a aac bgm.m4a
```

### 3.5 Mix Audio

```bash
ffmpeg -y \
  -i stitched_no_audio.mp4 \
  -i voiceover_proper.wav \
  -stream_loop 4 -i bgm.m4a \
  -filter_complex "\
[1:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[vo];\
[2:a]volume=0.15[bg];\
[vo][bg]amix=inputs=2:duration=shortest:normalize=0[aout]" \
  -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k -shortest final.mp4
```

> **BGM volume:** 0.10-0.15 with voiceover, 0.25-0.35 music-only.

### 3.6 Format for Platform

```bash
# Landscape → Vertical (9:16) with blurred bg
ffmpeg -i final.mp4 \
  -vf "split[bg][fg];[bg]scale=1080:1920,boxblur=20[bg];[fg]scale=1080:-1[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" \
  -c:a copy reel.mp4

# Square (1:1)
ffmpeg -i final.mp4 -vf "crop=ih:ih" -c:a copy square.mp4
```

### Anti-Patterns (Lucius L4)
- ❌ Publishing without platform-specific resize
- ❌ Using cheesy transitions (`radial`, `wipeleft`, `circleopen`) — use `fadeslow`
- ❌ Music louder than voiceover (BGM ≤ 15% volume)
- ❌ Speeding up TTS voiceover — sounds robotic, re-write shorter script instead
- ❌ Skipping final preview — always watch the full video before declaring done
- ❌ Using `gemini-2.5-flash` for TTS (wrong model, returns text only)

---

## Phase 4: Quality Review & Publish

> Output: Published video + `metadata.json`
> Gate: Full checklist passes + founder approval

### Quality Checklist

- [ ] **No artifacts**: No morphing, extra limbs, melting objects
- [ ] **Style consistent**: Colors match brand palette across all clips
- [ ] **Pacing natural**: Cuts every 2-4s, no static holds >3s
- [ ] **Audio clean**: No jarring transitions, appropriate for platform
- [ ] **Resolution correct**: Matches target platform (see table)
- [ ] **Brand aligned**: Fonts/colors match design system if text overlaid
- [ ] **No dead frames**: Clean start, clean end
- [ ] **Duration target**: Within platform sweet spot

### Platform Specs Reference

| Platform | Format | Duration | Resolution |
|----------|--------|----------|------------|
| Instagram Reel | 9:16 | 15-30s | 1080×1920 |
| TikTok | 9:16 | 15-60s | 1080×1920 |
| LinkedIn | 16:9 | 15-30s | 1920×1080 |
| YouTube Shorts | 9:16 | <60s | 1080×1920 |
| Twitter/X | 16:9 | 6-15s | 1920×1080 |

### Fix Common Issues

```bash
# Remove garbled audio
ffmpeg -i input.mp4 -an -c:v copy silent.mp4

# Speed up slow sections (1.5x)
ffmpeg -i input.mp4 -filter:v "setpts=0.67*PTS" -filter:a "atempo=1.5" faster.mp4

# Add text overlay (post-production)
ffmpeg -i input.mp4 \
  -vf "drawtext=text='Product Name':fontsize=48:fontcolor=white:x=(w-tw)/2:y=h-100" \
  output.mp4
```

### Confidence Gate (Lucius L5)
| Signal | Action |
|--------|--------|
| All checklist passes + founder says ship | ✅ HIGH — Publish |
| 1-2 minor issues (audio, trim) | ⁉️ MEDIUM — Quick fix, re-review |
| Fundamental style mismatch | ⚠️ LOW — Return to Phase 1 (new storyboard) |

### Anti-Patterns (Lucius L4)
- ❌ Publishing without watching the full video at least once
- ❌ Claiming "done" without running quality checklist
- ❌ Posting same format across all platforms (resize per platform)
- ❌ No metadata.json saved (breaks reproducibility)

---

## Output Structure

```
easestart/output/marketing/video/[slug]/
├── brief.md                  # Phase 0: concept + platform + style
├── storyboard.json           # Phase 1: beat outline + cinematic prompts
├── clip_01_hook.mp4           # Phase 2: individual clips
├── clip_02_reveal.mp4
├── clip_03_showcase.mp4
├── clip_04_cta.mp4
├── stitched.mp4               # Phase 3: raw concat
├── final.mp4                  # Phase 3: with transitions + music
├── reel-9x16.mp4              # Phase 3: platform-formatted
└── metadata.json              # Phase 4: generation metadata
```
