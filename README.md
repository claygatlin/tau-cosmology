# RGC World — tav_rgc_world.yaml

**Canonical world definition** for the Resonance Graph Core (RGC) deterministic finite-precision logistic lattice on the Tav framework.

## Overview

This package defines the real measured behavior of the 49-core RGC hardware ("Easter Lilly") based on multi-run telemetry.

- **16 cores** have periods that are *exactly resolved* by 24-bit telemetry.
- **33 cores** have periods that are only *lower bounds* (telemetry is a projection of a wider internal accumulator).
- The lattice tiles the full period-doubling route to chaos (`r_k = 3.500 + k/96`).
- Strict integrity rule: **only `delta_n = 49`** is considered valid data.

## Files

| File                      | Description                                      |
|---------------------------|--------------------------------------------------|
| `tav_rgc_world.yaml`      | Main world definition (v1.1)                     |
| `tav_rgc_world.py`        | Python loader for the world definition           |
| `example_load_run.py`     | Example: Load a single run with integrity checks |
| `compare_all_runs.py`     | Compare N1, N2, and N3 (with resolved/projected split + determinism check) |
| `README.md`               | This file                                        |

## Quick Start

```python
from tav_rgc_world import RGCWorld

world = RGCWorld("tav_rgc_world.yaml")

print(world.summary())
print("Resolved cores:", [c["core"] for c in world.get_resolved_cores()])
print("Projected cores:", world.get_projected_cores())
