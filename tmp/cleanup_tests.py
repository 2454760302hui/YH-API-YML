#!/usr/bin/env python3
"""
清理冗余测试文件
整理测试结构
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def cleanup_redundant_tests():
    """清理冗余的测试文件"""
    source_dir = Path("源码ing")
    
    # 需要移动到archive的测试文件模式
    redundant_patterns = [
        "test_fix",
        "verify_fix",
        "final_",
        "test_content_removal",
        "test_links_removal",
        "test_navigation_cleanup",
        "test_menu_fix",
        "test_address_fix",
        "test_download_fix",
        "test_encoding_fix",
        "test_syntax_fix",
        "test_psutil_fix",
        "test_ui_changes",
        "test_404_fixes",
        "diagnose_",
        "simple_test",
        "simple_homepage",
        "simple_project",
        "simple_server",
        "simple_docs",
        "quick_",
        "ultimate_",
        "windows_compatibility",
        "fix_",
        "add_copy",
        "demo_",
        "run_test_with_wait"
    ]
    
    # 创建archive目录
    archive_dir = source_dir / "tests_archive"
    archive_dir.mkdir(exist_ok=True)
    
    # 添加归档说明文件
    readme_content = f"""# 测试文件归档

此目录包含已归档的旧测试文件和临时测试脚本。

归档时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

这些文件在项目重构过程中被识别为：
- 临时测试脚本
- 重复的修复验证文件
- 已完成的一次性测试文件

如需使用这些文件，请从archive中恢复。
"""
    
    (archive_dir / "README.md").write_text(readme_content, encoding='utf-8')
    
    # 收集需要归档的文件
    files_to_archive = []
    for pattern in redundant_patterns:
        files_to_archive.extend(source_dir.glob(f"**/{pattern}*.py"))
    
    # 去重
    files_to_archive = list(set(files_to_archive))
    
    # 排除一些重要文件
    exclude_files = [
        "test_runner.py",
        "test_api.yaml",
        "test_basic_api.yaml"
    ]
    
    archived_count = 0
    print(f"🗂️  开始归档冗余测试文件...")
    print(f"📁 归档目录: {archive_dir}")
    print()
    
    for file_path in files_to_archive:
        if file_path.name in exclude_files:
            continue
        
        if file_path.is_file():
            # 移动到archive
            dest_path = archive_dir / file_path.name
            
            # 如果目标已存在，添加时间戳
            if dest_path.exists():
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                dest_path = archive_dir / f"{file_path.stem}_{timestamp}{file_path.suffix}"
            
            shutil.move(str(file_path), str(dest_path))
            print(f"  ✅ 归档: {file_path.name} -> {dest_path.name}")
            archived_count += 1
    
    print()
    print(f"📊 归档统计:")
    print(f"   已归档文件数: {archived_count}")
    print(f"   归档目录: {archive_dir}")
    
    # 创建简洁的测试目录结构
    create_clean_test_structure(source_dir)

def create_clean_test_structure(source_dir):
    """创建清晰的测试目录结构"""
    print()
    print("📁 创建标准测试结构...")
    
    # 创建tests目录
    tests_dir = source_dir / "tests"
    tests_dir.mkdir(exist_ok=True)
    
    # 创建子目录
    subdirs = {
        "unit": "单元测试",
        "integration": "集成测试",
        "e2e": "端到端测试",
        "performance": "性能测试"
    }
    
    for subdir, desc in subdirs.items():
        subdir_path = tests_dir / subdir
        subdir_path.mkdir(exist_ok=True)
        
        # 创建__init__.py
        init_file = subdir_path / "__init__.py"
        if not init_file.exists():
            init_file.write_text(f'"""\\n{desc}\\n"""\\n', encoding='utf-8')
        
        print(f"  ✅ 创建: tests/{subdir}/ - {desc}")
    
    # 创建tests/__init__.py
    tests_init = tests_dir / "__init__.py"
    if not tests_init.exists():
        tests_init.write_text('"""\\nYH API测试框架测试套件\\n"""\\n', encoding='utf-8')
    
    # 创建conftest.py
    conftest_path = tests_dir / "conftest.py"
    if not conftest_path.exists():
        conftest_content = '''"""
Pytest配置文件
定义fixtures和测试配置
"""

import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def test_data_dir():
    """测试数据目录"""
    return Path(__file__).parent.parent / "data"


@pytest.fixture(scope="session")
def test_config():
    """测试配置"""
    return {
        "base_url": "https://httpbin.org",
        "timeout": 30,
        "retry_count": 3
    }
'''
        conftest_path.write_text(conftest_content, encoding='utf-8')
        print(f"  ✅ 创建: tests/conftest.py")
    
    # 创建示例测试文件
    create_sample_test(tests_dir / "unit" / "test_example.py")
    
    print()
    print("✅ 测试结构创建完成！")

def create_sample_test(test_file_path):
    """创建示例测试文件"""
    if test_file_path.exists():
        return
    
    content = '''"""
示例测试文件
演示如何编写测试用例
"""

import pytest


def test_example():
    """示例测试：基础断言"""
    assert 1 + 1 == 2


def test_string_operations():
    """示例测试：字符串操作"""
    text = "Hello, World!"
    assert text.startswith("Hello")
    assert "World" in text
    assert len(text) == 13


@pytest.mark.parametrize("input_value,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_multiply_by_two(input_value, expected):
    """示例测试：参数化测试"""
    assert input_value * 2 == expected


class TestExample:
    """示例测试类"""
    
    def test_list_operations(self):
        """测试列表操作"""
        my_list = [1, 2, 3]
        my_list.append(4)
        assert len(my_list) == 4
        assert my_list[-1] == 4
    
    def test_dict_operations(self):
        """测试字典操作"""
        my_dict = {"name": "test", "value": 123}
        assert my_dict["name"] == "test"
        assert "value" in my_dict
'''
    
    test_file_path.write_text(content, encoding='utf-8')
    print(f"  ✅ 创建: tests/unit/test_example.py")


if __name__ == "__main__":
    print("🧹 开始清理冗余测试文件...\n")
    
    # 切换到项目根目录
    os.chdir(Path(__file__).parent.parent)
    
    cleanup_redundant_tests()
    
    print("\n✅ 测试文件清理完成！")
