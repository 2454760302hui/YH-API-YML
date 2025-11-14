#!/usr/bin/env python3
"""
修复项目中的导入和拼写错误
"""

import os
import re
from pathlib import Path

def fix_runner_imports():
    """修复runner.py中的导入错误"""
    runner_path = Path("源码ing/runner.py")
    
    if not runner_path.exists():
        print(f"❌ 文件不存在: {runner_path}")
        return
    
    content = runner_path.read_text(encoding='utf-8')
    
    # 修复拼写错误: create_funtion -> create_function
    content = content.replace('import create_funtion', 'import create_function')
    content = content.replace('create_funtion.', 'create_function.')
    
    # 修复 db 导入问题 - 改为可选导入
    old_import = 'from db import ConnectMysql'
    new_import = '''try:
    from db import ConnectMysql
except ImportError:
    ConnectMysql = None'''
    
    if old_import in content:
        content = content.replace(old_import, new_import)
    
    # 备份原文件
    backup_path = runner_path.with_suffix('.py.bak')
    runner_path.rename(backup_path)
    print(f"✅ 备份原文件: {backup_path}")
    
    # 写入修复后的内容
    runner_path.write_text(content, encoding='utf-8')
    print(f"✅ 已修复: {runner_path}")

def fix_ai_tester_imports():
    """修复ai_tester.py中的类型导入"""
    ai_tester_path = Path("源码ing/ai_tester.py")
    
    if not ai_tester_path.exists():
        print(f"❌ 文件不存在: {ai_tester_path}")
        return
    
    content = ai_tester_path.read_text(encoding='utf-8')
    
    # 查找是否已有typing导入
    if 'from typing import' not in content:
        # 在文件开头添加typing导入
        lines = content.split('\n')
        # 找到第一个import语句的位置
        import_pos = 0
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                import_pos = i
                break
        
        # 在第一个import之前插入typing导入
        lines.insert(import_pos, 'from typing import List, Dict, Any, Optional')
        content = '\n'.join(lines)
    else:
        # 如果已有typing导入，检查是否包含需要的类型
        if 'List' not in content.split('from typing import')[1].split('\n')[0]:
            # 补充缺失的类型
            content = content.replace(
                'from typing import',
                'from typing import List, Dict, Any, Optional,'
            )
    
    # 修复 urljoin 导入
    if 'from urllib.parse import urljoin' not in content:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                lines.insert(i, 'from urllib.parse import urljoin')
                break
        content = '\n'.join(lines)
    
    # 备份原文件
    backup_path = ai_tester_path.with_suffix('.py.bak')
    ai_tester_path.rename(backup_path)
    print(f"✅ 备份原文件: {backup_path}")
    
    # 写入修复后的内容
    ai_tester_path.write_text(content, encoding='utf-8')
    print(f"✅ 已修复: {ai_tester_path}")

def create_create_function_module():
    """创建 create_function.py 模块（如果不存在）"""
    target_path = Path("源码ing/create_function.py")
    
    if target_path.exists():
        print(f"ℹ️  文件已存在: {target_path}")
        return
    
    # 创建基础的 create_function 模块
    content = '''"""
动态函数创建模块
用于从参数动态创建测试函数
"""

from inspect import Parameter, Signature
from typing import Callable, List, Any
import types


def create_function_from_parameters(
    func: Callable,
    parameters: List[Parameter],
    documentation: str = "",
    func_name: str = None,
    func_filename: str = None
) -> Callable:
    """
    从参数列表动态创建函数
    
    Args:
        func: 原始函数
        parameters: 参数列表
        documentation: 函数文档
        func_name: 函数名称
        func_filename: 函数所在文件名
    
    Returns:
        动态创建的函数
    """
    # 创建新的函数签名
    sig = Signature(parameters=parameters)
    
    # 创建新函数
    new_func = types.FunctionType(
        func.__code__,
        func.__globals__,
        name=func_name or func.__name__,
        argdefs=func.__defaults__,
        closure=func.__closure__
    )
    
    # 设置函数签名
    new_func.__signature__ = sig
    
    # 设置函数文档
    if documentation:
        new_func.__doc__ = documentation
    
    # 设置函数所属文件
    if func_filename:
        new_func.__code__ = new_func.__code__.replace(
            co_filename=func_filename
        )
    
    return new_func
'''
    
    target_path.write_text(content, encoding='utf-8')
    print(f"✅ 已创建: {target_path}")

def create_db_module():
    """创建 db.py 模块（如果不存在）"""
    target_path = Path("源码ing/db.py")
    
    if target_path.exists():
        print(f"ℹ️  文件已存在: {target_path}")
        return
    
    # 创建基础的 db 模块
    content = '''"""
数据库连接模块
支持MySQL数据库操作
"""

import logging
from typing import List, Dict, Any, Optional

try:
    import pymysql
    from pymysql.cursors import DictCursor
    PYMYSQL_AVAILABLE = True
except ImportError:
    PYMYSQL_AVAILABLE = False

logger = logging.getLogger(__name__)


class ConnectMysql:
    """MySQL数据库连接类"""
    
    def __init__(self, host: str, user: str, password: str, 
                 port: int = 3306, database: str = None, **kwargs):
        """
        初始化MySQL连接
        
        Args:
            host: 数据库主机地址
            user: 用户名
            password: 密码
            port: 端口号
            database: 数据库名
        """
        if not PYMYSQL_AVAILABLE:
            raise ImportError("pymysql未安装，请执行: pip install pymysql")
        
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.database = database
        self.connection = None
        self.connect()
    
    def connect(self):
        """建立数据库连接"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database=self.database,
                charset='utf8mb4',
                cursorclass=DictCursor
            )
            logger.info(f"✅ 成功连接到MySQL: {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"❌ MySQL连接失败: {e}")
            raise
    
    def query_sql(self, sql: str) -> List[Dict[str, Any]]:
        """
        查询SQL
        
        Args:
            sql: SQL查询语句
        
        Returns:
            查询结果列表
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                logger.info(f"✅ 查询成功: {len(result)}条记录")
                return result
        except Exception as e:
            logger.error(f"❌ 查询失败: {e}")
            raise
    
    def execute_sql(self, sql: str) -> int:
        """
        执行SQL（INSERT, UPDATE, DELETE等）
        
        Args:
            sql: SQL执行语句
        
        Returns:
            影响的行数
        """
        try:
            with self.connection.cursor() as cursor:
                affected_rows = cursor.execute(sql)
                self.connection.commit()
                logger.info(f"✅ 执行成功: 影响{affected_rows}行")
                return affected_rows
        except Exception as e:
            self.connection.rollback()
            logger.error(f"❌ 执行失败: {e}")
            raise
    
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            logger.info("✅ 数据库连接已关闭")
    
    def __del__(self):
        """析构函数，自动关闭连接"""
        self.close()
'''
    
    target_path.write_text(content, encoding='utf-8')
    print(f"✅ 已创建: {target_path}")


if __name__ == "__main__":
    print("🔧 开始修复导入和拼写错误...\n")
    
    # 切换到项目根目录
    os.chdir(Path(__file__).parent.parent)
    
    # 创建缺失的模块
    print("📦 创建缺失的模块...")
    create_create_function_module()
    create_db_module()
    print()
    
    # 修复导入错误
    print("🔨 修复导入错误...")
    fix_runner_imports()
    fix_ai_tester_imports()
    print()
    
    print("✅ 所有修复完成！")
