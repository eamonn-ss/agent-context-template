# AI Project Context Template

一个面向 Cursor、Codex、Claude Code、Copilot 以及其他 AI Coding Agent 的通用项目级上下文模板。

核心原则：

> Chat Session 是临时上下文；Repository 是长期上下文；Git 是事实历史；代码与测试是最终事实来源。

## 目标

该模板解决以下问题：

- 新开 Agent / Chat 后需要重新探索整个项目
- 不同窗口不知道彼此做过什么
- 多个 Agent 对架构、接口或技术路线产生冲突
- 长会话压缩后遗漏关键决策
- 项目上下文文件越来越长，导致 token 浪费
- AI 把旧实验、旧假设误认为当前事实
- AI 修改代码后没有留下可供下一 Session 使用的交接信息

## 快速开始

在本仓库根目录执行初始化脚本（推荐，支持目标项目已有空/半空 `.ai/`）：

```bash
./scripts/init-ai-context.sh /path/to/your-project
```

或从本仓库根目录手动复制：

```bash
cp -r .ai /path/to/your-project/
cp AGENTS.md /path/to/your-project/
mkdir -p /path/to/your-project/.cursor/rules
cp .cursor/rules/ai-context.mdc /path/to/your-project/.cursor/rules/
cp .cursorignore.example /path/to/your-project/
mkdir -p /path/to/your-project/scripts
cp scripts/check-context.sh /path/to/your-project/scripts/
```

随后编辑目标项目中的：

```text
.ai/context.md
.ai/architecture.md
.ai/current.md
```

并运行：

```bash
./scripts/check-context.sh
```

首次进入新 Agent 时只需：

```text
Read AGENTS.md and restore project context before making changes.
```

## 上下文分层

```text
L0 Agent Protocol
   AGENTS.md
        ↓
L1 Navigation
   .ai/index.md
        ↓
L2 Stable Context
   context.md
   architecture.md
        ↓
L3 Decisions
   decisions/
        ↓
L4 Active State
   current.md
   tasks/
        ↓
L5 Session History
   handoffs/
   changelog.md
        ↓
Code / Tests / Git
```

文件骨架（task / ADR / handoff）位于 `.ai/templates/`，不要放进 `tasks/`、`decisions/`、`handoffs/` 活跃目录。

## Source of Truth

出现冲突时，按以下顺序判断：

1. 用户当前明确要求
2. 当前代码行为
3. 自动化测试 / 验收结果
4. 已接受 ADR
5. `.ai/architecture.md`
6. `.ai/context.md`
7. `.ai/current.md`
8. Handoff / Changelog
9. Chat history

注意：聊天记录不是项目事实的最终来源。

## 推荐使用方式

### 开始 Session

Agent 应：

1. 阅读 `AGENTS.md`
2. 阅读 `.ai/index.md`
3. 阅读 `.ai/current.md`
4. 按任务需要读取 architecture / ADR / task
5. 执行 `git status`
6. 查看最近 Git history
7. 检查未提交修改
8. 再开始工作

### 工作过程中

- 一个任务对应一个 Task 文件（从 `.ai/templates/TASK-000-template.md` 复制）
- 重要设计变化写 ADR
- 不把临时推理全部写入 context
- 不静默覆盖其他 Agent 的未提交修改
- 不为了“同步文档”而机械更新所有文件

### Session 结束

更新：

- 当前任务状态
- 必要的 changelog
- handoff
- 若发生架构决策，新增/更新 ADR

## 设计原则

### 1. Stable / Active 分离

稳定信息和当前状态必须分开。

### 2. Index First

Agent 不应每次读取 `.ai/` 下全部文件，而应从 `.ai/index.md` 导航。

### 3. Append History, Replace State

- `changelog.md`：追加历史
- `handoffs/`：保存交接
- `current.md`：直接覆盖为当前最新状态

### 4. Decision ≠ Discussion

只有已经形成影响后续工作的技术决定才进入 ADR。

### 5. Context Budget

上下文文件应保持短小：

- AGENTS.md：尽量 < 150 行
- index.md：尽量 < 100 行
- current.md：尽量 < 120 行
- context.md：只保留长期稳定事实
- architecture.md：只记录当前架构，不记录历史讨论

详细历史应进入 Git、ADR、handoff 或 docs。

## 推荐 Git 策略

多 Agent 并行时：

```text
main
├── feat/TASK-001-camera
├── feat/TASK-002-inspection
└── fix/TASK-003-threshold
```

尽量避免多个 Agent 同时修改同一个高冲突文件。

## Chat Session 提示词

完整 checklist 见：

- `.ai/templates/session-start.md`
- `.ai/templates/session-end.md`

### 新窗口启动

```text
Read AGENTS.md and restore project context.

Before making changes:
1. Read .ai/index.md
2. Read .ai/current.md
3. Read only task-relevant architecture, ADRs, and task files
4. Inspect git status, recent history, and uncommitted changes
5. Do not modify code yet

Then briefly summarize:
- project goal relevant to this task
- active task and status (or None)
- governing constraints / ADRs
- uncommitted changes or conflicts
- files likely involved
- recommended next action

Then continue the requested task.
```

### Session 结束

```text
Before finishing this session:
1. Verify with relevant tests/checks where possible
2. Update the active task file under .ai/tasks/ (verified results + next action)
3. Update .ai/current.md only if global project state changed
4. Append meaningful changes to .ai/changelog.md
5. Create/update a handoff under .ai/handoffs/ if work must continue elsewhere
6. Add or supersede an ADR under .ai/decisions/ only if a durable decision changed
7. Do not mechanically rewrite stable context files

Keep documents concise. Do not duplicate information already recorded elsewhere.
```

## 与工具集成

### Cursor

核心上下文放在 `AGENTS.md + .ai/`。

`.cursor/rules/ai-context.mdc` 仅负责提醒 Cursor 遵循该协议。

### Codex

以仓库根目录 `AGENTS.md` 作为统一入口。

### 其他 Agent

即使不自动识别 `AGENTS.md`，也只需在新会话中输入：

```text
Read AGENTS.md before working on this repository.
```
