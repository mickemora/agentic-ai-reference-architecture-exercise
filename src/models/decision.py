from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class Decision(StrEnum):
    APPROVE = "APPROVE"
    DENY = "DENY"
    HUMAN_REVIEW = "HUMAN_REVIEW"


class ReasonCode(StrEnum):
    ELIGIBLE = "ELIGIBLE"
    OUTSIDE_TIME_LIMIT = "OUTSIDE_TIME_LIMIT"
    OUTSIDE_MILEAGE_LIMIT = "OUTSIDE_MILEAGE_LIMIT"
    EXCLUDED_MODIFICATION = "EXCLUDED_MODIFICATION"
    UNRELATED_MODIFICATION = "UNRELATED_MODIFICATION"
    MISSING_DOCUMENTATION = "MISSING_DOCUMENTATION"
    UNKNOWN_FAILURE_CAUSE = "UNKNOWN_FAILURE_CAUSE"
    CONFLICTING_INFORMATION = "CONFLICTING_INFORMATION"


class CoverageDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    claim_id: str
    decision: Decision
    reason_codes: list[ReasonCode]
    explanation: str
    missing_evidence: list[str]
    requires_human_review: bool
    policy_references: list[str]
