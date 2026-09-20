# Synthetic Warranty Policy Corpus

This directory contains fictional policy documents created exclusively for the V2 retrieval exercise. They do not describe the policies, practices, warranties, or obligations of any real manufacturer, dealer, supplier, or insurer.

## Metadata convention

Every document uses YAML front matter with these fields:

| Field | Meaning |
|---|---|
| `document_id` | Stable synthetic document identifier |
| `title` | Human-readable policy title |
| `category` | Retrieval and filtering category |
| `component` | Primary component scope or `general` |
| `market` | Fictional market applicability |
| `effective_date` | Date the synthetic version becomes active |
| `version` | Document version |
| `status` | Lifecycle state such as `active` |
| `source_uri` | Planned S3 source location |
| `classification` | Data-handling classification |

Numbered headings form stable citation targets. A citation should combine the document ID and section, for example: `SYN-POL-003 §3.2`.

## Retrieval boundary

Only documents with `status: active` should support a current-policy answer. Retrieval does not authorize a claim decision, payment, mutation, or write-back. If the corpus does not contain sufficient supporting evidence, the application must return an insufficient-evidence response.
