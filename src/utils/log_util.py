"""
日志工具模块

该模块提供了基于loguru的日志配置功能，支持控制台输出和文件输出。
支持按日期分割日志文件，自动压缩和轮转。
"""

import os
import sys
import time
from typing import Optional

from loguru import logger
from config.settings import settings


def setup_logger(
    log_level: Optional[str] = None,
    log_format: Optional[str] = None,
    logs_dir: Optional[str] = None,
    enable_console: bool = True,
    enable_file: bool = True
) -> None:
    """
    设置日志配置
    
    Args:
        log_level: 日志级别，默认使用settings中的配置
        log_format: 日志格式，默认使用settings中的配置
        logs_dir: 日志目录，默认使用settings中的配置
        enable_console: 是否启用控制台输出
        enable_file: 是否启用文件输出
    """
    # 使用配置或默认值
    log_level = log_level or settings.LOG_LEVEL
    log_format = log_format or settings.LOG_FORMAT
    logs_dir = logs_dir or settings.LOGS_DIR
    
    # 确保日志目录存在
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # 移除默认的处理器
    logger.remove()
    
    # 添加控制台输出
    if enable_console:
        logger.add(
            sys.stdout,
            format=log_format,
            level=log_level,
            enqueue=True,
            colorize=True
        )
    
    # 添加文件输出
    if enable_file:
        # 设置日志文件路径
        current_date = time.strftime("%Y-%m-%d")
        log_path_error = os.path.join(logs_dir, f'{current_date}_error.log')
        log_path_info = os.path.join(logs_dir, f'{current_date}_info.log')
        
        # 添加错误日志文件
        logger.add(
            log_path_error,
            format=log_format,
            level="ERROR",
            rotation="50MB",
            encoding='utf-8',
            enqueue=True,
            compression='zip',
            retention="30 days"
        )
        
        # 添加信息日志文件
        logger.add(
            log_path_info,
            format=log_format,
            level=log_level,
            rotation="50MB",
            encoding='utf-8',
            enqueue=True,
            compression='zip',
            retention="30 days"
        )


# 初始化日志配置
setup_logger()

# 导出logger实例
__all__ = ['logger', 'setup_logger']


