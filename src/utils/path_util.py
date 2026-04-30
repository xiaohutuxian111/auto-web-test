"""
路径处理工具模块

该模块提供了路径相关的工具函数，用于处理文件路径和URL路径。
"""

import os
import re
from typing import Optional
from urllib.parse import urlsplit


def get_path(path: Optional[str] = None) -> str:
    """
    获取项目根目录的绝对路径，或基于根目录的相对路径
    
    Args:
        path: 相对路径字符串，支持 "/" 和 "\\" 分隔符
        
    Returns:
        str: 绝对路径
        
    Example:
        >>> get_path()
        '/path/to/project/root'
        >>> get_path('.temp')
        '/path/to/project/root/.temp'
        >>> get_path('src/utils')
        '/path/to/project/root/src/utils'
    """
    # 获取项目根目录（当前文件向上三级目录）
    root_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    
    if not path:
        return root_path
    
    # 处理路径分隔符
    if "/" in path:
        path_parts = path.split("/")
    elif "\\" in path:
        path_parts = path.split("\\")
    else:
        path_parts = [path]
    
    # 过滤空字符串
    path_parts = [part for part in path_parts if part]
    
    return os.path.join(root_path, *path_parts)


def get_sub_url(url: str) -> str:
    """
    将 URL 转换为可用于目录名的稳定标识。

    Example:
        >>> get_sub_url("http://192.168.10.240:8060/a-front/")
        '192.168.10.240_8060_a-front'
    """
    if not url:
        return "default"

    parsed = urlsplit(url if "://" in url else f"http://{url}")
    parts = [
        parsed.hostname or "",
        str(parsed.port or ""),
        parsed.path.strip("/"),
    ]
    raw_name = "_".join(part for part in parts if part)
    safe_name = re.sub(r"[^0-9A-Za-z._-]+", "_", raw_name).strip("._-")
    return safe_name or "default"


if __name__ == '__main__':
    # 测试路径处理函数
    print(f"项目根目录: {get_path()}")
    print(f"临时目录: {get_path('.temp')}")
    print(f"工具目录: {get_path('src/utils')}")
