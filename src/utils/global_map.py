"""
全局映射工具模块

该模块提供了基于JSON文件的全局数据存储功能，支持多进程安全的读写操作。
使用文件锁确保并发安全。
"""

import json
import os
from typing import Any, Dict, Optional, Tuple
from filelock import FileLock

from src.utils.path_util import get_path


class GlobalMap:
    """
    全局映射类
    
    提供基于JSON文件的全局数据存储功能，支持多进程安全的读写操作。
    使用文件锁确保并发安全。
    """
    
    def __init__(self, file_path: str = '.temp/GlobalMap.json'):
        """
        初始化GlobalMap
        
        Args:
            file_path: JSON文件路径，相对于项目根目录
        """
        # 确保目录存在
        full_path = get_path(file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # 初始化文件锁
        lock_path = get_path('.temp/GlobalMap.lock')
        
        with FileLock(lock_path):
            # 如果文件不存在，创建空文件
            if not os.path.exists(full_path):
                with open(full_path, 'w', encoding='utf-8') as f:
                    json.dump({}, f, ensure_ascii=False, indent=2)
        
        self.file_path = full_path
        self.lock_path = lock_path

    def __load(self) -> Dict[str, Any]:
        """
        从文件加载数据
        
        Returns:
            Dict[str, Any]: 加载的数据字典
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # 如果文件不存在或格式错误，返回空字典
            return {}

    def __dump(self, data: Dict[str, Any]) -> None:
        """
        将数据写入文件
        
        Args:
            data: 要写入的数据字典
        """
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def set(self, key: str, value: Any) -> None:
        """
        设置键值对
        
        Args:
            key: 键名
            value: 值
        """
        with FileLock(self.lock_path):
            data = self.__load()
            data[key] = value
            self.__dump(data)

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取键对应的值
        
        Args:
            key: 键名
            default: 默认值，当键不存在时返回
            
        Returns:
            Any: 键对应的值或默认值
        """
        with FileLock(self.lock_path):
            data = self.__load()
            return data.get(key, default)

    def delete(self, key: str) -> None:
        """
        删除指定的键
        
        Args:
            key: 要删除的键名
            
        Raises:
            KeyError: 当键不存在时
        """
        with FileLock(self.lock_path):
            data = self.__load()
            if key not in data:
                raise KeyError(f"键 '{key}' 不存在")
            data.pop(key)
            self.__dump(data)

    def get_all(self) -> Tuple[str, Any]:
        """
        获取所有键值对
        
        Returns:
            Tuple[str, Any]: 所有键值对的迭代器
        """
        with FileLock(self.lock_path):
            data = self.__load()
            return data.items()

    def set_all(self, **kwargs: Any) -> None:
        """
        批量设置多个键值对
        
        Args:
            **kwargs: 键值对参数
        """
        with FileLock(self.lock_path):
            data = self.__load()
            data.update(kwargs)
            self.__dump(data)

    def clear(self) -> None:
        """
        清空所有数据
        """
        with FileLock(self.lock_path):
            self.__dump({})

    def exists(self, key: str) -> bool:
        """
        检查键是否存在
        
        Args:
            key: 键名
            
        Returns:
            bool: 键是否存在
        """
        with FileLock(self.lock_path):
            data = self.__load()
            return key in data

    def keys(self) -> list:
        """
        获取所有键名
        
        Returns:
            list: 所有键名的列表
        """
        with FileLock(self.lock_path):
            data = self.__load()
            return list(data.keys())

    def values(self) -> list:
        """
        获取所有值
        
        Returns:
            list: 所有值的列表
        """
        with FileLock(self.lock_path):
            data = self.__load()
            return list(data.values())
