#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig片清单生成模块
从临时目录提取所有Fig片，生成待分析的Fig片清单
"""

from pathlib import Path
from typing import List
from datetime import datetime
from .config import IMAGE_EXTENSIONS


class ImageListGenerator:
    """Fig片清单生成器"""

    def __init__(self, temp_images_dir: Path, images_dir: Path):
        """
        初始化清单生成器

        Args:
            temp_images_dir: 临时Fig片目录（从TeX提取）
            images_dir: 最终images目录（存放清单）
        """
        self.temp_images_dir = temp_images_dir
        self.images_dir = images_dir



    def generate_image_list(self) -> List[str]:
        """
        生成Fig片清单文件

        流程：
        1. 从临时目录获取所有Fig片
        2. 生成 images.md 清单文件（供AI分析判断优先级）

        Returns:
            Fig片文件名列表
        """
        if not self.temp_images_dir.exists():
            print("   ⚠️  临时Fig片目录不存在")
            return []

        # 获取所有Fig片文件
        all_images = []
        for ext in IMAGE_EXTENSIONS:
            all_images.extend(self.temp_images_dir.glob(f"*{ext}"))

        if not all_images:
            print("   ⚠️  未找到任何Fig片")
            return []

        # 生成Fig片清单
        self._generate_markdown_list(all_images)

        print(f"   ✅ Fig片清单已生成: {self.images_dir / 'images.md'}")

        return [img.name for img in all_images]

    def _generate_markdown_list(self, image_files: List[Path]):
        """
        生成Markdown格式的Fig片清单，供AI分析判断优先级
        """
        current_date = datetime.now().strftime('%Y-%m-%d')

        content = f"""# Fig片清单

**论文**: {self.images_dir.parent.name}
**生成时间**: {current_date}
**总数**: {len(image_files)} 张Fig片

---

## [TASK] AI 任务说明

请根据以下流程处理Fig片：

### 步骤1：视觉分析所有Fig片
仔细查看下方的每张Fig片，理解其内容。

### 步骤2：判断优先级
根据Fig片内容分类（不能仅凭文件名猜测）：

| 优先级 | Fig标 | 类型 | 说明 |
|--------|------|------|------|
| **高** | 🔴 | 架构/方法Fig | 模型架构、系统设计、流程框架、核心方法 |
| **中** | 🟡 | 实验/结果Fig | 性能对比、消融实验、数据可视化 |
| **低** | ⚪ | 装饰/细节Fig | logo、附录、重复性Fig表 |

### 步骤3：输出分类结果
在下方列出你的判断，格式：

```
🔴 高优先级：
1. [Fig片文件名] - [简要理由]

🟡 中优先级：
2. [Fig片文件名] - [简要理由]

⚪ 低优先级/跳过：
- [Fig片文件名] - [简要理由]
```

### 步骤4：调用脚本处理
运行以下命令处理选中的Fig片：

```bash
cd "$HOME/.claude/skills/read-paper/scripts"
python process_selected_images.py "{self.images_dir.parent}" "[高优先级Fig片1],[高优先级Fig片2],[中优先级Fig片3],..."
```

**注意**：
- 只传入高/中优先级的Fig片（低优先级跳过）
- Fig片文件名必须完全匹配（包括扩展名）
- 脚本会自动：移动Fig片、PDF转PNG、生成解读模板

---

## [IMAGES] Fig片预览与分析

总共发现 **{len(image_files)}** 张Fig片：

"""

        for i, img_path in enumerate(sorted(image_files), 1):
            size_kb = img_path.stat().st_size / 1024

            content += f"""### Fig{i}: {img_path.name}

**元数据**:
- 文件名: `{img_path.name}`
- 大小: {size_kb:.1f} KB
- 格式: {img_path.suffix.lower()}

**你的判断**:
- 优先级: <!-- 🔴 高 / 🟡 中 / ⚪ 低 -->
- 理由: <!-- 为什么这样分类？ -->

**Fig片预览**:
![{img_path.name}|600]({img_path.name})

---

"""

        # 保存清单文件
        list_path = self.images_dir / 'images.md'
        with open(list_path, 'w', encoding='utf-8') as f:
            f.write(content)
