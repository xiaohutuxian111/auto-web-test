"""
测试用例模块初始化文件

该模块包含了所有测试用例的公共导入和配置。
"""

import os
import random
import pytest
import json
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Any, Dict, Tuple
from playwright.sync_api import Page, Locator, expect, Browser

# 数据模型导入
from src.data_models import *

# 工具类导入
from filelock import FileLock
from src.utils.path_util import get_path
from src.utils.log_util import logger
from src.utils.fake_util import *
from src.utils import date_uitl as oc_time
from src.utils.excel_util import ExcelUtil
from src.utils.db_util import db_util
from src.utils.date_uitl import 返回当前时间xxxx_xx_xx加N天
from src.utils.dict_util import replace_dict_key, compare_dicts, get_dict_info
from src.utils.file_util import generate_formatted_file, JsonCache
from src.utils.global_map import GlobalMap
from src.data_models.项目信息数据 import *
# 配置常量导入
from config.constants import FileType
from config.constants import (
    Qualifications,
    Degree,
    Title,
    InvestigateType,
    DeliverableType
)

# Allure测试框架导入
from allure import (
    severity as 用例级别,
    step as 测试步骤,
    title as 用例名称,
    description as 用例描述
)
from allure_commons.types import Severity

# 测试级别常量定义
阻塞 = Severity.BLOCKER
严重 = Severity.CRITICAL
普通 = Severity.NORMAL
不重要 = Severity.TRIVIAL
轻微 = Severity.MINOR
