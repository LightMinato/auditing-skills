# Auditing Skills

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

既存のスキルやエージェント向け指示をレビューするスキルです。誤った起動、不要な制約、過剰なコンテキスト、曖昧な完了条件を見つけ、必要な境界を維持しながら、根拠のある改善案を提示します。

## レビュー対象範囲

単一スキル、指定ディレクトリ内の全スキル、複数の配置先にあるインストール済みスキルをレビューできます。マシン全体を自動で走査しません。全体レビューではユーザー、プロジェクト、システム、有効なプラグインの配置先を確認し、明示的に指定します。キャッシュや無効なプラグインは有効なスキルとは限りません。ディレクトリのシンボリックリンクをたどり、実パスで重複と循環を防ぎ、スキップした項目を報告します。全体レビューでは競合や有用な組み合わせも確認します。

```bash
.venv/bin/python scripts/audit_skills.py ~/.agents/skills ~/.codex/skills --host codex --json
```

## 主な機能

- 単一スキル、スキル一覧、`AGENTS.md` / `CLAUDE.md` のレビュー。
- 構造上のエラー、検討候補、実際の挙動、比較検証の結果を区別。
- 競合するスキルと、有用なスキルの組み合わせを区別。
- 読み取り専用スキャナーと、軽量な挙動評価ガイドを提供。

OpenAI 公式の検証ツールでも、セキュリティ監査ツールでもありません。短いプロンプトほど優れているとは判断しません。他のスキルや MCP サーバーへの依存はありません。

## インストール

任意のスキャナーには Python 3.10 以降と PyYAML が必要です。スキルの指示だけを利用する場合、Python の実行は不要です。

```bash
git clone https://github.com/LightMinato/auditing-skills.git
cd auditing-skills
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

macOS/Linux では、Codex のユーザースキルディレクトリにリンクできます。リンク先がまだ存在しない場合に実行してください。

```bash
mkdir -p "$HOME/.agents/skills"
ln -s "$PWD" "$HOME/.agents/skills/auditing-skills"
```

すでにインストール済みの場合は、バックアップしてから既存の配置を更新してください。その中に別のコピーを作らないでください。必要に応じてエージェントのセッションを再開します。他のホストでは配置場所が異なる場合があります。

## エージェントへの依頼例

> $auditing-skills を使って `/path/to/my-skill` をレビューしてください。対象ホストは Codex です。問題箇所を引用して改善案を示し、ファイルは変更しないでください。

> $auditing-skills を使って `/path/to/my-skill` を改善してください。呼び出しポリシーと必要な承認境界を維持し、変更を検証してください。

## スキャナーの実行

リポジトリのルートで実行し、例のパスを実際の対象に置き換えてください。

```bash
.venv/bin/python scripts/audit_skills.py /path/to/skill --host codex --json
.venv/bin/python scripts/audit_skills.py /path/to/catalog --host generic
.venv/bin/python scripts/audit_skills.py /path/to/AGENTS.md
.venv/bin/python scripts/audit_skills.py /path/to/skill --max-description 500
```

`--host codex` は `agents/openai.yaml` の `policy.allow_implicit_invocation` を読み取ります。`generic` は呼び出し可否を推測しません。どちらもホストのローダー全体を再現しません。`--max-description` はレビュー用の予算であり、プラットフォームの上限や実際の切り詰めを示すものではありません。

終了コード：**0** 構造エラーなし（検討候補は残る場合あり）、**1** 構造エラーあり、**2** 入力・依存関係・読み取りの失敗。JSON には対象範囲と根拠の分類が含まれます。検討候補だけではコマンドは失敗しません。

## 制限と検証

正規表現は英語の指示と指定された入口ファイルを対象とします。参照文書の本文や、日本語・中国語の指示を網羅的に検査するものではありません。それらは意味に基づくレビューで確認します。検出結果が空でも、品質を保証しません。モデルによる停止理由の説明は手がかりであり、因果関係の証明ではありません。

```bash
.venv/bin/python tests/selftest.py
```

回帰テストは、呼び出しポリシー、正常・不正な YAML、入力の欠落、予算処理、コードブロックの例、リンク、対象範囲の報告を検証します。モデルの挙動改善を証明するものではありません。比較が必要な場合は[挙動評価ガイド](references/behavioral-evaluation.md)を使用してください。モデル性能のベンチマーク実施は主張していません。

## 設計と出典

入口は [SKILL.md](SKILL.md) です。必要に応じて[レビュー項目](references/checks.md)と[スキル一覧のレビュー](references/catalog-review.md)を参照してください。

- [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
- [Using GPT-6 Astra](https://developers.openai.com/api/docs/guides/latest-model)
- [Source attribution and host assumptions](references/sources.md)

## ライセンス

[MIT](LICENSE)。改善の提案には、具体的な失敗例、期待する挙動、関連する検証結果を添えてください。
