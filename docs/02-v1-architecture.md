# V1 Deterministic Architecture

V1 creates a stable business-services layer beneath the future agent. The model will eventually select and sequence tools, but it will not own claim facts, vehicle facts, eligibility rules, or authorization.

```mermaid
sequenceDiagram
    participant Caller
    participant ClaimTool
    participant VehicleTool
    participant Rules
    Caller->>ClaimTool: get_claim_details(claim_id)
    ClaimTool-->>Caller: validated WarrantyClaim
    Caller->>VehicleTool: get_vehicle_details(vin)
    VehicleTool-->>Caller: validated VehicleDetails
    Caller->>Rules: calculate_coverage(claim, vehicle)
    Rules-->>Caller: typed CoverageDecision
```

The JSON repositories are replaceable adapters. Later phases can swap them for Lambda and DynamoDB while preserving the tool contracts.
