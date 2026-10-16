# Devices → how to build them on this Mac

Defaults: 1920×1080 (or 1080×1920), 30 fps (60 fps for site/UI motion), every animated value a pure function of
time. Credits rule: Higgsfield (/katana, generate_image/video), Artlist generation and ElevenLabs need the user's
go plus a cost estimate first. Local builds (brag-slim/HTML, After Effects, Blender, ffmpeg) are free.

## Frosted glass on a light background (After Effects, scripted)
- Per card: a controller null; a hidden matte shape (the card silhouette); a full-frame **adjustment layer** with Fast Box
  Blur (radius 26-40, 3 iterations, repeat edge pixels) + Brightness +10, track-matted (ALPHA) to the silhouette; the
  shadow above it, track-matted ALPHA_INVERTED to the same silhouette; then a body precomp: white fill 50 %, a specular,
  a 1.5 px white inner stroke at 78 %, a 2 px #0B1020 bottom edge at 7 %. Keep colour blooms behind every card.
- Traps (each cost a rebuild):
  - A shadow under the card gets pulled into the glass by the backdrop blur (grey glass). Matte it to OUTSIDE the card.
  - Specular: use a WHITE solid with a Gradient Ramp converted to alpha (Shift Channels: alpha <- luminance, RGB <- full on).
    A black-to-white ramp in Screen mode inside a precomp adds black opacity and greys the glass.
  - Masks are applied BEFORE effects, so a Ramp refills a masked layer's whole rectangle. Clip with a track matte instead.
  - Assigning a layer as a track matte turns its visibility off. Re-enable it if it must also render (e.g. a logo used
    as the matte for its own light pass).
  - Parenting to a layer that is already keyed (a card mid-unfold) makes AE counter-scale the child. Reset the child's
    scale and rotation after parenting.
  - Opacity doesn't pass through parenting: drive each part with `parent.opacity * value / 100` so its own keys still work.
- Morphing players (16:9 <-> 9:16): drive every part from W/H/R sliders (rect size expressions, createPath masks) instead
  of scaling a precomp, so radius and stroke never distort; videos cover-fit by expression and share one video matte.

## Edge glow base
- **HTML (brag-slim):** `background: radial-gradient(120% 60% at 50% 115%, var(--accent) 0%, transparent 60%), #0b0a12;`
  plus a full-frame noise layer at 2 % opacity (an SVG `feTurbulence` or a tiled noise PNG) so the gradient never
  bands. Animate the gradient centre ±3 % over 6–8 s so the base breathes.
- **After Effects:** a dark solid, an accent solid with a big feathered elliptical mask at the bottom edge, Glow
  effect, Add Grain (intensity 0.1). Not shape-layer blur (it clips to the path bounds).

## Word-by-word kinetic type
- **HTML:** split the line into words; each word goes from `translateY(40%) scale(1.08)` with `filter: blur(12px)` and
  opacity 0 to its rest state in 0.28–0.4 s with `power3.out`, staggered 0.06–0.12 s. Motion blur comes from the
  blur filter on the move. Hold the settled line ≥ 0.3 s per word.
- **After Effects:** text animator (Position + Opacity 0 + Blur), Range Selector Shape = Ramp Up, Based On = Words,
  Offset −100 → 100, with Pixel Motion Blur on the layer.
- **Scale snap:** the word enters at 300–400 % (cropped), 0.2 s to 100 % with `expo.out`, a 1-frame blur peak.
- **Typewriter:** characters appear every 40–60 ms with a blinking caret (on 0.5 s, off 0.5 s); the replaced
  answer words use the word-chain hand-off.

## Tilted real UI panel / split beat
- **Material:** real screenshots or real components only. For a website, capture with Playwright/Chrome DevTools
  at 2× device scale; for a project, render its components (brag-slim "Show the thing").
- **HTML:** `perspective: 1600px; transform: rotateX(18deg) rotateY(-14deg) rotateZ(3deg)`, drift 2–4 % over the beat,
  an accent `box-shadow` edge light, rounded 16–24 px, a subtle top highlight.
- **After Effects:** 3D layer + a camera with a slow dolly; Depth of Field off for UI legibility.
- **Blender (premium):** plane with the UI as an emissive texture plus a beveled glass slab in front
  (Principled BSDF transmission 1, roughness 0.05), EEVEE bloom.

## Glowing hero object (cursor / orb) that carries every cut
- **Blender:** model the cursor (extruded arrow, bevel 2 mm) with an emissive violet/blue material (strength 8–15),
  EEVEE bloom, a camera with DOF f/1.8 focused on it. Animate one continuous path through all scenes; render the
  object pass with alpha (PNG sequence, RGBA) so it can be composited over HTML/AE scenes too.
- **Hand-off rule:** at every cut, the object leaves frame A and enters frame B at the same screen position and
  direction (± 5 % of the frame width), at the same speed.

## Push through a screen / button
- **Blender:** the camera dollies into the screen plane while the screen texture swaps to the next scene at the
  moment it fills the frame; add a 2-frame light flare at the crossing.
- **After Effects:** scale the screen layer up to fill the frame on `expo.in` (0.35 s), cut on the frame where it
  fills, then the next scene starts at 110 % scale settling to 100 % (`expo.out`).

## Glass pill buttons + click ripple
- **Blender:** a rounded-rect pill, thick bevel, glass with an inner emissive label; a macro lens (85–100 mm, f/2)
  with focus on the label.
- **HTML:** `backdrop-filter: blur(20px)`, a 1 px inner border at 40 % white, a gradient fill; on click, scale 0.96 →
  1 and a ring expands from 1 → 2.4× while fading out over 0.5 s.

## Rolling counters
- Only real numbers. Step through 3–4 waypoints (e.g. 3,512 → 6,651 → 9,791 → 10,000) with 0.35–0.5 s per step;
  each step rolls its digits vertically with blur. **HTML:** compute the value from time and format with
  `toLocaleString`. **After Effects:** a Slider Control keyframed per step, Source Text expression
  `Math.round(effect("Slider Control")(1)).toLocaleString()`.

## Metallic 3D accent / iso chip
- **Blender:** a gold/chrome Principled BSDF (metallic 1, roughness 0.15–0.25), studio HDRI, rendered with alpha.
  Iso chip: a beveled cube in an orthographic camera at 35°/45°, the logo as an emissive inset on top.
- **Higgsfield (credits):** generate_image for a hero still only when a modelled version would be too slow;
  keep the camera locked so it composites cleanly.

## Brand-colour-only world (Slack)
- Grade every shot to greyscale and keep only the brand hues: AE Hue/Saturation saturation −100 on an adjustment
  layer with a Color Range key (Keylight or Color Range effect) inverted for the brand colours.
- Illustrated characters or worlds: Higgsfield image generation in one locked style (credits), animated with Kling
  image-to-video 4–5 s clips, restrained moves.

## One continuous transformation (Nike)
- **After Effects:** a trim-path line drawing the opening shape, then morphing paths between shapes; an iridescent
  gradient stroke with Glow.
- **Blender:** a curve → geometry-nodes threads/particles → the product mesh, with one camera move throughout.
- **AI (credits):** start/end-frame video generation (/katana or Kling) to morph between two designed stills;
  reject any clip whose geometry warps.

## Site showcase (Help Scout / Urpal)
- Capture the real site: Playwright full-page screenshots at 2× (each section), or a 60 fps screencast of a
  real smooth scroll (Chrome DevTools `screencast_start`).
- Lay out in HTML or AE as one continuous camera: scroll with eased stops per section (0.6 s ease in, 0.4 s hold
  with drift, 0.6 s ease out), end with a zoom-out montage of the whole page; end frame = start frame for loops.

## End card
- Product icon + one-line promise + one CTA (button or URL) on the base, 3–8 s, with slow particles or a 1–2 %
  drift so it never freezes. Optional: the logo assembles from pieces (AE shape layers with trim paths, or
  Blender pieces) before it settles. Bake the settled frame as the poster/frame 0 (brag-slim step 4).

## Audio
- Music: Artlist `search_music` (previews; the user licenses the WAV) or brag's bundled tracks. Choose the track
  first, find its downbeats with librosa (the video Python env, see README), and put the logo, reveal and CTA on them.
- SFX: whoosh only on real transitions, soft UI ticks on real clicks/counters, one hit on the end card
  (business-motion-film `references/audio.md`, `scripts/sfx-candidates.py`, `scripts/solve-sfx-gains.py`).
- **Approved soft palette (glass launch, 2026-10-16).** The first mix was called "aggressive"; the replacement was
  approved. Start from this palette, and screen any new Artlist candidate by measurement, since names mislead:
  - **Keep:** Smartphone UI menu click (117389), Bright UI select confirm (111703), Wood UI typing tap (125991),
    TeaSound short swish (73713) and short swipe (73721), Krotos light airy whoosh (68217), Swift dry whoosh (84218),
    Sweet UI pluck (135684) and gentle alert (135688), Graphix low bell (99172) and Tap on Glass (99196),
    Cold Magic sparkle (71326).
  - **Reject:** Casual UI and Modern UI clicks (58–86 % of energy at 2–8 kHz), Ideal Impacts thud and Transitional
    Sub (about 100 % below 150 Hz; they muddy an EDM drop), Gliding Down Chime (86 % above 8 kHz), bubbly pops,
    game taps, synth beeps, card flips, laptop typing, risers, reverse swells.
  - **Treatment:** high-pass 120–400 Hz, low-pass 9–10 kHz, −3 dB shelf above 6 kHz, 5 ms fade-ins, one shared
    short reverb (RT60 ~0.7 s), tonal cues tuned to the song's key.
  - **Levels:** 8–18 dB under the music's local RMS, peaks capped at the music's local peak, 2–8 kHz lift ≤ 3.5 dB,
    and an own-band audibility floor (~1.5 dB) so nothing is buried. Keep repeats equal with a group median, and
    measure the 2–8 kHz reference over 1 s, because staccato micro-gaps fake "quiet".
  - **Working script:** `rolvibe-glass-launch/work/build/sfx_mix.py`.
- Artlist preview proxy: about 24 fast downloads trigger a Cloudflare 429 page saved as `.aac`. Fetch one every ~6 s,
  back off 90–300 s on 429, and check the first byte isn't `<`.
- Master: −14 to −10 LUFS integrated for kinetic films, true peak ≤ −1 dBTP; check with
  `~/.claude/skills/business-motion-film/scripts/loudness.sh`.

## Conform and master
- Keep one frame rate for the whole timeline. AI clips at 24 fps either set the film to 24 or conform with
  `minterpolate` (see SKILL.md section 5); then run `scripts/check_film.sh`.
- Export H.264 High, yuv420p, crf 16–18, `-movflags +faststart`; keep a ProRes master from AE when AE is used.
