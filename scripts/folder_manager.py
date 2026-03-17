#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件夹管理模块
处理论文文件夹的创建、命名和清理
"""

import re
import shutil
from pathlib import Path
from typing import Optional
from .config import (
    STOP_WORDS, MAX_FOLDER_NAME_LENGTH, 
    MAX_KEYWORDS_IN_FOLDER_NAME, MIN_KEYWORD_LENGTH
)


class FolderManager:
    """文件夹管理器"""
    
    def __init__(self, output_dir: Path):
        """
        初始化文件夹管理器
        
        Args:
            output_dir: 输出根目录
        """
        self.output_dir = Path(output_dir)
        self.paper_dir: Optional[Path] = None
        self.temp_images_dir: Optional[Path] = None
    
    def generate_folder_name(self, title: str, paper_id: str) -> str:
        """
        根据论文标题生成简洁的文件夹名称
        
        策略：
        1. 提取关键词
        2. 移除停用词
        3. 限制长度
        
        Args:
            title: 论文标题
            paper_id: arXiv ID（备用）
            
        Returns:
            文件夹名称
        """
        title_lower = title.lower()
        title_clean = re.sub(r'[^\w\s-]', ' ', title_lower)
        words = title_clean.split()
        
        # 过滤停用词和短词
        keywords = [
            w for w in words 
            if w not in STOP_WORDS and len(w) > MIN_KEYWORD_LENGTH
        ]
        
        # 如果没有有效关键词，使用所有非停用词
        if not keywords:
            keywords = [w for w in words if w not in STOP_WORDS]
        
        # 如果还是没有，使用原始单词
        if not keywords:
            keywords = words[:MAX_KEYWORDS_IN_FOLDER_NAME]
        
        # 限制关键词数量
        keywords = keywords[:MAX_KEYWORDS_IN_FOLDER_NAME]
        
        # 生成文件夹名
        folder_name = '-'.join(keywords)
        
        # 限制长度
        if len(folder_name) > MAX_FOLDER_NAME_LENGTH:
            folder_name = folder_name[:MAX_FOLDER_NAME_LENGTH].rsplit('-', 1)[0]
        
        # 确保不为空
        if not folder_name:
            folder_name = f"paper-{paper_id}"
        
        return folder_name
    
    def get_unique_folder_path(self, base_name: str) -> Path:
        """
        获取唯一的文件夹路径，处理重名情况
        
        Args:
            base_name: 基础文件夹名
            
        Returns:
            唯一的文件夹路径
            
        Raises:
            RuntimeError: 无法创建唯一文件夹名时抛出
        """
        folder_path = self.output_dir / base_name
        
        if not folder_path.exists():
            return folder_path
        
        # 如果存在，添加序号
        counter = 1
        while True:
            new_name = f"{base_name}-{counter}"
            folder_path = self.output_dir / new_name
            if not folder_path.exists():
                return folder_path
            counter += 1
            
            # 防止无限循环
            if counter > 100:
                raise RuntimeError(f"无法创建唯一文件夹名: {base_name}")
    
    def create_folder_structure(self, folder_name: str) -> Path:
        """
        创建论文文件夹结构
        
        Args:
            folder_name: 文件夹名称
            
        Returns:
            论文主目录路径
        """
        self.paper_dir = self.get_unique_folder_path(folder_name)
        
        # 创建子目录
        subdirs = ['pdf', 'tex', 'images']
        for subdir in subdirs:
            (self.paper_dir / subdir).mkdir(parents=True, exist_ok=True)
        
        # 创建临时图片目录
        self.temp_images_dir = self.paper_dir / '.temp_images'
        self.temp_images_dir.mkdir(parents=True, exist_ok=True)
        
        return self.paper_dir
    
    def cleanup_temp_directory(self) -> bool:
        """
        清理临时目录
        
        Returns:
            是否成功清理
        """
        if self.temp_images_dir and self.temp_images_dir.exists():
            try:
                shutil.rmtree(self.temp_images_dir)
                return True
            except Exception:
                return False
        return True
    
    @property
    def pdf_path(self) -> Path:
        """PDF文件目录路径"""
        if self.paper_dir is None:
            raise RuntimeError("Paper directory not created yet")
        return self.paper_dir / 'pdf'
    
    @property
    def tex_path(self) -> Path:
        """TeX源码目录路径"""
        if self.paper_dir is None:
            raise RuntimeError("Paper directory not created yet")
        return self.paper_dir / 'tex'
    
    @property
    def images_path(self) -> Path:
        """图片目录路径"""
        if self.paper_dir is None:
            raise RuntimeError("Paper directory not created yet")
        return self.paper_dir / 'images'
    
    def get_pdf_file_path(self, paper_id: str) -> Path:
        """获取PDF文件路径"""
        return self.pdf_path / f"{paper_id}.pdf"
