#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理AI筛选后的图片
接收AI生成的高/中优先级图片列表，执行PDF转换和生成模板
"""

import sys
import subprocess
from pathlib import Path


def process_selected_images(paper_dir: str, image_list: str):
    """
    处理AI筛选后的图片

    Args:
        paper_dir: 论文目录路径
        image_list: 图片文件名列表（用逗号分隔）
    """
    paper_path = Path(paper_dir)
    images_dir = paper_path / 'images'
    images_temp_dir = paper_path / '.temp_images'

    # 解析图片列表
    selected_images = [img.strip() for img in image_list.split(',') if img.strip()]

    print(f"\n🤖 处理AI筛选后的图片")
    print(f"   选中的图片: {len(selected_images)} 张")

    # 从临时目录移动选中的图片到images目录
    moved_count = 0
    for img_name in selected_images:
        src_path = images_temp_dir / img_name
        if src_path.exists():
            dest_path = images_dir / img_name
            try:
                subprocess.run(['cp', str(src_path), str(dest_path)], check=True)
                moved_count += 1
                print(f"   ✓ {img_name}")
            except subprocess.CalledProcessError as e:
                print(f"   ✗ {img_name}: {e}")

    print(f"\n   ✅ 已移动 {moved_count} 张图片到images目录")

    # PDF转PNG
    print(f"\n📄 PDF转PNG")
    pdf_files = list(images_dir.glob("*.pdf"))

    converted_count = 0
    for pdf_file in pdf_files:
        png_file = pdf_file.with_suffix('.png')

        # 如果PNG已存在，跳过
        if png_file.exists():
            print(f"   ⏭️  跳过: {pdf_file.name} (PNG已存在)")
            continue

        try:
            # 使用pdftoppm
            cmd = [
                'pdftoppm',
                '-png',
                '-r', '300',
                '-singlefile',
                str(pdf_file),
                str(png_file.with_suffix(''))
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"   ✓ {pdf_file.name} -> {png_file.name}")

            # 删除原PDF
            pdf_file.unlink()
            converted_count += 1

        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                # 使用ImageMagick
                cmd = [
                    'convert',
                    '-density', '300',
                    str(pdf_file),
                    '-quality', '100',
                    str(png_file)
                ]
                subprocess.run(cmd, check=True, capture_output=True)
                print(f"   ✓ {pdf_file.name} -> {png_file.name} (ImageMagick)")

                # 删除原PDF
                pdf_file.unlink()
                converted_count += 1
            except (subprocess.CalledProcessError, FileNotFoundError):
                print(f"   ❌ 转换失败: {pdf_file.name}")

    print(f"\n   ✅ 转换完成: {converted_count} 个文件")

    # 生成图片解读模板
    print(f"\n📖 生成图片解读模板")

    from datetime import datetime
    current_date = datetime.now().strftime('%Y-%m-%d')

    # 获取images目录中的所有图片
    all_images = []
    for ext in ['.png', '.jpg', '.jpeg', '.eps', '.svg']:
        all_images.extend(images_dir.glob(f"*{ext}"))

    generated_count = 0
    for img_path in sorted(all_images):
        md_filename = img_path.stem + '.md'
        md_path = images_dir / md_filename

        # 检查是否已存在
        if not md_path.exists():
            template = f"""# {img_path.name}

- **类型**: <!-- 架构图/流程图/实验结果图/其他 -->
- **简要描述**: <!-- 一句话描述图片内容 -->

![{img_path.name}]({img_path.name})

## 详细解读

<!-- 在此处添加详细的图片解读 -->

---

*生成时间: {current_date}*
"""

            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(template)
            generated_count += 1
            print(f"   ✓ {md_filename}")

    print(f"\n   ✅ 已生成 {generated_count} 个图片解读模板")

    # 清理临时目录
    if images_temp_dir.exists():
        subprocess.run(['rm', '-rf', str(images_temp_dir)])
        print(f"\n   ✅ 已清理临时目录")

    print("\n✅ 图片处理完成！")


def main():
    if len(sys.argv) < 3:
        print("用法: python process_selected_images.py <论文目录> <图片列表>")
        print("示例: python process_selected_images.py ./paper/efficient-attention 'arch.png,results.png,ablation.png'")
        sys.exit(1)

    paper_dir = sys.argv[1]
    image_list = sys.argv[2]

    process_selected_images(paper_dir, image_list)


if __name__ == '__main__':
    main()
