#!/usr/bin/env python3
"""
example_load_run.py
Demonstrates how to load an RGC run (N1/N2/N3) while respecting
the integrity rules defined in tav_rgc_world.yaml.
"""

import pandas as pd
from pathlib import Path
from tav_rgc_world import RGCWorld


def load_run(run_name: str, world: RGCWorld, base_dir: str = ".") -> pd.DataFrame:
    """
    Load a run CSV and apply the delta_n = 49 integrity filter.
    
    Args:
        run_name: 'N1', 'N2', or 'N3'
        world: Loaded RGCWorld instance
        base_dir: Directory containing the N1/, N2/, N3/ folders
    """
    run_dir = Path(base_dir) / run_name
    csv_files = list(run_dir.glob("*.csv"))
    
    if not csv_files:
        raise FileNotFoundError(f"No CSV found in {run_dir}")
    
    csv_path = csv_files[0]  # Take the first CSV found
    print(f"Loading {csv_path.name} ...")
    
    df = pd.read_csv(csv_path)
    
    # Apply integrity rule from the world definition
    valid_mask = df["delta_n"] == 49
    invalid_count = (~valid_mask).sum()
    
    if invalid_count > 0:
        print(f"  WARNING: Found {invalid_count} frames with delta_n != 49 (flagged as corrupted)")
    
    df_valid = df[valid_mask].copy()
    print(f"  Valid frames: {len(df_valid):,} / {len(df):,}")
    
    return df_valid


def main():
    # Load the world definition
    world = RGCWorld("tav_rgc_world.yaml")
    print(world.summary())
    print()
    
    # Example: Load N2 (current reference run)
    df = load_run("N2", world)
    
    # Show basic stats
    print("\nPer-core frame counts (after filtering):")
    core_counts = df.groupby("core_id").size()
    print(core_counts.head(10))
    
    # Example: Get only resolved cores
    resolved_ids = [c["core"] for c in world.get_resolved_cores()]
    df_resolved = df[df["core_id"].isin(resolved_ids)]
    print(f"\nFrames from resolved cores only: {len(df_resolved):,}")
    
    # Example: Get only projected cores
    projected_ids = world.get_projected_cores()
    df_projected = df[df["core_id"].isin(projected_ids)]
    print(f"Frames from projected cores only: {len(df_projected):,}")


if __name__ == "__main__":
    main()
