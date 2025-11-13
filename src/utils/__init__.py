"""
工具模块初始化文件

该模块包含了项目中常用的工具函数和类，包括：
- 假数据生成工具 (fake_util)
- 路径处理工具 (path_util)
- Excel处理工具 (excel_util)
- 全局映射工具 (global_map)
- 日志工具 (log_util)
- 数据处理工具 (pd_util, dict_util)
- 文件处理工具 (file_util)
- 数据库工具 (db_util)
- 日期处理工具 (date_uitl)
- 其他辅助工具 (tools, check_util, har_analyse)
"""

# 导入常用的工具函数
from .fake_util import (
    faker_text, faker_职业, faker_姓名, fake_身份证, faker_uuid,
    faker_城市, faker_地址, faker_移动电话, faker_邮箱,
    faker_随机数生成, faker_随机布尔值, faker_单位, faker_产品型号
)
from .path_util import get_path
from .date_uitl import 返回当前时间xxxx_xx_xx, 返回当前时间xxxx_xx_xx加N天
from .dict_util import compare_dicts, get_dict_info, replace_dict_key
from .file_util import generate_formatted_file, check_file_exists
from .db_util import DBUtil, db_util
from .global_map import GlobalMap

__all__ = [
    # 假数据生成
    'faker_text', 'faker_职业', 'faker_姓名', 'fake_身份证', 'faker_uuid',
    'faker_城市', 'faker_地址', 'faker_移动电话', 'faker_邮箱',
    'faker_随机数生成', 'faker_随机布尔值', 'faker_单位', 'faker_产品型号',
    
    # 路径和日期
    'get_path', '返回当前时间xxxx_xx_xx', '返回当前时间xxxx_xx_xx加N天',
    
    # 数据处理
    'compare_dicts', 'get_dict_info', 'replace_dict_key',
    
    # 文件处理
    'generate_formatted_file', 'check_file_exists',
    
    # 数据库
    'DBUtil', 'db_util',
    
    # 全局映射
    'GlobalMap',
]
