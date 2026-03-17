#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Read Paper Skill - 程序入口
自动创建论文阅读环境（v1.2 智能筛选与精读版）
"""

import argparse
import sys
from .paper_reader import PaperReader


def main():
    """程序主入口"""
    parser = argparse.ArgumentParser(
        description='Read Paper - 自动创建论文阅读环境 (v1.2 智能筛选与精读版)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python -m scripts.main https://arxiv.org/abs/2401.12345
  python -m scripts.main 2401.12345
  python -m scripts.main arXiv:2401.12345 --output-dir my-papers/

功能:
  1. 解析arXiv链接，获取论文元数据
  2. 创建规范的论文文件夹结构
  3. 下载PDF和TeX源码
  4. 智能筛选重要图片（避免分析无关图片）
  5. PDF转PNG并清理
  6. 为每张重要图片生成精读文档
  7. 生成完整精读笔记模板
        """
    )
    
    parser.add_argument(
        'arxiv_input',
        help='arXiv链接或ID (例如: https://arxiv.org/abs/2401.12345 或 2401.12345)'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        default='paper',
        help='输出根目录 (默认: paper/)'
    )
    
    args = parser.parse_args()
    
    # 创建阅读器并运行
    reader = PaperReader(output_dir=args.output_dir)
    success = reader.run(args.arxiv_input)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
