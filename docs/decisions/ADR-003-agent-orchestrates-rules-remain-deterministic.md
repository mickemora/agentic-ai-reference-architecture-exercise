# ADR-003: Agent orchestrates; rules remain deterministic

## Status

Accepted

## Decision

Use Strands to interpret a request and orchestrate controlled tools. Keep claim facts in repositories and coverage decisions in the deterministic rules engine. Render decision-bearing response fields from the validated `CoverageDecision`, not from free-form model output.

## Rationale

This separates probabilistic planning from consequential business logic. It makes tool selection measurable while preventing model wording from changing a decision, reason code, human-review flag, or policy reference.

## Consequences

- The agent can be evaluated independently from the rules engine.
- A model can still choose the wrong tool or arguments; the orchestration harness must detect this.
- Changing coverage policy requires a versioned rule or policy change, not prompt editing.
- Model-generated narrative is supplementary and cannot authorize a real-world action.
