#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF to PNG Converter - 将PDF格式图片转换为PNG格式
支持批量转换，转换后可选择删除原PDF文件
"""

import os
import subprocess
from pathlib import Path
import argparse


def convert_pdf_to_png(images_dir, delete_original=True, dpi=300):
    """
    将images目录下的所有PDF文件转换为PNG格式
    
    Args:
        images_dir: 图片目录路径
        delete_original: 转换成功后是否删除原PDF文件（默认True）
        dpi: 输出图片分辨率（默认300）
    
    Returns:
        tuple: (成功转换数量, 失败数量, 跳过数量)
    """
    images_path = Path(images_dir)
    
    if not images_path.exists():
        print(f"❌ 目录不存在: {images_dir}")
        return 0, 0, 0
    
    pdf_files = list(images_path.glob("*.pdf"))
    
    if not pdf_files:
        print("ℹ️  没有发现PDF格式的图片文件")
        return 0, 0, 0
    
    print(f"📄 发现 {len(pdf_files)} 个PDF文件，开始转换...")
    print(f"   分辨率: {dpi} DPI")
    print(f"   删除原文件: {'是' if delete_original else '否'}")
    print()
    
    success_count = 0
    fail_count = 0
    skip_count = 0
    
    for pdf_file in pdf_files:
        png_file = pdf_file.with_suffix('.png')
        
        # 如果PNG文件已存在，跳过
        if png_file.exists():
            print(f"  ⏭️  跳过: {pdf_file.name} (PNG已存在)")
            skip_count += 1
            continue
        
        converted = False
        
        # 方法1: 使用pdftoppm (推荐，质量高)
        try:
            cmd = [
                'pdftoppm',
                '-png',
                '-r', str(dpi),
                '-singlefile',
                str(pdf_file),
                str(png_file.with_suffix(''))  # pdftoppm会自动添加.png后缀
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"  ✓ {pdf_file.name} -> {png_file.name}")
            converted = True
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            # 方法2: 使用ImageMagick的convert
            try:
                cmd = [
                    'convert',
                    '-density', str(dpi),
                    str(pdf_file),
                    '-quality', '100',
                    str(png_file)
                ]
                subprocess.run(cmd, check=True, capture_output=True)
                print(f"  ✓ {pdf_file.name} -> {png_file.name} (使用ImageMagick)")
                converted = True
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                print(f"  ❌ 转换失败: {pdf_file.name}")
                print(f"     请手动安装 pdftoppm (poppler-utils) 或 ImageMagick")
                fail_count += 1
                continue
        
        if converted:
            success_count += 1
            
            # 删除原PDF文件（如果启用）
            if delete_original:
                try:
                    pdf_file.unlink()
                    print(f"     🗑️  已删除原文件: {pdf_file.name}")
                except Exception as e:
                    print(f"     ⚠️  删除原文件失败: {e}")
    
    print()
    print("=" * 50)
    print("📊 转换统计:")
    print(f"   ✅ 成功: {success_count}")
    print(f"   ❌ 失败: {fail_count}")
    print(f"   ⏭️  跳过: {skip_count}")
    print("=" * 50)
    
    return success_count, fail_count, skip_count


def main():
    parser = argparse.ArgumentParser(
        description='将PDF格式图片转换为PNG格式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python convert_pdf_to_png.py ./images
  python convert_pdf_to_png.py ./images --keep-original
  python convert_pdf_to_png.py ./images --dpi 150
        """
    )
    
    parser.add_argument(
        'images_dir',
        help='图片目录路径'
    )
    
    parser.add_argument(
        '--keep-original', '-k',
        action='store_true',
        help='保留原PDF文件（默认会删除）'
    )
    
    parser.add_argument(
        '--dpi', '-d',
        type=int,
        default=300,
        help='输出图片分辨率DPI（默认300）'
    )
    
    args = parser.parse_args()
    
    delete_original = not args.keep_original
    convert_pdf_to_png(args.images_dir, delete_original, args.dpi)


if __name__ == "__main__":
    main()
