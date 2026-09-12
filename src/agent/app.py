"""Deterministic V1 entry point. Strands orchestration follows in V1.1."""

from __future__ import annotations

import argparse

from src.models import CoverageDecision
from src.tools.warranty import calculate_coverage, get_claim_details, get_vehicle_details


def analyze_claim(claim_id: str) -> CoverageDecision:
    claim = get_claim_details(claim_id)
    vehicle = get_vehicle_details(claim.vin)
    return calculate_coverage(vehicle=vehicle, claim=claim)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claim-id", required=True)
    args = parser.parse_args()
    print(analyze_claim(args.claim_id).model_dump_json(indent=2))


if __name__ == "__main__":
    main()
