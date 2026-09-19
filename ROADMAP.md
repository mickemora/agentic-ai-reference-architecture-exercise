# Roadmap

## V1 — Deterministic foundation

- [x] Define claim, vehicle, and decision schemas
- [x] Implement `get_claim_details`
- [x] Implement `get_vehicle_details`
- [x] Implement deterministic `calculate_coverage`
- [x] Add stable decision and reason-code contracts
- [x] Complete and pass the first 10 evaluation cases
- [x] Add Strands orchestration and tool-selection traces
- [x] Add 10-case offline orchestration contract evaluation
- [ ] Run and benchmark the live orchestration dataset against Amazon Bedrock

**Current result:** V1 deterministic cases and the V1.1 offline orchestration baseline both pass 10/10. The Strands/Bedrock live path is implemented but requires configured AWS credentials, model access, and a live benchmark run.

## V2 — Retrieval

- [ ] Write 10–20 synthetic policy documents
- [ ] Create S3 document layout and metadata taxonomy
- [ ] Provision Bedrock Knowledge Base
- [ ] Compare vector-only, reranked, and agentic retrieval
- [ ] Require citations in recommendations

## V3 — Memory

- [ ] Document what may and may not be remembered
- [ ] Demonstrate short-term session continuity
- [ ] Demonstrate consent-based long-term preferences
- [ ] Test isolation, retention, deletion, and stale-memory behavior

## V4 — Security and governance

- [ ] Configure PII and content safeguards
- [ ] Add prompt-injection and poisoned-document tests
- [ ] Add contextual-grounding checks
- [ ] Enforce authorization at the tool boundary
- [ ] Add human approval for consequential actions
- [ ] Explore Automated Reasoning for formal coverage rules

## V5 — Evaluation and operations

- [ ] Expand the golden dataset to 100 cases
- [ ] Score decision, retrieval, citation, tool, safety, latency, and cost
- [ ] Integrate AgentCore Evaluations
- [ ] Emit OpenTelemetry-compatible traces
- [ ] Build a CloudWatch dashboard
- [ ] Publish final findings and architecture tradeoffs
