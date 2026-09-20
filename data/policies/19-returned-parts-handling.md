---
document_id: SYN-POL-019
title: Returned Parts Handling and Inspection
category: parts-handling
component: general
market: synthetic-us
effective_date: 2026-01-01
version: "1.0"
status: active
source_uri: s3://agentic-ai-reference-architecture-exercise/policies/19-returned-parts-handling.md
classification: synthetic-public-training
---

# Returned Parts Handling and Inspection

> Synthetic training policy. Shipping, retention, and inspection rules are fictional.

## 1.0 Retention

A removed part identified for possible return must be retained for 45 calendar days after claim submission or until disposition instructions are completed, whichever occurs later. Safety-sensitive items must follow applicable fictional hazardous-material instructions.

## 2.0 Identification

The part must be labeled with the synthetic claim ID, VIN suffix, repair order, part number, removal date, and repair facility. Labels must not obscure the observed failure area or required serial number.

## 3.0 Condition preservation

The facility must protect the part from weather, contamination, disassembly, or further damage. Fluids must be contained safely. Components requiring diagnostic integrity must not be altered unless an approved inspection procedure authorizes it.

## 4.0 Shipment and chain of custody

When return is requested, the record must include request date, ship date, carrier, tracking identifier, receiving location, and receiving confirmation. Each transfer should identify the responsible party and timestamp.

## 5.0 Inspection findings

Inspection results must distinguish verified observations from hypotheses. A finding that differs from the original diagnosis creates a discrepancy under `SYN-POL-018` and may require reevaluation.

## 6.0 Missing part

Failure to retain or return a requested part may suspend evaluation and require human review. It does not permit the system to invent inspection results or automatically infer fraud or non-coverage.
