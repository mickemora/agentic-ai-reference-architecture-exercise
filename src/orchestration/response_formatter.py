from src.models import CoverageDecision


def format_decision(decision: CoverageDecision) -> str:
    """Render only validated deterministic output, never free-form model conclusions."""
    reasons = ", ".join(reason.value for reason in decision.reason_codes)
    policies = ", ".join(decision.policy_references)
    review = "Yes" if decision.requires_human_review else "No"
    return (
        f"Claim: {decision.claim_id}\n"
        f"Recommendation: {decision.decision.value}\n"
        f"Reason codes: {reasons}\n"
        f"Human review required: {review}\n"
        f"Policy references: {policies}\n"
        f"Explanation: {decision.explanation}"
    )
