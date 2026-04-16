---
name: markitdown
type: concept
module: tools
status: verified
confidence: 0.8
created: 2026-04-13
tags: [python, document-conversion, markdown, microsoft, pdf, docx, pptx, xlsx]
---

# MarkItDown — 文件转 Markdown 工具

## 概述

Microsoft 开源的轻量 Python 工具，将各种文件格式转为 Markdown。专注保留文档结构（标题、列表、表格、链接），输出适合 LLM 消费。

**仓库**：https://github.com/microsoft/markitdown
**协议**：MIT
**要求**：Python >= 3.10

## 支持的文件格式

| 格式 | 扩展名 | 依赖组 |
|------|--------|--------|
| PDF | `.pdf` | `[pdf]` |
| Word | `.docx` | `[docx]` |
| PowerPoint | `.pptx` | `[pptx]` |
| Excel | `.xlsx` | `[xlsx]` |
| 旧版 Excel | `.xls` | `[xls]` |
| 图片 | `.jpg`, `.png` 等 | 内置(EXIF)，OCR 需插件 |
| 音频 | `.wav`, `.mp3` | `[audio-transcription]` |
| HTML | `.html`, `.htm` | 内置 |
| 文本格式 | `.csv`, `.json`, `.xml` | 内置 |
| ZIP | `.zip` | 内置（迭代内容） |
| YouTube | URL | `[youtube-transcription]` |
| Outlook | `.msg` | `[outlook]` |
| EPub | `.epub` | 内置 |
| Azure 文档智能 | 任意 | `[az-doc-intel]` |

## 安装

```bash
# 完整安装
pip install 'markitdown[all]'

# 按需安装
pip install 'markitdown[pdf, docx, pptx]'

# 使用 uv
uv pip install 'markitdown[all]'
```

## 典型使用场景

### 场景1：Agent 读取 PDF 需求文档

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("requirements.pdf")
# result.text_content 包含 Markdown 文本
```

### 场景2：批量提取文件内容

```bash
# CLI 批量处理
for f in *.pdf; do markitdown "$f" -o "${f%.pdf}.md"; done
```

### 场景3：图片描述（需 LLM）

```python
from markitdown import MarkItDown
from openai import OpenAI

md = MarkItDown(llm_client=OpenAI(), llm_model="gpt-4o")
result = md.convert("diagram.png")
```

## 与 AgentFlow 的集成

- **Skill**：`.agent-flow/skills/documentation/markitdown/handler.md` — 操作 SOP
- **白名单**：`need_confirmation` 级别（pip 安装包名确认）
- **触发词**：文件转 markdown、pdf 转文本、文档解析、内容提取

## 注意事项

- `convert_stream()` 需二进制流（`open(path, "rb")`），不接受文本流
- 输出面向 LLM 消费，非高保真人类排版
- OCR 需额外 `markitdown-ocr` 插件 + OpenAI 客户端
- 推荐虚拟环境安装避免依赖冲突

## 相关条目
- [[doc-conversion]](../../skills/documentation/markitdown/handler.md) — 文档转换 Skill
