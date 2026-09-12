# 01 — Problem Statement

## Objective

Create an AWS reference architecture that teams can reuse to build governed agents—not merely a chatbot. The exercise uses a synthetic warranty scenario because it requires structured system data, unstructured policy knowledge, deterministic rules, uncertainty handling, and human oversight.

## Primary interaction

Given a synthetic claim ID, the system should:

1. retrieve claim and vehicle facts through tools;
2. retrieve relevant policy passages;
3. apply deterministic eligibility rules where possible;
4. identify missing, conflicting, or risky evidence;
5. recommend `APPROVE`, `DENY`, or `HUMAN_REVIEW`;
6. cite the supporting policy;
7. record an observable execution trace.

## Architecture principles

- Use the model for interpretation and coordination, not arithmetic or authorization.
- Treat retrieved content as untrusted data, never as system instructions.
- Enforce identity and authorization at every tool boundary.
- Prefer abstention and human review when evidence is insufficient.
- Separate enterprise knowledge (retrieval) from interaction history (memory).
- Make quality measurable through a versioned golden dataset.
- Use synthetic data exclusively.

## Initial non-goals

- Production integration
- Autonomous financial or warranty approval
- Real customer, dealer, vehicle, or claim data
- A polished web UI before core behavior is measurable
- Multi-agent design without evidence that one agent is insufficient

## Initial success measures

| Measure | V1 target |
|---|---:|
| Decision accuracy on deterministic cases | 100% |
| Correct tool selection | ≥ 95% |
| Correct tool arguments | ≥ 98% |
| Unsupported factual claims | 0 |
| Sensitive-data leakage | 0 |
| P95 local execution latency | Recorded, then baselined |
