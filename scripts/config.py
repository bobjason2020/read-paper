#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置常量模块
包含所有配置常量和关键词定义
"""

# 停用词列表（用于生成文件夹名称）
STOP_WORDS = {
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
    'before', 'after', 'above', 'below', 'between', 'among', 'within',
    'using', 'based', 'via', 'through', 'toward', 'towards'
}

# 高优先级图片关键词（核心架构/方法）
HIGH_PRIORITY_KEYWORDS = [
    'architecture', 'model', 'framework', 'overview', 'structure',
    'pipeline', 'flow', 'process', 'workflow', 'method', 'system',
    'network', 'design', 'approach'
]

# 中优先级图片关键词（实验/结果）
MEDIUM_PRIORITY_KEYWORDS = [
    'results', 'comparison', 'performance', 'accuracy', 'evaluation',
    'ablation', 'analysis', 'component', 'experiment', 'chart', 'graph',
    'plot', 'figure', 'table', 'benchmark'
]

# 低优先级图片关键词（装饰性/附录）
LOW_PRIORITY_KEYWORDS = [
    'logo', 'icon', 'decoration', 'banner', 'header', 'footer',
    'appendix', 'supplementary', 'detail', 'thumbnail', 'badge'
]

# 支持的图片格式
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.pdf', '.eps', '.svg'}

# 常见图片目录名（TeX源码中）
IMAGE_DIRECTORIES = ['pics', 'figures', 'fig', 'images', 'img', 'diagrams']

# 默认配置
DEFAULT_OUTPUT_DIR = "paper"
DEFAULT_DPI = 300
DEFAULT_TIMEOUT = 30  # API请求超时时间（秒）
DOWNLOAD_TIMEOUT = 120  # 下载超时时间（秒）

# arXiv API配置
ARXIV_API_URL = "https://export.arxiv.org/api/query"
ARXIV_PDF_URL_TEMPLATE = "https://arxiv.org/pdf/{paper_id}.pdf"
ARXIV_ABSTRACT_URL_TEMPLATE = "https://arxiv.org/abs/{paper_id}"
ARXIV_SOURCE_URL_TEMPLATE = "https://arxiv.org/e-print/{paper_id}"

# 文件夹命名配置
MAX_FOLDER_NAME_LENGTH = 50
MAX_KEYWORDS_IN_FOLDER_NAME = 5
MIN_KEYWORD_LENGTH = 2

# 输出格式配置
DATE_FORMAT = "%Y-%m-%d"
