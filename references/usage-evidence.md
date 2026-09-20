# Usage evidence for catalog decisions

Use when the user requests usage analysis, low-use ranking, or evidence-informed catalog pruning. Do not require history access for an ordinary skill review.

## Establish the denominator

Identify the installed skills and requested roots separately from the runtime-visible catalog. State the host, available history interval, files or tasks examined, skipped or unreadable records, and whether installation dates are known. Use only history authorized for the task. Keep raw conversations, credentials and customer data out of reports and public repositories.

Distinguish explicit selection, instruction loading, execution of a skill-specific workflow, and verified successful completion. Host-injected skill blocks and successful SKILL.md reads can support loading counts; a catalog entry, skill-name mention, script path, or model assertion alone cannot prove use. Keep failed or unverified reads in a separate candidate column.

For local history without a dedicated usage event, report “tasks with observed loading evidence,” not “actual calls.” Deduplicate copied fork events and repeated loads within a task. Report explicit selection and read evidence separately, using their union for the task total. Associate reads with tool outputs when available; document detection gaps such as relative paths, batched reads, encrypted history and other clients.

Separate audits, installation checks, edits and ordinary task use where traces allow. Prefer excluding the affected turns rather than an entire long-lived task; if whole tasks are excluded, list that limitation. Preserve a small known-positive sample to check the detector. Do not interpret a skill known to be used in an excluded task as unused.

## Rank and decide

Show ascending observed counts with ties, last observed date and evidence confidence. Without installation dates and relevant task opportunities, do not call raw counts a usage rate. Zero means “not observed in this sample”; newly installed, renamed, explicit-only and rarely needed recovery skills need special care. A frequently loaded skill can still be harmful or redundant.

Combine frequency with unique value, overlap, maintenance cost, observed failures and dependencies. Distinguish the browser or other tool capability from the skill instructions that explain how to use it.

- Retain skills with useful unique knowledge, even when infrequent.
- Make specialized workflows explicit-only when the user requests that invocation policy.
- Consolidate genuinely duplicate entrypoints; inspect references and preserve the capability still needed by consumers.
- Retire unnecessary skills within authorized scope, preferably to a backup outside discovery roots, with original paths and restoration instructions.

Do not automatically delete or change policy based on a usage threshold. A ranked candidate list can be the correct result when history is insufficient. Check retained references, preserve unrelated metadata and report what changed versus what is merely recommended.

## Future measurement

If accurate ongoing counts are requested, distinguish host-supported telemetry from a proposed instrumentation scheme. Useful fields are skill identity/version, task identifier, timestamp, selection/loading/execution/outcome event and audit-versus-task purpose. Minimize retained data. Do not claim retroactive precision, invent a native counter, or install monitoring as part of an ordinary review.
