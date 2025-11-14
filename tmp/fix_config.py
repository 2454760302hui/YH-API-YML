#!/usr/bin/env python3
"""
统一配置文件，解决pyproject.toml和setup.py的冲突
"""

import os
from pathlib import Path
import shutil

def unify_package_config():
    """统一包配置"""
    print("🔧 统一包配置...")
    
    # 切换到源码目录
    source_dir = Path("源码ing")
    
    # 1. 备份setup.py
    setup_path = source_dir / "setup.py"
    if setup_path.exists():
        backup_path = setup_path.with_suffix('.py.bak2')
        shutil.copy(setup_path, backup_path)
        print(f"✅ 备份setup.py: {backup_path}")
    
    # 2. 使用pyproject.toml作为标准，但修正包名为统一名称
    pyproject_path = source_dir / "pyproject.toml"
    
    if pyproject_path.exists():
        content = pyproject_path.read_text(encoding='utf-8')
        
        # 修正包名
        content = content.replace('name = "api-test-kb-pro"', 'name = "api-test-yh-pro"')
        
        # 备份原文件
        backup_path = pyproject_path.with_suffix('.toml.bak')
        shutil.copy(pyproject_path, backup_path)
        print(f"✅ 备份pyproject.toml: {backup_path}")
        
        # 写入修正后的内容
        pyproject_path.write_text(content, encoding='utf-8')
        print(f"✅ 已修正pyproject.toml中的包名")
    
    # 3. 删除setup.py（使用pyproject.toml作为唯一配置）
    if setup_path.exists():
        setup_path.unlink()
        print(f"✅ 已删除setup.py（使用pyproject.toml作为唯一配置）")
    
    print("\n📝 配置统一完成！")
    print(f"   包名: api-test-yh-pro")
    print(f"   版本: 3.0.0")
    print(f"   配置文件: pyproject.toml")

if __name__ == "__main__":
    print("🔧 开始统一配置文件...\n")
    
    # 切换到项目根目录
    os.chdir(Path(__file__).parent.parent)
    
    unify_package_config()
    
    print("\n✅ 配置文件统一完成！")
