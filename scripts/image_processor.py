#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片处理模块
处理图片的提取、筛选、转换和移动
"""

import shutil
from pathlib import Path

from .config import IMAGE_EXTENSIONS, IMAGE_DIRECTORIES


class ImageExtractor:
    """图片提取器 - 从TeX源码中提取图片"""
    
    def __init__(self, tex_dir: Path, temp_images_dir: Path):
        """
        初始化图片提取器
        
        Args:
            tex_dir: TeX源码目录
            temp_images_dir: 临时图片目录
        """
        self.tex_dir = tex_dir
        self.temp_images_dir = temp_images_dir
    
    def extract_images(self) -> int:
        """
        从TeX源码中提取图片到临时目录
        
        Returns:
            提取的图片数量
        """
        if not self.tex_dir.exists():
            return 0
        
        extracted_count = 0
        
        for img_dir_name in IMAGE_DIRECTORIES:
            src_dir = self.tex_dir / img_dir_name
            if src_dir.exists() and src_dir.is_dir():
                print(f"  🖼️  从 {img_dir_name}/ 提取图片...")
                
                for file_path in src_dir.iterdir():
                    if file_path.suffix.lower() in IMAGE_EXTENSIONS:
                        dest_path = self.temp_images_dir / file_path.name
                        try:
                            shutil.copy2(file_path, dest_path)
                            extracted_count += 1
                            print(f"     ✓ {file_path.name}")
                        except Exception as e:
                            print(f"     ✗ {file_path.name}: {e}")
        
        if extracted_count > 0:
            print(f"  ✅ 成功提取 {extracted_count} 张图片到临时目录")
        
        return extracted_count


class ImageExtractor:
    """图片提取器 - 从TeX源码中提取图片"""

    def __init__(self, tex_dir: Path, temp_images_dir: Path):
        """
        初始化图片提取器

        Args:
            tex_dir: TeX源码目录
            temp_images_dir: 临时图片目录
        """
        self.tex_dir = tex_dir
        self.temp_images_dir = temp_images_dir

    def extract_images(self) -> int:
        """
        从TeX源码中提取图片到临时目录

        Returns:
            提取的图片数量
        """
        if not self.tex_dir.exists():
            return 0

        extracted_count = 0

        for img_dir_name in IMAGE_DIRECTORIES:
            src_dir = self.tex_dir / img_dir_name
            if src_dir.exists() and src_dir.is_dir():
                print(f"  🖼️  从 {img_dir_name}/ 提取图片...")

                for file_path in src_dir.iterdir():
                    if file_path.suffix.lower() in IMAGE_EXTENSIONS:
                        dest_path = self.temp_images_dir / file_path.name
                        try:
                            shutil.copy2(file_path, dest_path)
                            extracted_count += 1
                            print(f"     ✓ {file_path.name}")
                        except Exception as e:
                            print(f"     ✗ {file_path.name}: {e}")

        if extracted_count > 0:
            print(f"  ✅ 成功提取 {extracted_count} 张图片到临时目录")

        return extracted_count
