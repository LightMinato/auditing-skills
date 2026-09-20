# Auditing Skills

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

An agent skill for reviewing existing skills and instruction files: identify misrouting, unnecessary constraints, excessive context, and unclear completion criteria. Produce evidence and actionable revisions while preserving useful boundaries.

## Review scope

Supports one skill, every skill in specified directories, or a cross-directory audit of installed skills. Nothing scans the whole machine by default. For a global review, first inventory user, project, system and active plugin skill locations; pass those paths explicitly. Cached or disabled plugins are not necessarily active. Directory symlinks are followed with cycle prevention and real-path deduplication; skipped entries are reported. Catalog review also considers routing conflicts and useful combinations.

```bash
.venv/bin/python scripts/audit_skills.py ~/.agents/skills ~/.codex/skills --host codex --json
```

## What it does

- Reviews one skill, a catalog, or `AGENTS.md` / `CLAUDE.md`.
- Separates structural errors, heuristic candidates, observed behavior, and comparison evidence.
- Distinguishes competing skills from useful combinations.
- Provides a read-only scanner and a lightweight behavioral evaluation guide.

It is not an official OpenAI validator, a security audit, or proof that shorter prompts perform better. The review workflow does not require other skills or MCP servers.

## Install

Requires Python 3.10+ and PyYAML for the optional scanner. Skill instructions can be used without running Python.

```bash
git clone https://github.com/LightMinato/auditing-skills.git
cd auditing-skills
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

For Codex discovery on macOS/Linux, link the repository into your user skills directory (only if the destination does not already exist):

```bash
mkdir -p "$HOME/.agents/skills"
ln -s "$PWD" "$HOME/.agents/skills/auditing-skills"
```

If a skill is already installed there, back it up and update that installation deliberately; do not nest another copy inside it. Reload your agent session if necessary. Other hosts may use different installation paths.

## Use with an agent

> Use $auditing-skills to review `/path/to/my-skill`. Target Codex. Quote actionable issues and propose changes; keep the review read-only.

> Use $auditing-skills to improve `/path/to/my-skill`. Preserve its invocation policy and necessary approval boundaries, then verify the changes.

## Run the scanner

Run from the repository root; replace example paths with actual targets.

```bash
.venv/bin/python scripts/audit_skills.py /path/to/skill --host codex --json
.venv/bin/python scripts/audit_skills.py /path/to/catalog --host generic
.venv/bin/python scripts/audit_skills.py /path/to/AGENTS.md
.venv/bin/python scripts/audit_skills.py /path/to/skill --max-description 500
```

`--host codex` reads `policy.allow_implicit_invocation` from `agents/openai.yaml`. `generic` leaves invocation eligibility unknown. Neither profile simulates a full host loader. `--max-description` sets your review budget; it does not assert a platform limit or actual truncation.

Exit codes: **0** no structural errors (candidates may remain), **1** structural errors, **2** invalid input/dependency/read failure. JSON includes coverage and evidence labels. Candidates never fail the command by themselves.

## Limitations and verification

English regexes inspect selected entrypoints; they do not review reference prose or detect all Chinese/Japanese instructions. Semantic review can cover those languages. An empty result is not a quality certificate. A model's explanation of a pause is a clue, not causal proof.

```bash
.venv/bin/python tests/selftest.py
```

Regression tests cover invocation policy, valid and invalid YAML, missing input, budget handling, fenced examples, links and coverage reporting. They do not establish improved model behavior. Use [behavioral evaluation](references/behavioral-evaluation.md) for controlled comparisons; no model benchmark is claimed.

## Design and sources

Start with [SKILL.md](SKILL.md). Supporting references cover [review checks](references/checks.md) and [catalog interactions](references/catalog-review.md).

- [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
- [Using GPT-6 Astra](https://developers.openai.com/api/docs/guides/latest-model)
- [Source attribution and host assumptions](references/sources.md)

## License

[MIT](LICENSE). Contributions should include a realistic failing case, the intended behavior, and relevant verification.
