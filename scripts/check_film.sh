#!/usr/bin/env bash
# Measure a finished render and score it against a rolvibe-launch-style family.
# Usage: check_film.sh <render.mp4> <family> [out_dir]
#   families: dark-glow-kinetic | dark-glow-kinetic-hype | 3d-product-world | site-showcase | crafted-story
# Writes <out_dir> (default: <render dir>/_check/<render name>) with report.md, sheets, motion.json.
set -euo pipefail
f="$1"; fam="$2"
# Python with opencv-python-headless<5, numpy, librosa (see README). Override with VIDEO_PY=/path/to/python.
PY="${VIDEO_PY:-$HOME/.venvs/video-dissect/bin/python}"
[ -x "$PY" ] || PY="python3"
HERE="$(cd "$(dirname "$0")" && pwd)"
STUDY="$HERE/vendor/study.py"
name="$(basename "${f%.*}")"
out="${3:-$(dirname "$f")/_check/$name}"
mkdir -p "$out"
"$PY" "$STUDY" --file "$f" --slug "$name" --out "$out" > "$out/study.log" 2>&1 || { tail -5 "$out/study.log"; exit 2; }
"$PY" "$HERE/motion_profile.py" "$f" --cuts "$out/cuts/cuts.txt" --events "$out/cuts/events.txt" --out "$out/motion.json" > /dev/null
"$PY" "$HERE/compare_targets.py" "$out" "$fam"
