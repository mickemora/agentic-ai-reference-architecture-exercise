---
document_id: SYN-POL-002
title: Time and Mileage Limits
category: eligibility
component: general
market: synthetic-us
effective_date: 2026-01-01
version: "1.0"
status: active
source_uri: s3://agentic-ai-reference-architecture-exercise/policies/02-time-and-mileage-limits.md
classification: synthetic-public-training
---

# Time and Mileage Limits

> Synthetic training policy. All dates, limits, and rules are fictional.

## 1.0 Standard limit

Basic warranty eligibility ends at the earlier of 36 months from the in-service date or 36,000 accumulated vehicle miles. Both limits must be satisfied on the documented repair date.

## 2.0 Determining vehicle age

Vehicle age begins on the verified in-service date. The repair order open date is used as the repair date unless evidence shows the repair began earlier. Calendar months, rather than a fixed number of days, determine the 36-month boundary.

If the in-service date is missing, invalid, or inconsistent across approved systems, the claim must route to human review rather than assuming a date.

## 3.0 Determining mileage

The primary mileage value is the verified odometer reading captured when the repair order was opened. A difference greater than 250 miles between claim-reported mileage and the approved vehicle record is a material discrepancy and requires human review.

The system must not reduce mileage, substitute an earlier reading, or estimate mileage to create eligibility.

## 4.0 Boundary examples

- A vehicle at exactly 36 months and exactly 36,000 miles remains within the standard limit.
- A vehicle at 35 months and 36,001 miles exceeds the mileage limit.
- A vehicle at 37 months and 20,000 miles exceeds the time limit.
- Missing mileage is insufficient evidence for an automated recommendation.

## 5.0 Extended categories

Some component categories may have separate limits defined in their own active policies. A category-specific policy overrides the standard limit only for the components explicitly named in that policy.
