---
document_id: SYN-POL-017
title: Policy Version and Effective-Date Governance
category: governance
component: general
market: synthetic-us
effective_date: 2026-01-01
version: "1.0"
status: active
source_uri: s3://agentic-ai-reference-architecture-exercise/policies/17-policy-version-and-effective-date.md
classification: synthetic-public-training
---

# Policy Version and Effective-Date Governance

> Synthetic training policy. It defines version-control behavior for this corpus only.

## 1.0 Applicable version

Unless an active policy states otherwise, the version effective on the documented repair date governs the evaluation. Retrieval must use metadata filters to exclude draft, future, and superseded versions from a current-policy answer.

## 2.0 Required version metadata

Every policy document must include a stable document ID, version, lifecycle status, effective date, market, category, and source location. Section identifiers should remain stable when content is unchanged.

## 3.0 Superseded policy

A superseded document remains available for historical evaluation but must be labeled `superseded` and linked to its replacement. It must not be cited as current policy unless the repair date falls within its effective period.

## 4.0 Conflicting active versions

If retrieval returns multiple active versions covering the same market, category, and date, the application must not select one silently. It must return a policy-version conflict and route the case to human review.

## 5.0 Citation requirements

A citation must identify the document ID and section. When version affects interpretation, the answer must also display the version and effective date. The cited text must come from the retrieved source rather than model memory.

## 6.0 Change control

Material changes require a new version, documented rationale, approval, and effective date. Editing an active version in place is prohibited except for non-substantive formatting corrections that preserve meaning.
