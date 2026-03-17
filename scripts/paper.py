#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
论文数据模型模块
定义论文和图片的数据类
"""

from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path


@dataclass
class PaperInfo:
    """论文信息数据类"""
    id: str
    title: str
    summary: str
    authors: List[str]
    published: str
    categories: List[str]
    primary_category: str = ""
    
    @property
    def arxiv_url(self) -> str:
        """arXiv摘要页面URL"""
        return f"https://arxiv.org/abs/{self.id}"
    
    @property
    def pdf_url(self) -> str:
        """PDF下载URL"""
        return f"https://arxiv.org/pdf/{self.id}.pdf"
    
    @property
    def source_url(self) -> str:
        """源码下载URL"""
        return f"https://arxiv.org/e-print/{self.id}"
    
    def get_authors_string(self, max_count: int = 3) -> str:
        """获取作者列表字符串"""
        if not self.authors:
            return "Unknown"
        
        authors_str = ', '.join(self.authors[:max_count])
        if len(self.authors) > max_count:
            authors_str += '...'
        return authors_str
    
    def get_categories_string(self) -> str:
        """获取类别列表字符串"""
        return ', '.join(self.categories) if self.categories else "N/A"


@dataclass
class ImageInfo:
    """图片信息数据类"""
    path: Path
    name: str
    priority: str  # 'high', 'medium', 'low'
    reason: str
    
    def __post_init__(self):
        """验证priority值"""
        if self.priority not in ('high', 'medium', 'low'):
            raise ValueError(f"Invalid priority: {self.priority}. Must be 'high', 'medium', or 'low'")
    
    @property
    def is_high_priority(self) -> bool:
        """是否为高优先级"""
        return self.priority == 'high'
    
    @property
    def is_medium_priority(self) -> bool:
        """是否为中优先级"""
        return self.priority == 'medium'
    
    @property
    def is_low_priority(self) -> bool:
        """是否为低优先级"""
        return self.priority == 'low'
    
    @property
    def priority_icon(self) -> str:
        """获取优先级图标"""
        icons = {
            'high': '🔴',
            'medium': '🟡',
            'low': '⚪'
        }
        return icons.get(self.priority, '⚪')
    
    def get_size_kb(self) -> float:
        """获取图片大小（KB）"""
        if self.path.exists():
            return self.path.stat().st_size / 1024
        return 0.0
