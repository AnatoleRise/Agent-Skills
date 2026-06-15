# Agent Skills

这个仓库用于管理个人和收藏的 Agent Skill。当前内容以产品需求、交互走查、文本游戏等通用工作流技能为主，同时保留一组收藏技能作为可参考或可迁移的能力库。

## 目录结构

```text
.
├── interaction-walkthrough/      # 交互走查技能
├── moyu-skill/                   # 文本游戏技能
├── requirement-review/           # PRD 需求评审技能
└── 收藏skills/                   # 收藏和参考技能
```

## 当前技能

| 目录 | 技能名 | 用途 |
|------|--------|------|
| `requirement-review/` | PRD需求评审专家 | 评审 PRD、产品需求、功能说明、验收标准和多角色需求风险 |
| `interaction-walkthrough/` | 交互走查 | 评审前端页面、Web 应用、原型、设计稿和页面流程的交互正确性 |
| `moyu-skill/` | moyu-skill | 提供井字棋、五子棋、中国象棋等文本游戏 |

## 收藏技能

`收藏skills/` 下是可复用或可参考的外部技能：

| 目录 | 用途 |
|------|------|
| `brand-guidelines/` | Anthropic 品牌颜色、字体和视觉规范 |
| `dispatching-parallel-agents/` | 多个独立任务并行分派给智能体 |
| `prd-generator/` | 生成结构化 PRD，包含中文和英文版本 |
| `security-best-practices/` | Python、JavaScript/TypeScript、Go 等技术栈的安全最佳实践 |
| `theme-factory/` | 为文档、幻灯片、报告、HTML 页面等应用主题风格 |
| `using-git-worktrees/` | 使用 Git worktree 创建隔离开发工作区 |

## 技能结构

每个技能目录通常包含一个 `SKILL.md`，部分技能还包含 `references/`、`scripts/` 或授权文件：

- `SKILL.md`：技能入口文档，定义触发条件、工作流和关键约束。
- `references/`：长参考材料、模板、检查清单或标准。
- `scripts/`：技能需要复用的脚本工具。
- `LICENSE.txt`：收藏技能自带授权说明时保留。

使用时将需要的技能目录放入目标 Agent 支持的 skills 目录，或在当前仓库内直接按 `SKILL.md` 的说明读取和执行。
