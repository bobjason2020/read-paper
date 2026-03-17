#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
论文下载模块
处理PDF和TeX源码的下载
"""

import os
import tarfile
import tempfile
from pathlib import Path
from typing import Optional
import requests

from .paper import PaperInfo
from .folder_manager import FolderManager
from .config import DOWNLOAD_TIMEOUT


class PaperDownloader:
    """论文下载器"""
    
    def __init__(self, paper_info: PaperInfo, folder_manager: FolderManager):
        """
        初始化下载器
        
        Args:
            paper_info: 论文信息
            folder_manager: 文件夹管理器
        """
        self.paper_info = paper_info
        self.folder_manager = folder_manager
    
    def download_pdf(self) -> Optional[Path]:
        """
        下载PDF文件
        
        Returns:
            PDF文件路径，下载失败返回None
        """
        pdf_url = self.paper_info.pdf_url
        pdf_path = self.folder_manager.get_pdf_file_path(self.paper_info.id)
        
        try:
            print(f"  📥 正在下载PDF...")
            response = requests.get(pdf_url, timeout=DOWNLOAD_TIMEOUT, stream=True)
            response.raise_for_status()
            
            with open(pdf_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"  ✅ PDF下载成功: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            print(f"  ⚠️  PDF下载失败: {e}")
            print(f"     请手动下载: {pdf_url}")
            return None
    
    def download_and_extract_tex(self) -> Optional[Path]:
        """
        下载并解压TeX源码
        
        Returns:
            TeX源码目录路径，下载失败返回None
        """
        source_url = self.paper_info.source_url
        tex_dir = self.folder_manager.tex_path
        
        try:
            print(f"  📥 正在下载TeX源码...")
            
            # 创建临时文件
            with tempfile.NamedTemporaryFile(suffix='.tar.gz', delete=False) as tmp_file:
                response = requests.get(source_url, timeout=DOWNLOAD_TIMEOUT, stream=True)
                response.raise_for_status()
                
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        tmp_file.write(chunk)
                
                tmp_path = tmp_file.name
            
            # 解压文件
            print(f"  📦 正在解压TeX源码...")
            with tarfile.open(tmp_path, 'r:gz') as tar:
                tar.extractall(path=tex_dir)
            
            # 清理临时文件
            os.unlink(tmp_path)
            
            print(f"  ✅ TeX源码下载成功: {tex_dir}")
            return tex_dir
            
        except Exception as e:
            print(f"  ⚠️  TeX源码下载失败: {e}")
            print(f"     arXiv可能不提供该论文的源码")
            return None
    
    def download_all(self) -> dict:
        """
        下载所有文件
        
        Returns:
            下载结果字典 {'pdf': Path|None, 'tex': Path|None}
        """
        pdf_path = self.download_pdf()
        tex_path = self.download_and_extract_tex()
        
        return {
            'pdf': pdf_path,
            'tex': tex_path
        }
