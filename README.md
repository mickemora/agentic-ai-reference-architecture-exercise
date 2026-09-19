# Agentic AI Reference Architecture Exercise

A hands-on, production-minded AWS portfolio project demonstrating a reusable enterprise pattern across **orchestration, retrieval, memory, tools, guardrails, evaluation, and observability**.

> Status: V1.1 orchestration implemented — deterministic and offline orchestration suites each pass 10/10. Live Strands/Bedrock benchmarking is the next checkpoint.

## Business scenario

The reference implementation is an **Enterprise Warranty Decision Agent** operating exclusively on synthetic claims, vehicles, and policies. The system gathers structured facts, applies deterministic rules, and returns `APPROVE`, `DENY`, or `HUMAN_REVIEW` with stable reason codes and policy references.

This is an educational reference architecture—not a production claims-decision system.

## V1 architecture

```mermaid
flowchart TD
    C["Caller — future Strands agent"] --> CT["Claim tool"]
    CT --> CR["Synthetic claim repository"]
    C --> VT["Vehicle tool"]
    VT --> VR["Synthetic vehicle repository"]
    C --> RT["Coverage tool"]
    RT --> RE["Deterministic rules engine"]
    RE --> D["Typed decision + reason codes"]
```

The model will eventually orchestrate the tools. It will not own system facts, coverage rules, or authorization.

## Target AWS architecture

```mermaid
flowchart TD
    U["User / CLI"] --> A["Strands Agent"]
    A --> R["AgentCore Runtime"]
    R --> K["Bedrock Knowledge Base"]
    R --> M["AgentCore Memory"]
    R --> G["AgentCore Gateway / MCP"]
    G --> T["Lambda business tools"]
    R --> B["Bedrock Guardrails"]
    R --> E["AgentCore Evaluations"]
    R --> O["CloudWatch observability"]
```

## Implemented in V1

- Pydantic contracts for claims, vehicles, and decisions
- JSON repository adapters designed to be replaceable by AWS-backed implementations
- Independent `get_claim_details`, `get_vehicle_details`, and `calculate_coverage` tools
- Deterministic coverage logic with explicit reason codes
- Human-review routing for missing, ambiguous, unrelated-modification, and conflicting evidence
- Ten-case golden evaluation dataset and repeatable runner
- Unit tests, architectural documentation, and decision records

## Implemented in V1.1

- Local Strands agent configured for an Amazon Bedrock model
- Controlled tool registry around the three deterministic services
- Explicit orchestration instructions and trust boundaries
- Per-tool trace capture for tool name, sequence, arguments, result, and error
- Deterministic final-response formatting from validated coverage output
- Offline orchestration baseline that requires neither Strands nor AWS
- Ten orchestration scenarios covering normal, ambiguous, missing-record, bypass, and VIN-substitution requests
- Metrics for tool selection, order, argument accuracy, and decision fidelity

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
python -m evaluation.run_evaluation
python -m evaluation.run_orchestration_evaluation
python -m src.agent.app --claim-id CLM-1001
```

### Run the live Strands path

Configure AWS credentials with permission to invoke an enabled Amazon Bedrock model, then install the optional agent dependency:

```bash
pip install -e ".[dev,agent]"
export AWS_REGION=us-west-2
export BEDROCK_MODEL_ID=<your-enabled-bedrock-model-id>

python -m src.orchestration.agent \
  --prompt "Review claim CLM-1001 and explain the recommendation."
```

Run the live 10-case benchmark:

```bash
python -m evaluation.run_orchestration_evaluation --mode live
```

The live runner invokes Amazon Bedrock and may incur model usage charges. Its result is intentionally reported separately from the offline baseline.

## Documentation

- [Roadmap](ROADMAP.md)
- [Problem statement](docs/01-problem-statement.md)
- [V1 architecture](docs/02-v1-architecture.md)
- [Data model](docs/03-data-model.md)
- [V1.1 orchestration](docs/04-orchestration.md)
- [ADR-001: Deterministic business rules](docs/decisions/ADR-001-deterministic-business-rules.md)
- [ADR-002: Synthetic data only](docs/decisions/ADR-002-synthetic-data-only.md)
- [ADR-003: Agent orchestrates; rules remain deterministic](docs/decisions/ADR-003-agent-orchestrates-rules-remain-deterministic.md)

## Responsible-use boundaries

- No OEM, dealer, customer, production, or confidential data
- No autonomous claim approval or write-back
- No LLM-owned business rules or authorization
- Ambiguous and conflicting evidence routes to human review
- AWS permissions will follow least privilege; secrets will not be committed
