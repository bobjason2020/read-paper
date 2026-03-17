#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本 - 绕过emoji编码问题
"""

import sys
import subprocess
from pathlib import Path

def test_phase1():
    """测试阶段一"""
    skill_dir = Path(__file__).parent
    test_id = "2305.15924"  # 一个真实存在的arXiv论文ID

    print("Testing read-paper phase 1...")
    print(f"Paper ID: {test_id}")

    # 使用subprocess调用，设置环境变量
    env = {
        "PYTHONIOENCODING": "utf-8",
        "PYTHONPATH": str(skill_dir / "scripts")
    }

    result = subprocess.run(
        [sys.executable, "-m", "scripts.main", test_id, "--output-dir", "paper_test"],
        cwd=skill_dir,
        env=env,
        capture_output=True,
        text=True,
        encoding='utf-8'
    )

    print("STDOUT:")
    print(result.stdout)
    print("\nSTDERR:")
    print(result.stderr)
    print(f"\nReturn code: {result.returncode}")

    # 检查文件结构
    paper_dir = skill_dir / "paper_test"
    if paper_dir.exists():
        print("\n[OK] paper_test directory created")
        # 列出子目录和文件
        for sub in ['pdf', 'tex', 'images']:
            subdir = paper_dir / sub
            if subdir.exists():
                files = list(subdir.iterdir())
                print(f"  - {sub}/: {len(files)} items")
            else:
                print(f"  - {sub}/: NOT FOUND")
        # 检查关键文件
        readme = paper_dir / "README.md"
        if readme.exists():
            print(f"  - README.md: EXISTS")
        images_md = paper_dir / "images.md"
        if images_md.exists():
            print(f"  - images.md: EXISTS")
    else:
        print("\n[FAIL] paper_test directory not found")

if __name__ == "__main__":
    test_phase1()
