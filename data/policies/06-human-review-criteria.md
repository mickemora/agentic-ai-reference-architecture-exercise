---
document_id: SYN-POL-006
title: Human Review Criteria
category: governance
component: general
market: synthetic-us
effective_date: 2026-01-01
version: "1.0"
status: active
source_uri: s3://agentic-ai-reference-architecture-exercise/policies/06-human-review-criteria.md
classification: synthetic-public-training
---

# Human Review Criteria

> Synthetic training policy. This document defines fictional escalation conditions.

## 1.0 Required human review

A claim must be routed to a qualified human reviewer when any of the following conditions exists:

- Required documentation or diagnostic evidence is missing.
- The reported failure cause is unknown or ambiguous.
- Claim and vehicle records contain material conflicts.
- An aftermarket modification exists but causality is not established.
- Multiple active policies appear to produce different outcomes.
- An exception, goodwill request, or policy interpretation is required.
- The requested action would create a payment, denial, write-back, or legal obligation.

## 2.0 Automated system behavior

The automated system may organize evidence, retrieve policy, identify conflicts, and recommend review. It must not resolve ambiguity by inventing facts or selecting the outcome most favorable to either party.

## 3.0 Review package

The reviewer should receive the structured claim facts, retrieved policy sections, reason codes, missing-evidence list, detected conflicts, model/tool trace, and the policy versions used. The package must distinguish verified facts from model-generated explanation.

## 4.0 Reviewer outcomes

Permitted reviewer outcomes are request additional evidence, return for correction, approve recommendation, reject recommendation, or escalate to an authorized specialist. Reviewer identity, rationale, timestamp, and supporting evidence must be retained.

## 5.0 No silent fallback

If the human-review workflow is unavailable, the system must hold the claim in a non-final state. It must not silently convert the recommendation to approval or denial.
