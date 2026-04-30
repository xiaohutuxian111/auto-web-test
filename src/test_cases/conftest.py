# -*- coding: utf-8 -*-
import asyncio
import inspect
import json
import shutil
import sys
import os
import tempfile
import time
import traceback
import random
from typing import Any, Dict, Generator, List

import allure
import pytest
from _pytest.python import Function
from allure import step
from filelock import FileLock
from src.core.components.locators import *

from src.page_object.pageIns import PageInstance
from playwright._impl._locator import Locator as LocatorImpl
from playwright._impl._sync_base import mapping
from playwright.sync_api import (
    BrowserContext,
    BrowserType,
    Dialog,
    Error,
    Playwright,
    sync_playwright,
    expect,
)
from playwright.sync_api._generated import Locator as _Locator
from slugify import slugify
from src.utils.feishu_api import FeiShuApi
from src.utils.global_map import GlobalMap
from src.utils.har_analyse import analyse_har
from src.utils.path_util import get_path
from src.utils.tools import get_sub_url, get_frame_bytes_png

if sys.platform == "linux":
    sys.stdout = sys.stderr
elif sys.platform == "win32":
    sys.stdout = sys.stderr
artifacts_folder = tempfile.TemporaryDirectory(prefix="playwright-pytest-")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "")))

video_index = 0
api_Count = []
time_out = 30_000
base_timeout = 30_000
失败行的源码 = "没有获取到"
最后一次执行的步骤 = "没有获取到"
call_log = "没有获取到"
send_feishu_message = 0
test_name_flag = ""
ws_endpoint_use_list = []
最后操作的page = None


#
# # 直接用 ANSI escape codes
# print("\033[31m这是红色文本\033[0m")
# print("\033[32m这是绿色文本\033[0m")
# print("\033[33m这是黄色文本\033[0m")
# print("\033[34m这是蓝色文本\033[0m")
# print("\033[1;37m这是加粗白色（亮白）\033[0m")
# # 背景色
# print("\033[30;47m黑字白底\033[0m")


def pytest_sessionstart(session):
    global_map = GlobalMap()
    if not hasattr(session.config, "workerinput"):
        # 设置环境变量
        base_url = session.config.getoption("--base-url")  # type:str
        global_map.set("base_url", base_url)
        global_map.set("jobUrl", session.config.getoption("--jobUrl"))
        global_map.set("feishu_receive_id", session.config.getoption("--feishu"))
        global_map.set("use_feishu", session.config.getoption("--use_feishu"))
        global_map.set("total_requests", session.config.getoption("--total_requests"))
        # todo 默认为测试环境,后续写入配置文件
        global_map.set("env", "test")
        if session.config.getoption("--api_port"):
            api_base_url = ":".join(base_url.split(":")[:-1]) + ":" + session.config.getoption("--api_port")
        else:
            api_base_url = base_url.removesuffix("/") + "/api"
        global_map.set("api_base_url", api_base_url)
        # os.environ["wsendpoint_url"] = "ws://192.168.9.46:14295/1ac2610b0dc710291a521c274331915a"


# 解析测试函数的装饰器获取 Allure 标题
def _get_original_allure_title(func):
    # 检查函数是否有 __allure_title__ 属性（由 @allure.title 设置）
    if hasattr(func, "__allure_title__"):
        return func.__allure_title__

    # 检查函数是否被 @allure.title 装饰
    source_code = inspect.getsource(func)
    for line in source_code.splitlines():
        line = line.strip()
        if line.startswith("@用例名称"):
            # 提取标题参数（简单正则匹配）
            import re

            match = re.search(r'@用例名称\(["\'](.*?)["\']\)', line)
            if match:
                return match.group(1)

    # 没有找到装饰器，使用函数名
    return func.__name__


# 获取所有测试用例的 ID
def pytest_collection_modifyitems(session, config, items):
    suffix = config.getoption("--test-suffix")
    if suffix:
        for item in items:
            # 修改测试项的原始名称（nodeid）
            original_name = item.name
            item.name = f"{original_name}_{suffix}"

            # 如果需要修改完整的 nodeid（包括模块路径）
            # 注意：修改 nodeid 可能会影响某些依赖原始 nodeid 的功能
            original_nodeid = item.nodeid
            item._nodeid = f"{original_nodeid}_{suffix}"
            if isinstance(item, Function):
                # 获取测试函数的原始标题
                original_title = _get_original_allure_title(item.function)
                item.original_allure_title = original_title
    # if session.config.getoption("--monitor") == "on":
    #     # todo 开启会导致执行失败，待解决
    #     # 随机打乱测试用例的顺序
    #     items_monitor = []
    #     for item in items:
    #         if "monitor" in str(item.own_markers):
    #             items_monitor.append(item)
    #     items.clear()
    #     for item_fix in items_monitor:
    #         items.append(item_fix)
    #     random.seed(time.time())  # 重置seed,否则每次都一致
    #     random.shuffle(items)
    #     # 设置需要执行的测试用例数量
    #     number_of_tests_to_run = 1
    #     # 如果有更多的测试用例，则只保留前 number_of_tests_to_run 个
    #     if len(items) > number_of_tests_to_run:
    #         items[:] = items[:number_of_tests_to_run]
    # else:
    #     with FileLock(get_path(".Auth/seed.lock"), timeout=30):
    #         if os.path.exists(get_path("../../.Auth/seed.txt")):
    #             with open(get_path("../../.Auth/seed.txt"), "r") as f:
    #                 seed = int(f.read())
    #         else:
    #             seed = random.randint(0, 1000)
    #             with open(get_path("../../.Auth/seed.txt"), "w") as f:
    #                 f.write(str(seed))
    #     random.seed(seed)
    #     random.shuffle(items)
    # else:
    #     # with open(get_path(".Auth/items.txt"), "w") as f:
    #     #     f.write(str(items).replace("<Function ", "").replace(">", "")[1:-1])
    #     appoint_classes = {"TestUser": [], "TestOrder": [], "TestStock": []}
    #     for item in items:
    #         for cls_name in appoint_classes:
    #             if item.parent.name == cls_name:
    #                 appoint_classes[cls_name].append(item)
    #     items.clear()
    #     for cases in appoint_classes.values():
    #         items.extend(cases)


@pytest.hookimpl
def pytest_runtest_call(item):
    suffix = item.config.getoption("--test-suffix")
    if suffix and hasattr(item, "original_allure_title"):
        allure.dynamic.title(f"{item.original_allure_title}_{suffix}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.failed:
        try:
            for page in item.funcargs["oc_page"].page.context.pages:
                if page.is_closed():
                    continue
                bytes_png = page.screenshot(timeout=5000, full_page=True)
                allure.attach(bytes_png, f"失败截图---{page.title()}")
            if sys.gettrace():
                try:
                    item.funcargs["oc_page"].page.context.pages[-1].pause()
                except:
                    pass
        except:
            ...
        try:
            stack_trace = traceback.extract_tb(call.excinfo.tb)
            for frame in reversed(stack_trace):
                # 获取帧对应的模块路径
                module_path = frame.filename
                # 判断是否是测试用例代码所在的模块
                if "test_" in os.path.basename(module_path):
                    global 失败行的源码
                    失败行的源码 = frame.line
                    break
            global 最后一次执行的步骤
            最后一次执行的步骤 = list(
                filter(
                    lambda line: "with 测试步骤" in line,
                    report.longreprtext.splitlines(),
                )
            )[
                -1
            ].strip()[len('with 测试步骤("') : -len('"):')]
            for index, element in enumerate(reversed(report.longreprtext.splitlines())):
                if "> " in element:
                    global call_log
                    call_log = "\n".join(report.longreprtext.splitlines()[-index:])
                    break
        except:
            pass


@pytest.fixture(scope="session")
def global_map():
    global_map = GlobalMap()
    yield global_map


@pytest.fixture
def test_name(request):
    random.seed(time.time())
    return request.node.name.split("[")[0]


@pytest.fixture(scope="session", autouse=True)
def rename_test_id(playwright):
    playwright.selectors.set_test_id_attribute("data-tester-id")


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each p-tes case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def pytest_addoption(parser: Any) -> None:
    group = parser.getgroup("playwright", "Playwright")
    group.addoption(
        "--har",
        default="off",
        help="har record and analyse",
        choices=["on", "analyse", "off"],
    )
    group.addoption(
        "--persistent",
        default="clear_on_video_round",
        help="save and use local user data",
        choices=["on", "off"],
    )
    group.addoption(
        "--otherAuth",
        default=None,
        help="Other Environmental Authentication,ex: tc,clm",
    )
    group.addoption(
        "--feishu",
        default=None,
        help="feishu_receive_id",
    )
    group.addoption(
        "--jobUrl",
        default=None,
        help="Jenkins Job url",
    )
    group.addoption(
        "--ui_timeout",
        default=30000,
        help="locator timeout and expect timeout",
    )
    group.addoption(
        "--monitor",
        default="off",
        help="monitor mode,only run one testcase randomly",
    )
    group.addoption(
        "--send_feishu_report",
        default="off",
        help="monitor mode,only run one testcase randomly",
    )
    group.addoption(
        "--report_mark",
        default="",
        help="飞书的report消息的title里的mark",
    )
    group.addoption(
        "--tempdir",
        default="",
        help="为默认的空时,使用系统临时文件夹,否则使用传过来的文件夹,在指定路径下新建文件夹pw_temp",
    )
    group.addoption(
        "--use_feishu",
        default="on",
        help="如果私网跑自动化,设置为off就不使用任何飞书api",
        choices=["on", "off"],
    )
    group.addoption(
        "--wsendpoint",
        type=str,
        default="",
        help="""
        可以通过cdp启动或者使用'playwright launch-server --browser=chromium --config ws-config.json'来启动,
        传入的参数举例: ws://192.168.3.46:33013/0867ca426dcfb6474c055e1c7035ec49,2;local,4
        前半部分为ws地址,逗号后面的2是ws支持的并发上限,多个ws用;分割,local代表本机执行
        """,
    )
    group.addoption(
        "--admin_password",
        default="off",
        help="如果设置这个密码,则把平台层操作用户名改成zl_auto_admin,密码改为传入值",
    )
    group.addoption(
        "--api_port",
        default="",
        help="如果设置了,会使用此端口替换掉原接口的'/api'",
    )
    group.addoption(
        "--total_requests",
        default="1",
        help="设置性能造数时要生成的数据量",
    )
    group.addoption(
        "--rerun_add_timeout",
        default="0",
        help="根据rerun增加超时时间,每次重试都增加相应的时间,比如初始的timeout是30_000,如果设置rerun_add_timeout为10_000,则第一次重试的timeout改为40_000",
    )
    parser.addoption("--test-suffix", action="store", default="", help="为所有测试用例名称添加后缀")


@pytest.fixture(scope="session")
def total_requests(pytestconfig):
    return str(pytestconfig.getoption("--total_requests"))


@pytest.fixture(scope="session")
def timeout(pytestconfig, request):
    global base_timeout
    base_timeout = float(pytestconfig.getoption("--ui_timeout"))
    return float(pytestconfig.getoption("--ui_timeout"))


@pytest.fixture(scope="session")
def admin_pwd(pytestconfig):
    return pytestconfig.getoption("--admin_password")


@pytest.fixture(scope="session")
def playwright() -> Generator[Playwright, None, None]:
    pw = sync_playwright().start()
    session_start_time = time.time()
    yield pw
    print(f"本轮测试耗时{int(time.time() - session_start_time)}秒")
    pw.stop()


@pytest.fixture
def browser_context_args(browser_context_args, request: pytest.FixtureRequest, pytestconfig: Any):
    output_dir = pytestconfig.getoption("--output")
    har_option = pytestconfig.getoption("--har")
    har_cap = har_option in ["on", "analyse"]
    if har_cap:
        har_path = os.path.join(output_dir, request.node.name, f"{request.node.name}.har")
        har = {"record_har_path": har_path}
    else:
        har = {}

    return {
        **browser_context_args,
        **har,
        "viewport": {"width": 1440, "height": 900},
        "record_video_size": {"width": 1440, "height": 900},
        "locale": "zh-CN",
        "ignore_https_errors": True,
    }


@pytest.fixture
def oc_context(
    playwright: Playwright,
    browser_type: BrowserType,
    browser_type_launch_args: Dict,
    browser_context_args: Dict,
    pytestconfig: Any,
    global_map,
    request: pytest.FixtureRequest,
    timeout,
) -> Generator[BrowserContext, None, None]:
    context, tracing_option, capture_trace, pages, video_option, video_on = context_setup(
        playwright,
        browser_type,
        browser_type_launch_args,
        browser_context_args,
        pytestconfig,
        global_map,
        request,
        persistent_ability=True,
        is_h5=False,
    )
    global time_out
    global base_timeout

    time_out = int(base_timeout) + (
        int(pytestconfig.getoption("--rerun_add_timeout")) * (int(request.node.execution_count) - 1)
    )

    context.set_default_timeout(timeout=time_out)
    context.set_default_navigation_timeout(timeout=time_out * 2)

    expect.set_options(timeout=time_out)
    yield context
    context_teardown(
        context,
        request,
        pytestconfig,
        tracing_option,
        capture_trace,
        pages,
        video_option,
        video_on,
    )


@pytest.fixture()
def oc_page(oc_context, pytestconfig, request, test_name, global_map):
    output_dir = pytestconfig.getoption("--output")
    log_dir = os.path.join(output_dir, request.node.name)
    global_map.set("last_run_testcase", test_name)
    yield PageInstance(oc_context, log_dir, test_name)


@pytest.fixture
def oc_context_backup(
    playwright: Playwright,
    browser_type: BrowserType,
    browser_type_launch_args: Dict,
    browser_context_args: Dict,
    pytestconfig: Any,
    global_map,
    request: pytest.FixtureRequest,
    timeout,
) -> Generator[BrowserContext, None, None]:
    context, tracing_option, capture_trace, pages, video_option, video_on = context_setup(
        playwright,
        browser_type,
        browser_type_launch_args,
        browser_context_args,
        pytestconfig,
        global_map,
        request,
    )
    global time_out
    global base_timeout
    time_out = int(base_timeout) + (
        int(pytestconfig.getoption("--rerun_add_timeout")) * (int(request.node.execution_count) - 1)
    )
    context.set_default_timeout(timeout=time_out)
    context.set_default_navigation_timeout(timeout=time_out * 2)
    expect.set_options(timeout=time_out)
    yield context
    context_teardown(
        context,
        request,
        pytestconfig,
        tracing_option,
        capture_trace,
        pages,
        video_option,
        video_on,
    )


@pytest.fixture()
def oc_page_backup(oc_context_backup, pytestconfig, request, test_name, global_map):
    output_dir = pytestconfig.getoption("--output")
    log_dir = os.path.join(output_dir, request.node.name)
    global_map.set("last_run_testcase", test_name)
    yield PageInstance(oc_context_backup, log_dir, test_name)


def response_filter(request):
    def inner(dialog: Dialog):
        message = dialog.message
        if "失败信息" in message:
            url = message.split(sep="失败信息:")[0]
            fail_info = message.split(sep="失败信息:")[1]
            error_list = [
                "Response status is 403",
                "程序出现错误，请联系管理员",
                "数据校验不通过",
                "error.resource.notExist",
            ]
            if fail_info not in error_list:
                dialog.accept()
                return
            dialog.accept()
            api_error_img_binary = dialog.page.screenshot(timeout=5000)
            global_map = GlobalMap()
            base_ul = global_map.get("base_url")
            use_feishu = global_map.get("use_feishu")
            if use_feishu == "on":
                feishu = FeiShuApi()
                image_key = feishu.upload_img(api_error_img_binary)
                feishu.send(
                    receive_id_type="chat_id",
                    receive_id="oc_b2350e0a81b15becb99e59e62c772e1f",
                    msg_type="interactive",
                    content=json.dumps(
                        {
                            "config": {"wide_screen_mode": True},
                            "header": {
                                "title": {
                                    "tag": "plain_text",
                                    "content": f"{base_ul}的测试用例{request.node.name}发现接口告警:",
                                },
                                "template": "turquoise",
                            },
                            "elements": [
                                {
                                    "tag": "div",
                                    "text": {
                                        "tag": "lark_md",
                                        "content": f"url:\n{url}\n失败信息:\n{fail_info}",
                                    },
                                },
                                {
                                    "tag": "img",
                                    "img_key": image_key,
                                    "alt": {
                                        "tag": "plain_text",
                                        "content": "失败时的截图",
                                    },
                                },
                            ],
                        }
                    ),
                )

    return inner


@pytest.fixture
def h5_context(
    playwright: Playwright,
    browser_type: BrowserType,
    browser_type_launch_args: Dict,
    browser_context_args: Dict,
    pytestconfig: Any,
    global_map,
    request: pytest.FixtureRequest,
    timeout,
) -> Generator[BrowserContext, None, None]:
    context, tracing_option, capture_trace, pages, video_option, video_on = context_setup(
        playwright,
        browser_type,
        browser_type_launch_args,
        browser_context_args,
        pytestconfig,
        global_map,
        request,
        persistent_ability=False,
        is_h5=True,
    )
    global time_out
    global base_timeout
    time_out = int(base_timeout) + (
        int(pytestconfig.getoption("--rerun_add_timeout")) * (int(request.node.execution_count) - 1)
    )
    context.set_default_timeout(timeout=time_out)
    context.set_default_navigation_timeout(timeout=time_out * 2)
    expect.set_options(timeout=time_out)
    yield context
    context_teardown(
        context,
        request,
        pytestconfig,
        tracing_option,
        capture_trace,
        pages,
        video_option,
        video_on,
    )


@pytest.fixture()
def h5_page(h5_context, pytestconfig, request, test_name, global_map):
    output_dir = pytestconfig.getoption("--output")
    log_dir = os.path.join(output_dir, request.node.name)
    global_map.set("last_run_testcase", test_name)
    yield PageInstance(h5_context, log_dir, test_name)


def pytest_terminal_summary(terminalreporter, config):
    mark = config.getoption("report_mark")
    global_map = GlobalMap()
    base_ul = global_map.get("base_url")
    failed_test_name_str = global_map.get("failed_test_name_str", default="")
    for report in terminalreporter.getreports("failed"):
        test_name = report.nodeid  # 获取失败用例的名称
        if f"{mark}:{test_name}" not in global_map.get("failed_test_name_str", default=""):
            failed_test_name_str = f"{failed_test_name_str}\n{mark}:{test_name}"
            global_map.set("failed_test_name_str", failed_test_name_str)
    for report in terminalreporter.getreports("error"):
        test_name = report.nodeid  # 获取错误用例的名称
        if f"{mark}:{test_name}" not in global_map.get("failed_test_name_str", default=""):
            failed_test_name_str = f"{failed_test_name_str}\n{mark}:{test_name}"
            global_map.set("failed_test_name_str", failed_test_name_str)
    feishu_receive_id = global_map.get("feishu_receive_id")
    jobUrl = global_map.get("jobUrl")
    if not hasattr(config, "workerinput"):
        print("进入阶段性数据获取:------------------------------------------")
        try:
            os.remove(get_path(".Auth/ws-endpoint.json"))
            print(f"文件ws-endpoint.json已成功删除。")
        except FileNotFoundError:
            print(f"未找到文件ws-endpoint.json")
        except PermissionError:
            print(f"没有权限删除文件ws-endpoint.json")
        except Exception as e:
            print(f"删除文件ws-endpoint.json时出现错误: {e}")
        passed = len([i for i in terminalreporter.stats.get("passed", []) if i.when != "teardown"])
        failed = len([i for i in terminalreporter.stats.get("failed", []) if i.when != "teardown"])
        error = len([i for i in terminalreporter.stats.get("error", []) if i.when != "teardown"])
        # skipped = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
        total = passed + failed + error
        环境字典 = {"http://192.168.10.240:8060/basic-front/login": "test"}
        环境信息 = 环境字典.get(base_ul, base_ul)
        # 把结果写入global_map,如果已有结果,则改为追加数量
        for stat, value in {
            "passed": passed,
            "failed": failed,
            "error": error,
            "total": total,
        }.items():
            if global_map.get(f"{环境信息}-{stat}") is None:
                global_map.set(f"{环境信息}-{stat}", value)
            else:
                global_map.set(
                    f"{环境信息}-{stat}",
                    int(global_map.get(f"{环境信息}-{stat}")) + value,
                )
        if config.getoption("send_feishu_report") == "on":
            # 增加取global_map中总计结果的代码
            if feishu_receive_id is not None and feishu_receive_id != "auto":
                if config.getoption("--monitor") == "off" or (
                    config.getoption("--monitor") == "on" and (failed or error)
                ):
                    feishu_send = FeiShuApi()
                    if "ou_" in feishu_receive_id:
                        receive_id_type = "open_id"
                    else:
                        receive_id_type = "chat_id"
                    if config.getoption("--monitor") == "off":
                        if config.getoption("report_mark") == "汇总":
                            total_final = global_map.get(f"{环境信息}-total")
                            total_passed = global_map.get(f"{环境信息}-passed")
                            total_failed = global_map.get(f"{环境信息}-failed")
                            total_error = global_map.get(f"{环境信息}-error")
                            # total_skipped = global_map.get(f"{env}-skipped")
                        else:
                            total_final = total
                            total_passed = passed
                            total_failed = failed
                            total_error = error
                            # total_skipped = skipped
                        if mark == "汇总":
                            feishu_json = {
                                "config": {"wide_screen_mode": True},
                                "header": {
                                    "title": {
                                        "tag": "plain_text",
                                        "content": f"{环境信息}-{mark}-自动化测试结果:",
                                    },
                                    "template": "turquoise",
                                },
                                "elements": [
                                    {
                                        "tag": "div",
                                        "text": {
                                            "tag": "lark_md",
                                            "content": f"测试结果:\n测试用例总数:{total_final}\n测试用例成功数:{total_passed}\n测试用例失败数:{total_failed + total_error}\n失败的用例为:{failed_test_name_str}",
                                        },
                                    },
                                ],
                            }
                            if jobUrl and jobUrl != "None":
                                feishu_json["elements"].append(
                                    {
                                        "tag": "action",
                                        "actions": [
                                            {
                                                "tag": "button",
                                                "text": {
                                                    "tag": "plain_text",
                                                    "content": "立即查看log",
                                                },
                                                "type": "default",
                                                "url": f"{jobUrl}allure/",
                                            }
                                        ],
                                    }
                                )
                            feishu_send.send(
                                receive_id_type=receive_id_type,
                                receive_id=feishu_receive_id,
                                msg_type="interactive",
                                content=json.dumps(feishu_json),
                            )
                        elif mark == "冒烟":
                            feishu_json = {
                                "config": {"wide_screen_mode": True},
                                "header": {
                                    "title": {
                                        "tag": "plain_text",
                                        "content": f"{环境信息}-{mark}-自动化测试结果:",
                                    },
                                    "template": "turquoise",
                                },
                                "elements": [
                                    {
                                        "tag": "div",
                                        "text": {
                                            "tag": "lark_md",
                                            "content": f"测试结果:\n测试用例总数:{total_final}\n测试用例成功数:{total_passed}\n测试用例失败数:{total_failed + total_error}\n失败的用例为:{failed_test_name_str}",
                                        },
                                    },
                                ],
                            }
                            feishu_send.send(
                                receive_id_type=receive_id_type,
                                receive_id=feishu_receive_id,
                                msg_type="interactive",
                                content=json.dumps(feishu_json),
                            )
                    else:
                        testcase_name = str(terminalreporter.stats)[
                            str(terminalreporter.stats).index("testcases") : str(terminalreporter.stats).index("' when")
                        ]
                        feishu_json = {
                            "config": {"wide_screen_mode": True},
                            "header": {
                                "title": {
                                    "tag": "plain_text",
                                    "content": f"{环境信息}生产监控发生失败:",
                                },
                                "template": "turquoise",
                            },
                            "elements": [
                                {
                                    "tag": "div",
                                    "text": {
                                        "tag": "lark_md",
                                        "content": f"失败用例名称:\n{testcase_name}",
                                    },
                                },
                            ],
                        }
                        if jobUrl and jobUrl != "None":
                            feishu_json["elements"].append(
                                {
                                    "tag": "action",
                                    "actions": [
                                        {
                                            "tag": "button",
                                            "text": {
                                                "tag": "plain_text",
                                                "content": "立即查看log",
                                            },
                                            "type": "default",
                                            "url": f"{jobUrl}allure/",
                                        }
                                    ],
                                }
                            )
                        feishu_send.send(
                            receive_id_type=receive_id_type,
                            receive_id=feishu_receive_id,
                            msg_type="interactive",
                            content=json.dumps(feishu_json),
                        )


class CustomBrowserType:
    def __init__(self, browser_type, custom_name):
        self.browser_type = browser_type
        self.custom_name = custom_name

    @property
    def name(self):
        return self.custom_name

    def __getattr__(self, attr):
        # 将其他属性和方法代理到原始的 BrowserType 对象
        return getattr(self.browser_type, attr)


def context_setup(
    playwright: Playwright,
    browser_type: BrowserType,
    browser_type_launch_args: Dict,
    browser_context_args: Dict,
    pytestconfig: Any,
    global_map,
    request: pytest.FixtureRequest,
    persistent_ability=False,
    is_h5=False,
):
    if is_h5:
        h5_config = playwright.devices["iPhone 13"]
        browser_context_args.update(**h5_config)
        browser_type = CustomBrowserType(playwright.webkit, "h5_webkit")
        browser_context_args["record_video_size"] = h5_config["viewport"]
    if pytestconfig.getoption("--tempdir"):
        tempdir = os.path.join(pytestconfig.getoption("--tempdir"), "pw_temp")
    else:
        tempdir = tempfile.gettempdir()
    base_url = global_map.get("base_url")
    pages: List[Page] = []
    # 如果不在这创建,可能会导致后面使用路径时找不到
    output_dir = pytestconfig.getoption("--output")
    log_dir = os.path.join(output_dir, request.node.name)
    os.makedirs(log_dir, exist_ok=True)
    persistent_option = pytestconfig.getoption("--persistent")
    video_option = pytestconfig.getoption("--video")
    rerun_count = pytestconfig.getoption("--reruns")
    tracing_option = pytestconfig.getoption("--tracing")
    browser_context_args["record_video_dir"] = artifacts_folder.name
    video_on = False
    if video_option == "on" or video_option == "retain-on-failure":
        if rerun_count:
            if rerun_count == request.node.execution_count:
                if tracing_option in "on, retain-on-failure":
                    video_on = True
            elif rerun_count == request.node.execution_count - 1:
                if tracing_option not in "on, retain-on-failure":
                    video_on = True
        else:
            video_on = True
    if not video_on:
        browser_context_args.pop("record_video_dir")
    if (
        persistent_option != "off"
        and persistent_ability
        and "persistent_off" not in [mark.name for mark in request.node.iter_markers()]
        and rerun_count != request.node.execution_count - 1
    ):

        def filter_kwargs(func, kwargs):
            """过滤函数不支持的关键字参数"""
            sig = inspect.signature(func)
            supported_params = sig.parameters
            return {k: v for k, v in kwargs.items() if k in supported_params}

        base_u = get_sub_url(base_url)
        print("start with persistent context")
        if request.node.execution_count != 1:
            file_path = os.path.join(tempdir, base_u, request.node.name)
            shutil.rmtree(file_path, ignore_errors=True)
            time.sleep(3)
            if not os.path.exists(file_path):
                print(f"文件夹 {file_path} 不存在")
            else:
                print(f"文件夹 {file_path} 存在")
            print(f"user-data文件{tempdir}/{base_u}/{request.node.name}已被清除并重新记录")
        print(f"user-data文件的地址是:{tempdir}/{base_u}/{request.node.name}")
        context = browser_type.launch_persistent_context(
            f"{tempdir}/{base_u}/{request.node.name}",
            **filter_kwargs(
                browser_type.launch_persistent_context,
                {
                    **browser_type_launch_args,
                    **browser_context_args,
                },
            ),
        )
    else:
        if is_h5:
            print("start with local h5 context")
        else:
            print("start with local context")
        if os.getenv("PLAYWRIGHT_SERVICE_ACCESS_TOKEN", default=None) and os.getenv(
            "PLAYWRIGHT_SERVICE_URL", default=None
        ):
            print("use azure playwright service")
            context = browser_type.connect(
                ws_endpoint=f'{os.getenv("PLAYWRIGHT_SERVICE_URL")}?' + 'cap={"os":"linux","runId":"test111"}',
                headers={"x-mpt-access-key": os.getenv("PLAYWRIGHT_SERVICE_ACCESS_TOKEN")},
            ).new_context(**{**browser_context_args})
        else:
            print("use local playwright service")
            if is_h5:
                context = browser_type.launch(**browser_type_launch_args, slow_mo=2_000).new_context(
                    **{**browser_context_args}
                )
            else:
                context = browser_type.launch(**browser_type_launch_args).new_context(**{**browser_context_args})
    # context.add_init_script(path=get_path("/utils/domObserver2.js"))
    # todo 弹框报错监听待改造
    # context.on("dialog", response_filter(request))

    #  上下文里监听,有新的page就添加到列表中
    global api_Count

    def on_page(page: Page):
        def on_clear(my_page: Page):
            try:
                api_Count.clear()
                my_page.wait_for_timeout(500)
            except:
                pass

        pages.append(page)
        page.on("close", on_clear)
        page.on("load", on_clear)

    def on_add_request(req):
        if (base_url in req.url) and ("/api/hadm/v1/market/config/show-flag" not in req.url):
            api_Count.append(req.url)

    def on_remove_request(req):
        try:
            api_Count.remove(req.url)
        except:
            pass

    context.on("page", on_page)
    context.on("request", on_add_request)
    context.on("requestfinished", on_remove_request)
    context.on("requestfailed", on_remove_request)

    capture_trace = tracing_option in "on, retain-on-failure" and rerun_count == request.node.execution_count - 1
    if capture_trace:
        context.tracing.start(
            name=slugify(request.node.name),
            screenshots=True,
            snapshots=True,
            sources=True,
        )
    return context, tracing_option, capture_trace, pages, video_option, video_on


def context_teardown(
    context,
    request,
    pytestconfig,
    tracing_option,
    capture_trace,
    pages,
    video_option,
    video_on,
):
    failed = request.node.rep_call.failed if hasattr(request.node, "rep_call") else True
    if not hasattr(request.node, "rep_fin"):
        if failed:
            print(f"\n{request.node.name} is failed")
        else:
            print(f"\n{request.node.name} is pass")
        setattr(request.node, "rep_fin", "")
    output_dir = pytestconfig.getoption("--output")
    if capture_trace:
        retain_trace = tracing_option == "on" or (failed and tracing_option == "retain-on-failure")
        if retain_trace:
            trace_path = os.path.join(output_dir, request.node.name, f"{time.time_ns()}trace.zip")
            context.tracing.stop(path=trace_path)
            allure.attach.file(trace_path, "trace.playwright.dev", extension="zip")
        else:
            context.tracing.stop()

    for index, page in enumerate(pages):
        try:
            bytes_png = page.screenshot(timeout=5000)
            allure.attach(bytes_png, f"最终截图---{page.title()}")
        except Error:
            pass

    context.close()
    if video_option == "retain-on-failure":
        video_on = failed
    if video_on:
        global video_index
        for page in pages:
            video_index += 1
            video = page.video
            if not video:
                continue
            try:
                if page is 最后操作的page and failed:
                    失败的录像名字 = f"{video_index}_{request.node.name}_失败时的录像.webm"
                else:
                    失败的录像名字 = f"{video_index}_{request.node.name}.webm"
                video.save_as(
                    path=os.path.join(
                        output_dir,
                        request.node.name,
                        失败的录像名字,
                    )
                )
                allure.attach.file(
                    os.path.join(
                        output_dir,
                        request.node.name,
                        失败的录像名字,
                    ),
                    失败的录像名字,
                    allure.attachment_type.WEBM,
                )
            except Error:
                pass
    try:
        global_map = GlobalMap()
        base_ul = global_map.get("base_url")
        feishu_receive_id = global_map.get("feishu_receive_id")
        use_feishu = global_map.get("use_feishu")
        global send_feishu_message

        test_name_flag = request.node.name
        if test_name_flag == request.node.name:
            send_feishu_message = 1
            #  加上 reruns 为0 的特判
        if request.node.execution_count == 1 and request.node.reruns:
            send_feishu_message = 0

        if (
            request.node.execution_count - 1 == request.config.option.reruns
            and feishu_receive_id
            and failed
            and not send_feishu_message
        ):
            send_feishu_message = send_feishu_message + 1
            if feishu_receive_id == "auto" or use_feishu != "on":
                return
            if "ou_" in feishu_receive_id:
                receive_id_type = "open_id"
            else:
                receive_id_type = "chat_id"
            环境字典 = {
                "http://192.168.10.240:8060/a-front/": "测试环境",
                "https://dev.baidu.com": "开发环境",
                "https://uat.baidu.com": "UAT环境",
            }
            环境信息 = 环境字典.get(base_ul, base_ul)
            feishu = FeiShuApi()

            def get_frame_bytes_png(video_path):
                import io

                from moviepy import VideoFileClip
                from PIL import Image

                clip = VideoFileClip(video_path)
                _frame = clip.get_frame(5)
                pil_image = Image.fromarray(_frame)
                output = io.BytesIO()
                pil_image.save(output, format="PNG")
                byte_png = output.getvalue()
                return byte_png

            def process_webm_files(folder_path):
                video_key_list = []
                img_key_list = []
                webm_files = [
                    os.path.join(folder_path, f)
                    for f in os.listdir(folder_path)
                    if f.endswith(".webm") and "_失败时的录像" in f
                ]
                if not webm_files:
                    webm_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".webm")]
                for webm_file in webm_files:
                    try:
                        file_key = feishu.upload_mp4(webm_file)
                        video_key_list.append(file_key)
                        img_key_0 = feishu.upload_img(get_frame_bytes_png(webm_file.replace(".webm", ".mp4")))
                        img_key_list.append(img_key_0)
                    except Exception as e:
                        print(f"处理文件 {webm_file} 时出错: {str(e)}")
                return video_key_list, img_key_list

            video_keys, img_keys = process_webm_files(os.path.join(output_dir, request.node.name))
            消息总个数 = len(video_keys)
            当前消息轮次 = 0
            for video_key, img_key in zip([0] + video_keys, [0] + img_keys):
                if 当前消息轮次 == 0:
                    print("********************************")
                    feishu.send(
                        receive_id_type=receive_id_type,
                        receive_id=feishu_receive_id,
                        msg_type="interactive",
                        content=json.dumps(
                            {
                                "config": {"wide_screen_mode": True},
                                "header": {
                                    "title": {
                                        "tag": "plain_text",
                                        "content": f"{环境信息}的测试用例{request.config.option.report_mark}:{request.node.name}的失败信息:",
                                    },
                                    "template": "turquoise",
                                },
                                "elements": [
                                    {
                                        "tag": "div",
                                        "text": {
                                            "tag": "plain_text",
                                            "content": f"失败的步骤为:\n{最后一次执行的步骤}",
                                            "text_color": "yellow",
                                        },
                                    },
                                    {
                                        "tag": "div",
                                        "text": {
                                            "tag": "plain_text",
                                            "content": f"失败的源码:\n{失败行的源码}",
                                            "text_color": "blue",
                                        },
                                    },
                                    {
                                        "tag": "div",
                                        "text": {
                                            "tag": "plain_text",
                                            "content": f"失败的报错:\n{call_log}",
                                            "text_color": "red",
                                        },
                                    },
                                ],
                            }
                        ),
                    )
                else:
                    feishu.send(
                        receive_id_type=receive_id_type,
                        receive_id=feishu_receive_id,
                        msg_type="post",
                        content=json.dumps(
                            {
                                "zh_cn": {
                                    "title": f"{环境信息}的测试用例{request.config.option.report_mark}:{request.node.name}失败录像:({当前消息轮次}/{消息总个数})",
                                    "content": [
                                        [
                                            {
                                                "tag": "media",
                                                "file_key": video_key,
                                                "image_key": img_key,
                                            }
                                        ]
                                    ],
                                }
                            }
                        ),
                    )
                当前消息轮次 = 当前消息轮次 + 1
    except:
        pass
    har_option = pytestconfig.getoption("--har")
    update_list = []
    if har_option == "analyse":
        har_path = os.path.join(output_dir, request.node.name, f"{request.node.name}.har")
        header = ["请求类型", "请求地址", "请求参数", "请求耗时(ms)"]
        analyse_list = analyse_har(har_path, rspTime=1000)
        analyse_list_split = [analyse_list[i : i + 400] for i in range(0, len(analyse_list), 400)]
        for analyse_list_temp in analyse_list_split:
            update_list = []
            for har_one in analyse_list_temp:
                har_one[2] = str(har_one[2])
                har_dict_one = dict(zip(header, har_one))
                update_list.append(har_dict_one)
        if update_list:
            feishu = FeiShuApi()
            table_token = "Bk4CbfXQ0adtvmsaSitcDoBrnyc"
            table_id = "tbl0rIx1AqSP5Ns0"
            feishu.bitable_create_records(table_token=table_token, table_id=table_id, raw_fields=update_list)


class Locator(_Locator):
    __last_step = None

    @property
    def selector(self):
        _repr = self.__repr__()
        if "selector" in _repr:
            __selector = []
            for _ in _repr.split("selector=")[1][1:-2].split(" >> "):
                if r"\\u" not in _:
                    __selector.append(_)
                    continue
                __selector.append(_.encode("utf8").decode("unicode_escape").encode("utf8").decode("unicode_escape"))
            return " >> ".join(__selector)

    def __getattribute__(self, attr):
        global api_Count
        global time_out
        try:
            orig_attr = super().__getattribute__(attr)
            if callable(orig_attr):

                def wrapped(*args, **kwargs):
                    step_title = None
                    if attr == "_sync" and self.__last_step:
                        step_title = self.__last_step
                    else:
                        self.__last_step = attr
                    start_time = time.time()
                    global 最后操作的page
                    最后操作的page = self.page
                    while True:
                        if time.time() - start_time < int(time_out / 1333):
                            try:
                                if attr in [
                                    "click",
                                    "fill",
                                    "type",
                                    "press_sequentially",
                                    "hover",
                                    "check",
                                    "uncheck",
                                    "set_checked",
                                    "blur",
                                    "focus",
                                    "clear",
                                    "tap",
                                ]:
                                    try:
                                        self.page.wait_for_load_state()
                                        self.page.locator("//*[contains(@class, 'spin-dot-spin')]").filter(
                                            visible=True
                                        ).last.wait_for(state="hidden", timeout=time_out)
                                        start = time.time()
                                        while time.time() - start > 3:
                                            if self.page.evaluate("document.readyState === 'complete';"):
                                                break
                                    except:
                                        pass
                                    api_length = len(api_Count)
                                    if api_Count:
                                        try:
                                            self.page.evaluate(
                                                """() => {
                                                   const spanToRemove = document.getElementById('ainotestgogogo');
                                                   if (spanToRemove) {
                                                       spanToRemove.remove();
                                                   }
                                               }"""
                                            )
                                            self.page.evaluate(
                                                f"""() => {{
                                                    const span = document.createElement('span');
                                                    span.textContent = '{attr}:{api_length}';
                                                    span.style.position = 'absolute';
                                                    span.style.top = '0';
                                                    span.style.left = '50%';
                                                    span.style.transform = 'translateX(-50%)';
                                                    span.style.backgroundColor = 'yellow'; // 设置背景色以便更容易看到
                                                    span.style.zIndex = '9999';
                                                    span.id = 'ainotestgogogo';
                                                    document.body.appendChild(span);
                                                }}"""
                                            )
                                        except:
                                            pass
                                    else:
                                        # 在这里可以添加自己需要等待或者处理的动作,比如等待转圈,关闭弹窗等等(当然,弹窗最好单独做个监听)
                                        self.page.locator("//*[contains(@class, 'spin-dot-spin')]").filter(
                                            visible=True
                                        ).last.wait_for(state="hidden", timeout=time_out)
                                        if (
                                            self.page.locator(
                                                '//div[@class="antHcbm_routesDashboardCardsHcbmCards_down"][text()="关闭"]'
                                            )
                                            .filter(visible=True)
                                            .or_(
                                                self.page.locator(".driver-close-btn")
                                                .filter(has_text="关闭")
                                                .filter(visible=True)
                                            )
                                            .count()
                                        ):
                                            self.page.locator(
                                                '//div[@class="antHcbm_routesDashboardCardsHcbmCards_down"][text()="关闭"]'
                                            ).filter(visible=True).or_(
                                                self.page.locator(".driver-close-btn")
                                                .filter(has_text="关闭")
                                                .filter(visible=True)
                                            ).last.evaluate(
                                                "node => node.click()"
                                            )
                                        try:
                                            self.page.evaluate(
                                                """() => {
                                                    const spanToRemove = document.getElementById('ainotestgogogo');
                                                    if (spanToRemove) {
                                                        spanToRemove.remove();
                                                    }
                                                }"""
                                            )
                                            self.page.evaluate(
                                                f"""() => {{
                                                    const span = document.createElement('span');
                                                    span.textContent = '{attr}:{api_length}';
                                                    span.style.position = 'absolute';
                                                    span.style.top = '0';
                                                    span.style.left = '50%';
                                                    span.style.transform = 'translateX(-50%)';
                                                    span.style.backgroundColor = 'green'; // 设置背景色以便更容易看到
                                                    span.style.zIndex = '9999';
                                                    span.id = 'ainotestgogogo';
                                                    document.body.appendChild(span);
                                                }}"""
                                            )
                                        except:
                                            pass
                                        break
                                else:
                                    break
                            except:
                                try:
                                    self.page.evaluate(
                                        """() => {
                                            const spanToRemove = document.getElementById('ainotestgogogo');
                                            if (spanToRemove) {
                                                spanToRemove.remove();
                                            }
                                        }"""
                                    )
                                    self.page.evaluate(
                                        f"""() => {{
                                            const span = document.createElement('span');
                                            span.textContent = '操作等待中.....';
                                            span.style.position = 'absolute';
                                            span.style.top = '0';
                                            span.style.left = '50%';
                                            span.style.transform = 'translateX(-50%)';
                                            span.style.backgroundColor = 'red'; // 设置背景色以便更容易看到
                                            span.style.zIndex = '9999';
                                            span.id = 'ainotestgogogo';
                                            document.body.appendChild(span);
                                        }}"""
                                    )
                                except:
                                    pass
                                break
                        else:
                            try:
                                self.page.evaluate(
                                    """() => {
                                        const spanToRemove = document.getElementById('ainotestgogogo');
                                        if (spanToRemove) {
                                            spanToRemove.remove();
                                        }
                                    }"""
                                )
                                escaped_api_count = json.dumps(api_Count)
                                self.page.evaluate(
                                    f"""() => {{
                                        const span = document.createElement('span');
                                        span.textContent = `当前列表内容为: {escaped_api_count}`;
                                        span.style.position = 'absolute';
                                        span.style.top = '0';
                                        span.style.left = '50%';
                                        span.style.transform = 'translateX(-50%)';
                                        span.style.backgroundColor = 'red'; // 设置背景色以便更容易看到
                                        span.style.zIndex = '9999';
                                        span.id = 'ainotestgogogo';
                                        document.body.appendChild(span);
                                    }}"""
                                )
                                self.page.wait_for_timeout(int(time_out / 6))
                                self.page.evaluate(
                                    """() => {
                                        const spanToRemove = document.getElementById('ainotestgogogo');
                                        if (spanToRemove) {
                                            spanToRemove.remove();
                                        }
                                    }"""
                                )
                            except:
                                pass
                            if sys.platform != "linux":

                                # pdb.set_trace()  侵入式端点调试
                                print(f"卡了{int(time_out / 1333)}秒了:")
                                try:
                                    print(escaped_api_count)
                                except:
                                    pass
                                pass
                            api_Count.clear()
                            break

                    if step_title:
                        # print(self.selector)
                        with step(f"{step_title}: {self.selector}"):
                            return orig_attr(*args, **kwargs)
                    return orig_attr(*args, **kwargs)

                return wrapped
            return orig_attr
        except AttributeError:
            ...


mapping.register(LocatorImpl, Locator)
