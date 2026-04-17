---
name: markitdown
type: tool
module: tools
status: verified
confidence: 0.8
created: 2026-04-13
last_validated: 2026-04-16
tags: [python, document-conversion, markdown, microsoft, pdf, docx, pptx, xlsx]
---

# MarkItDown — 文件转 Markdown 工具

Microsoft 开源的轻量 Python 工具，将各种文件格式转为 Markdown。专注保留文档结构（标题、列表、表格、链接），输出适合 LLM 消费。

**仓库**：https://github.com/microsoft/markitdown | **协议**：MIT | **要求**：Python >= 3.10

## 支持格式

PDF, Word(.docx), PowerPoint(.pptx), Excel(.xlsx/.xls), 图片(内置EXIF, OCR需插件), 音频, HTML, CSV/JSON/XML, ZIP, YouTube, Outlook(.msg), EPub, Azure文档智能

## 快速上手

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("requirements.pdf")  # result.text_content 包含 Markdown 文本
```

```bash
pip install 'markitdown[all]'           # 完整安装
pip install 'markitdown[pdf, docx]'     # 按需安装
```

## 注意事项

- `convert_stream()` 需二进制流（`open(path, "rb")`），不接受文本流
- OCR 需额外 `markitdown-ocr` 插件 + OpenAI 客户端
- 推荐虚拟环境安装避免依赖冲突

## 完整操作 SOP

详见 [[markitdown-skill|skills/documentation/markitdown/handler]] — 包含 CLI/Docker/MCP 用法、依赖组详细表格、完整格式列表和故障排除。

## 相关条目

- [[markitdown-skill|skills/documentation/markitdown/handler]] — 文档转换 Skill（权威操作参考）
