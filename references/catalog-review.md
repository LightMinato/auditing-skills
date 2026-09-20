# Catalog review

Use for a multi-skill audit, not as a prerequisite for reviewing one skill.

## Scope and visibility (X1)

Separate discovered files, configured invocation eligibility, and skills actually exposed by the host. A local scanner cannot establish the runtime catalog. Record the host/version and unknowns. Count descriptions if useful, but do not equate characters with tokens or assume a universal truncation limit.

Explicit-only invocation can be appropriate for a deliberately selected workflow. It is not a general remedy for a large catalog and should not be enabled without authorization to change invocation behavior.

## Selection and composition (X2)

Use realistic requests to specify the intended skill or skill combination, including requests that need none. Overlap can be useful: diagram creation and design review may cooperate. Identify competing responsibilities, unnecessary duplication, and aggregator/member boundaries rather than insisting on one skill per request.

Catalog-only routing probes are cheap approximations. Compare them with actual selections when available; do not label a lexical similarity score a routing defect.

## Conflicts and pruning (X3)

For a questionable instruction, ask what failure or preference it addresses, whether evidence still supports it on the target model, and where enforcement belongs.

Move deterministic enforcement to schemas, validators or permissions where practical. Retain concise instructions explaining the contract, how to invoke checks, and what to do with failures. Keep intent and non-obvious rationale discoverable.

Choose retain, clarify, move or delete based on evidence and authorized scope. Do not delete merely because a rule is old or strict. Report unresolved conflicts and missing coverage separately from confirmed defects.

## Usage-informed decisions (X4)

When usage history is relevant, follow [usage evidence](usage-evidence.md). Rank observed task counts separately from success or usefulness; combine them with overlap, dependencies and user preferences before pruning.
