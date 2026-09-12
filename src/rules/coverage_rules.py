from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from src.models import CoverageDecision, Decision, FailureCause, ReasonCode, VehicleDetails, WarrantyClaim

RULES_PATH = Path(__file__).resolve().parents[2] / "data" / "synthetic" / "coverage_rules.json"


def evaluate_coverage(claim: WarrantyClaim, vehicle: VehicleDetails) -> CoverageDecision:
    rules = json.loads(RULES_PATH.read_text(encoding="utf-8"))
    missing: list[str] = []
    reasons: list[ReasonCode] = []

    if claim.vin != vehicle.vin or abs(claim.reported_mileage - vehicle.mileage) > rules["mileage_conflict_tolerance"]:
        reasons.append(ReasonCode.CONFLICTING_INFORMATION)
    if not claim.documentation_complete:
        missing.append("required_claim_documentation")
        reasons.append(ReasonCode.MISSING_DOCUMENTATION)
    if claim.failure_cause == FailureCause.UNKNOWN:
        missing.append("confirmed_failure_cause")
        reasons.append(ReasonCode.UNKNOWN_FAILURE_CAUSE)
    if claim.failure_cause == FailureCause.UNRELATED_MODIFICATION:
        reasons.append(ReasonCode.UNRELATED_MODIFICATION)

    if reasons:
        return CoverageDecision(claim_id=claim.claim_id, decision=Decision.HUMAN_REVIEW,
            reason_codes=reasons, explanation="The claim requires human review because evidence is incomplete, ambiguous, or conflicting.",
            missing_evidence=missing, requires_human_review=True, policy_references=[rules["policy_reference"]])

    age_months = (claim.repair_date.year - vehicle.in_service_date.year) * 12 + claim.repair_date.month - vehicle.in_service_date.month
    denial_reasons: list[ReasonCode] = []
    if age_months > rules["max_age_months"]:
        denial_reasons.append(ReasonCode.OUTSIDE_TIME_LIMIT)
    if vehicle.mileage > rules["max_mileage"]:
        denial_reasons.append(ReasonCode.OUTSIDE_MILEAGE_LIMIT)
    if claim.failure_cause == FailureCause.EXCLUDED_MODIFICATION:
        denial_reasons.append(ReasonCode.EXCLUDED_MODIFICATION)
    if denial_reasons:
        return CoverageDecision(claim_id=claim.claim_id, decision=Decision.DENY,
            reason_codes=denial_reasons, explanation="The claim does not satisfy the synthetic coverage rules.",
            missing_evidence=[], requires_human_review=False, policy_references=[rules["policy_reference"]])

    return CoverageDecision(claim_id=claim.claim_id, decision=Decision.APPROVE,
        reason_codes=[ReasonCode.ELIGIBLE], explanation="The claim satisfies the synthetic coverage rules.",
        missing_evidence=[], requires_human_review=False, policy_references=[rules["policy_reference"]])
