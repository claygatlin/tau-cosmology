#!/usr/bin/env python3
"""
compare_all_runs.py v2
Compares N1, N2, and N3 with:
- Resolved vs Projected split for all runs
- Common prefix determinism check
"""

import pandas as pd
from pathlib import Path
from tav_rgc_world import RGCWorld


def load_and_filter(run_name: str, world: RGCWorld, base_dir: str = "."):
    run_dir = Path(base_dir) / run_name
    csv_files = list(run_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV found in {run_dir}")

    df = pd.read_csv(csv_files[0])
    valid = df[df["delta_n"] == 49].copy()
    corrupted = len(df) - len(valid)
    return valid, corrupted


def get_resolved_projected_split(df: pd.DataFrame, world: RGCWorld):
    resolved_ids = [c["core"] for c in world.get_resolved_cores()]
    projected_ids = world.get_projected_cores()

    resolved_frames = len(df[df["core_id"].isin(resolved_ids)])
    projected_frames = len(df[df["core_id"].isin(projected_ids)])
    return resolved_frames, projected_frames


def main():
    world = RGCWorld("tav_rgc_world.yaml")
    print("=" * 75)
    print(f"Comparing runs using: {world.name} v{world.version}")
    print("=" * 75)

    runs = ["N1", "N2", "N3"]
    results = {}

    for run in runs:
        try:
            df, corrupted = load_and_filter(run, world)
            resolved_f, projected_f = get_resolved_projected_split(df, world)

            results[run] = {
                "valid": len(df),
                "corrupted": corrupted,
                "resolved_frames": resolved_f,
                "projected_frames": projected_f,
            }

            print(f"\n{run}: {len(df):,} valid frames ({corrupted} corrupted)")
            print(f"   Resolved cores : {resolved_f:,} frames")
            print(f"   Projected cores: {projected_f:,} frames")

        except Exception as e:
            print(f"\n{run}: Could not load ({e})")
            results[run] = None

    # Summary Table
    print("\n" + "=" * 75)
    print("SUMMARY TABLE")
    print("=" * 75)
    print(f"{'Run':<6} {'Valid Frames':>14} {'Corrupted':>10} {'Resolved':>12} {'Projected':>12}")
    print("-" * 60)
    for run in runs:
        if results[run]:
            r = results[run]
            print(f"{run:<6} {r['valid']:>14,} {r['corrupted']:>10} {r['resolved_frames']:>12,} {r['projected_frames']:>12,}")

    # Common Prefix Determinism Check
    print("\n" + "=" * 75)
    print("COMMON PREFIX DETERMINISM CHECK")
    print("=" * 75)

    if results["N1"] and results["N2"]:
        df_n1, _ = load_and_filter("N1", world)
        df_n2, _ = load_and_filter("N2", world)

        min_len = min(len(df_n1), len(df_n2))
        prefix_n1 = df_n1.iloc[:min_len][["core_id", "x_raw24", "n"]].reset_index(drop=True)
        prefix_n2 = df_n2.iloc[:min_len][["core_id", "x_raw24", "n"]].reset_index(drop=True)

        match = prefix_n1.equals(prefix_n2)
        print(f"N1 vs N2 common prefix ({min_len:,} frames): {'MATCH ✓' if match else 'MISMATCH ✗'}")

    if results["N2"] and results["N3"]:
        df_n2, _ = load_and_filter("N2", world)
        df_n3, _ = load_and_filter("N3", world)

        min_len = min(len(df_n2), len(df_n3))
        prefix_n2 = df_n2.iloc[:min_len][["core_id", "x_raw24", "n"]].reset_index(drop=True)
        prefix_n3 = df_n3.iloc[:min_len][["core_id", "x_raw24", "n"]].reset_index(drop=True)

        match = prefix_n2.equals(prefix_n3)
        print(f"N2 vs N3 common prefix ({min_len:,} frames): {'MATCH ✓' if match else 'MISMATCH ✗'}")

    print("\nIntegrity Rule: Only delta_n = 49 is valid.")


if __name__ == "__main__":
    main()
