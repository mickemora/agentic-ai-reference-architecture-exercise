# V1 Data Model

| Contract | Purpose | Key controls |
|---|---|---|
| `WarrantyClaim` | Claim and repair facts | Synthetic identifiers, enumerated cause, no extra fields |
| `VehicleDetails` | Vehicle eligibility facts | Validated VIN, dates, and non-negative mileage |
| `CoverageDecision` | Auditable result | Closed decision vocabulary, reason codes, evidence gaps, policy reference |

Pydantic rejects malformed or unexpected data at the boundary. Stable reason codes make tests, metrics, traces, and future integrations independent of explanatory prose.
