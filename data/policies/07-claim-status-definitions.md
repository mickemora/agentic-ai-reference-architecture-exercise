---
document_id: SYN-POL-007
title: Claim Status Definitions
category: workflow
component: general
market: synthetic-us
effective_date: 2026-01-01
version: "1.0"
status: active
source_uri: s3://agentic-ai-reference-architecture-exercise/policies/07-claim-status-definitions.md
classification: synthetic-public-training
---

# Claim Status Definitions

> Synthetic training policy. These statuses are fictional workflow labels.

## 1.0 Status model

Claim status communicates workflow position, not final legal entitlement. A status lookup must return only the approved status and reason fields.

## 2.0 Available statuses

### 2.1 `ready_for_evaluation`

The minimum claim documentation is present and the claim may proceed to rules-based or human evaluation. This status is not an approval.

### 2.2 `pending_review`

The claim requires additional evidence, conflict resolution, specialist judgment, or another human-review condition. The reason should identify the primary blocker, such as `documentation_incomplete`.

### 2.3 `unavailable`

The requested claim cannot be returned through the approved lookup. Example reasons include `claim_not_found` or `access_not_authorized`. The response must not reveal whether an inaccessible real-world record exists.

### 2.4 `evaluation_complete`

An authorized evaluation has finished and an outcome exists in the designated system of record. This training implementation does not expose that outcome or perform write-back.

## 3.0 Status versus decision

`pending_review` and `ready_for_evaluation` are workflow statuses. They are not equivalent to `APPROVE`, `DENY`, or `HUMAN_REVIEW` recommendations produced by the synthetic coverage engine.

## 4.0 Status transitions

Only an authorized deterministic service may change status. A language model may request a status lookup and explain the returned value but may not create or transition a status.
