# Roadmap

## V1 — Orchestration and tools

**Goal:** prove that an agent can choose and sequence deterministic tools while the business rules remain outside the model.

- [ ] Define claim, vehicle, and decision schemas
- [ ] Implement `get_claim_details`
- [ ] Implement `get_vehicle_details`
- [ ] Implement deterministic `calculate_coverage`
- [ ] Add Strands orchestration
- [ ] Capture tool-selection traces
- [ ] Complete the first 10 evaluation cases

**Exit criteria:** deterministic cases return the expected decision, selected tools, and tool arguments.

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
