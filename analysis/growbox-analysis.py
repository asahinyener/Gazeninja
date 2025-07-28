#!/usr/bin/env python3
"""
Analyse eye-tracking CSVs produced by index.html and emit:
  • episodes  – every dwell episode, with flicker info
  • metrics   – rescues / okays / timings

Usage
-----
python analyze_growbox.py --csv       2025-07-28.csv \
                          --episodes  out/2025-07-28_episodes.csv \
                          --metrics   out/2025-07-28_metrics.json
"""
import argparse, json
import pandas as pd

# ── constants copied from index.html ──────────────────────────
DWELL_MS      = 800     # dwell threshold (ms)
GROW_AFTER_MS = 120     # delay before box starts growing (ms)

# ── episode detection + metrics ───────────────────────────────
def detect_episodes(df: pd.DataFrame,
                    dwell_ms=DWELL_MS,
                    grow_after_ms=GROW_AFTER_MS) -> pd.DataFrame:
    df = (df.sort_values('timestamp')
            .assign(lasthit=lambda d: d['lasthit'].fillna('')))
    samp_ms = df['timestamp'].diff().median()

    episodes, cur_id = [], ''
    start_ts = prev_ts = None
    grow_on = fired = False
    flicker_frames = 0

    for row in df.itertuples():
        same = (row.lasthit == cur_id) and row.lasthit != ''

        # ── boundary ──────────────────────────────────────────
        if not same:
            if cur_id:
                episodes.append(_close_episode(cur_id, start_ts, prev_ts,
                                               fired, grow_on,
                                               flicker_frames, samp_ms))
            cur_id, start_ts = row.lasthit, row.timestamp
            grow_on = 'g' in row.mode
            fired = False
            flicker_frames = 0

        # ── inside episode ───────────────────────────────────
        if cur_id:
            dt = row.timestamp - start_ts
            if not fired and dt >= dwell_ms:
                fired = True
            if dt >= grow_after_ms and row.hitGrow == 1 and row.hitExact == 0:
                flicker_frames += 1
        prev_ts = row.timestamp

    # trailing episode
    if cur_id:
        episodes.append(_close_episode(cur_id, start_ts, prev_ts,
                                       fired, grow_on,
                                       flicker_frames, samp_ms))
    return pd.DataFrame(episodes)

def _close_episode(aoi_id, start, end, fired, grow_on, flk_frames, samp_ms):
    duration = end - start
    flicker_ms = flk_frames * samp_ms
    saved = fired and grow_on and flicker_ms > 0
    return dict(id=aoi_id, startTS=start, endTS=end,
                duration=duration, flicker_ms=flicker_ms,
                grow_on=grow_on, fired=fired, saved=saved)

def compute_metrics(ep: pd.DataFrame) -> dict:
    return {
        "rescues"              : int(ep['saved'].sum()),
        "okays"                : int((ep['fired'] & (ep['flicker_ms']
                                      .fillna(0) == 0)).sum()),
        "avg_unsaved_grow_ms"  : int(ep.loc[ep['grow_on'] & ~ep['fired'],
                                            'duration'].mean() or 0),
        "mean_flicker_ms"      : round(ep.loc[ep['saved'], 'flicker_ms']
                                         .mean() if ep['saved'].any() else 0, 1)
    }

# ── main CLI ──────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(description="Grow-Box CSV analyser")
    p.add_argument('--csv',          required=True,
                   help='input gaze_samples CSV')
    p.add_argument('--episodes',     required=True,
                   help='output episodes CSV')
    p.add_argument('--metrics',      required=True,
                   help='output metrics JSON')
    args = p.parse_args()

    df = pd.read_csv(args.csv)
    ep = detect_episodes(df)
    ep.to_csv(args.episodes, index=False)

    mets = compute_metrics(ep)
    with open(args.metrics, 'w') as fp:
        json.dump(mets, fp, indent=2)

    print(f"[OK] episodes → {args.episodes}")
    print(f"[OK] metrics  → {args.metrics}")
    print(json.dumps(mets, indent=2))

if __name__ == '__main__':
    main()
