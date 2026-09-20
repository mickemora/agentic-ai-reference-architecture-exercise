---
document_id: SYN-POL-014
title: Repeat Repair Review Guidelines
category: review
component: general
market: synthetic-us
effective_date: 2026-01-01
version: "1.0"
status: active
source_uri: s3://agentic-ai-reference-architecture-exercise/policies/14-repeat-repair-guidelines.md
classification: synthetic-public-training
---

# Repeat Repair Review Guidelines

> Synthetic training policy. Repeat-repair thresholds are fictional.

## 1.0 Definition

A repeat repair is a subsequent visit within 90 days for the same symptom, component, or underlying failure mechanism. Similar wording alone does not establish that two repairs are related.

## 2.0 Required review

The reviewer must compare the prior customer concern, diagnosis, corrective action, installed parts, mileage, and post-repair result with the current visit. The review should determine whether the original repair was incomplete, a replacement part failed, or a new condition exists.

## 3.0 Additional evidence

Repeat repairs require prior repair orders, current diagnostic results, part history, and an explanation of why the proposed action differs from or repeats the earlier repair. A third related visit requires specialist escalation.

## 4.0 Coverage handling

A repeat visit is not automatically excluded and must not be automatically approved. Eligibility depends on the verified cause and active policy. If the prior repair introduced the current failure, the case requires human review and separate accountability assessment.

## 5.0 Customer-impact signal

The system may flag repeat repairs for priority handling because of increased customer impact. Priority affects workflow timing only; it must not change evidence requirements or the coverage recommendation.

## 6.0 Duplicate distinction

A repeat repair is a new service event. A duplicate claim is a second submission for the same service event. Suspected duplicates follow `SYN-POL-009` rather than this policy.
