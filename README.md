# 📚 Read Paper Skill

<div align="center">

**AI驱动的arXiv论文精读助手**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0-orange.svg)](https://github.com)

*让论文阅读更高效、更深入、更有条理*

</div>

---

## ✨ 核心特性

- 🤖 **双阶段智能架构** - 脚本机械化准备 + AI创造性分析
- 📥 **一键下载论文** - 自动获取arXiv论文PDF和TeX源码
- 🖼️ **智能图片提取** - 从TeX源码中提取所有图表
- 🎯 **AI优先级判断** - 智能识别核心架构图和关键实验结果
- 📝 **结构化笔记生成** - 自动生成完整的精读笔记模板
- 🔄 **图文并茂** - 图片智能穿插在对应章节，而非堆砌末尾
- 📊 **任务追踪** - 完整的7步骤工作流，确保不遗漏关键环节

---

## 📋 目录

- [安装](#-安装)
- [快速开始](#-快速开始)
- [工作流程](#-工作流程)
- [文件结构](#-文件结构)
- [配置说明](#-配置说明)
- [常见问题](#-常见问题)
- [贡献指南](#-贡献指南)
- [许可证](#-许可证)

---

## 🚀 安装

### 前置要求

- Python 3.8 或更高版本
- pip 包管理器

### 系统依赖（PDF转PNG）

<details>
<summary><b>Linux (Ubuntu/Debian)</b></summary>

```bash
sudo apt-get install poppler-utils imagemagick
```

</details>

<details>
<summary><b>macOS</b></summary>

```bash
brew install poppler imagemagick
```

</details>

<details>
<summary><b>Windows</b></summary>

1. 下载并安装 [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/)
2. 下载并安装 [ImageMagick](https://imagemagick.org/script/download.php#windows)
3. 将安装路径添加到系统环境变量

</details>

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/your-username/read-paper-skill.git

# 进入目录
cd read-paper-skill

# 安装Python依赖
pip install requests
```

---

## 🎯 快速开始

### 基本用法

```bash
# 使用arXiv链接
python -m scripts.main https://arxiv.org/abs/2401.12345

# 使用arXiv ID
python -m scripts.main 2401.12345

# 指定输出目录
python -m scripts.main 2401.12345 --output-dir my-papers/
```

### 完整工作流

**阶段一：机械化准备（Python脚本）**

```bash
cd read-paper-skill
python -m scripts.main https://arxiv.org/abs/2401.12345 --output-dir paper
```

脚本会自动完成：
1. ✅ 解析arXiv ID，获取论文元数据
2. ✅ 创建规范的文件夹结构
3. ✅ 下载PDF和TeX源码
4. ✅ 提取所有图片到临时目录
5. ✅ PDF自动转换（阶段一完成）
6. ✅ 生成图片清单（`images.md`）
7. ✅ 生成笔记模板（`[论文名].md`）

**阶段二：AI深度分析**

AI助手会自动：
1. 📖 读取图片清单，视觉分析每张图片
2. 🎯 判断图片优先级（高/中/低）
3. 🔧 调用脚本处理选中图片
4. 📚 深度阅读PDF和TeX源码
5. ✍️ 填充完整的精读笔记
6. 🖼️ 智能穿插图片到对应章节

---

## 🔄 工作流程

### 流程图

```
┌─────────────────────────────────────────────────────────────┐
│                     阶段一：机械化准备                        │
│                    （Python脚本自动完成）                      │
├─────────────────────────────────────────────────────────────┤
│  1. 解析arXiv链接 → 获取论文元数据                            │
│  2. 创建文件夹结构 → pdf/, tex/, images/, .temp_images/      │
│  3. 下载论文文件 → PDF + TeX源码                              │
│  4. 提取图片 → 提取所有图表到.temp_images/目录                    │
│  5. 自动转换 → PDF转PNG（使用pdftoppm或ImageMagick）           │
│  6. 生成清单 → images.md (图片预览)                            │
│  7. 生成模板 → [论文名].md (空章节，待填充)                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     阶段二：AI深度分析                        │
│                    （AI助手创造性工作）                        │
├─────────────────────────────────────────────────────────────┤
│  1. 验证输出 → 检查images.md和[论文名].md                      │
│  2. 视觉分析 → 逐个查看图片，判断优先级                       │
│  3. 处理图片 → 调用process_selected_images.py脚本处理选中图片 │
│  4. 深度阅读 → 分析PDF和TeX源码                              │
│  5. 填充笔记 → 图文并茂的完整精读笔记                         │
│  6. 更新状态 → 标记为"已完成"                                │
│  7. 输出反馈 → 生成摘要报告                                  │
└─────────────────────────────────────────────────────────────┘
```

### 图片优先级判断标准

| 优先级 | 图标 | 类型 | 判断标准 |
|--------|------|------|----------|
| **高** | 🔴 | 架构/方法图 | 模型整体架构、网络结构、系统流程图、核心组件设计 |
| **中** | 🟡 | 实验/结果图 | 性能对比柱状图、折线图、消融实验、数据表格可视化 |
| **低** | ⚪ | 装饰/细节图 | logo、图标、附录细节、重复性图表、非核心插图 |

---

## 📂 文件结构

### 技能目录结构

```
read-paper/
├── README.md                   # 本文件
├── skill.md                    # 技能定义文件
└── scripts/                    # Python脚本包
    ├── __init__.py
    ├── main.py                 # 程序入口
    ├── config.py               # 配置常量
    ├── paper.py                # 数据模型
    ├── arxiv_client.py         # arXiv API客户端
    ├── folder_manager.py       # 文件夹管理
    ├── downloader.py           # 论文下载器
    ├── image_processor.py      # 图片提取器
    ├── image_list_generator.py # 图片清单生成器
    ├── template_generator.py   # 模板生成器
    ├── paper_reader.py         # 主控制器
    └── process_selected_images.py  # 图片处理脚本
```

### 生成的论文文件夹结构

```
paper/
└── [论文关键词-id]/
    ├── pdf/
    │   └── [arxiv-id].pdf      # 论文PDF
    ├── tex/                    # TeX源码目录
    │   ├── main.tex
    │   ├── introduction.tex
    │   ├── method.tex
    │   └── ...
    ├── images/                 # 重要图片目录
    │   ├── architecture.png    # 架构图
    │   ├── architecture.md     # 图片解读文档
    │   ├── results.png         # 实验结果图
    │   ├── results.md          # 图片解读文档
    │   └── ...
    ├── .temp_images/           # 临时图片目录（阶段一）
    ├── images.md               # 图片清单（供AI分析）
    └── [论文名].md             # 完整精读笔记
```

---

## ⚙️ 配置说明

### 环境变量

无需配置环境变量，所有配置通过命令行参数传递。

### 命令行参数

| 参数 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `arxiv_input` | - | 必填 | arXiv链接或ID |
| `--output-dir` | `-o` | `paper` | 输出根目录 |

### 配置文件

可在 `scripts/config.py` 中修改以下配置：

- `DEFAULT_DPI`: PDF转PNG的分辨率（默认300）
- `DEFAULT_TIMEOUT`: API请求超时时间（默认30秒）
- `DOWNLOAD_TIMEOUT`: 下载超时时间（默认120秒）
- `MAX_FOLDER_NAME_LENGTH`: 文件夹名称最大长度（默认50）

---

## ❓ 常见问题

<details>
<summary><b>Q: TeX源码下载失败怎么办？</b></summary>

A: 部分论文可能没有提供TeX源码。此时脚本会继续使用PDF进行分析，但图片提取可能受限。建议：
- 检查arXiv页面是否提供源码下载
- 手动下载源码后放入 `tex/` 目录

</details>

<details>
<summary><b>Q: 图片提取数量为0怎么办？</b></summary>

A: 可能的原因：
1. 论文没有TeX源码
2. 图片使用了特殊格式或嵌套引用
3. 图片目录名称不在预设列表中

解决方案：
- 检查 `tex/` 目录是否存在
- 查看 `config.py` 中的 `IMAGE_DIRECTORIES` 配置
- 手动从PDF中提取图片

</details>

<details>
<summary><b>Q: PDF转PNG失败怎么办？</b></summary>

A: 确保已安装系统依赖：
- Linux: `sudo apt-get install poppler-utils imagemagick`
- macOS: `brew install poppler imagemagick`
- Windows: 下载安装包并配置环境变量

</details>

<details>
<summary><b>Q: 如何在AI助手中使用此技能？</b></summary>

A: 此技能设计用于AI助手（如Claude、ChatGPT等）：
1. 将 `skill.md` 内容添加到AI助手的系统提示中
2. AI助手会自动执行两阶段工作流
3. 用户只需提供arXiv链接即可

</details>

<details>
<summary><b>Q: 支持哪些图片格式？</b></summary>

A: 支持以下格式：
- PNG (`.png`)
- JPEG (`.jpg`, `.jpeg`)
- PDF (`.pdf`) - 会自动转换为PNG
- EPS (`.eps`)
- SVG (`.svg`)

</details>

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

### 如何贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范

- 使用 Python 3.8+ 语法
- 遵循 PEP 8 编码规范
- 添加必要的注释和文档字符串
- 编写单元测试

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- [arXiv](https://arxiv.org/) - 开放获取的学术论文库
- [Poppler](https://poppler.freedesktop.org/) - PDF渲染库
- [ImageMagick](https://imagemagick.org/) - 图像处理工具

---

## 📮 联系方式

- 问题反馈: [GitHub Issues](https://github.com/your-username/read-paper-skill/issues)
- 功能建议: [GitHub Discussions](https://github.com/your-username/read-paper-skill/discussions)

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐️ Star！**

Made with ❤️ by the community

</div>
