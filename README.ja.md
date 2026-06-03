# Agent Work Snapshot

Agent Work Snapshot は、AIエージェントの作業状況を小さなJSONとして報告するための、read-onlyなチェックポイント契約です。

Codex、Claude Code、Gemini CLI、ローカルLLM、手元の自動化スクリプトなど、複数のAIツールを同じプロジェクトで使い始めると、誰が何を進めていて、どこで止まっていて、何を成果物として出したのかが会話ログやツールごとの履歴に散らばりがちです。人間の共同開発者や実装担当者も混ざると、状況確認はさらに難しくなります。

Agent Work Snapshot は、その散らばった作業状況を「短い作業報告」としてそろえるための仕組みです。プロジェクトオーナーやPM/PLが、複数のエージェント、複数の端末、複数メンバーとそれぞれが使うAIエージェントの作業を、安全に確認し、照合し、承認できるようにすることを目指しています。

重要なのは、このリポジトリがAIオーケストラ全体を作るものではないという点です。提供するのは、JSON Schema、Pythonの検証CLI、Markdown renderer、サンプル、テスト、ドキュメントという小さな部品です。AI管理ツールやエージェント実行環境が今後変わっても、その間に置ける安定したcontrol boundaryとして使えることを重視しています。

## 何ができるか

Agent Work Snapshot は、AIエージェントや自動化ツールが次のような情報を報告するための形式を提供します。

- どのタスクに関する報告か
- 現在の状態
- 進捗数
- 今取り組んでいる内容
- blocker
- 出力したファイルや成果物
- 次のcheckpoint予定
- この報告がいつまで有効か
- 完了候補かどうか

この報告は、タスクを直接完了させる命令ではありません。たとえば `completed_candidate` は「エージェントは完了したと思っている」という報告であり、実際にタスクを完了扱いにするかは、人間の確認、検証、承認gate、または外部のreducerが判断します。

## なぜ必要か

AIエージェントとの会話ログは便利ですが、そのまま共有・集約するには向いていません。

- 長くなりやすい
- ツールごとに形式が違う
- 個人情報や秘密情報が混ざりやすい
- プロジェクト全体の進捗管理には細かすぎる
- 複数メンバーがそれぞれAIを使うと状況が見えにくくなる

Agent Work Snapshot は、会話全文ではなく、作業管理に必要な最小限の状態だけを外に出すためのフォーマットです。

## 想定している使い方

たとえば、1つのプロジェクトで次のような作業が同時に走っている場合を想定しています。

- Codex が実装を進める
- Claude Code がレビューやドキュメント確認をする
- Gemini CLI が別の調査をする
- ローカルLLMが補助的な分類や要約をする
- 人間メンバーがそれぞれ自分のAIツールを使う

それぞれのツールが同じ小さなsnapshot形式で作業状況を出せば、プロジェクトオーナーは会話全文を読まなくても、タスク単位で状況を確認できます。

## Quick Start

Python 3.10以上が必要です。

```bash
git clone https://github.com/manabu619/agent-work-snapshot.git
cd agent-work-snapshot
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
agent-work-snapshot --version
agent-work-snapshot validate examples/codex.snapshot.json
agent-work-snapshot render examples/codex.snapshot.json
```

絶対パスを警告ではなくエラーとして扱いたい場合:

```bash
agent-work-snapshot validate --strict-paths examples/codex.snapshot.json
```

## Snapshotの例

```json
{
  "schema_version": "agent-work-snapshot/v1",
  "snapshot_id": "snap_example_0001",
  "agent_id": "example-coding-agent",
  "parent_task_id": "task_example_0001",
  "observed_at": "2026-01-01T00:00:00Z",
  "source": "local_file",
  "status": "working",
  "progress": {"total": 3, "completed": 1, "blocked": 0},
  "current_focus": "Add validation tests",
  "blockers": [],
  "outputs": ["tests/test_validation.py"],
  "next_checkpoint_at": "2026-01-01T01:00:00Z",
  "ttl_seconds": 3600
}
```

## 上位概念：WBS-driven Agent Control

Agent Work Snapshotは、上位概念 WBS-driven Agent Control (WdAC)の配下で最大の結果をもたらします。WdACは、PMやPLがWBSでタスクと担当者を管理するという、現場に馴染みのあるプロジェクト管理の型を、AI駆動開発に持ち込む考え方です。

PMBOK、ITSM、SI、Webサービス開発、社内システム開発など、現場によって名称や粒度は違っても、「タスクを分ける」「担当を決める」「進捗を確認する」「完了を承認する」という共通の管理方法です。WdACは、この管理の型を全てのエージェントに適用します。

ここでいう「エージェント」はAIだけではありません。Codex や Claude Code のようなAIツール、ローカル自動化、共同開発者、人間の実装担当者など、プロジェクト上で作業する全てを含みます。誰が作業していても、管理者が確認したいのは「どのタスクが、誰によって、どこまで進み、何が出て、承認してよい状態なのか」という点に尽きます。

Agent Work Snapshot は、そのための最小の報告フォーマットです。各エージェントや担当者は会話全文ではなく、タスクに紐づいた短いsnapshotを提示します。管理者はそれを正本のタスクモデルと照合し、必要に応じてレビューし、承認します。snapshotはあくまで定型化された報告手法であり、作業者がタスクの正本を書き換えないことがポイントです。

Agent Work Snapshot は、AI時代向けにまったく新しい管理手法を作るというより、すでに現場で信頼されているWBSベースの管理をAI駆動開発に拡張するための小さな部品です。

詳しくは [WBS-driven Agent Control](docs/wbs-driven-agent-control.md) を参照してください。

## PlanExeとの違い

PlanExe は、goalから計画やWBSを作り、実行に使える形にするplanner/executor patternに近いプロジェクトです。

Agent Work Snapshot は、それとは別の境界を扱います。すでに存在するWBSやタスクモデルに対して、AIエージェントの作業状況をread-only checkpointとして返すcontrol-plane/checkpoint patternに近いものです。

この2つは競合するものではありません。PlanExeのような仕組みで計画を作り、Agent Work Snapshotで実行中のcheckpointを返す、というように補完的に使えます。

## このリポジトリがしないこと

Agent Work Snapshot は、次のものではありません。

- 完全なAIオーケストラ
- プロジェクト管理ツールの置き換え
- agent-to-agent通信プロトコル
- 承認ワークフローサービス
- reducer実装
- dashboard、scheduler、dispatcher、chat bot
- 会話全文、prompt、chain of thoughtの保存場所

小さく保つことで、他のAI管理ツールや将来の実行環境にも組み込みやすい部品にする方針です。

## Privacy

snapshotには、作業管理に必要な最小限の情報だけを入れてください。

入れてはいけないもの:

- APIキー、token、credential
- 個人情報
- 実在のhost名
- ローカルPC固有の絶対パス
- 会話全文
- prompt履歴
- chain of thought

validatorは簡単なpolicy checkを行いますが、完全なDLPツールではありません。公開や外部送信の前には、別途secret scanと人間レビューを行ってください。

## License

Apache License 2.0. See [LICENSE](LICENSE).
