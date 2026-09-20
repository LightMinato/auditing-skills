# Behavioral evaluation

Use when a recommendation claims to change routing, stopping, testing effort or permission behavior. Small structural fixes need only relevant structural checks.

## Minimal comparison

Select realistic cases for the disputed behavior: an intended trigger, a neighboring non-trigger, and a case where an important boundary must survive. For catalog composition, include a request that legitimately needs complementary skills.

Record the model/version, host, task, available tools and initial artifacts. Run the original and proposed instructions under comparable conditions, changing only the disputed instruction where practical. Use isolated fixtures and stay within authorized side effects. Repeat ambiguous outcomes rather than treating one stochastic result as proof.

Observe selection, actual actions, completion, unnecessary approvals, verification relevance, and preservation of important constraints. Context length or tool-call count alone is not quality. Prefer observable outputs and traces over asking the model to predict its behavior.

A model can be asked to quote the skill instruction behind a pause. Treat the answer as an attribution lead; inspect the trace and competing rules before concluding causation.

## Record

A compact table is enough: request, expected behavior, baseline outcome, revised outcome, constraints preserved, and evidence link. If no model execution is available, provide probe cases and label them **not run**. Unit tests of the scanner are not model evaluations.

Suggested probes:

- A read-only skill review should return evidence without modifying the target.
- A narrow typo task should not trigger an unrelated full-repository workflow.
- A request to prepare a deployment should preserve the boundary before publishing it.
- Creating a diagram and reviewing its layout may correctly use two complementary skills.
