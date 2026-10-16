# rolvibe-launch-style

A Claude Code skill that makes AI-built launch videos look like premium SaaS and startup films: smooth, continuous,
never frozen. It sits on top of [/brag](https://github.com/latent-spaces/brag) (or Higgsfield's /katana) as a style
layer, and it checks the finished render against numbers measured from real launch films.

## What it gives the agent

- **Five style families** with a look, a pace and target numbers: `dark-glow-kinetic`, `dark-glow-kinetic-hype`,
  `3d-product-world`, `site-showcase` and `crafted-story`.
- **A continuity plan.** Every cut must hand off in one of eight ways (a carried object, a push through the screen,
  a shape match, a word chain, a scale snap, a directional whip, a dip through the base, or a continuous camera).
  Plain crossfades between busy layouts are banned.
- **13 signature devices** with build recipes for HTML/GSAP (via /brag), After Effects, Blender, Higgsfield,
  Artlist and ffmpeg, in `references/devices-and-tools.md`.
- **A measured check.** `scripts/check_film.sh` measures a render and scores it against the family's targets:
  pace, still moments, end-card hold, camera movement, flash frames, brightness, loudness and judder.

## What the reference films taught it

Measured from 9 launch and brand films (ClickUp Brain, Bolt's hackathon promo, Framer's 3D launch, the Urpal AI and
Help Scout site films, Slack "Spaceship", Nike Flyknit and the Style Frames 2016 titles):

- **Smooth comes from continuity, not speed.** The smoothest films barely cut: Nike runs one 64 s take, the site
  films are a single camera move, and Framer's glowing cursor carries direction across two-thirds of its cuts.
- **Nothing sits still before the end card.** Before the end card, the SaaS films never hold a frozen moment longer
  than 0.75 s. Then each holds a clean end card for 2–6 s.
- **Something new every 1–2.5 s:** a word, a panel, a counter tick or a camera turn.
- **One accent colour** on a dark base. Flash frames are only for hype pieces.

Per-film notes with timestamps are in `references/reference-notes.md`. The films themselves are not included; they
belong to their owners.

## Install

```bash
git clone https://github.com/broom609/rolvibe-launch-style ~/.claude/skills/rolvibe-launch-style
```

Requirements for the check script: `ffmpeg`/`ffprobe`, and a Python with OpenCV 4 (not 5: OpenCV 5 dropped the
face detector the analysis uses), numpy and librosa:

```bash
python3 -m venv ~/.venvs/video-dissect
~/.venvs/video-dissect/bin/pip install "opencv-python-headless<5" numpy librosa
```

`check_film.sh` uses `~/.venvs/video-dissect/bin/python` by default. Set `VIDEO_PY=/path/to/python` to use another.

Works best alongside:
- [/brag](https://github.com/latent-spaces/brag): builds the video itself (free, local).
- `business-motion-film` from [motion-video-kit](https://github.com/echris6/motion-video-kit): the critic loop,
  quality bar and audio rules.
- Higgsfield's /katana, After Effects, Blender and Artlist for the devices that need them. Generation tools spend
  credits, and the skill tells the agent to ask before using them.

## Use

In Claude Code: *"/brag this in rolvibe style, dark-glow-kinetic"*, or *"make a premium launch video for this
site"*. The skill loads, picks a family, adds a continuity column to the storyboard, and checks the render:

```bash
~/.claude/skills/rolvibe-launch-style/scripts/check_film.sh brag-output/brag.mp4 dark-glow-kinetic
```

```
dark-glow-kinetic-hype  (Bolt hackathon (counters, flashes, metallic 3D accents))
  PASS  new_thing_every_s                     1.1   target 0.8 .. 1.6
  PASS  longest_static_before_end_s           0.0   target - .. 1.0
  PASS  end_card_hold_s                       6.0   target 2.0 .. 8.0
  ...
all targets met
```

## Status

Iteration 1 (2026-10-16). Seven of the eight reference films pass their own family's targets. The exception is
Nike's slow 17 s title opening, which is documented in `scripts/targets.json`. The style hasn't been proven on a
demo render yet.

## Credits

- `scripts/vendor/study.py` comes from [open-edits](https://github.com/kevinbadi/open-edits) by Kevin Bahrabadi
  (MIT, see `scripts/vendor/LICENSE-open-edits`), with one local change: contact-sheet labels fall back to OpenCV
  when ffmpeg is built without `drawtext`.
- Company and product names in the notes are trademarks of their owners and are referenced only for analysis.
  This project is not affiliated with any of them.

## License

MIT, see `LICENSE`.
