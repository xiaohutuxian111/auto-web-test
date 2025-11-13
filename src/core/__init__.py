"""
核心基础组件模块

该模块包含了自动化测试框架的核心基础组件，包括：
- 页面基类 (base_page.py)
- 表格处理 (table.py)
- 文件上传 (upload_file.py)
- 定位器 (locators.py)

提供了页面对象模型的基础功能和通用工具。
"""

import os
import re
import json
import time
import random
import inspect
import datetime
from time import sleep
from pathlib import Path
from urllib.parse import quote
from typing import Union, Optional, Literal, List, Dict, Tuple, Optional, Any

import allure
import pytest
from playwright.sync_api import Page, Locator, expect, Browser

from src.utils.tools import get_token
from src.utils.path_util import get_path
from src.utils.excel_util import ExcelUtil
from src.utils.date_uitl import 返回当前时间xxxx_xx_xx加N天
from src.utils.api_count import api_count
from src.utils.dict_util import replace_dict_key
from src.utils.fake_util import faker_text
from src.utils.file_util import generate_formatted_file
from src.utils.log_util import logger
from src.utils.db_util import db_util
from src.data_models.auth_data import auth_data

import inspect


def assert_with_loop(statement: str, timeout: float = 30_000):
    """
        循环assert,直到超时为止
        :param statement:字符串形式包裹的布尔表达式,比如"a=='是""
        :param timeout:单位是毫秒
    """

    start_time = time.time()
    frame = inspect.currentframe().f_back
    global_vars = frame.f_globals
    local_vars = frame.f_locals
    sec_timeout = int(timeout / 1000)
    while True:
        try:
            exec(f"assert {statement}", global_vars, local_vars)
            return
        except:
            if time.time() - start_time > sec_timeout:
                raise AssertionError(f"{sec_timeout}秒内assert没有成功,源表达式为:{statement}")
