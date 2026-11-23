---
name: "aipm-concept-walkthrough-reel"
description: "Build an AI Product Simplified concept-walkthrough reel: Ben Meer-style gold-ball motion on black with a real product screen recording composited in, the user's own voiceover and a soft music bed. Use for aipm.decoded reels that teach one AI concept by showing it."
---

# AI Product Simplified — concept-walkthrough reel

Makes a 1080x1920 / 30fps vertical reel that teaches ONE AI concept with moving gold balls on black (Ben Meer style) and a real product screen recording composited into a gold frame. Second format alongside the kinetic-caption explainer. Everything is built in the cloud workspace with a canvas film + Playwright + ffmpeg; the only thing the user supplies is a voiceover recording and a raw screen recording.

## 0. Read first (content rules live in the project)
This is a build recipe, not a content brief. Before scripting, read the project docs: `instagram-playbook.md` (hook, length, CTA, weekly plan), `reel-learnings.md` (what's working + the "Concept-walkthrough production" notes), and `brand-end-card.md`. The playbook and learnings decide the idea, hook and length; this skill decides how it's built.

## 1. Concept + beats
- One idea, puzzle to payoff: open on a contradiction, resolve it at the end with the SAME visual element (e.g. a ball that misses a ring early lands in it at the end — the reel rhymes).
- Map each idea to a ball behaviour: a ball drops in = the thing; balls scatter with motion-blur trails = chaos/volume; a ball overshoots a ring = a miss/wrong; balls drop into a frame = inputs; a ball tethered by dotted lines = cited/linked; a ball lands in a ring = success.
- Write the beat list and get the user's OK before animating.

## 2. Visual language
- Pure black. Gold balls are the actors. Motion-blur trails on anything moving (draw fading echoes along the position function). Dotted lines for paths/tethers.
- Text is minimal: 3-4 word UPPERCASE lines split top and bottom, calm. The balls carry the story.
- Brand: gold #FFD36B, Inter, one display face. (Avoid drifting to other golds/fonts.) One accent only.
- Study any reference reel IN MOTION — sample many frames across its loop, never judge from one frozen frame.

## 3. Build the film (frame-exact, re-renderable)
- Author one self-contained HTML canvas whose every frame is a pure function of time: `window.seek(t)` paints frame t (no rAF/timeouts/state in render mode; seeded noise only). A silent scrub UI for preview is fine behind a `?render` gate.
- Leave the gold clip frames EMPTY in the film (just the gold border); the real clips are overlaid later, so you don't need placeholder UI inside them.
- Render headless: Playwright opens the page with `?render`, loops frames calling `window.seek(t)`, screenshots the 1080x1920 canvas to JPEGs; `ffmpeg -framerate 30 ... -crf 18` encodes `base.mp4`. (Playwright lives at /opt/npm-tools/node_modules — set `NODE_PATH`.)

## 4. Voiceover (user's own voice) + sync
- Give the user ~6 short lines to read with ~1s gaps between lines. Their own voice reads warmer than TTS.
- Find line boundaries with `ffprobe` duration + `ffmpeg silencedetect` (gaps >~0.8s = line breaks). Map each visual beat onto its line's time window (a piecewise time remap from visual-time to audio-time). Forced-alignment model downloads are blocked in the sandbox; silence mapping is accurate enough for a calm read.

## 5. Music bed (optional, if approved)
- Synthesize a soft pad (numpy) ~ the reel length. Mix low under the voice with ffmpeg `sidechaincompress` (music keyed by the voice so it ducks when they speak) -> `amix normalize=0` -> `loudnorm I=-14:TP=-1`. Keep the voice clearly on top.

## 6. Screen-recording privacy edit (DO THIS EVERY TIME)
- NEVER use a file-open dialog raw: it leaks the folder path (names), other files, drive and sidebar folder names, and the Google profile photo.
- To show a file being selected: blur the whole frame (`gblur=sigma~26`), overlay the SHARP crop of only the selected row back on top, add a gold highlight box on it; crop the profile photo, URL bar and path out of frame entirely.
- For an answer/result: crop to the content column only (no chrome, no avatar).
- Then extract frames across each cleaned clip start->end and SCAN for any leak before using it.

## 7. Legibility
- The screen recording is the credibility payoff and must read on a phone WITHOUT zooming. Make the on-screen frame big and crop the clip tighter so text scales up: a wide short frame for a filename, a large frame for an answer. If you have to zoom to read it, it's too small.

## 8. Composite + audio
- Prep each cleaned clip to the frame-interior size (scale + black pad, contain), stretched to its beat length.
- Overlay onto `base.mp4` with ffmpeg: `[clip]setpts=PTS+<beatStart>/TB[c]; [base][c]overlay=X:Y:enable='between(t,A,B)'`. Mux the voice+music audio, `-c:v libx264 -pix_fmt yuv420p -ar 48000 -movflags +faststart`.

## 9. Instagram safe zone + overlap check
- Keep every word and the brand card inside roughly y 250-1520 and x 120-950; the bottom ~400px and right ~130px are covered by IG's caption/handle/audio and action buttons. Verify by overlaying guide rectangles on sample frames.
- Scan every beat for overlaps: two same-gold elements touching merge into a blob (e.g. a gold X on a gold ball). Separate them with real spacing, and keep dropping balls clear of captions.

## 10. End card (non-negotiable)
- The last ~2.4s is ALWAYS the standard brand end card from `brand-end-card.md` (AI Product / Simplified, gold #FFD36B, Inter, #0B0D12 + gold grid, Follow or keyword pill). Never a reel-specific sign-off, never tease the next topic, never put the reel's metaphor on the card.

## 11. Deliver + log
- Deliver the final mp4 (confirm 1080x1920, 30fps, audio present). Draft the caption + hashtags (<=5) + pinned-comment keyword per the playbook.
- Write a per-reel doc to the project and add a review-log line to `reel-learnings.md`. Remind the user to review stats ~24h after posting and feed the lesson into the next reel.