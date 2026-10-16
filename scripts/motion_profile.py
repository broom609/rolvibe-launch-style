#!/usr/bin/env python3
"""motion_profile.py: measure HOW a video moves, to complement study.py (which measures pacing, colour, loudness).

    ~/.venvs/video-dissect/bin/python motion_profile.py video.mp4 [--cuts cuts.txt] [--events events.txt] [--out profile.json]

Measures, from dense optical flow on a 256 px proxy at 12 fps plus a native-fps luma/diff pass:
  camera     % of time the whole frame moves (pan/truck, push-in, pull-out, roll) vs held camera with object motion vs static
  direction  dominant pan directions and zoom sign
  cuts       speed at the cut (cut mid-move or on a still), and whether motion direction is CARRIED across the cut
  smoothness speed jumps per minute (non-eased velocity changes) and repeated frames during motion (judder)
  ramps      speed ramps per minute (>=3x speed change within 0.5 s)
  stills     longest near-still stretch, also excluding an end-card hold that runs to the last frame
  flashes    1-4 frame luma spikes (white or black flash frames) per minute
  beat       BPM, and % of cuts / visual events landing within 60 ms of a beat or onset (with the chance baseline)
"""
from __future__ import annotations
import argparse, json, math, os, subprocess, sys, statistics
import numpy as np
import cv2

PROXY_FPS = 12.0
PROXY_W = 256


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate:format=duration",
                        "-of", "json", path], capture_output=True, text=True, check=True)
    j = json.loads(r.stdout)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    n, d = v["r_frame_rate"].split("/")
    return {"w": v["width"], "h": v["height"], "fps": float(n) / float(d), "dur": float(j["format"]["duration"]),
            "audio": any(s["codec_type"] == "audio" for s in j["streams"])}


def gray_frames(path, fps, width, H, W):
    h = max(2, int(round(width * H / W / 2)) * 2)
    vf = (f"fps={fps}," if fps else "") + f"scale={width}:{h},format=gray"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", vf, "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, width)


def load_times(p):
    if not p or not os.path.exists(p):
        return []
    return [float(x) for x in open(p).read().split() if x.strip()]


def global_fit(flow, X, Y, r2sum):
    t = flow.reshape(-1, 2).mean(0)
    fx, fy = flow[..., 0] - t[0], flow[..., 1] - t[1]
    s = float((fx * X + fy * Y).sum() / r2sum)          # zoom: + = push in (content expands)
    rot = float((fx * -Y + fy * X).sum() / r2sum)       # roll
    gx, gy = t[0] + s * X - rot * Y, t[1] + s * Y + rot * X
    glob = float(np.hypot(gx, gy).mean())
    local = float(np.hypot(flow[..., 0] - gx, flow[..., 1] - gy).mean())
    return t, s, rot, glob, local


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video"); ap.add_argument("--cuts"); ap.add_argument("--events"); ap.add_argument("--out")
    a = ap.parse_args()
    info = probe(a.video)
    cuts = load_times(a.cuts); events = load_times(a.events)

    # ---------- proxy flow pass ----------
    G = gray_frames(a.video, PROXY_FPS, PROXY_W, info["h"], info["w"])
    n, h, w = G.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    X, Y = xx - (w - 1) / 2, yy - (h - 1) / 2
    r2sum = float((X ** 2 + Y ** 2).sum()); rmean = float(np.hypot(X, Y).mean())
    rows = []
    for i in range(1, n):
        t0, t1 = (i - 1) / PROXY_FPS, i / PROXY_FPS
        straddle = any(t0 - 0.02 <= c <= t1 + 0.02 for c in cuts)
        flow = cv2.calcOpticalFlowFarneback(G[i - 1], G[i], None, 0.5, 3, 15, 3, 5, 1.2, 0)
        t, s, rot, glob, local = global_fit(flow, X, Y, r2sum)
        rows.append({"t": round(t1, 3), "cut": straddle, "dx": float(t[0]) / w * PROXY_FPS, "dy": float(t[1]) / w * PROXY_FPS,
                     "zoom": s * PROXY_FPS, "roll": rot * PROXY_FPS, "glob": glob / w * PROXY_FPS, "local": local / w * PROXY_FPS,
                     "pan_px": float(np.hypot(*t)), "zoom_px": abs(s) * rmean, "rot_px": abs(rot) * rmean})
    ok = [r for r in rows if not r["cut"]]
    MOVE = 0.02   # 2 % of frame width per second
    cls = {}
    for r in ok:
        if r["glob"] < MOVE and r["local"] < MOVE:
            k = "static"
        elif r["local"] > 1.5 * r["glob"]:
            k = "object_motion_held_camera"
        else:
            comp = {"pan": r["pan_px"], "zoom": r["zoom_px"], "roll": r["rot_px"]}
            k = max(comp, key=comp.get)
            if k == "zoom":
                k = "push_in" if r["zoom"] > 0 else "pull_out"
        r["class"] = k
        cls[k] = cls.get(k, 0) + 1
    tot = max(1, len(ok))
    camera = {k: round(100 * v / tot, 1) for k, v in sorted(cls.items(), key=lambda kv: -kv[1])}
    cam_moving = round(100 * sum(1 for r in ok if r["glob"] >= MOVE and r["local"] <= 1.5 * r["glob"]) / tot, 1)
    pans = [r for r in ok if r.get("class") == "pan"]
    pan_dirs = {}
    for r in pans:
        d = ("right" if r["dx"] < 0 else "left") if abs(r["dx"]) >= abs(r["dy"]) else ("down" if r["dy"] < 0 else "up")
        pan_dirs[d] = pan_dirs.get(d, 0) + 1   # camera direction (content moves the opposite way)
    speed = np.array([r["glob"] + r["local"] for r in rows])

    # ---------- smoothness: speed jumps + ramps (within shots) ----------
    sp = np.array([r["glob"] + r["local"] if not r["cut"] else np.nan for r in rows])
    jumps, ramps, k = 0, 0, 0
    for i in range(1, len(sp)):
        a0, a1 = sp[i - 1], sp[i]
        if np.isnan(a0) or np.isnan(a1):
            continue
        hi, lo = max(a0, a1), min(a0, a1)
        if hi > 0.06 and hi > 2.0 * max(lo, 1e-3):
            jumps += 1
    win = int(0.5 * PROXY_FPS)
    i = 0
    while i + win < len(sp):
        seg = sp[i:i + win + 1]
        if not np.isnan(seg).any() and seg.max() > 0.08 and seg.max() >= 3 * max(seg.min(), 1e-3):
            imax, imin = int(seg.argmax()), int(seg.argmin())
            if abs(imax - imin) >= 2:          # gradual, not a one-sample jump
                ramps += 1; i += win; continue
        i += 1
    dur_min = info["dur"] / 60

    # ---------- cuts: speed at cut + direction carried ----------
    def window(t0, t1):
        return [r for r in ok if t0 <= r["t"] <= t1]
    med_speed = float(np.nanmedian(sp)) if np.isfinite(np.nanmedian(sp)) else 0
    carried = reset = reversed_ = mid_move = 0
    for c in cuts:
        b, f = window(c - 0.34, c - 0.02), window(c + 0.1, c + 0.42)
        if not b or not f:
            continue
        vb = np.array([np.mean([r["dx"] for r in b]), np.mean([r["dy"] for r in b]), np.mean([r["zoom"] for r in b]) * 0.5])
        vf = np.array([np.mean([r["dx"] for r in f]), np.mean([r["dy"] for r in f]), np.mean([r["zoom"] for r in f]) * 0.5])
        sb, sf = np.mean([r["glob"] + r["local"] for r in b]), np.mean([r["glob"] + r["local"] for r in f])
        if min(sb, sf) > max(MOVE, 0.5 * med_speed):
            mid_move += 1
        nb, nf = np.linalg.norm(vb), np.linalg.norm(vf)
        if nb < MOVE or nf < MOVE:
            reset += 1
        elif float(vb @ vf) / (nb * nf) > 0.5:
            carried += 1
        else:
            reversed_ += 1
    nc = max(1, carried + reset + reversed_)

    # ---------- still stretches (study.py's definition: 4 fps, mean abs diff < 1.2) ----------
    G4 = G[::3].astype(np.int16); d4 = np.abs(np.diff(G4, axis=0)).mean(axis=(1, 2))
    runs, st = [], None
    for i, x in enumerate(d4):
        if x < 1.2:
            st = i if st is None else st
        elif st is not None:
            runs.append((st / 4, i / 4)); st = None
    if st is not None:
        runs.append((st / 4, len(d4) / 4))
    end_card = [r for r in runs if r[1] >= info["dur"] - 0.75]      # a hold that runs to the last frame
    body = [r for r in runs if r not in end_card]
    longest = lambda rs: round(max((b - a for a, b in rs), default=0.0), 2)
    stills = {"longest_static_s": longest(runs), "longest_static_before_end_s": longest(body),
              "end_card_hold_s": longest(end_card),
              "longest_stills": [f"{a:.2f}-{b:.2f}s" for a, b in sorted(runs, key=lambda r: r[0] - r[1])[:3]]}

    # ---------- native pass: flashes + judder ----------
    N = gray_frames(a.video, None, 128, info["h"], info["w"]).astype(np.float32)
    L = N.mean(axis=(1, 2)); D = np.abs(np.diff(N, axis=0)).mean(axis=(1, 2))
    fps = info["fps"]
    flashes, white, black, i = 0, 0, 0, 3
    while i < len(L) - 5:
        base = float(np.median(L[i - 3:i]))
        if abs(L[i] - base) > 30:
            back = next((k for k in range(1, 5) if abs(L[i + k] - base) < 15), None)
            if back:
                flashes += 1; white += L[i] > base; black += L[i] < base; i += back + 1; continue
        i += 1
    rep, moving = 0, 0
    for i in range(5, len(D) - 5):
        loc = float(np.median(D[i - 5:i + 6]))
        if loc > 1.0:
            moving += 1
            if D[i] < 0.15 * loc:
                rep += 1

    # ---------- beat alignment ----------
    beat = {}
    if info["audio"]:
        try:
            import librosa
            wav = subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-ac", "1", "-ar", "22050", "-f", "f32le", "-"],
                                 capture_output=True, check=True).stdout
            y = np.frombuffer(wav, np.float32)
            if len(y) and float(np.abs(y).max()) > 1e-3:
                tempo, bt = librosa.beat.beat_track(y=y, sr=22050, units="time")
                on = librosa.onset.onset_detect(y=y, sr=22050, units="time", backtrack=False)
                bpm = float(np.atleast_1d(tempo)[0])
                def hit(ts, ref, tol=0.06):
                    return round(100 * sum(1 for t in ts if len(ref) and np.min(np.abs(np.asarray(ref) - t)) <= tol) / max(1, len(ts)), 1) if ts else None
                chance = lambda ref: round(min(100.0, 100 * 2 * 0.06 * len(ref) / max(1e-6, info["dur"])), 1)
                beat = {"bpm": round(bpm, 1), "cuts_on_beat_pct": hit(cuts, bt), "cuts_on_onset_pct": hit(cuts, on),
                        "events_on_beat_pct": hit(events, bt), "events_on_onset_pct": hit(events, on),
                        "chance_beat_pct": chance(bt), "chance_onset_pct": chance(on)}
        except Exception as e:  # noqa: BLE001
            beat = {"error": str(e)[:200]}

    R = {"video": os.path.basename(a.video), "duration": round(info["dur"], 2), "fps": round(fps, 3),
         "camera_moving_pct": cam_moving, "time_by_motion_type_pct": camera,
         "camera_pan_directions": pan_dirs,
         "median_speed_frame_widths_per_s": round(med_speed, 3),
         "speed_p90": round(float(np.nanpercentile(sp, 90)), 3) if np.isfinite(np.nanmedian(sp)) else 0,
         "speed_jumps_per_min": round(jumps / dur_min, 1), "speed_ramps_per_min": round(ramps / dur_min, 1),
         "cuts_analysed": nc if (carried + reset + reversed_) else 0,
         "cuts_mid_move_pct": round(100 * mid_move / nc, 1) if cuts else None,
         "cuts_direction_carried_pct": round(100 * carried / nc, 1) if cuts else None,
         "cuts_from_or_to_still_pct": round(100 * reset / nc, 1) if cuts else None,
         "cuts_direction_reversed_pct": round(100 * reversed_ / nc, 1) if cuts else None,
         **stills,
         "flash_frames_per_min": round(flashes / dur_min, 1), "flash_white": int(white), "flash_black": int(black),
         "repeated_frames_in_motion_pct": round(100 * rep / max(1, moving), 2),
         "beat": beat}
    out = a.out or os.path.splitext(a.video)[0] + ".motion.json"
    json.dump(R, open(out, "w"), indent=2)
    print(json.dumps(R, indent=1))


if __name__ == "__main__":
    main()
