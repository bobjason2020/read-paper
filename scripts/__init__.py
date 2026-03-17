#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Read Paper Skill - 自动创建论文阅读环境（v1.2 智能筛选与精读版）

模块化结构：
- config: 配置常量
- paper: 数据模型
- arxiv_client: arXiv API客户端
- folder_manager: 文件夹管理
- downloader: 论文下载
- image_processor: 图片处理
- template_generator: 模板生成
- paper_reader: 主控制器
- main: 程序入口
"""

__version__ = "1.2.0"
__author__ = "OrbitOS"

# 暴露主要接口
from .paper import PaperInfo, ImageInfo
from .paper_reader import PaperReader

__all__ = [
    'PaperInfo',
    'ImageInfo', 
    'PaperReader',
    '__version__'
]
