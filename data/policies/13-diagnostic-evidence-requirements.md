---
document_id: SYN-POL-013
title: Diagnostic Evidence Requirements
category: documentation
component: general
market: synthetic-us
effective_date: 2026-01-01
version: "1.0"
status: active
source_uri: s3://agentic-ai-reference-architecture-exercise/policies/13-diagnostic-evidence-requirements.md
classification: synthetic-public-training
---

# Diagnostic Evidence Requirements

> Synthetic training policy. Diagnostic standards are illustrative only.

## 1.0 Evidence standard

Diagnostic evidence must be sufficient for another qualified reviewer to understand the reported symptom, tests performed, observations, failure cause, and reason for the corrective action.

## 2.0 Required diagnostic elements

When applicable, the record must include:

- Diagnostic trouble codes and freeze-frame data.
- Measured voltage, resistance, pressure, temperature, clearance, or other values.
- The fictional specification or comparison value.
- Test conditions and equipment used.
- Photographs or videos showing the relevant condition.
- Results before and after repair.

## 3.0 No-code conditions

The absence of a diagnostic trouble code does not prove that no defect exists. For intermittent, mechanical, noise, vibration, or appearance concerns, the technician must document the alternative method used to reproduce and isolate the condition.

## 4.0 Unsupported conclusions

Statements such as “part bad,” “known issue,” or “replace and retest” are insufficient without supporting observations. A model-generated summary may organize diagnostic evidence but is not itself evidence.

## 5.0 Conflicting results

If test results conflict, the claim must identify the conflict and route to human review. The system may not discard the less favorable result without a documented technical reason.

## 6.0 Reproducibility

Where practical, retain the steps needed to reproduce the test. Proprietary credentials, personal data, and unrelated vehicle information must not be copied into the claim record.
