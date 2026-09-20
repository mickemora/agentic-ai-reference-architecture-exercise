---
document_id: SYN-POL-003
title: Required Claim Documentation
category: documentation
component: general
market: synthetic-us
effective_date: 2026-01-01
version: "1.0"
status: active
source_uri: s3://agentic-ai-reference-architecture-exercise/policies/03-required-claim-documentation.md
classification: synthetic-public-training
---

# Required Claim Documentation

> Synthetic training policy. This document defines fictional evidence requirements.

## 1.0 Purpose

Complete documentation allows a reviewer to verify the vehicle, reported condition, diagnosis, repair, and relationship between the failure and the requested coverage.

## 2.0 Minimum documentation

Every submitted claim must include:

1. Claim identifier and full synthetic VIN.
2. Repair order number, open date, close date, and odometer reading.
3. Customer-stated condition or symptom.
4. Technician diagnosis and identified failure cause.
5. Diagnostic trouble codes, measurements, or test results when applicable.
6. Corrective action performed and parts used.
7. Labor operations and requested amounts.

## 3.0 Evidence by risk level

### 3.1 Routine repair

A routine repair requires the minimum documentation in Section 2.0 and a clear causal diagnosis.

### 3.2 High-cost or repeat repair

A high-cost or repeat repair also requires photographs, prior-repair history, and documented technical authorization when the applicable policy requires it.

### 3.3 Modification-related condition

When a vehicle has an aftermarket modification, the submission must describe the modification and provide evidence showing whether it contributed to the failure.

## 4.0 Incomplete evidence

Missing required evidence results in `pending_review / documentation_incomplete`. The reviewer may request additional evidence. Missing documentation alone must not be converted into an approval or a definitive causal denial.

## 5.0 Evidence integrity

Documents must be attributable to the claim and must not be altered to change dates, mileage, diagnosis, or causal findings. Conflicting evidence routes to human review under `SYN-POL-018`.
