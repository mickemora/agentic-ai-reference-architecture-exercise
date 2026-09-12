"""Local V1 entry point for the synthetic warranty decision exercise."""

from __future__ import annotations

import argparse
import json

from src.tools.warranty import calculate_coverage, get_claim_details, get_vehicle_details


def analyze_claim(claim_id: str) -> dict:
    """Run the deterministic V1 flow before LLM orchestration is introduced."""
    claim = get_claim_details(claim_id)
    vehicle = get_vehicle_details(claim["vin"])
    return calculate_coverage(vehicle=vehicle, claim=claim)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claim-id", required=True)
    args = parser.parse_args()
    print(json.dumps(analyze_claim(args.claim_id), indent=2))


if __name__ == "__main__":
    main()
