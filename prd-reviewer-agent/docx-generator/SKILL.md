---
name: docx-generator
description: 专业的 Microsoft Word (.docx) 文档生成器，支持复杂排版、表格、代码块、图片等功能，并强制在每页页脚注入 "AI生成，仅供参考" 的合规声明。
---

## When to Use
在以下场景自动调用此 Skill：
- **文档生成请求**：用户要求生成 Word 文档、创建 DOCX 文件、导出内容到 Word
- **报告自动化**：需要生成结构化报告、技术文档、会议纪要
- **内容格式化**：将文本、表格、代码转换为专业排版的文档
- **合规性要求**：文档需要包含 "AI生成，仅供参考" 的法律声明/免责声明
- **批量文档处理**：需要程序化生成多个格式统一的文档

**触发关键词**：
- "生成 Word 文档"、"创建 DOCX"、"导出到 Word"
- "制作报告"、"生成文档"、"保存为 docx"
- "带免责声明的文档"、"AI 声明页脚"

## Capabilities
### 核心功能
- **强制合规页脚**：自动在每页底部添加 "AI生成，仅供参考" 灰色斜体页脚，不可遗漏
- **丰富内容支持**：标题、段落、列表、表格、代码块、图片、超链接、引用块
- **专业排版**：标题层级自动格式化（一级标题居中，其他左对齐）
- **页眉页脚自定义**：支持自定义页眉文本，页脚文本可配置（默认强制 AI 声明）
- **链式 API**：流畅的接口设计，支持方法链式调用
- **样式精细化**：字体大小、颜色、加粗、斜体、对齐方式完全可控

### 高级特性
- **代码高亮**：支持多种编程语言的代码块格式化
- **表格样式**：自定义表格边框、背景色、对齐方式
- **图片处理**：支持图片插入、尺寸调整、环绕方式
- **分页控制**：手动分页、自动分页优化
- **错误验证**：参数类型检查、文件路径验证、依赖自动安装

## CLI 使用方法

除了 Python API 外，本技能还支持通过命令行界面（CLI）直接生成 DOCX 文档，无需编写代码。

### 基本命令格式

```bash
python scripts/docx_cli.py --input <markdown文件> --output <docx文件> [选项]
```

### 参数说明

| 参数 | 简写 | 必填 | 说明 |
|------|------|------|------|
| `--input` | `-i` | 是 | 输入的 Markdown 文件路径 |
| `--output` | `-o` | 是 | 输出的 DOCX 文件路径 |
| `--header` | `-H` | 否 | 自定义页眉文本 |
| `--footer` | `-f` | 否 | 自定义页脚文本（默认：AI生成，仅供参考）|
| `--font-size` | `-s` | 否 | 正文字号（默认：12）|
| `--title-font-size` | `-t` | 否 | 标题字号（默认：18）|
| `--verbose` | `-v` | 否 | 显示详细日志 |
| `--help` | `-h` | 否 | 显示帮助信息 |

### CLI 使用示例

**基本用法：**
```bash
python scripts/docx_cli.py --input document.md --output output.docx
```

**带自定义页眉：**
```bash
python scripts/docx_cli.py -i report.md -o report.docx --header "公司机密"
```

**调整字体大小：**
```bash
python scripts/docx_cli.py -i document.md -o output.docx --font-size 14 --title-font-size 20
```

**显示详细日志：**
```bash
python scripts/docx_cli.py -i document.md -o output.docx --verbose
```

## Markdown 格式规范

CLI 工具支持标准 Markdown 语法，并扩展了 frontmatter 元数据支持。

### 支持的 Markdown 语法

| 元素 | 语法示例 | 说明 |
|------|----------|------|
| 一级标题 | `# 标题` | 居中显示 |
| 二级标题 | `## 标题` | 左对齐 |
| 三级标题 | `### 标题` | 左对齐 |
| 段落 | 直接输入文本 | 自动换行 |
| 粗体 | `**粗体**` | 加粗显示 |
| 斜体 | `*斜体*` | 斜体显示 |
| 无序列表 | `- 项目` 或 `* 项目` | 圆点列表 |
| 有序列表 | `1. 项目` | 数字列表 |
| 代码块 | \`\`\`python<br>代码<br>\`\`\` | 带语言标识 |
| 行内代码 | `` `代码` `` | 等宽字体 |
| 引用 | `> 引用内容` | 缩进显示 |
| 分隔线 | `---` 或 `***` | 水平分隔线 |
| 表格 | `\| 列1 \| 列2 \|` | 支持多行多列 |
| 超链接 | `[文本](URL)` | 可点击链接 |
| 图片 | `![描述](路径)` | 插入图片 |

### Frontmatter 元数据

在 Markdown 文件开头可添加 YAML 格式的 frontmatter 来配置文档属性：

```yaml
---
title: 文档标题
author: 作者姓名
date: 2024-01-15
header: 页眉文本
footer: 自定义页脚
font_size: 12
title_font_size: 18
---
```

### Markdown 模板示例

```markdown
---
title: 项目报告
author: 张三
date: 2024-01-15
header: 内部资料
---

# 项目报告

## 项目概述

本项目旨在开发一个**智能文档生成系统**，支持以下功能：

- 自动生成 Word 文档
- 支持 Markdown 格式
- 自定义样式和布局

## 技术架构

### 核心技术栈

1. Python 3.8+
2. python-docx 库
3. Markdown 解析器

### 代码示例

```python
from scripts.docx_generator import DocxGenerator

gen = DocxGenerator()
gen.add_title("示例文档")
gen.save("output.docx")
```

## 数据表格

| 模块 | 状态 | 负责人 |
|------|------|--------|
| 核心引擎 | 已完成 | 张三 |
| CLI 工具 | 开发中 | 李四 |
| 文档站点 | 待开始 | 王五 |

## 注意事项

> 本文档由 AI 辅助生成，内容仅供参考。

---

如有疑问，请联系项目组。
```

## 文件结构

```
docx-generator/
├── SKILL.md                    # Skill 配置和文档
└── scripts/
    ├── __init__.py             # 模块导出
    ├── docx_generator.py       # 核心实现
    └── docx_cli.py             # CLI 命令行工具
```

## 使用方法

### 快速开始

```python
from scripts.docx_generator import create_simple_document

create_simple_document(
    title="我的文档",
    content="文档内容...",
    output_path="./output/document.docx"
)
```

### 创建报告

```python
from scripts.docx_generator import create_report

sections = [
    {"title": "第一章", "content": "第一章的内容"},
    {"title": "第二章", "content": "第二章的内容"}
]

create_report(
    title="报告标题",
    sections=sections,
    output_path="./output/report.docx"
)
```

### 高级用法（链式调用）

```python
from scripts.docx_generator import DocxGenerator

(DocxGenerator()
    .set_header_text("文档页眉")
    .add_title("文档标题", level=1)
    .add_paragraph("介绍段落", bold=True)
    .add_list(["要点1", "要点2", "要点3"])
    .add_code_block("print('Hello, World!')", language="Python")
    .add_quote("这是一段引用")
    .add_table([["列1", "列2"], ["数据1", "数据2"]])
    .save("./output/advanced.docx"))
```

### 样式控制

```python
gen = DocxGenerator()

gen.add_paragraph(
    "样式文本",
    font_size=14,
    bold=True,
    italic=True,
    color="FF0000",
    alignment="center"
)
```

### CLI 示例

```bash
python scripts/docx_cli.py --input document.md --output output.docx
```

## 安全注意事项

### 输入验证机制

CLI 工具实现了多层输入验证，确保处理的数据安全可靠：

- **文件类型检查**：仅接受 `.md` 和 `.markdown` 格式的输入文件
- **路径验证**：验证输入文件存在且可读，输出目录可写
- **编码检测**：自动检测并处理 UTF-8 编码的文本文件
- **内容长度限制**：防止超大文件导致内存溢出

### 路径遍历防护

为防止路径遍历攻击，CLI 工具实施了以下安全措施：

- **路径规范化**：所有路径经过 `os.path.normpath()` 和 `os.path.abspath()` 处理
- **目录限制**：输出文件只能写入到指定目录或其子目录
- **非法字符过滤**：过滤路径中的非法字符（如 `..`、`~`、`$` 等特殊符号）
- **符号链接检查**：检测并拒绝指向目录外的符号链接

### 命令注入防护

- **参数转义**：所有用户输入参数经过安全转义处理
- **禁止 shell 执行**：不通过 shell 执行任何外部命令
- **白名单验证**：页眉、页脚等文本内容仅允许白名单字符
- **HTML 转义**：自动转义 Markdown 中的 HTML 标签，防止 XSS

## 错误恢复机制

### 常见错误及解决方法

| 错误信息 | 原因 | 解决方法 |
|----------|------|----------|
| `输入文件不存在` | 指定的 Markdown 文件路径错误 | 检查文件路径是否正确，使用绝对路径或相对路径 |
| `输出目录不可写` | 没有写入权限或目录不存在 | 确保输出目录存在且有写入权限 |
| `文件格式不支持` | 输入文件不是 Markdown 格式 | 确保文件扩展名为 `.md` 或 `.markdown` |
| `编码错误` | 文件编码不是 UTF-8 | 将文件转换为 UTF-8 编码 |
| `依赖缺失` | python-docx 库未安装 | 运行 `pip install python-docx` 安装依赖 |
| `内存不足` | 文件过大或内容过多 | 分批处理或减小文件大小 |
| `图片路径错误` | Markdown 中的图片路径无效 | 确保图片路径正确，使用相对路径或绝对路径 |
| `表格格式错误` | Markdown 表格语法不正确 | 检查表格的 `|` 和 `-` 对齐方式 |

### 退出码说明

| 退出码 | 含义 | 说明 |
|--------|------|------|
| `0` | 成功 | 文档生成成功 |
| `1` | 一般错误 | 未分类的错误 |
| `2` | 参数错误 | 命令行参数无效或缺失 |
| `3` | 文件不存在 | 输入文件不存在 |
| `4` | 权限错误 | 文件或目录权限不足 |
| `5` | 格式错误 | 文件格式不支持或损坏 |
| `6` | 解析错误 | Markdown 解析失败 |
| `7` | 生成错误 | DOCX 生成过程出错 |
| `8` | 依赖错误 | 缺少必要的依赖库 |
| `9` | 安全错误 | 安全检查未通过 |

### 日志级别

使用 `--verbose` 参数可查看详细日志：

```bash
python scripts/docx_cli.py -i input.md -o output.docx --verbose
```

日志级别说明：
- **INFO**：一般信息，显示处理进度
- **WARNING**：警告信息，不影响生成但需要注意
- **ERROR**：错误信息，可能导致生成失败
- **DEBUG**：调试信息，仅在 verbose 模式下显示

## 功能特性

- ✅ **自动页脚**：每页自动添加 "AI生成，仅供参考" 页脚
- ✅ **丰富内容**：支持标题、段落、列表和表格
- ✅ **标题样式**：Level 1 标题居中，其他级别左对齐
- ✅ **高级功能**：代码块、引用、图片、超链接
- ✅ **页眉支持**：为文档添加自定义页眉
- ✅ **链式调用**：流畅的 API，代码更优雅
- ✅ **样式控制**：字体大小、颜色、加粗、斜体、对齐
- ✅ **参数验证**：全面的错误检查
- ✅ **简单易用**：初学者也能轻松使用

## API 参考

### DocxGenerator 类

| 方法 | 说明 |
|------|------|
| `set_header_text(text)` | 设置文档页眉 |
| `set_footer_text(text)` | 设置文档页脚 |
| `add_title(title, level=1)` | 添加标题（级别 1-9，Level 1 居中，其他左对齐） |
| `add_paragraph(text, **kwargs)` | 添加段落（可选样式） |
| `add_list(items, ordered=False)` | 添加无序或有序列表 |
| `add_table(data, **kwargs)` | 添加表格 |
| `add_code_block(code, language)` | 添加代码块 |
| `add_quote(text)` | 添加引用块 |
| `add_image(path, **kwargs)` | 添加图片 |
| `add_hyperlink(text, url)` | 添加超链接 |
| `add_page_break()` | 添加分页符 |
| `add_spacing(lines)` | 添加空行 |
| `save(filepath)` | 保存文档 |

### 便捷函数

| 函数 | 说明 |
|------|------|
| `create_simple_document()` | 快速创建简单文档 |
| `create_report()` | 创建结构化报告 |

## 依赖项

- python-docx>=1.1.0

**自动安装**：首次运行时，技能会自动将依赖安装到技能目录的 `lib/` 文件夹中，之后无需重复安装。

## 示例

Skill 会自动为每页添加 "AI生成，仅供参考" 页脚，样式为灰色、居中、斜体。

输出文档包含：
- 标准 Word 文档格式 (.docx)
- 您的内容（标题、段落、列表、表格等）
- 自动生成的 AI 免责声明页脚
