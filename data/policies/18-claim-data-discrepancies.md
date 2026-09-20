---
document_id: SYN-POL-018
title: Claim Data Discrepancy Resolution
category: data-quality
component: general
market: synthetic-us
effective_date: 2026-01-01
version: "1.0"
status: active
source_uri: s3://agentic-ai-reference-architecture-exercise/policies/18-claim-data-discrepancies.md
classification: synthetic-public-training
---

# Claim Data Discrepancy Resolution

> Synthetic training policy. Discrepancy thresholds and workflows are fictional.

## 1.0 Material discrepancies

A discrepancy is material when it could change eligibility, policy selection, causal assessment, payment, or auditability. Examples include mismatched VINs, repair dates, component identities, failure causes, or mileage differences greater than 250 miles.

## 2.0 System behavior

When a material discrepancy is detected, automated evaluation must stop and return `HUMAN_REVIEW` with reason code `CONFLICTING_INFORMATION`. The system must preserve both values and their sources rather than overwriting one with the other.

## 3.0 Source assessment

The reviewer should consider source authority, capture time, data-entry controls, supporting documents, and whether a correction is independently verifiable. Newer data is not automatically more accurate.

## 4.0 Correction record

A resolved discrepancy must record the original value, corrected value, evidence, correcting person or service, timestamp, and reason. Corrections must be traceable and must not remove the original audit history.

## 5.0 Unresolved discrepancy

If available evidence cannot resolve a material conflict, the claim remains in human review. The system may describe the conflict and request evidence, but it may not average values, select the more favorable value, or invent a reconciliation.

## 6.0 Non-material differences

Formatting differences, capitalization, or equivalent normalized representations may be corrected automatically when meaning does not change. The normalization rule must be deterministic and tested.
