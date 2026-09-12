"""Deterministic synthetic warranty tools.

The model may select these tools, but it does not own the underlying business rules.
"""

from __future__ import annotations

CLAIMS = {
    "CLM-1001": {
        "claim_id": "CLM-1001",
        "vin": "SYNTH-VIN-0001",
        "component": "alternator",
        "failure_cause": "manufacturing_defect",
        "documentation_complete": True,
    },
    "CLM-1002": {
        "claim_id": "CLM-1002",
        "vin": "SYNTH-VIN-0002",
        "component": "alternator",
        "failure_cause": "unknown",
        "documentation_complete": False,
    },
}

VEHICLES = {
    "SYNTH-VIN-0001": {"vin": "SYNTH-VIN-0001", "age_months": 18, "mileage": 21_000},
    "SYNTH-VIN-0002": {"vin": "SYNTH-VIN-0002", "age_months": 30, "mileage": 31_000},
}


def get_claim_details(claim_id: str) -> dict:
    if claim_id not in CLAIMS:
        raise ValueError(f"Unknown synthetic claim: {claim_id}")
    return CLAIMS[claim_id].copy()


def get_vehicle_details(vin: str) -> dict:
    if vin not in VEHICLES:
        raise ValueError(f"Unknown synthetic VIN: {vin}")
    return VEHICLES[vin].copy()


def calculate_coverage(*, vehicle: dict, claim: dict) -> dict:
    """Apply intentionally simple V1 rules with explicit human-review routing."""
    if not claim["documentation_complete"] or claim["failure_cause"] == "unknown":
        decision, reason = "HUMAN_REVIEW", "Evidence is incomplete or failure cause is unknown."
    elif vehicle["age_months"] > 36 or vehicle["mileage"] > 36_000:
        decision, reason = "DENY", "Vehicle is outside the synthetic basic-coverage limits."
    elif claim["failure_cause"] == "excluded_modification":
        decision, reason = "DENY", "Failure is attributed to an excluded modification."
    else:
        decision, reason = "APPROVE", "Synthetic eligibility rules are satisfied."

    return {
        "claim_id": claim["claim_id"],
        "decision": decision,
        "reason": reason,
        "requires_human_review": decision == "HUMAN_REVIEW",
        "policy_citations": [],
    }
