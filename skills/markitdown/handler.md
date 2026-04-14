---
name: markitdown
version: 1.0.0
trigger: markitdown, 文件转markdown, pdf转文本, docx转markdown, pptx转markdown, xlsx转markdown, 文件内容提取, 文档解析, file to markdown, document conversion
applicable_agents: [main, coder, researcher]
confidence: 0.8
abstraction: universal
created: 2026-04-13
---

# Skill: markitdown

## Trigger
当需要将文件（PDF、Word、Excel、PowerPoint、图片、音频、HTML 等）转换为 Markdown 文本时触发。适用于：
- 读取二进制文档内容供 LLM 分析
- 提取文档结构化信息
- 批量文件内容转换

## Required Reading
无前置技能要求

## What is MarkItDown

Microsoft 开源的轻量 Python 工具，将各种文件格式转为 Markdown。专注保留文档结构（标题、列表、表格、链接），输出适合 LLM 消费。

GitHub: https://github.com/microsoft/markitdown

**支持的格式**：PDF, PowerPoint(.pptx), Word(.docx), Excel(.xlsx/.xls), 图片(EXIF+OCR), 音频(EXIF+语音转录), HTML, CSV/JSON/XML, ZIP(迭代内容), YouTube URL, EPub

## Procedure

### 1. 安装

```bash
# 完整安装（推荐，含所有可选依赖）
pip install 'markitdown[all]'

# 按需安装（仅特定格式）
pip install 'markitdown[pdf, docx, pptx]'

# 使用 uv
uv pip install 'markitdown[all]'
```

**可选依赖组**：
| 组名 | 用途 |
|------|------|
| `[all]` | 全部可选依赖 |
| `[pdf]` | PDF 文件 |
| `[docx]` | Word 文件 |
| `[pptx]` | PowerPoint 文件 |
| `[xlsx]` | Excel 文件 |
| `[xls]` | 旧版 Excel 文件 |
| `[outlook]` | Outlook 邮件 |
| `[az-doc-intel]` | Azure 文档智能 |
| `[audio-transcription]` | 音频转录(wav/mp3) |
| `[youtube-transcription]` | YouTube 视频转录 |

### 2. 命令行使用

```bash
# 基本用法（输出到 stdout）
markitdown path-to-file.pdf

# 保存到文件
markitdown path-to-file.pdf -o output.md

# 管道输入
cat path-to-file.pdf | markitdown

# 启用插件
markitdown --use-plugins path-to-file.pdf

# 列出已安装插件
markitdown --list-plugins
```

### 3. Python API 使用

```python
from markitdown import MarkItDown

# 基本用法
md = MarkItDown(enable_plugins=False)
result = md.convert("test.xlsx")
print(result.text_content)

# 转换多个文件
for f in ["doc1.pdf", "doc2.docx", "data.xlsx"]:
    result = md.convert(f)
    print(result.text_content)

# 使用 LLM 进行图片描述（需 OpenAI 兼容客户端）
from openai import OpenAI
client = OpenAI()
md = MarkItDown(llm_client=client, llm_model="gpt-4o", llm_prompt="optional custom prompt")
result = md.convert("image.jpg")
print(result.text_content)

# 使用 Azure Document Intelligence
md = MarkItDown(docintel_endpoint="<endpoint>")
result = md.convert("test.pdf")
print(result.text_content)
```

### 4. Docker 使用

```bash
docker build -t markitdown:latest https://github.com/microsoft/markitdown.git
docker run --rm -i markitdown:latest < ~/your-file.pdf > output.md
```

### 5. MCP Server 集成

MarkItDown 提供 MCP Server，可用于 Claude Desktop 等 LLM 应用：

详见：https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp

## Rules
- 要求 Python >= 3.10
- 推荐使用虚拟环境安装，避免依赖冲突
- `convert_stream()` 需要二进制文件对象（如 `open(path, "rb")` 或 `io.BytesIO`），不接受文本流
- CLI 管道输入时需注意二进制内容可能需要特殊处理
- 输出面向 LLM 消费，不保证人类阅读的高保真排版
- 图片 OCR 需额外安装 `markitdown-ocr` 插件 + OpenAI 兼容客户端
- 安装需用户确认（pip install 非白名单工具包，但 pip 本身在白名单内）
