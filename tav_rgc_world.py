#!/usr/bin/env python3
"""
tav_rgc_world.py
Simple loader for tav_rgc_world.yaml
"""

import yaml
from pathlib import Path
from typing import Dict, List, Any


class RGCWorld:
    def __init__(self, yaml_path: str = "tav_rgc_world.yaml"):
        self.path = Path(yaml_path)
        with open(self.path, "r") as f:
            self.data = yaml.safe_load(f)

    @property
    def name(self) -> str:
        return self.data["name"]

    @property
    def version(self) -> str:
        return self.data["version"]

    @property
    def total_cores(self) -> int:
        return self.data["hardware"]["total_cores"]

    def get_resolved_cores(self) -> List[Dict]:
        """Return list of cores with exact period resolution."""
        return self.data["cores"]["resolved"]

    def get_projected_cores(self) -> List[int]:
        """Return list of core IDs that are lower-bounded only."""
        return self.data["cores"]["projected"]["cores"]

    def get_provenance(self) -> Dict:
        return self.data["provenance"]

    def get_simulation_config(self) -> Dict:
        return self.data["simulation"]

    def get_integrity_rule(self) -> str:
        return self.data["provenance"]["integrity_rule"]

    def is_valid_frame(self, delta_n: int) -> bool:
        """Check if a frame satisfies the delta_n = 49 integrity rule."""
        return delta_n == 49

    def summary(self) -> str:
        resolved = len(self.get_resolved_cores())
        projected = len(self.get_projected_cores())
        return (
            f"{self.name} v{self.version}\n"
            f"Total cores: {self.total_cores} "
            f"({resolved} resolved, {projected} projected)"
        )


# Example usage
if __name__ == "__main__":
    world = RGCWorld("tav_rgc_world.yaml")
    print(world.summary())
    print("\nResolved cores:", [c["core"] for c in world.get_resolved_cores()])
    print("Projected cores:", world.get_projected_cores()[:10], "...")
