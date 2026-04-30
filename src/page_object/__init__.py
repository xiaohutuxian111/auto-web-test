"""
页面对象模型模块

该模块实现了页面对象模式（POM），包括：
- 页面实例管理 (pageIns.py)
- 登录页面 (登录页.py)
- 审批中心 (审批中心.py)
- 我的待办 (我的待办.py)
- 项目管理页面
- 合同管理页面

提供了统一的页面操作接口和元素定位方法。
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
from typing import Union, Optional, Literal, List, Dict, Tuple,Any

import allure
import pytest
from playwright.sync_api import Page, Locator, expect, Browser,BrowserContext




from src.utils.tools import get_token
from src.utils.path_util import get_path
from src.utils.excel_util import ExcelUtil
from src.utils.date_uitl import 返回当前时间xxxx_xx_xx加N天
from src.utils.api_count import api_count
from src.utils.dict_util import replace_dict_key
from src.utils.fake_util import faker_text, faker_随机数生成,faker_产品型号,faker_单位
from src.utils.file_util import generate_formatted_file
from src.utils.log_util import logger
from src.utils.db_util import db_util
from src.data_models.auth_data import auth_data
from src.core.components.table import Table
