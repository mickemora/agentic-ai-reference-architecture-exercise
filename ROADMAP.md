# Roadmap

This roadmap follows the same V1–V10 enterprise Agentic AI journey presented in the main README. Each stage adds one architectural capability while preserving the project’s core principles: controlled autonomy, deterministic boundaries, measurable behavior, and clear business context.

![Enterprise Agentic AI Reference Architecture](docs/images/enterprise-agentic-ai-reference-architecture.png)


### V1.0 — Deterministic foundation

- [x] Define claim, vehicle, and decision schemas
- [x] Implement `get_claim_details`
- [x] Implement `get_vehicle_details`
- [x] Implement deterministic `calculate_coverage`
- [x] Add stable decision and reason-code contracts
- [x] Route incomplete, ambiguous, and conflicting evidence to human review
- [x] Complete and pass the first 10 golden evaluation cases

### V1.1 — Agent orchestration

- [x] Add Strands orchestration above the deterministic tools
- [x] Capture tool names, sequence, arguments, results, and errors
- [x] Preserve deterministic decision authority outside the model
- [x] Add a 10-case offline orchestration evaluation
- [x] Measure tool selection, tool order, argument accuracy, and decision fidelity
- [ ] Run and benchmark the live 10-case orchestration dataset against Amazon Bedrock

### V1.2 — Bounded Amazon Bedrock tool use

- [x] Implement the read-only `lookup_claim_status` tool
- [x] Define a strict Bedrock Converse tool schema
- [x] Validate model-supplied arguments with Pydantic
- [x] Enforce an explicit tool allowlist
- [x] Require exactly one tool request
- [x] Bound execution to one request → tool result → final response sequence
- [x] Fail closed for direct answers, malformed requests, multiple tool calls, and unknown claims
- [x] Limit tool output to the minimum approved fields
- [x] Validate known-claim and unknown-claim scenarios live
- [x] Document the technical flow, management view, controls, and test procedure

## V2 — Retrieval (RAG)

**Executive outcome:** Grounded answers from authoritative enterprise knowledge.

- [x] Write 10–20 synthetic warranty policy documents
- [x] Define document IDs, sections, categories, effective dates, and metadata taxonomy
- [ ] Create the S3 document layout
- [ ] Define typed retrieval and citation contracts
- [ ] Implement a local retrieval baseline
- [ ] Provision an Amazon Bedrock Knowledge Base
- [ ] Add a controlled `retrieve_warranty_policy` tool
- [ ] Require citations for every policy-based answer
- [ ] Create a retrieval golden dataset
- [ ] Measure document accuracy, section accuracy, citation accuracy, and groundedness
- [ ] Compare vector-only, reranked, and agentic retrieval
- [ ] Refuse unsupported answers when authoritative evidence is insufficient

## V3 — Memory

**Executive outcome:** Context-aware experiences that persist appropriately over time.

- [ ] Define what the agent may and may not remember
- [ ] Separate session history from durable memory
- [ ] Demonstrate short-term conversational continuity
- [ ] Demonstrate consent-based long-term preferences
- [ ] Prevent sensitive claim facts from becoming durable user memory
- [ ] Test user and session isolation
- [ ] Test retention, deletion, expiration, and stale-memory behavior
- [ ] Document memory governance and lifecycle controls

## V4 — Guardrails

**Executive outcome:** Policy enforcement, safety boundaries, and responsible AI controls.

- [ ] Configure sensitive-information and PII safeguards
- [ ] Add denied-topic and content controls
- [ ] Add prompt-injection and poisoned-document tests
- [ ] Add contextual-grounding checks
- [ ] Enforce authorization at every tool boundary
- [ ] Test attempted policy and tool bypasses
- [ ] Explore Automated Reasoning for formal coverage rules
- [ ] Document the separation between prompts, guardrails, authorization, and business rules

## V5 — Evaluation

**Executive outcome:** Evidence-based confidence in quality, reliability, and safety.

- [ ] Expand the golden dataset to at least 100 representative cases
- [ ] Version evaluation datasets and expected outcomes
- [ ] Score decision accuracy, retrieval accuracy, citation accuracy, and groundedness
- [ ] Score tool selection, argument accuracy, policy compliance, and safety
- [ ] Capture latency, token usage, tool calls, and estimated cost
- [ ] Add adversarial and regression suites
- [ ] Integrate AgentCore Evaluations
- [ ] Define release thresholds and quality gates
- [ ] Publish evaluation findings and known limitations

## V6 — Observability

**Executive outcome:** Visibility into agent behavior, performance, cost, and failures.

- [ ] Emit OpenTelemetry-compatible traces
- [ ] Correlate user request, model invocation, retrieval, tool calls, and final response
- [ ] Capture latency, tokens, cost, errors, and retry metrics
- [ ] Record guardrail and human-review outcomes
- [ ] Integrate AgentCore and CloudWatch observability
- [ ] Build operational dashboards
- [ ] Define alerts and service-level objectives
- [ ] Document diagnostic and incident-response procedures

## V7 — Human-in-the-Loop

**Executive outcome:** Human judgment and approval for consequential decisions.

- [ ] Define which actions require human approval
- [ ] Add explicit review and approval states
- [ ] Pause execution before consequential actions
- [ ] Support approve, reject, request-evidence, and escalate outcomes
- [ ] Preserve reviewer identity, rationale, timestamp, and evidence
- [ ] Test timeout, reassignment, and rejected-action behavior
- [ ] Measure review workload and decision turnaround time
- [ ] Document accountability and decision-rights boundaries

## V8 — Multi-Agent

**Executive outcome:** Specialized agents collaborating on complex, multi-step work.

- [ ] Define claim, policy, evidence, and review specialist responsibilities
- [ ] Add a bounded coordinator or supervisor
- [ ] Define shared-context and information-isolation rules
- [ ] Prevent circular delegation and uncontrolled agent spawning
- [ ] Add task, turn, token, time, and cost limits
- [ ] Test partial failure, conflicting recommendations, and escalation
- [ ] Compare multi-agent performance with the single-agent baseline
- [ ] Document when multi-agent complexity is justified

## V9 — MCP / Gateway

**Executive outcome:** Standardized, governed access to enterprise tools and services.

- [ ] Expose approved tools through MCP-compatible interfaces
- [ ] Integrate AgentCore Gateway
- [ ] Define tool discovery, registration, versioning, and ownership
- [ ] Add identity-aware authentication and authorization
- [ ] Apply least-privilege permissions at the tool boundary
- [ ] Add rate limits, quotas, timeouts, and revocation
- [ ] Capture tool-level audit records
- [ ] Demonstrate that orchestration can change without changing business-tool contracts

## V10 — Production

**Executive outcome:** An integrated, secure, observable, governed, and business-ready architecture.

- [ ] Deploy the agent through AgentCore Runtime or a documented alternative
- [ ] Provision AWS resources through Terraform
- [ ] Add automated tests, linting, security checks, and CI/CD
- [ ] Separate development, test, and production configuration
- [ ] Implement secrets management and least-privilege IAM
- [ ] Define availability, latency, quality, safety, and cost SLOs
- [ ] Add rollback, recovery, and disaster-response procedures
- [ ] Complete threat modeling and production-readiness review
- [ ] Publish the final reference architecture, operating model, and tradeoffs
- [ ] Demonstrate the complete governed workflow end to end
