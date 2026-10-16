#!/usr/bin/env python3
"""compare_targets.py: score a render's study.py + motion_profile.py numbers against a style family.

    compare_targets.py <study folder with report.json and motion.json> <family>   (families: see targets.json)
Prints PASS / MISS per metric and exits 1 if anything misses. A miss is a rule the edit broke, or a rule the
skill hasn't encoded yet: fix the edit first, then the skill.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    study, fam = sys.argv[1], sys.argv[2]
    T = json.load(open(os.path.join(HERE, "targets.json")))
    if fam not in T:
        sys.exit(f"unknown family {fam!r}; choose from: {', '.join(k for k in T if not k.startswith('_'))}")
    R = json.load(open(os.path.join(study, "report.json")))
    M = json.load(open(os.path.join(study, "motion.json")))
    have = {
        "new_thing_every_s": R["visual"].get("event_gap_median"),
        "longest_static_s": R["visual"].get("longest_static_s"),
        "longest_static_before_end_s": M.get("longest_static_before_end_s"),
        "end_card_hold_s": M.get("end_card_hold_s") or None,
        "brightness_mean": R["visual"].get("brightness_mean"),
        "cuts_per_min": R["shots"].get("cuts_per_min"),
        "loudness_lufs": (R.get("audio") or {}).get("loudness_lufs"),
        "camera_moving_pct": M.get("camera_moving_pct"),
        "cuts_direction_carried_pct": M.get("cuts_direction_carried_pct"),
        "flash_frames_per_min": M.get("flash_frames_per_min"),
        "repeated_frames_in_motion_pct": M.get("repeated_frames_in_motion_pct"),
    }
    misses = 0
    print(f"{fam}  ({T[fam].get('_from', '')})")
    for k, rng in T[fam].items():
        if k.startswith("_"):
            continue
        v = have.get(k)
        lo, hi = rng
        if v is None:
            print(f"  ----  {k:32s} n/a (not measured: no cuts / no audio)")
            continue
        ok = (lo is None or v >= lo) and (hi is None or v <= hi)
        misses += not ok
        print(f"  {'PASS' if ok else 'MISS'}  {k:32s} {v:>8}   target {lo if lo is not None else '-'} .. {hi if hi is not None else '-'}")
    print("all targets met" if not misses else f"{misses} target(s) missed")
    sys.exit(1 if misses else 0)


if __name__ == "__main__":
    main()
