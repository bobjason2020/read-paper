#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
论文阅读器主控制器
整合所有模块，提供简化的主流程控制
"""

from pathlib import Path
from typing import Optional, List
from datetime import datetime

from .paper import PaperInfo
from .arxiv_client import ArxivClient
from .folder_manager import FolderManager
from .downloader import PaperDownloader
from .image_list_generator import ImageListGenerator
from .image_processor import ImageExtractor
from .template_generator import TemplateGenerator


class PaperReader:
    """论文阅读器主类（简化版）"""
    
    def __init__(self, output_dir: str = "paper"):
        """
        初始化论文阅读器
        
        Args:
            output_dir: 输出根目录
        """
        self.output_dir = Path(output_dir)
        self.paper_info: Optional[PaperInfo] = None
        self.folder_manager: Optional[FolderManager] = None
    
    def run(self, arxiv_input: str) -> bool:
        """
        运行完整的论文阅读流程
        
        Args:
            arxiv_input: arXiv链接或ID
            
        Returns:
            是否成功完成
        """
        print("=" * 70)
        print("[READ PAPER] Read Paper - 论文阅读助手 (v1.2 智能筛选与精读版)")
        print("=" * 70)
        
        try:
            # 步骤1: 解析arXiv ID并获取论文信息
            self._step1_fetch_paper_info(arxiv_input)

            # 步骤2: 创建文件夹结构
            self._step2_create_folders()

            # 步骤3: 下载论文
            self._step3_download_papers()

            # 步骤4: 提取图片并生成清单
            self._step4_extract_and_list_images()

            # 步骤5: 生成README模板
            self._step5_generate_readme_template()

            # 步骤6: 输出完成信息
            self._step6_print_summary()

            return True

        except Exception as e:
            self._print_error(e)
            return False

    def _generate_readme_template(self):
        """生成README模板（使用TemplateGenerator）"""
        print(f"\nGenerating 步骤6: 生成精读笔记模板")

        # 确保 images 目录存在（模板生成需要）
        self.folder_manager.images_path.mkdir(parents=True, exist_ok=True)

        # 创建模板生成器（传入空的重要图片列表）
        template_gen = TemplateGenerator(
            paper_info=self.paper_info,
            images_dir=self.folder_manager.images_path
        )

        # 生成模板文件（阶段一不生成图片解读文档）
        template_gen.save_templates(important_images=[])

        print(f"   ✓ README模板: {self.folder_manager.paper_dir / 'README.md'}")
        print(f"   ✓ 图片清单: {self.folder_manager.paper_dir / 'images.md'}")
    
    def _step1_fetch_paper_info(self, arxiv_input: str):
        """步骤1: 解析arXiv ID并获取论文信息"""
        print(f"\nStep 1: 步骤1: 解析arXiv链接")
        paper_id = ArxivClient.parse_arxiv_id(arxiv_input)
        print(f"   ✓ arXiv ID: {paper_id}")
        
        print(f"\nStep 2: 步骤2: 获取论文元数据")
        self.paper_info = ArxivClient.fetch_paper_info(paper_id)
        print(f"   ✓ 标题: {self.paper_info.title[:60]}...")
        print(f"   ✓ 作者: {self.paper_info.get_authors_string()}")
    
    def _step2_create_folders(self):
        """步骤2: 创建文件夹结构"""
        print(f"\nDirectory: 步骤3: 创建文件夹结构")
        
        self.folder_manager = FolderManager(self.output_dir)
        folder_name = self.folder_manager.generate_folder_name(
            self.paper_info.title,
            self.paper_info.id
        )
        self.folder_manager.create_folder_structure(folder_name)
        
        print(f"   ✓ 文件夹: {self.folder_manager.paper_dir}")
        print(f"   ✓ 子目录: pdf/, tex/, images/")
        print(f"   ✓ 临时目录: .temp_images/")
    
    def _step3_download_papers(self):
        """步骤3: 下载论文"""
        print(f"\nDownloading  步骤4: 下载论文文件")
        downloader = PaperDownloader(self.paper_info, self.folder_manager)
        downloader.download_all()
    
    def _step4_extract_and_list_images(self):
        """步骤4: 提取图片并生成清单（供AI分析）"""
        print(f"\nImages  步骤5: 提取图片并生成清单")

        # 提取图片到临时目录
        from .image_processor import ImageExtractor
        extractor = ImageExtractor(
            self.folder_manager.tex_path,
            self.folder_manager.temp_images_dir
        )
        total_extracted = extractor.extract_images()

        if total_extracted > 0:
            # 生成图片清单供AI分析
            list_generator = ImageListGenerator(
                self.folder_manager.temp_images_dir,
                self.folder_manager.images_path
            )
            list_generator.generate_image_list()  # 生成 images.md 文件

            # 清理临时目录
            self.folder_manager.cleanup_temp_directory()
    
    def _step5_generate_readme_template(self):
        """步骤5: 生成README模板（机械化，不依赖图片）"""
        print(f"\nGenerating 步骤6: 生成精读笔记模板")

        # 确保 images 目录存在（模板生成需要）
        self.folder_manager.images_path.mkdir(parents=True, exist_ok=True)

        # 创建模板生成器（传入空的重要图片列表 - 阶段一只生成清单）
        template_gen = TemplateGenerator(
            paper_info=self.paper_info,
            images_dir=self.folder_manager.images_path
        )

        # 保存模板文件
        template_gen.save_templates(important_images=[])
    
    def _step6_print_summary(self):
        """步骤6: 输出完成摘要"""
        print("\n" + "=" * 70)
        print("[OK] 论文文件夹创建成功！")
        print("=" * 70)
        
        print(f"\nStep 2: 论文信息:")
        print(f"   标题: {self.paper_info.title}")
        print(f"   作者: {', '.join(self.paper_info.authors)}")
        print(f"   arXiv ID: {self.paper_info.id}")
        
        print(f"\nDirectory: 文件夹结构:")
        print(f"   {self.folder_manager.paper_dir}/")
        print(f"   ├── pdf/")
        print(f"   │   └── {self.paper_info.id}.pdf")
        print(f"   ├── tex/")
        print(f"   │   └── [TeX源文件...]")
        print(f"   ├── images/")
        if self.important_images:
            print(f"   │   ├── [重要图片文件...]")
            print(f"   │   ├── [图片同名].md    ← 图片精读文档")
            print(f"   │   └── index.md")
        else:
            print(f"   │   └── (无图片)")
        print(f"   └── README.md")
        
        if self.important_images:
            high_count = sum(1 for img in self.important_images if img.is_high_priority)
            medium_count = sum(1 for img in self.important_images if img.is_medium_priority)
            
            print(f"\n📊 图片分析统计:")
            print(f"   🔴 高优先级图片: {high_count} 张")
            print(f"   🟡 中优先级图片: {medium_count} 张")
            print(f"   Generating 图片解读文档: {len(self.important_images)} 个")
        
        print(f"\n🎯 下一步:")
        print(f"   1. 打开 {self.folder_manager.paper_dir}/README.md 开始精读")
        print(f"   2. 查看 images/ 目录下的图片精读文档")
        print(f"   3. 阅读PDF文件深入理解论文")
        print("=" * 70)
    
    def _print_error(self, error: Exception):
        """打印错误信息"""
        print("\n" + "=" * 70)
        print("❌ 错误发生")
        print("=" * 70)
        print(f"错误信息: {error}")
        print("\n建议:")
        print("   1. 检查网络连接")
        print("   2. 确认arXiv链接或ID正确")
        print("   3. 检查输出目录权限")
        print("=" * 70)
