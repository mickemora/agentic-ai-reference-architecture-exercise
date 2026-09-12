# ADR-001: Keep Coverage Rules Deterministic

**Status:** Accepted

The LLM may interpret a request and orchestrate tools, but eligibility rules execute in ordinary code. This makes decisions reproducible, testable, explainable, and suitable for independent authorization. Ambiguity is routed to `HUMAN_REVIEW`.
