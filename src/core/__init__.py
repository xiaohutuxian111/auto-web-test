"""
核心基础组件模块

该模块包含自动化测试框架的核心基础能力。
核心使用入口是 PageObject(base_page.py)，组件和动作能力应围绕 PageObject 使用。

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
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

import allure
import pytest
from playwright.sync_api import Page, Locator, expect, Browser

from src.core.assertions import assert_with_loop

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

# core 的统一使用入口。业务页面应继承 PageObject，再通过 self.locators、
# self.table()、self.component()、self.actions 使用底层组件能力。
from src.core.base_page import PageObject
from src.core.actions import ComponentActions, UploadFile
from src.core.components import (
    COMPONENT_REGISTRY,
    ComponentRootNotFoundError,
    FrontendComponent,
    Locators,
    Table,
    component,
)
