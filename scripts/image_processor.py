#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片提取和处理模块
从TeX源码中提取图片，并在阶段一自动转换PDF为PNG
"""

import shutil
import subprocess
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
        从TeX源码中提取图片到临时目录，并自动转换PDF为PNG

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
            # 自动转换PDF为PNG（阶段一的核心任务）
            self._convert_pdfs_to_png()

        return extracted_count

    def _convert_pdfs_to_png(self) -> int:
        """
        将临时目录中的所有PDF文件转换为PNG格式
        转换成功后删除原PDF文件

        Returns:
            转换成功的文件数量
        """
        pdf_files = list(self.temp_images_dir.glob("*.pdf"))

        if not pdf_files:
            print(f"  ℹ️  没有发现PDF格式的图片，跳过转换")
            return 0

        print(f"\n  📄 PDF转PNG (阶段一自动化)")
        print(f"     发现 {len(pdf_files)} 个PDF文件")
        converted_count = 0

        for pdf_file in pdf_files:
            png_file = pdf_file.with_suffix('.png')

            # 如果PNG已存在，跳过
            if png_file.exists():
                print(f"    ⏭️  跳过: {pdf_file.name} (PNG已存在)")
                continue

            # 尝试转换
            if self._convert_single_pdf(pdf_file, png_file):
                # 删除原PDF
                try:
                    pdf_file.unlink()
                    print(f"    🗑️  已删除原文件: {pdf_file.name}")
                    converted_count += 1
                except Exception as e:
                    print(f"    ⚠️  删除原文件失败: {e}")

        if converted_count > 0:
            print(f"\n  ✅ PDF转换完成: {converted_count} 个文件已转为PNG")

        return converted_count

    def _convert_single_pdf(self, pdf_file: Path, png_file: Path) -> bool:
        """
        转换单个PDF文件为PNG

        Args:
            pdf_file: PDF文件路径
            png_file: 目标PNG文件路径

        Returns:
            是否转换成功
        """
        try:
            # 方法1: 使用pdftoppm (推荐，质量高)
            cmd = [
                'pdftoppm',
                '-png',
                '-r', '300',
                '-singlefile',
                str(pdf_file),
                str(png_file.with_suffix(''))  # pdftoppm会自动添加.png后缀
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"    ✓ {pdf_file.name} -> {png_file.name} (pdftoppm)")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            # 方法2: 使用ImageMagick的convert
            try:
                cmd = [
                    'convert',
                    '-density', '300',
                    str(pdf_file),
                    '-quality', '100',
                    str(png_file)
                ]
                subprocess.run(cmd, check=True, capture_output=True)
                print(f"    ✓ {pdf_file.name} -> {png_file.name} (ImageMagick)")
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                print(f"    ❌ 转换失败: {pdf_file.name}")
                print(f"       请手动安装 pdftoppm (poppler-utils) 或 ImageMagick")
                return False
