# Auditing Skills

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

用于审查现有 skill 和智能体指令文件的技能：发现误触发、不必要的约束、过多的上下文和不清晰的完成条件，提供有证据的修改建议，同时保留有价值的边界。

## 能做什么

- 审查单个 skill、技能目录，以及 `AGENTS.md` / `CLAUDE.md`。
- 区分结构错误、启发式线索、实际行为观察和对照验证。
- 区分技能职责冲突与合理的多技能协作。
- 提供只读扫描器和轻量行为评估方法。

它不是 OpenAI 官方验证器，也不进行安全审计，不会把“提示词更短”等同于“效果更好”。审查流程不依赖其他 skills 或 MCP 服务。

## 安装

可选扫描器需要 Python 3.10+ 和 PyYAML；只使用技能说明时不必运行 Python。

```bash
git clone https://github.com/LightMinato/auditing-skills.git
cd auditing-skills
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

在 macOS/Linux 中，可将仓库链接到 Codex 用户技能目录（目标不存在时执行）：

```bash
mkdir -p "$HOME/.agents/skills"
ln -s "$PWD" "$HOME/.agents/skills/auditing-skills"
```

如果该位置已安装此技能，请先备份，再更新已有安装，不要在其中嵌套另一份副本。必要时重新开启智能体会话。其他宿主的安装路径可能不同。

## 对智能体说

> 使用 $auditing-skills 审查 `/path/to/my-skill`，目标宿主是 Codex。引用有实际影响的问题并提出修改建议，只审查，不修改。

> 使用 $auditing-skills 优化 `/path/to/my-skill`，保留调用策略和必要的审批边界，并验证改动。

## 运行扫描器

在仓库根目录运行，将示例路径替换为真实目标。

```bash
.venv/bin/python scripts/audit_skills.py /path/to/skill --host codex --json
.venv/bin/python scripts/audit_skills.py /path/to/catalog --host generic
.venv/bin/python scripts/audit_skills.py /path/to/AGENTS.md
.venv/bin/python scripts/audit_skills.py /path/to/skill --max-description 500
```

`--host codex` 读取 `agents/openai.yaml` 中的 `policy.allow_implicit_invocation`；`generic` 不推断调用资格。两种模式都不模拟完整宿主加载器。`--max-description` 仅设置审查预算，不表示平台上限或实际发生截断。

退出码：**0** 无结构错误（仍可能有待判断线索）；**1** 有结构错误；**2** 输入、依赖或读取失败。JSON 包含覆盖范围和证据标签。启发式线索本身不会使命令失败。

## 限制与验证

正则规则仅覆盖英语，并只扫描指定入口文件，不审查参考文件正文，也不能检测全部中文或日文指令。这些内容需要语义审查。没有命中不代表技能质量合格。模型对暂停原因的解释是线索，不是因果证明。

```bash
.venv/bin/python tests/selftest.py
```

回归测试覆盖调用策略、合法与非法 YAML、缺失输入、预算处理、代码块示例、链接和覆盖范围报告。它们不能证明模型行为得到改善；需要时使用[行为评估方法](references/behavioral-evaluation.md)开展对照测试。本项目不宣称已完成模型效果基准测试。

## 设计与来源

入口为 [SKILL.md](SKILL.md)，按需查阅[审查规则](references/checks.md)和[技能目录审查](references/catalog-review.md)。

- [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
- [Using GPT-6 Astra](https://developers.openai.com/api/docs/guides/latest-model)
- [Source attribution and host assumptions](references/sources.md)

## 许可证

[MIT](LICENSE)。欢迎贡献，请附上真实失败案例、预期行为和相关验证。
