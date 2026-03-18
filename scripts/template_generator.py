#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模板生成模块
生成README笔记模板和图片索引
"""

from pathlib import Path
from datetime import datetime
from typing import List

from .paper import PaperInfo, ImageInfo
from .config import DATE_FORMAT


class TemplateGenerator:
    """模板生成器"""
    
    def __init__(self, paper_info: PaperInfo, images_dir: Path):
        """
        初始化模板生成器
        
        Args:
            paper_info: 论文信息
            images_dir: 图片目录
        """
        self.paper_info = paper_info
        self.images_dir = images_dir
    
    def generate_readme_template(self, important_images: List[ImageInfo]) -> str:
        """
        生成精读笔记模板
        
        Args:
            important_images: 重要图片列表
            
        Returns:
            README模板内容
        """
        current_date = datetime.now().strftime(DATE_FORMAT)
        authors_str = self.paper_info.get_authors_string()
        categories_str = self.paper_info.get_categories_string()
        
        # 生成图片列表
        img_list = self._generate_image_list(important_images)
        
        return f"""# {self.paper_info.title}

## 基本信息
- **arXiv ID**: {self.paper_info.id}
- **标题**: {self.paper_info.title}
- **作者**: {authors_str}
- **发布时间**: {self.paper_info.published}
- **类别**: {categories_str}
- **链接**: {self.paper_info.arxiv_url}
- **PDF**: [pdf/{self.paper_info.id}.pdf](pdf/{self.paper_info.id}.pdf)

## 摘要

### 英文摘要
{self.paper_info.summary}

### 中文翻译
<!-- AI_TASK: 将英文摘要翻译成流畅的中文 -->

### 核心要点
<!-- AI_TASK: 基于PDF分析，提炼5个核心要点 -->
- **研究背景**: 
- **研究问题**: 
- **核心方法**: 
- **主要结果**: 
- **研究意义**: 

## 研究背景与动机

### 领域现状
<!-- AI_TASK: 读取PDF，分析该研究领域的发展现状 -->

### 现有方法的局限性
<!-- AI_TASK: 分析现有方法存在的问题和不足 -->

### 研究动机
<!-- AI_TASK: 解释为什么需要这项研究 -->

## 核心方法

### 方法概述
<!-- AI_TASK: 用通俗易懂的语言解释方法的核心思想 -->

### 方法架构

**架构图展示：**
<!-- AI_TASK: 读取images/目录下的架构图，在下方插入 -->
```
<!-- 例如: ![架构图|800](images/architecture.png) -->
```

**架构说明：**
<!-- AI_TASK: 详细描述架构组件 -->

### 关键技术
<!-- AI_TASK: 详细描述方法的技术细节和创新点 -->

### 创新点
<!-- AI_TASK: 列出2-3个主要创新点 -->
- **创新1**: 
- **创新2**: 
- **创新3**: 

## 实验与结果

### 实验设置

**数据集：**
<!-- AI_TASK: 读取PDF，提取数据集信息 -->
| 数据集 | 样本数 | 任务类型 |
|--------|--------|----------|
| 数据集1 | - | - |

**评估指标：**
<!-- AI_TASK: 列出评估指标及含义 -->

### 主要结果

**性能对比表：**
<!-- AI_TASK: 读取PDF中的实验结果，生成对比表格 -->
| 方法 | 指标1 | 指标2 | 指标3 |
|------|-------|-------|-------|
| 基线1 | - | - | - |
| **本文方法** | **-** | **-** | **-** |

**实验结果图：**
<!-- AI_TASK: 读取images/目录下的实验结果图，在下方插入 -->
```
<!-- 插入实验结果图 -->
```

### 结果分析
<!-- AI_TASK: 对实验结果进行深度解读 -->

### 消融实验
<!-- AI_TASK: 如果有消融实验，分析各组件的贡献 -->

## 关键图表解读

<!-- 重要图片列表： -->
{img_list}

<!-- AI_TASK: 对每个重要图片，引用对应的解读文档内容 -->

## 深度分析

### 研究价值
- **理论贡献**: <!-- AI_TASK: 分析理论贡献 -->
- **实际应用**: <!-- AI_TASK: 分析实际应用价值 -->
- **领域影响**: <!-- AI_TASK: 分析对领域的影响 -->

### 优势与局限性

**优势：**
<!-- AI_TASK: 列出论文的主要优势 -->
- 
- 

**局限性：**
<!-- AI_TASK: 分析论文的局限性和假设 -->
- 
- 

### 未来工作
<!-- AI_TASK: 基于论文内容，建议未来研究方向 -->

## 个人评价

### 总体评分: /10
<!-- AI_TASK: 给出总体评分和理由 -->

### 分项评分
| 维度 | 分数 | 理由 |
|------|------|------|
| 创新性 | /10 | <!-- AI_TASK: 评分理由 --> |
| 技术质量 | /10 | <!-- AI_TASK: 评分理由 --> |
| 实验充分性 | /10 | <!-- AI_TASK: 评分理由 --> |
| 实用性 | /10 | <!-- AI_TASK: 评分理由 --> |

### 推荐指数
<!-- AI_TASK: 给出星级推荐和理由 -->
⭐⭐⭐⭐⭐ 

## 相关论文
<!-- AI_TASK: 列出相关参考文献 -->
- 

## 备注
- 创建时间: {current_date}
- 阅读状态: 待分析

---

## 图片解读文档

本论文的重要图片已生成独立的解读文档，位于 `images/` 目录下：

{img_list}

每张图片都有对应的 `.md` 文件，包含详细的AI解读模板。
"""
    
    def generate_images_index(self, important_images: List[ImageInfo]) -> str:
        """
        生成图片索引文件内容（index.md - 详细版，带图片预览）

        Args:
            important_images: 重要图片列表

        Returns:
            图片索引内容
        """
        # 获取所有图片文件
        img_files = [
            f for f in self.images_dir.iterdir()
            if f.suffix.lower() in {'.png', '.jpg', '.jpeg', '.eps', '.svg'}
        ]

        if not img_files:
            return f"""# 图片索引

论文: {self.paper_info.title}
总计: 0 张图片
"""

        index_content = f"""# 图片索引

论文: {self.paper_info.title}
总计: {len(img_files)} 张重要图片

## 重要图片列表

"""

        for i, img_path in enumerate(sorted(img_files), 1):
            size_kb = img_path.stat().st_size / 1024
            md_file = img_path.stem + '.md'

            # 查找对应的ImageInfo获取优先级
            priority_icon = '🟡'
            for img_info in important_images:
                if img_info.name == img_path.name:
                    priority_icon = img_info.priority_icon
                    break

            index_content += f"""### {i}. {img_path.name} {priority_icon}
- 路径: `images/{img_path.name}`
- 解读文档: [{md_file}]({md_file})
- 大小: {size_kb:.1f} KB
- 格式: {img_path.suffix.lower()}

![{img_path.name}]({img_path.name})

---

"""

        return index_content

    def generate_images_summary(self, important_images: List[ImageInfo]) -> str:
        """
        生成图片总览文件（images.md - 简洁版，便于插入笔记）

        Args:
            important_images: 重要图片列表

        Returns:
            图片总览内容
        """
        # 获取所有图片文件
        img_files = [
            f for f in self.images_dir.iterdir()
            if f.suffix.lower() in {'.png', '.jpg', '.jpeg', '.eps', '.svg'}
        ]

        if not img_files:
            return f"""# 图片总览

论文: {self.paper_info.title}
总计: 0 张图片

> 本文用于快速预览所有图片，便于插入到精读笔记中。
"""

        summary_content = f"""# 图片总览

论文: {self.paper_info.title}
总计: {len(img_files)} 张重要图片

> 本文用于快速预览所有图片，便于插入到精读笔记中。
> 使用方式：复制下方的 Markdown 图片引用到笔记文件的对应位置。

---

"""

        for i, img_path in enumerate(sorted(img_files), 1):
            # 查找对应的ImageInfo获取优先级和描述
            priority_icon = '🟡'
            priority = '中优先级'
            suggestion = '建议位置：实验与结果章节'

            for img_info in important_images:
                if img_info.name == img_path.name:
                    priority_icon = img_info.priority_icon
                    if img_info.is_high_priority:
                        priority = '高优先级'
                        if 'architecture' in img_path.name.lower() or 'model' in img_path.name.lower() or 'framework' in img_path.name.lower():
                            suggestion = '建议位置：核心方法 > 方法架构'
                        elif 'pipeline' in img_path.name.lower() or 'flow' in img_path.name.lower() or 'process' in img_path.name.lower():
                            suggestion = '建议位置：核心方法 > 关键技术'
                    else:
                        priority = '中优先级'
                        if 'result' in img_path.name.lower() or 'comparison' in img_path.name.lower() or 'performance' in img_path.name.lower():
                            suggestion = '建议位置：实验与结果 > 主要结果'
                        elif 'ablation' in img_path.name.lower():
                            suggestion = '建议位置：实验与结果 > 消融实验'
                    break

            summary_content += f"""## 图{i}: {img_path.name} {priority_icon}

**优先级**: {priority}
**建议插入位置**: {suggestion}

**Markdown 引用**:
```markdown
![{img_path.name}|800](images/{img_path.name})

> 图{i}: {img_path.name}
```

![{img_path.name}|600]({img_path.name})

---

"""

        return summary_content
    
    def _generate_image_list(self, important_images: List[ImageInfo]) -> str:
        """生成图片列表字符串"""
        if not important_images:
            return "_暂无图片_"
        
        lines = []
        for i, img_info in enumerate(important_images, 1):
            md_file = Path(img_info.name).stem + '.md'
            lines.append(f"{img_info.priority_icon} 图{i}: [{img_info.name}](images/{md_file})")
        
        return '\n'.join(lines)
    
    def save_templates(self, important_images: List[ImageInfo]):
        """
        保存所有模板文件

        Args:
            important_images: 重要图片列表
        """
        # 保存笔记文件（使用文件夹同名）
        paper_dir = self.images_dir.parent
        notes_filename = f"{paper_dir.name}.md"
        notes_content = self.generate_readme_template(important_images)
        notes_path = paper_dir / notes_filename
        with open(notes_path, 'w', encoding='utf-8') as f:
            f.write(notes_content)
        print(f"   ✓ 精读笔记: {notes_path}")

        # 保存图片索引
        if important_images:
            # 保存详细版（index.md - 带图片预览）
            index_content = self.generate_images_index(important_images)
            index_path = self.images_dir / 'index.md'
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_content)
            print(f"   ✓ 详细索引: {index_path}")

            # 保存简洁版（images.md - 便于插入笔记）
            summary_content = self.generate_images_summary(important_images)
            summary_path = self.images_dir.parent / 'images.md'
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(summary_content)
            print(f"   ✓ 图片总览: {summary_path}")
