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

## 文件结构

```
docx-generator/
├── SKILL.md                    # Skill 配置和文档
└── scripts/
    ├── __init__.py             # 模块导出
    └── docx_generator.py       # 核心实现
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
