# Review checks

Use the relevant families. IDs identify areas of concern, not a mandatory checklist. The scanner covers a subset; missing matches do not clear a family.

## T — Trigger and routing

- **T1:** Is the description concise enough to distinguish the task? Only claim truncation with evidence from the selected host/version. Length is a review signal.
- **T2–T4:** Does it describe a concrete action or artifact, or claim an entire topic? Test intended and neighboring requests. Emphasis and missing English trigger words alone prove nothing.
- **T5–T6:** Where skills overlap, decide whether they compete or compose. Lists are a problem when they introduce unrelated triggers, not because they exceed a fixed count.

## C — Context and references

- **C1:** Does a multi-workflow entrypoint load irrelevant details? Move conditional material when doing so helps. Keep short single-purpose skills together.
- **C2:** Do references explain when they help? Do not require a formulaic phrase.
- **C3:** Can the agent reach needed resources from the entrypoint? Follow actual links and callers before declaring a file orphaned. The scanner checks simple relative Markdown links only; inspect images, anchors and reference-style links separately when relevant.
- **C4:** Are pre-reads proportional to the task? Keep necessary prerequisite knowledge; replace unconditional repository tours with contextual pointers.
- **C5:** Do repeated instructions drift? Establish an owner while retaining short reminders when they materially help. Instruction priority is not simply last-read-wins.

## S — Useful constraints versus unnecessary prescription

- **S1–S2:** Does a fixed sequence prevent a concrete failure? Preserve transactions, dependency ordering and fragile tool procedures. Relax ordering that adds no value.
- **S3:** Does background explain project-specific facts or merely repeat common knowledge? Expertise varies by target model.
- **S4:** Are examples distinguishable from requirements? Retain examples that clarify hard cases.

## M — Model behavior and completion

- **M1:** Does testing guidance cause unnecessary work, or prevent an actual omission? Match verification to the change and target model. Do not infer that all newer models need no testing guidance.
- **M2:** Does an approval gate protect a consequential action, user preference or policy? Reuse existing authorization, prepare reviewable work, and keep the boundary attached to the protected action.
- **M3–M4:** Is completion clear? A first draft may be the requested outcome; otherwise ensure the workflow reaches the requested implementation and relevant verification.
- **M5:** Does narration help the user or only repeat generic reasoning instructions? Preserve useful progress communication.
- **M6:** Do instructions claim inappropriate authority or conflict with host/user rules? Apply the actual instruction hierarchy; do not invent authority for audited documents.
- **M7:** Treat a model's account of why it paused as a hypothesis. Use the [evaluation guide](behavioral-evaluation.md) when attribution matters.

## P — Structure and portability

- **P1:** Validate YAML and nonempty name/description strings. Distinguish portable naming conventions from verified host restrictions. Unknown keys are not proof of rejection.
- **P2:** Investigate name/directory differences without assuming every host forbids them.
- **P3:** Check machine-specific paths against the intended audience. Personal skills can legitimately reference local resources; public skills need portable alternatives.
- **P4:** Read the selected host's invocation configuration. Codex uses `agents/openai.yaml`; generic mode makes no visibility claim. Preserve existing invocation policy unless changes are authorized.
- **P5:** Record target models when behavior depends on their strengths or weaknesses. Do not generalize one model's behavior to all agents.

## X — Catalog interactions

For multiple skills, use [catalog review](catalog-review.md): X1 context budget, X2 selection/composition, X3 conflicting instructions. Static analysis identifies candidates; runtime traces can reveal additional interactions.
