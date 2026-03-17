#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arXiv API 客户端模块
处理arXiv ID解析和论文元数据获取
"""

import re
import requests
import xml.etree.ElementTree as ET
from typing import List
from .paper import PaperInfo
from .config import ARXIV_API_URL, DEFAULT_TIMEOUT


class ArxivClient:
    """arXiv API 客户端"""
    
    API_URL = ARXIV_API_URL
    
    @staticmethod
    def parse_arxiv_id(input_str: str) -> str:
        """
        从各种格式中提取arXiv ID
        
        支持格式：
        - 完整链接：https://arxiv.org/abs/2401.12345
        - PDF链接：https://arxiv.org/pdf/2401.12345
        - ID格式：2401.12345 或 arXiv:2401.12345
        
        Args:
            input_str: 输入字符串
            
        Returns:
            arXiv ID (如: 2401.12345)
            
        Raises:
            ValueError: 无法解析ID时抛出
        """
        input_str = input_str.strip()
        
        # 匹配完整的arXiv URL
        abs_match = re.search(r'arxiv\.org/abs/(\d{4}\.\d{4,5})', input_str, re.IGNORECASE)
        if abs_match:
            return abs_match.group(1)
        
        # 匹配PDF URL
        pdf_match = re.search(r'arxiv\.org/pdf/(\d{4}\.\d{4,5})', input_str, re.IGNORECASE)
        if pdf_match:
            return pdf_match.group(1)
        
        # 匹配arXiv:ID格式
        arxiv_match = re.search(r'arxiv:(\d{4}\.\d{4,5})', input_str, re.IGNORECASE)
        if arxiv_match:
            return arxiv_match.group(1)
        
        # 匹配纯ID格式
        id_match = re.match(r'^(\d{4}\.\d{4,5})$', input_str)
        if id_match:
            return id_match.group(1)
        
        raise ValueError(f"无法解析arXiv ID: {input_str}")
    
    @classmethod
    def fetch_paper_info(cls, paper_id: str) -> PaperInfo:
        """
        从arXiv API获取论文元数据
        
        Args:
            paper_id: arXiv ID
            
        Returns:
            PaperInfo对象
            
        Raises:
            ConnectionError: 网络连接失败
            ValueError: 解析失败或论文不存在
        """
        api_url = f"{cls.API_URL}?id_list={paper_id}"
        
        try:
            response = requests.get(api_url, timeout=DEFAULT_TIMEOUT)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            
            ns = {
                'atom': 'http://www.w3.org/2005/Atom',
                'arxiv': 'http://arxiv.org/schemas/atom'
            }
            
            entry = root.find('.//atom:entry', ns)
            if entry is None:
                raise ValueError(f"未找到论文: {paper_id}")
            
            # 提取标题
            title_elem = entry.find('atom:title', ns)
            title = title_elem.text.strip() if title_elem is not None else ""
            title = re.sub(r'\s+', ' ', title)  # 规范化空白字符
            
            # 提取摘要
            summary_elem = entry.find('atom:summary', ns)
            summary = summary_elem.text.strip() if summary_elem is not None else ""
            
            # 提取作者
            authors = []
            for author in entry.findall('atom:author', ns):
                name_elem = author.find('atom:name', ns)
                if name_elem is not None:
                    authors.append(name_elem.text.strip())
            
            # 提取发布日期
            published_elem = entry.find('atom:published', ns)
            published = published_elem.text[:10] if published_elem is not None else ""
            
            # 提取类别
            categories = []
            for cat in entry.findall('atom:category', ns):
                term = cat.get('term')
                if term:
                    categories.append(term)
            
            primary_category = categories[0] if categories else ""
            
            return PaperInfo(
                id=paper_id,
                title=title,
                summary=summary,
                authors=authors,
                published=published,
                categories=categories,
                primary_category=primary_category
            )
            
        except requests.RequestException as e:
            raise ConnectionError(f"无法连接到arXiv API: {e}")
        except ET.ParseError as e:
            raise ValueError(f"解析arXiv响应失败: {e}")
