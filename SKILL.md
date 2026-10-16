---
name: rolvibe-launch-style
description: Rolvibe's house style for premium startup, SaaS and business launch films, measured from the user's "Claudes learning curve" reference set (ClickUp Brain, Bolt, Framer 3D, Urpal AI, Help Scout, Slack Spaceship, Nike Flyknit, Style Frames). A style layer that sits on top of /brag (brag-slim) or /katana and supplies the look, the motion rules for smooth continuous flow, a device-to-tool map for this Mac, and a measured check of the finished render. Use when the user asks for a premium or smooth launch video, a SaaS/startup promo, "make it like my learning curve videos", "rolvibe style", or runs /brag or /katana for a client or startup and wants it to look premium.
---

# Rolvibe launch style (iteration 1)

Measured on 2026-10-16 from 9 reference videos (the author's "Claudes learning curve" folder). The films belong
to their owners and are not included; on the author's machine the study (reports, contact sheets, motion
profiles) is in `~/Desktop/rolvibe/Claudes learning curve/_analysis/`.
Per-reference notes with timestamps: `references/reference-notes.md`. How to build each device on this Mac:
`references/devices-and-tools.md`. **Learn the grammar; never copy their footage, logos, wording or music.**

## 0. How this layers on the other skills

| Skill | Owns | This skill adds |
|---|---|---|
| `/brag` (on Opus 5.5 it hands off to `/brag-slim`) | product inspection, angle, hook, storyboard, build, poster, share copy | the style family, the continuity plan, devices per beat, the check targets |
| `/katana` (Higgsfield) | AI footage from a reference: hero plates, textures, morphs | which shots are worth generating and which are cheaper to build; the energy ceiling |
| `business-motion-film` | truth rules, critic loop ("Gauntlet"), quality bar, audio rules | read its `references/gauntlet.md` + `audio.md` for every client film |
| `video-style-reverse-engineer` (optional; its `study.py` is bundled in `scripts/vendor/`) | measuring new references | add new references to this skill with it (section 7) |

Flow: run /brag or /katana as usual, and at its **plan** step pick a family (section 1), write the continuity plan
(section 3) into `brag-plan.md`, and pick devices (section 4). Pass the family to brag as freeform tone, e.g.
`--tone "rolvibe dark-glow-kinetic: dark base, one accent glow, word-by-word type, tilted real UI"`.
Before delivery run the check (section 6). **/katana and every Higgsfield/Artlist/ElevenLabs generation spend
credits: show the user the planned calls and cost and wait for a go.** /brag-slim builds locally for free.

## 1. Pick one family

| Family | Use for | References | Look in one line |
|---|---|---|---|
| `dark-glow-kinetic` | SaaS feature launch, AI tools, apps | ClickUp Brain | near-black base, one accent glow rising from an edge, big centred type built word by word, alternating with tilted real UI |
| `dark-glow-kinetic-hype` | events, funding, milestones, numbers | Bolt hackathon | same base, heavy italic caps, rolling counters, warm metallic 3D accents, white flash cuts |
| `3d-product-world` | flagship launches, templates, hardware-ish software | Framer 3D, Urpal AI | Blender scene, one glowing hero object travels through every shot, glass UI pills in macro, push through the screen |
| `site-showcase` | website/landing-page launches, portfolio pieces | Help Scout, Urpal AI | the real site, scrolled and zoomed as one continuous camera move, loops end to start |
| `crafted-story` | brand films, non-SaaS businesses, anthems | Slack, Nike Flyknit, Style Frames | strong art direction: monochrome + brand accent, one continuous transformation, or a pastel 3D world |

Mixing is fine inside one film (ClickUp uses a 3D chip; Framer uses kinetic type), but the base, palette and
type system come from one family.

## 2. The numbers (measured; hit these)

| reference | shot median | new thing every | longest still before the end card | end card hold | camera moving | flashes/min | cuts that carry direction | loudness |
|---|---|---|---|---|---|---|---|---|
| ClickUp Brain | 11.9 s* | 2.5 s | 0.5 s | 3.25 s | 24 % | 0 | n/a | −11.5 LUFS, LRA 3.2 |
| Bolt hackathon | 2.05 s | 1.1 s | 0 s | 6.0 s | 28 % | 15.4 | 38 % | −9.8 LUFS, LRA 1.1 |
| Framer 3D launch | 7.3 s* | 2.45 s | 0.5 s | 2.5 s | 52 % | 0 | 67 % | −14.0 LUFS, LRA 15.5 |
| Urpal AI site | one take | 0.97 s | 0.75 s | loops | 7 % | 0 | n/a | silent |
| Help Scout site | one take | 2.3 s | 0 s | loops | 33 % | 3.1 | n/a | silent |
| Slack Spaceship | 1.75 s | 2.0 s | 0.25 s | 2.0 s | 25 % | 1.0 | 14 % | −14.3 LUFS, LRA 3.0 |
| Nike Flyknit | one take (64 s) | 0.5 s | 17 s (slow title fades) | 1.25 s | 9 % | 0 | n/a | −15.1 LUFS, LRA 17.3 |
| Style Frames titles | 4.2 s | 0.8 s | 8.0 s | 2.0 s | 12 % | 0 | 3 % | −11.9 LUFS, LRA 11.5 |

\* Long "shots" mean the film changes through transitions inside one continuous move, not hard cuts. Pace by
**new thing every**, not cuts.

Rules that follow:
- **Smooth = continuous, not fast.** The smoothest references barely cut: Nike runs 64 s as one take, the site
  films are one camera move, and Framer carries direction across 2 of 3 cuts. Prefer transformation, match cuts and
  carried objects to hard cuts.
- **Something new every 1–2.5 s** (a word, a panel, a counter tick, a camera turn). Every SaaS reference sits in
  this band.
- **Nothing still for more than ~1 s before the end card.** This is the strongest pattern in the set: before
  the end card, ClickUp's longest still moment is 0.5 s, Framer's 0.5 s, Bolt's 0 s, Urpal's 0.75 s and Help Scout's
  0 s. Even "holds" drift, breathe or build. Then the end card holds clean for 2–6 s. Only luxury brand films
  (Nike, Style Frames) hold longer, and that is not a SaaS pattern.
- **One accent colour.** Dark families average luma 10–65 of 255 with a single saturated glow (violet/magenta, or
  electric blue, or warm peach/gold). Slack's whole world is grey and only the brand colours are coloured.
- **Flash frames are a hype device** (Bolt 15/min). Everything else uses 0–3/min.
- **No judder.** Repeated frames during motion stay at 0–2.3 % (Slack's 6 % is deliberate 12 fps cartoon timing).
  Render at 30 or 60 fps and conform AI clips properly (section 5).
- **Hit the big moments on the music, not every cut.** In the references cuts land on beats only slightly above
  chance; the logo, the reveal and the CTA are what land on downbeats.
- **Loudness:** kinetic SaaS films master at −15 to −9 LUFS with a compressed music bed (LRA 1–3); story films are
  dynamic (LRA 11–17).

## 3. Continuity plan (the part that makes it smooth)

Add a column to the storyboard: **how each beat hands off to the next.** Every transition must be one of these;
plain crossfades between busy layouts are banned (they go muddy, as brag-slim warns).

| Hand-off | What happens | Seen in |
|---|---|---|
| Carried object | one hero object (cursor, orb, product, line) crosses the cut at the same screen position and direction | Framer cursor; Nike line; Urpal orb |
| Push through | the camera dives into a screen, button or letter and comes out in the next scene | Framer 3.0 s (into the laptop) |
| Shape match | a shape becomes the next layout (circle → button ring → logo) | Framer Publish ring; Bolt gold ring; Katana notes |
| Word chain | the next word slides in while the last one leaves, same baseline, motion blur on the move | ClickUp 6.0 s; Bolt 2–8 s |
| Scale snap | a giant cropped word or number snaps down to readable size | ClickUp "Your Voice" 9 s; Bolt "FOR" 6.5 s |
| Directional whip | 3–4 frames of blur in one direction, sharp landing | Katana notes; Bolt counters |
| Dip through the base | old content clears to the dark base, then new content builds in | ClickUp between sections |
| Continuous camera | no cut at all: the camera keeps travelling over one surface (page, set, world) | Help Scout; Urpal; Style Frames trucks |

Write it as: `3.0 s  laptop → UI tunnel  | push through screen | cursor carried, moving right`.
Aim for ≥ 50 % of hand-offs being carried object, push through, shape match or continuous camera in
`3d-product-world`, and ≥ 30 % in the other families.

## 4. Devices (pick 4–6 per film)

Full build notes per tool are in `references/devices-and-tools.md`. Short list:

- **Edge glow base:** near-black with a soft accent gradient rising from the bottom edge, plus 1–2 % grain so it
  never bands. (ClickUp, Bolt)
- **Word-by-word kinetic type:** heavy geometric sans, centred, 1–4 words per beat, each word entering with motion
  blur and settling; key word in the accent colour or gradient. Readable lines hold ≥ 0.3 s per word once settled.
- **Typewriter search line:** `Find answe_` with a caret, then the answer words swap in. (ClickUp 17 s)
- **Tilted real UI panel:** the product's real interface on a plane at ~15–25° tilt, drifting slowly, edge-lit in
  the accent colour. Always real UI, never a mock. (ClickUp, Framer)
- **Split beat:** real UI left, 2–4 words right, words changing every ~0.5 s while the panel holds. (ClickUp 30 s)
- **Glowing hero object:** an emissive cursor or orb that travels through the film and clicks things. (Framer, Urpal)
- **Glass pill buttons in macro:** thick glossy pills ("Create", "Publish"), shallow depth of field, a ripple ring
  on click. (Framer 4–18 s)
- **Rolling counters:** numbers rolling up in steps (3,512 → 6,651 → 9,791 → 10,000), with a label under them.
  Only real numbers. (Bolt 12–17 s)
- **Metallic 3D accent:** one warm gold/chrome object (arrow, ring, sphere) that moves the layout, e.g. an arrow
  pushing a grid of faces in. (Bolt 20–25 s)
- **Iso hardware chip:** the product as a glowing isometric chip with the logo on top. (ClickUp 47 s)
- **Brand-colour-only world:** grade everything grey and leave only the brand colours. (Slack)
- **One continuous transformation:** a line → material → product in one take, with tiny wide-tracked captions.
  (Nike)
- **End card:** product icon + one-line promise + one CTA button or URL on the base, held 3–8 s with ambient
  particles or a slow drift. Logo can assemble from pieces first. (ClickUp, Framer, Bolt, Slack)

## 5. Build: which tool makes what (on this Mac)

| Need | First choice | Notes |
|---|---|---|
| Kinetic type, UI panels, counters, end cards | /brag-slim (HTML + GSAP, Hyperframes) | real components and real copy; every frame a pure function of time |
| Precise motion-graphics finishing, glow, motion blur | After Effects scripted with ExtendScript (`osascript -e 'tell application "Adobe After Effects 2026" to DoScriptFile "<file.jsx>"'`) | text animator Range Selector by Words; Pixel Motion Blur |
| 3D hero object, glass pills, iso chip, screen push, metallic accents | Blender (MCP when Blender is open; headless `Blender -b -P` otherwise) | EEVEE bloom + DOF, render PNG sequences with alpha |
| Hero AI footage, morphs, textures, illustrated worlds | /katana or Higgsfield `generate_video` | **ask first, quote credits**; 4–5 s clips, restrained camera, reject warping |
| Real website/app material | Playwright / Chrome DevTools (screenshots, 60 fps scroll capture), the project code | reuse real markup and CSS, as brag-slim says |
| Music + SFX | Artlist `search_music` / `search_sfx` (previews; the user licenses WAVs), brag's bundled tracks | follow business-motion-film `references/audio.md` |
| Voice-over (opt-in) | ElevenLabs creative speech or Artlist voiceover | credits; ask first |
| Assembly, conform, mastering | ffmpeg | Homebrew ffmpeg has **no drawtext**: put text in AE/HTML, never ffmpeg |

**Conforming AI clips (anti-judder):** Higgsfield/Kling clips arrive at 24 fps, often 720p. Either keep the whole
film at 24 fps, or conform with motion interpolation (`ffmpeg -vf minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc`),
then check `repeated_frames_in_motion_pct` and look for warping at the motion peaks. Never leave a 24 fps clip
frame-doubled inside a 30 fps timeline.

## 6. Check before delivery (mandatory)

```bash
~/.claude/skills/rolvibe-launch-style/scripts/check_film.sh <render.mp4> <family>
```

It runs the bundled `scripts/vendor/study.py` plus `scripts/motion_profile.py` on your render and scores it
against `scripts/targets.json`. Then:
1. Fix every MISS in the edit (pace, holds, flashes, judder, loudness), re-render, re-check.
2. Look at `_check/<name>/frames/hook.jpg` and `shots_00.jpg` beside the matching reference sheet in `_analysis/`.
3. Run a business-motion-film critic round on the actual render before calling it done.
Report the numbers table to the user with the video.

## 7. Grow the skill

- New reference: `scripts/vendor/study.py --file <ref> --slug <name> --out <your reference folder>/_analysis/<name>`
  then `scripts/motion_profile.py`; look at every sheet; add a row to section 2, a note to
  `references/reference-notes.md`, and adjust `targets.json`.
- The author's `download-all.sh` lists 11 more launch films (Linear, Figma, Arc, Notion, Perplexity, Cursor, Framer 3,
  Anthropic, Claude, 7up, Figure, SOM, Porsche, Airbnb, BeoLab) that are not in the folder yet. Downloading them is
  the user's call.
- After each delivered film, add a Learnings line below.

## 8. Don'ts

- No mock UI, invented numbers, fake logos or testimonials (business-motion-film truth rules apply).
- No plain crossfade between two busy layouts; no hard cut from a moving shot to a dead-still one unless it is the
  end card; no frozen moment longer than ~1 s before the end card.
- No second accent colour fighting the first; no rainbow gradients.
- No flash frames outside `dark-glow-kinetic-hype`; no strobing (> 16/min) anywhere.
- No text that leaves before it can be read; no ffmpeg text.
- No Higgsfield, Artlist generation or ElevenLabs call without the user's go and a cost estimate.

## 9. Learnings

- 2026-10-16: iteration 1 built from 9 references. Not yet proven with a demo render: next step is a 20 s
  rolvibe.com film via /brag-slim in `dark-glow-kinetic`, then `check_film.sh`, then tune the targets.
