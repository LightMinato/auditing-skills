# Sources and host assumptions

Reviewed 2026-09-20. These documents can change; check the target host/version before asserting loader behavior.

- [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra): precise triggers, progressive disclosure, contextual pre-reads, model-dependent scaffolding, boundaries and completion.
- [Using GPT-6 Astra](https://developers.openai.com/api/docs/guides/latest-model): instruction following, calibrated verification and diagnostic transparency. The latest-model URL is mutable.
- [Codex skill metadata](https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/references/openai_yaml.md): `policy.allow_implicit_invocation` in `agents/openai.yaml`; false disables implicit invocation, true is the default.

The evidence levels, probe design, regex patterns and optional review budgets in this repository are author recommendations. The articles do not establish a universal 500-character limit, require one skill per task, or recommend removing all tool-enforced rules from prose.

The scanner's generic profile validates basic document structure without claiming runtime visibility. Its Codex profile reads the documented invocation setting; it does not emulate a complete loader or guarantee acceptance. Other hosts require contextual inspection. No DSH-specific defaults are applied.
