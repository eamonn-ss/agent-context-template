<p align="center">
  <a href="./README.md">English</a> |
  <strong>简体中文</strong>
</p>

# agent-context-template

## 1. 项目介绍

`agent-context-template` 是一套厂商无关的 Context 生命周期协议，用于在
Codex、Cursor、Claude Code 等编码 Agent 之间持久化项目状态、保存有证据的
Memory、移交 Session 并恢复上下文。它只要求 Markdown 和 Python 3.10+；Git
是有价值但可选的证据来源。

## 2. 要解决的问题

聊天会结束，假设会漂移。旧布局还会把框架自己的 `docs/`、`scripts/`、
`tests/` 与业务项目的同名目录并列，使 Context System 难以安全嵌入真实仓库。

## 3. 核心思想

```text
Rules           AGENTS.md
Discovery       .agents/skills/
Context Root    .agent-context/
Canonical State .agent-context/state/
Evidence        业务代码、测试和可选 Git
```

仓库证据高于 canonical prose；canonical state 高于 Memory、Handoff、历史和
Agent 原生 Memory。

## 4. 架构

`.agents/` 只保存 Agent 可发现的能力。`.agent-context/` 保存 Context System
的状态、Memory、历史、工具、模板、文档、集成和框架测试。这是 DEC-0003
确定的 V2.2 边界。

## 5. 快速开始

预览或安装 embedded profile：

```bash
.agent-context/scripts/init-ai-context.sh --dry-run /path/to/project
.agent-context/scripts/init-ai-context.sh /path/to/project
```

接入后，业务项目仍保留原有结构：

```text
your-project/
├── src/
├── docs/                  # 业务文档
├── scripts/               # 业务脚本
├── tests/                 # 业务测试
├── .agents/
│   └── skills/
└── .agent-context/
    ├── state/
    ├── memory/
    ├── sessions/
    ├── archive/
    └── scripts/
```

首次运行 `/project-init`；每个新 Session 运行 `/context-start`；结束有意义但
未完成的工作前运行 `/session-handoff`。

## 6. Context 生命周期

`context-start` 路由到 `INIT_REQUIRED`、`BOOTSTRAP` 或 `RESUME`，并包含对应步骤。
Fact 必须有 Evidence，Decision 保留理由，Compaction 提取持久知识后再归档。

## 7. Skills

| Skill | 用途 |
|---|---|
| `project-init` | 首次接入时初始化 Project 和 Architecture |
| `context-start` | 路由会话并只加载对应视图 |
| `session-handoff` | 跨 Session/工具移交已验证工作 |
| `record-decision` | 新增或取代持久决策 |
| `context-compact` | 提取知识并归档合格摘要 |

## 8. Namespace Isolation

业务项目原有 `docs/`、`scripts/`、`tests/`、`templates/`、`integrations/`
保持自己的职责；Context System 自身资产统一隔离在 `.agent-context/`。唯一单独
保留的框架目录是用于 Agent 自动发现的 `.agents/skills/`。不要把框架实现当成
业务源码。

## 9. Non-invasive Installation

安装器不会覆盖已有文件、修改业务源码，也不会向通用业务目录写入框架资产。
已有 `AGENTS.md` 会被跳过。安装器报告已安装版本、检测明确的 V2.1 `.agent/`
marker，并支持不写文件的 `--dry-run` 预览。

## 10. Development vs Embedded Profile

默认 `--profile embedded` 只安装生命周期 Skills、状态骨架、运行脚本、必要模板、
元数据和轻量可选配置。`--profile development` 额外安装框架文档、集成和测试，
但这些内容仍全部位于 `.agent-context/`。

## 11. 目录结构

模板仓库使用完整 development layout：

```text
.
├── AGENTS.md
├── .agents/skills/
└── .agent-context/
    ├── VERSION
    ├── state/        ├── memory/       ├── decisions/
    ├── sessions/     ├── archive/      ├── scripts/
    ├── templates/    ├── docs/         ├── integrations/
    └── tests/
```

旧 `.ai/` 目录只作为 V1 迁移证据保留。

## 12. Context Root Discovery

Python 工具从当前目录逐级向上查找 `.agent-context/`，因此可以在
`src/module/` 中运行，不要求 shell 位于仓库根目录。`context_paths.py` 集中定义
Context、state、memory、sessions 和 archive 路径。

## 13. V2.1 Migration

系统会检测 V2.1 `.agent/` 状态，但不会长期双写。预览并执行一次性迁移：

```bash
python .agent-context/scripts/migrate_v21_to_v22.py --dry-run
python .agent-context/scripts/migrate_v21_to_v22.py
```

目标存在不同内容时会阻断迁移。详见
[`migration-v2.1-to-v2.2.md`](.agent-context/docs/migration-v2.1-to-v2.2.md)。

## 14. Vendor Integrations

Cursor、Codex 和 Claude 通过根目录 `AGENTS.md` 与 `.agents/skills/` 工作；
[`.agent-context/integrations/`](.agent-context/integrations/) 下的说明只是薄适配层。
canonical state 不会迁入厂商原生 Memory。

## 15. 验证与测试

```bash
python .agent-context/scripts/context_start.py
python .agent-context/scripts/context_status.py
python .agent-context/scripts/validate_context.py
python .agent-context/scripts/compact_sessions.py
python -m unittest discover -s .agent-context/tests -v
```

无 Git 项目仍可运行，只会明确显示 Git evidence unavailable。Validator warning
不导致失败，阻断性错误返回非零状态。

## 16. Roadmap

- V2.0：Context lifecycle foundation。
- V2.1：首次初始化、`context-start` 和双语文档。
- V2.2：Namespace isolation 与 non-invasive installation。
- V2.3：Context freshness / state drift detection。
- V2.4：可选本地 search / retrieval。
- V3：可选 MCP Context Server。

详见完整[协议](.agent-context/docs/protocol.md)、
[设计原则](.agent-context/docs/design-principles.md)和
[V1 迁移指南](.agent-context/docs/migration-v1-to-v2.md)。
