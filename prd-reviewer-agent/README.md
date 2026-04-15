# PRD Reviewer Agent — 跨平台需求评审智能体

一个通用的产品需求文档（PRD）评审 AI 智能体，支持在 **Claude Code**、**TRAE**、**OpenClaw** 和 **Hermes Agent** 四个平台中部署使用。

## 功能特性

- **8 大评审维度**：完整性、一致性、可测试性、可行性、清晰度、优先级、边界场景、合规性
- **14 个专业角色评审**：专家产品经理、项目经理、测试工程师、UI/UX 设计师、前端工程师、后端工程师、算法工程师、Android/iOS/PC/鸿蒙客户端工程师、安全工程师、数据工程师、DevOps/运维
- **三角色默认激活**：专家产品经理、项目经理、测试工程师（所有 PRD 自动激活）
- **角色按需自动激活**：根据 PRD 内容自动识别需要哪些角色参与评审，不相关的角色不会干扰
- **两种评审模式**：
  - 🚀 **快速扫描**：5-10 分钟完成，输出 Top 10 关键问题，适合日常快速评审
  - 🔍 **深度评审**：全维度 + 全角色覆盖，输出完整报告 + 评分矩阵 + 改进建议，适合正式评审会议
- **标准化输出**：🔴严重 / 🟡警告 / 💡建议 三级问题清单 + 综合评分
- **35+ 问题模式库**：内置常见 PRD 问题模式及改写示例
- **NESMA 合规**：内置 NESMA 功能点评估规范检查（敏感词检测 + 动宾结构校验）
- **交互式模式选择**：发送 PRD 后自动弹出模式选择，🚀 快速扫描 / 🔍 深度评审二选一
- **报告自动保存**：每次评审自动生成报告文件至 `review-reports/` 目录，支持版本管理
- **版本变更对比**：同一产品二次评审时，自动与上一版本对比，生成分数变化、问题解决追踪摘要

## 谁可以使用

- **产品经理**：写完 PRD 后自检，确保需求质量达到可开发标准
- **项目经理**：评审需求文档的排期合理性、依赖关系、风险识别
- **研发工程师（前端/后端/客户端/算法）**：从技术视角审查需求的可行性、完整性、技术风险
- **测试工程师**：检查需求是否具备可测试性、验收标准是否量化、异常场景是否覆盖
- **UI/UX 设计师**：评审交互流程完整性、用户体验一致性
- **数据工程师**：审查数据埋点方案、数据质量指标是否定义
- **安全工程师**：检查认证授权、数据加密、漏洞防护、隐私合规
- **DevOps/运维**：评审部署架构、监控告警、弹性扩容方案
- **团队 TL/技术负责人**：作为 PRD 进入开发前的质量门禁，减少返工

## 能解决什么问题

| 痛点场景 | 解决方式 |
|---------|---------|
| PRD 质量参差不齐，开发过程中频繁返工 | 8 大维度 + 14 角色标准化评审，量化评分 A/B/C/D |
| 需求遗漏关键信息（如异常流程、边界条件） | 35+ 问题模式库自动匹配，覆盖常见隐性缺陷 |
| 多人评审效率低，角色视角不全面 | 自动识别需要参与评审的角色，各角色独立输出专业视角问题 |
| PRD 修改后无法追踪改进效果 | 自动保存评审报告，二次评审时生成版本变更摘要，直观对比改进效果 |
| 缺乏统一的质量门禁标准 | 量化评分 + 严重度分级，D 级 PRD 不允许进入开发 |
| NESMA 合规要求难以手动检查 | 内置 NESMA 敏感词检测和动宾结构规范检查 |
| 评审标准不统一，不同人评审结果差异大 | 统一的评审标准和评分规则，确保评审结果可复现 |

## 评审标准

评审采用 **8 大维度 + 14 专业角色** 的量化评分体系：

- **8 大维度**：完整性(20%)、一致性(15%)、可测试性(20%)、可行性(10%)、清晰度(15%)、优先级(5%)、边界场景(10%)、合规性(5%)
- **3 级严重度**：🔴严重(-25分)、🟡警告(-10分)、💡建议(-3分)
- **4 级评级**：A(90-100)、B(75-89)、C(60-74)、D(0-59)
- **14 个专业角色**：每个角色有独立的检查清单（9-14 项/角色），按 PRD 内容自动激活

完整的量化评分标准、扣分规则、判定矩阵请查看 → [评审标准.md](评审标准.md)

---

## 文件结构

```
prd-reviewer-agent/
├── core/
│   └── SKILL.md                       # 核心评审技能（所有平台共用）
├── references/
│   ├── review-checklist.md            # 评审检查清单（24 项）
│   ├── quality-criteria.md            # 质量判定标准 + 评分规则
│   ├── report-template.md             # 评审报告模板（快速 + 深度）
│   └── common-issues.md               # 35+ 常见 PRD 问题模式库
├── platforms/
│   ├── openclaw/
│   │   └── agent.md                   # OpenClaw Agent 身份定义
│   ├── hermes/
│   │   └── SOUL.md                    # Hermes Agent 人格定义
│   └── trae/
│       └── agent-prompt.md            # TRAE Agent Prompt 参考
├── review-reports/
│   └── *.md                           # 评审报告自动生成目录
├── scripts/
│   └── deploy.py                      # 一键部署脚本
├── 评审标准.md                        # 量化评分标准（8 维度 + 14 角色检查清单）
├── CLAUDE.md                          # Claude Code 项目指引
└── README.md
```

## 快速部署

> 将以下对应指令直接复制发送给你的 AI 工具（如 TRAE、Cursor、Codex、Claude Code），让它替你完成安装。

### Claude Code

```bash
# 项目级部署（仅当前项目生效）
mkdir -p .claude/skills/prd-reviewer
cp Agents/prd-reviewer-agent/core/SKILL.md .claude/skills/prd-reviewer/
cp -r Agents/prd-reviewer-agent/references .claude/skills/prd-reviewer/

# 全局部署（所有项目生效）
mkdir -p ~/.claude/skills/prd-reviewer
cp Agents/prd-reviewer-agent/core/SKILL.md ~/.claude/skills/prd-reviewer/
cp -r Agents/prd-reviewer-agent/references ~/.claude/skills/prd-reviewer/
```

### TRAE

```bash
# 项目级部署
mkdir -p .trae/skills/prd-reviewer
cp Agents/prd-reviewer-agent/core/SKILL.md .trae/skills/prd-reviewer/
cp -r Agents/prd-reviewer-agent/references .trae/skills/prd-reviewer/

# 全局部署
mkdir -p ~/.trae/skills/prd-reviewer
cp Agents/prd-reviewer-agent/core/SKILL.md ~/.trae/skills/prd-reviewer/
cp -r Agents/prd-reviewer-agent/references ~/.trae/skills/prd-reviewer/
```

### OpenClaw

```bash
# 创建 Agent
openclaw agents add prd-reviewer \
  --identity .openclaw/agents/prd-reviewer/agent.md \
  --tools file,shell,browser \
  --description "PRD 需求评审专家"

# 复制文件
mkdir -p .openclaw/agents/prd-reviewer
cp platforms/openclaw/agent.md .openclaw/agents/prd-reviewer/agent.md

# 部署技能（可选，用于技能系统）
mkdir -p skills/prd-reviewer
cp core/SKILL.md skills/prd-reviewer/
cp -r references skills/prd-reviewer/
```

### Hermes Agent

```bash
# 部署技能
mkdir -p ~/.hermes/skills/prd-reviewer
cp core/SKILL.md ~/.hermes/skills/prd-reviewer/
cp -r references ~/.hermes/skills/prd-reviewer/

# 部署人格定义（如不使用已有 SOUL.md）
cp platforms/hermes/SOUL.md ~/.hermes/SOUL.md
```

### 一键部署

```bash
python3 Agents/prd-reviewer-agent/scripts/deploy.py all
```

## 使用方式

### 触发评审

直接向 Agent 发送 PRD 文件或内容：

```
# 快速扫描
快速评审这个 PRD: @path/to/prd.md

# 深度评审（默认模式）
深度评审这个需求文档: @path/to/prd.md

# 多角色评审
多角色评审这个 PRD: @path/to/prd.md

# 指定角色评审
指定角色评审：测试,前端,后端 @path/to/prd.md

# 跳过角色评审，仅通用评审
跳过角色评审这个 PRD: @path/to/prd.md

# 激活全部角色
激活全部角色评审: @path/to/prd.md

# 直接粘贴内容
帮我评审以下 PRD：
[粘贴 PRD 内容]
```

### 角色自动识别示例

当 PRD 中包含以下内容时，会自动激活对应角色：

| PRD 关键词 | 自动激活角色 |
|-----------|-------------|
| 所有 PRD | 专家产品经理（默认激活） |
| 所有 PRD | 项目经理（默认激活） |
| 所有 PRD | 测试工程师（默认激活） |
| H5、React、浏览器兼容 | 前端工程师 |
| API、数据库、缓存 | 后端工程师 |
| 推荐算法、大模型、Prompt | 算法工程师 |
| 页面设计、动效、交互 | UI/UX 设计师 |
| 埋点、数据看板 | 数据工程师 |
| 加密、鉴权、漏洞 | 安全工程师 |
| Android、APK | Android 客户端 |
| iOS、App Store | iOS 客户端 |
| 鸿蒙、HarmonyOS | 鸿蒙客户端 |
| 部署、监控、CI/CD | DevOps/运维 |

### 评审报告

评审报告自动生成并保存至 `review-reports/` 目录，文件名格式：`{mode}-{date}-{product_name}.md`。

**快速扫描报告示例：**

```
# PRD 快速评审报告

## 总体评分
| 指标 | 值 |
|------|-----|
| 综合评分 | 72/100 |
| 评级 | C |
| 🔴严重 | 2 个 |
| 🟡警告 | 5 个 |
| 💡建议 | 8 个 |

## Top 3 关键问题

### 1. [🔴严重] 核心功能缺少验收标准
- 位置：3.2 用户管理
- 描述：「支持用户登录注册」未定义成功标准和异常流程
- 建议：补充登录方式的验收标准（响应时间、错误提示等）
...
```

**版本变更摘要示例**（二次评审时自动生成）：

```
## 版本变更摘要（对比上一版本）

| 指标 | 上次评审 | 本次评审 | 变化 |
|------|---------|---------|------|
| 综合评分 | 52/100 | 72/100 | +20 |
| 评级 | D | C | ↑ |
| 🔴严重 | 6 个 | 2 个 | -4 |
| 🟡警告 | 7 个 | 5 个 | -2 |

### 已解决的问题（4 个）
1. 缺少产品背景与目标说明
2. 核心功能缺少验收标准
...
```

> 完整报告示例请查看 `review-reports/` 目录。

## AI 智能体集成指南

本节介绍如何将 PRD Reviewer Agent 集成到其他 AI 智能体或平台中，让其他 AI 助手能够调用评审能力。

### 方式一：作为 Skill 部署到 AI 编码助手（推荐）

这是最简单的方式，直接将 `SKILL.md` 部署到目标 AI 助手的技能目录，即可通过自然语言触发评审。

#### Claude Code

```bash
# 项目级（仅当前项目生效）
python3 scripts/deploy.py claude-code

# 全局级（所有项目生效）
python3 scripts/deploy.py claude-code  # 脚本会自动部署到 ~/.claude/skills/
```

部署后，在 Claude Code 中直接发送 "评审这个 PRD: @path/to/prd.md" 即可触发。

#### TRAE

```bash
python3 scripts/deploy.py trae
```

#### OpenClaw

```bash
# 注册为 Agent
openclaw agents add prd-reviewer \
  --identity .openclaw/agents/prd-reviewer/agent.md \
  --tools file,shell,browser \
  --description "PRD 需求评审专家"

# 部署技能文件
python3 scripts/deploy.py openclaw
```

#### Hermes Agent

```bash
python3 scripts/deploy.py hermes
```

### 方式二：作为提示词模板在其他 AI 平台复用

如果你想在非原生支持 Skill 的 AI 平台（如 ChatGPT、Gemini、通义千问、Kimi 等）中使用评审能力，可以直接加载核心提示词。

**步骤：**

1. 读取 `core/SKILL.md` 的全部内容
2. 将其作为 System Prompt 或对话的第一条消息发送给 AI
3. 在后续对话中发送 PRD 内容即可触发评审

```
# 第一步：发送 System Prompt
[粘贴 core/SKILL.md 的完整内容]

# 第二步：发送待评审的 PRD
请深度评审以下 PRD：
[粘贴 PRD 内容]
```

**注意事项：**
- `core/SKILL.md` 约 480 行，部分平台有上下文长度限制，建议确认 token 上限
- 如需更轻量的版本，可只保留 `角色定义` + `评审模式` + `触发词` 部分
- `references/` 目录下的参考文件可作为补充知识按需加载

## 定制扩展

你可以基于自身需求修改以下文件来定制评审行为：

- `references/review-checklist.md` — 添加/删除检查项
- `references/quality-criteria.md` — 调整评分规则和权重
- `references/common-issues.md` — 补充团队特有的问题模式
- `core/SKILL.md` — 调整评审流程和触发词
