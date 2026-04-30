import datetime
import random
import re
import sys
import os
import time
import allure
import pytest
import json
from jsonpath import jsonpath
from urllib.parse import quote, unquote

from utils.tools import get_path, get_sub_url
from playwright.sync_api import Page, expect, Locator, Request, Response, TimeoutError
from utils.oc_time import 返回当前时间xxxx_xx_xx加N天
from .Locators import Locators
from .table import Table
from typing import Union, Optional, Literal
from utils.excel import Excel
from utils.ApiCount import apiCount

if sys.version_info >= (3, 8):
    from typing import Literal, Union
else:
    from typing_extensions import Literal


class PageObject:
    def __init__(self, page: Page):
        self.page = page
        self.url = ""
        self.__tenant_id = None
        self.api_headers = None
        # default_timeout = 30_000
        # self.default_timeout = default_timeout
        # self.page.set_default_navigation_timeout(2 * default_timeout)
        # self.page.set_default_timeout(default_timeout)
        self.locators = Locators(page)
        self.组件类型 = "OCANT"
        self.loc_tab指定审批人员工 = self.locators.modal_弹窗().locator('[role="tab"]', has_text='员工')
        self.loc_tab指定审批人用户 = self.locators.modal_弹窗().locator('[role="tab"]', has_text='用户')
        try:
            self.page.add_locator_handler(
                self.page.frame_locator("//iframe[contains(@src,'www.xmplus.cn')]").locator("#surveyClient").filter(
                    visible=True),
                lambda overlay: page.frame(url=re.compile("www.xmplus.cn")).frame_element().evaluate("""(element) => {
                    element.style.display = 'none'
                }"""))
            self.page.add_locator_handler(self.page.locator(".driver-close-btn").filter(visible=True).last,
                                          lambda overlay: self.page.locator(".driver-close-btn").filter(
                                              visible=True).last.click())
        except:
            pass

    def navigate(self, 操作环境: str = None):
        """
        跳转到指定页面
        :param 操作环境: 默认传None时,使用base_url里的环境信息,否则传指定的环境信息,比如"https://clm.onecontract-cloud.com"
        :return:
        """
        if 操作环境:
            self.page.goto(f"{操作环境}{self.url}")
        else:
            self.page.goto(self.url)
        try:
            self.page.wait_for_timeout(200)
            # self.page.wait_for_load_state("networkidle", timeout=10_000)
            self.page.locator("*").filter(visible=True).first.click(trial=True)
            self.locators.loading_页面四瓣加载().wait_for(state="hidden")
        except:
            pass

    @property
    def tenant_id(self):
        if self.__tenant_id is None:
            from utils.globalMap import GlobalMap
            global_map = GlobalMap()
            api_base_url = global_map.get("api_base_url")
            result = self.page.request.get(url=f"{api_base_url}/iam/hzero/v1/users/self",
                                           headers=self.api_headers).json()
            self.__tenant_id = result["tenantId"]
            global_map.set("tenantId", self.__tenant_id)
        return self.__tenant_id

    def table(self, 唯一文字, 表格序号=-1):
        return Table(self.page, 唯一文字, 表格序号=表格序号)

    def close_tab(self, tab):
        self.page.click(f"[role=tab] div span:text('{tab}')", button="right")
        self.page.click("'关闭全部'")

    def wait_for_page_title_active(self, page_head_title):
        self.page.wait_for_selector(f".ant-tabs-tabpane-active span:text('{page_head_title}')")

    def set_设置当前用户为(self, 显示用户名: str = None, 登录用户名: str = None, 登录密码: str = None, 环境: str = None,
                           切换租户: str = None, 切换角色: str = None):
        """
        通过更改cookie的方法切换用户，需要切换后再navigate到目标页面
        :param 显示用户名: 显示用户名，比如"Qy业务员"
        :param 登录用户名: 登录用户名，比如"admin"
        :param 登录密码: 登录密码，比如"password"
        :param 环境: 如果要使用非默认的环境,比如在test环境下使用tc的账号,可以设置为"https://tc.onecontract-cloud.com/"
        :param 切换租户: 当用户有多个角色时,可以切换到需要使用的角色
        :param 切换角色: 当用户有多个角色时,可以切换到需要使用的角色
        :return:
        """
        from utils.globalMap import GlobalMap
        from filelock import FileLock
        is_h5 = self.page.viewport_size["width"] < self.page.viewport_size["height"]
        pages = self.page.context.pages
        for page in pages:
            if page is not self.page:
                page.close()
        if not 环境:
            env = get_sub_url(GlobalMap().get("base_url"))
            baseurl = ""
        else:
            env = get_sub_url(环境)
            if 环境.endswith("/"):
                baseurl = 环境[:-1]
            else:
                baseurl = 环境
        if 登录用户名:
            用户名 = 登录用户名
        else:
            用户名 = 显示用户名
        with FileLock(get_path(f".Auth/{env}-{用户名}.lock"), timeout=60):
            self.page.context.clear_cookies()
            access_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            self.page.goto("about:blank")
            storage_state_exists = os.path.exists(get_path(f".Auth/{env}-{用户名}.json"))
            if storage_state_exists:
                with open(get_path(f".Auth/{env}-{用户名}.json"), "r") as f:
                    storage_state_json = json.load(f)
                cookies = storage_state_json["cookies"]
                self.page.context.add_cookies(cookies)
                if is_h5:
                    access_token = jsonpath(cookies, "$.[?(@.name=='access_token')].value")[0]
                    if not access_token:
                        access_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            try:
                if is_h5:
                    self.page.goto(f"{baseurl}{self.url}#access_token={access_token}")
                else:
                    self.page.goto(baseurl + self.url)
            except:
                pass
            # 跳转后的url,判断token是否已过期或账号未登录,如是,则登录.
            for _ in range(5):
                try:
                    self.page.get_by_text("菜单搜索").filter(visible=True).or_(
                        (self.page.get_by_alt_text("个人中心").filter(visible=True))).or_(
                        self.page.locator("#loginFormAccount").filter(visible=True)).or_(
                        self.page.get_by_text("重新登录").or_(self.page.get_by_text("登录失败，请重新打开应用")).or_(
                            self.page.locator(".tenantName")).filter(visible=True)).last.wait_for()
                    break
                except:
                    self.page.goto(baseurl + self.url)
                if _ == 4:
                    pytest.fail("登录时加载页面失败")
            if "/public/unauthorized" in self.page.url or "/oauth/login" in self.page.url or "/mobile/#/login" in self.page.url:
                self.page.context.clear_cookies()
                from models.登录页 import 登录页
                from models.合同查询页 import 合同查询页
                self.page.goto(f"{baseurl}/workplace")
                if 登录用户名:
                    登录页(self.page).login_页面登录(登录用户名, 登录密码)
                else:
                    # from utils.feishu_api import FeiShuApi
                    # feishu = FeiShuApi()
                    # user_info = feishu.get_bitable_records("bascnzFGLdVgybxipQLyLeDfAch", "tbl3LKdJduteNRij",
                    #                                        filter=f'CurrentValue.[名称]="{显示用户名}" && CurrentValue.[环境]="{env}"').json()
                    # 登录用户名 = user_info["data"]["items"][0]["fields"]["账号"]
                    # 登录密码 = user_info["data"]["items"][0]["fields"]["密码"]
                    with open(get_path("config/all_auth.txt"), "r", encoding="utf-8") as auth:
                        auth_info = json.loads(auth.read())
                    登录用户名 = auth_info[显示用户名]["账号"]
                    登录密码 = auth_info[显示用户名]["密码"]
                    登录页(self.page).login_页面登录(登录用户名, 登录密码)
                self.page.context.storage_state(path=get_path(f".Auth/{env}-{用户名}.json"))
                try:
                    合同查询页(self.page).navigate()
                    合同查询页(self.page).switch_切换到列表视图()
                except:
                    pass
                try:
                    if is_h5:
                        access_token = jsonpath(self.page.context.cookies(), "$.[?(@.name=='access_token')].value")[0]
                        self.page.goto(f"{baseurl}{self.url}#access_token={access_token}")
                    else:
                        self.page.goto(baseurl + self.url)
                except:
                    pass
                self.page.bring_to_front()
            for cookie in self.page.context.cookies():
                if cookie.get("name") == "access_token" and cookie.get("domain") in self.page.url:
                    self.api_headers = {"Authorization": f"bearer {cookie.get('value')}"}
        if 切换租户:
            expect(self.page.locator(".hzero-normal-header-right").locator(
                ".ant-select-selection-selected-value").last.or_(self.page.get_by_alt_text("个人中心"))).to_be_visible()
            if self.page.locator(".hzero-normal-header-right").locator(
                    ".ant-select-selection-selected-value").last.count():
                self.wait_等待网络请求结束()
                if self.page.locator(".hzero-normal-header-right").locator(
                        ".ant-select-selection-selected-value").last.text_content() == 切换租户:
                    pass
                else:
                    self.hover_加重试的hover(self.page.locator(".hzero-normal-header-right").locator(
                        ".ant-select-selection-selected-value").last,
                                             self.page.locator("li").filter(has_text="查看所有租户"),
                                             "click", "click")
                    self.page.locator("a").filter(has_text=切换租户).click()
            else:
                self.hover_加重试的hover(self.page.get_by_alt_text("个人中心"), self.page.get_by_text("租户切换"))
                self.page.get_by_text(切换租户, exact=True).click()
            self.wait_等待网络请求结束()
            self.page.wait_for_load_state()
            self.page.wait_for_timeout(3_000)
            try:
                if is_h5:
                    access_token = jsonpath(self.page.context.cookies(), "$.[?(@.name=='access_token')].value")[0]
                    self.page.goto(f"{baseurl}{self.url}#access_token={access_token}")
                else:
                    self.page.goto(baseurl + self.url)
            except:
                pass
            self.page.bring_to_front()
        if 切换角色:
            for _ in range(3):
                try:
                    self.page.locator(".hzero-normal-header-right-item-avatar-name").click()
                    self.page.locator(".ant-menu-submenu-title").click(timeout=3_000)
                    self.page.locator('//li[@role="menuitem"]').get_by_text(切换角色, exact=True).filter(
                        visible=True).last.click(timeout=3_000)
                    self.page.wait_for_timeout(3_000)
                    try:
                        self.page.goto(baseurl + self.url, timeout=5_000)
                        self.page.get_by_text("菜单搜索").filter(visible=True).last.click(trial=True)
                    except:
                        pass
                    break
                except:
                    pass
                try:
                    if is_h5:
                        access_token = jsonpath(self.page.context.cookies(), "$.[?(@.name=='access_token')].value")[0]
                        self.page.goto(f"{baseurl}{self.url}#access_token={access_token}")
                    else:
                        self.page.goto(baseurl + self.url)
                except:
                    pass
                self.page.bring_to_front()

            # self.page.get_by_text("菜单搜索").last.or_(self.page.locator(".ant-btn-lg").last).or_(
            #     self.page.locator('//*[@id="username"]').last).wait_for()
            # 登录成功 = self.page.get_by_text("菜单搜索").count()
            # 身份失效 = self.page.locator(".ant-btn-lg").count()
            # 需要登录 = self.page.locator('//*[@id="username"]').count()
            # if 登录成功:
            #     return
            # if 身份失效 or 需要登录:
            #     from models.登录页 import 登录页
            #     self.page.goto(f"https://{env}.onecontract-cloud.com/oauth/login")
            #     if 登录用户名:
            #         登录页(self.page).login_页面登录(登录用户名, 登录密码)
            #     else:
            #         from utils.feishu_api import FeiShuApi
            #         feishu = FeiShuApi()
            #         user_info = feishu.get_bitable_records("bascnzFGLdVgybxipQLyLeDfAch", "tbl3LKdJduteNRij",
            #                                                filter=f'CurrentValue.[名称]="{显示用户名}" && CurrentValue.[环境]="{env}"').json()
            #         登录用户名 = user_info["data"]["items"][0]["fields"]["账号"]
            #         登录密码 = user_info["data"]["items"][0]["fields"]["密码"]
            #         登录页(self.page).login_页面登录(登录用户名, 登录密码)
            #     self.page.context.storage_state(path=get_path(f".Auth/{env}-{显示用户名}.json"))
            #     self.navigate()
            # self.page.bring_to_front()

    def click_button(self, text, nth=-1, timeout: int = "default", delay: int = None):
        try:
            self.page.locator("*").filter(visible=True).last.click(trial=True, timeout=5_000)
        except:
            pass
        if timeout == "default":
            self.wait_等待元素对象稳定(self.locators.button_按钮(text, nth))
        else:
            self.wait_等待元素对象稳定(self.locators.button_按钮(text, nth), timeout=timeout)
        if delay:
            self.page.wait_for_timeout(delay)
        if timeout == "default":
            self.locators.button_按钮(text, nth).click()
        else:
            self.locators.button_按钮(text, nth).click(timeout=timeout)

    def click_js点击隐藏的元素(self, locator: Locator):
        locator.wait_for(state="attached")
        locator.element_handle().wait_for_element_state(state="enabled")
        self.page.locator("#apiCounter").wait_for(state="detached")
        locator.evaluate("node => node.click()")

    def wait_等待button消失(self, text, nth=-1):
        self.locators.button_按钮(text, nth).wait_for(state="hidden")

    def wait_等待转圈出现并消失(self, timeout=10_000):
        try:
            self.locators.loading_页面四瓣加载().wait_for(timeout=timeout)
            self.locators.loading_页面四瓣加载().wait_for(state="hidden", timeout=timeout)
        except:
            pass

    def search_填写搜索框(self, 关键字=None, LOV内搜索=False, placeholder=None, delay=0, **字段_值):
        with self.page.expect_response(lambda response: (
                                                                quote(关键字) in response.request.url or 关键字 in response.request.url or 关键字 in str(
                                                                response.request.post_data) or quote(关键字) in str(
                                                                response.request.post_data)) and response.status == 200,
                                       timeout=120_000):
            self.locators.loading_页面四瓣加载().wait_for(state="detached")
            if placeholder:
                关键字定位 = self.page.get_by_placeholder(placeholder)
            else:
                关键字定位 = self.page.locator("//div[contains(@class, '_proSrcFilter_filter')]").or_(
                    self.page.locator("//*[@class='c7n-pro-table-filter-search']")).filter(visible=True).last.locator(
                    "input[type='text']").first
            if not LOV内搜索:
                try:
                    self.locators.modal_弹窗().wait_for(state="detached", timeout=500)
                except:
                    pass
            else:
                关键字定位 = self.locators.modal_弹窗().locator(关键字定位)
            if 关键字 is not None:
                关键字定位.clear()
                关键字定位.fill(关键字)
            for 字段, 值 in 字段_值.items():
                字段 = str(字段)
                值 = str(值)
                上层DIV定位 = self.page.locator('div[class*=-form-item-control-input]').filter(has_text=字段).locator(
                    'visible=true').nth(0)
                字段Select定位 = 上层DIV定位.locator('div[class*=-select-show-search]')
                字段日期定位 = 上层DIV定位.locator('div[class*=_datePicker]')
                字段输入框定位 = 上层DIV定位.locator("input[type='text']")
                if LOV内搜索:
                    上层DIV定位 = self.locators.modal_弹窗().locator(上层DIV定位)
                    字段Select定位 = self.locators.modal_弹窗().locator(字段Select定位)
                    字段日期定位 = self.locators.modal_弹窗().locator(字段日期定位)
                    字段输入框定位 = self.locators.modal_弹窗().locator(字段输入框定位)
                字段是LOV = 上层DIV定位.locator('div[class*=_proSrcLovPicker_picker]').count()
                if 字段是LOV:
                    当前modal元素数量 = self.locators.modal_弹窗().count()
                    点击LOV搜索按钮后modal数量 = 当前modal元素数量
                    self.page.locator(上层DIV定位).click()
                    LOV弹窗元素定位 = self.locators.modal_弹窗().nth(点击LOV搜索按钮后modal数量)
                    值列表 = 值.split("|")
                    for LOV值 in 值列表:
                        self.search_填写搜索框(LOV值, LOV内搜索=True)
                        LOV内checkbox = LOV弹窗元素定位.locator("input[type='checkbox']").count()
                        if LOV内checkbox:
                            LOV弹窗元素定位.locator("tr").filter(has_text=LOV值).locator(
                                'input[type="checkbox"]').click()
                        else:
                            LOV弹窗元素定位.locator("tr").filter(has_text=LOV值).locator('input[type="radio"]').click()
                    LOV弹窗内确定元素 = LOV弹窗元素定位.locator("button").filter(has_text="确")
                    LOV弹窗内确定 = LOV弹窗内确定元素.count()
                    if LOV弹窗内确定:
                        LOV弹窗内确定元素.click()
                    LOV弹窗元素定位.wait_for(state="detached")
                    continue
                字段是Select = 字段Select定位.count()
                if 字段是Select:
                    上层DIV定位.click()
                    值列表 = 值.split("|")
                    for Select值 in 值列表:
                        内部值列表 = Select值.split("/")
                        for 选项值 in 内部值列表:
                            self.locators.list_下拉项的定位(选项值).click()
                            # self.page.get_by_text(选项值).click()
                            if "|" in 值 or "/" in 值:
                                self.page.wait_for_timeout(100)
                    continue
                上层DIV定位.click()
                字段是日期 = 字段日期定位.count()
                if 字段是日期:
                    值列表 = 值.split("|")
                    上层DIV定位.locator("//input").nth(0).fill(值列表[0])
                    上层DIV定位.locator("//input").nth(2).fill(值列表[1])
                    self.page.keyboard.press("Enter")
                    continue
                输入框有波浪线 = 上层DIV定位.locator('input[placeholder="~"]').count()
                if 输入框有波浪线:
                    值列表 = 值.split("|")
                    上层DIV定位.locator("//input").nth(0).fill(值列表[0])
                    if len(值列表) == 2:
                        上层DIV定位.locator("//input").nth(2).fill(值列表[1])
                    self.page.keyboard.press("Enter")
                    continue
                字段输入框定位.fill(值)
            self.page.keyboard.press("Enter")
        try:
            self.page.wait_for_timeout(delay)
            # self.page.wait_for_load_state(state="networkidle", timeout=10_000)
            self.page.locator("*").filter(visible=True).first.click(trial=True, timeout=10_000)
            self.locators.loading_页面四瓣加载().wait_for(state="hidden", timeout=10_000)
        except:
            pass

    def search_条件搜索(self, 搜索条件: str, 搜索内容: str):
        start = time.time()
        while True:
            if time.time() - start > 30:
                pytest.fail("等待条件搜素页面出现超过30秒")
            是搜索框 = self.page.locator('button').filter(has_text=re.compile(fr"^{搜索条件}$")).count()
            if 是搜索框:
                break
        self.page.locator('//*[contains(@class,"proSrcQueryBaseLight")]').filter(
            has_text=re.compile(fr"^{搜索条件}$")).last.click()
        for _ in range(10):
            try:
                self.page.locator('//*[contains(@class,"proSrcQueryBaseLight")]').filter(
                    has_text=re.compile(fr"^{搜索条件}$")).filter(has=self.page.locator("input")).last.locator(
                    '//input').fill(
                    搜索内容, timeout=3_000)
                break
            except:
                pass
            try:
                self.page.locator(f'//li[@title="{搜索内容}"]').filter(visible=True).last.click(timeout=3_000)
                break
            except:
                pass
        try:
            with self.page.expect_response(lambda response: response.request.method == 'GET',
                                           timeout=60000):
                self.page.locator('//*[contains(@class,"-select-item-option")]').and_(
                    self.page.get_by_text(搜索内容, exact=True)).filter(visible=True).click(timeout=3000)
        except:
            pass
        self.page.locator("body").click()  # 模拟点击空白

    @allure.step("fill_快捷操作_填写表格")
    def fill_快捷操作_填写表格(self, table: Table, 行定位或行号: Union[Locator, int], 保存=True, **填写的字段_值):
        """
        填写表格中字段对应的值
        :param table: 表格对象,需要在各自pege中进行初始化
        :param 行定位或行号: 可以传入行序号(int)或者行定位(locator)
        :param 保存: 绿色√的点击
        :param 填写的字段_值: 关键字参数,要填写的项和对应的值
        :return: None
        """
        # list_temp = []
        for 字段, 值 in 填写的字段_值.items():
            with allure.step(f"{字段}={值}:"):
                # list_temp.append(值)
                字段名列表 = 字段.split("OR")
                start = time.time()
                已经拿到正确的数据 = False
                while True:
                    if time.time() - start > 30 or 已经拿到正确的数据:
                        break
                    for 分割后的字段 in 字段名列表:
                        if len(字段名列表) == 1:
                            表格cell_td元素 = table.get_cell(字段, 行定位或行号)
                            已经拿到正确的数据 = True
                            break
                        else:
                            try:
                                table.get_header_index(分割后的字段, timeout=1000)
                                表格cell_td元素 = table.get_cell(分割后的字段, 行定位或行号)
                                已经拿到正确的数据 = True
                                break
                            except:
                                continue
                self.fill_快捷操作_填写表单(default_value={表格cell_td元素: 值})
        if 保存:
            with allure.step("表格保存:"):
                操作列td元素 = table.get_cell("操作", 行定位或行号)
                操作列td元素.locator('//*[text()="保存"]|//*[contains(@*,"check-circle-fill")]').filter(
                    visible=True).nth(-1).click()
                self.wait_等待网络请求结束()

    @allure.step("fill_快捷操作_填写表单")
    def fill_快捷操作_填写表单(self, 完成后点击=None, default_value: dict = None, 操作块定位: Locator = None, **kwargs):
        """
        快速填写表单
        当值传参中包含"nth(0)"时,select和lov选择值集第一项,也支持"nth(-1)","nth(2)"等等
        当值传参中包含"nth(r)"时,下拉框会选择随机项(目前不支持搜索后的结果随机选择)
        当值传参中包含"[0]"时,页面有多个同样的字段,会选择第一位置的字段,也支持"[-1]","[2]"等等
        当值传参中包含"搜索按钮"时,程序会直接按照搜索弹窗的方式进行选择()
        当值传参中包含"loading"时,会对字段所在的值进行非空和非"-"的等待
        如果需要在某个字段填写后进行网络等待,可以在数据类此字段上方加入特殊数据,详情请参考"相对方数据类"
        LOV和SELECT为多选时不会清空已输入值，如需选则多个值，需多次调用此方法
        :param 完成后点击: None为不操作,否则传对应的按钮文字即可
        :param default_value: 默认的参数,可以通过update或者在关键字参数中进行更新,主要作用传输Locator的key,方便表格使用
        :param 操作块定位: 页面上有相同的操作块(比如签约方多个我方),给出精确的表单操作块的locator
        :param kwargs: key=value的方式传参
        :return:
        """
        try:
            # self.page.wait_for_load_state(state="networkidle", timeout=1_000)
            self.page.locator("*").filter(visible=True).last.click(trial=True)
        except:
            pass
        if default_value is not None:
            default_value.update(kwargs)
        else:
            default_value = kwargs
        原始的字段列表 = []
        for key in list(default_value.keys()):
            if isinstance(key, Locator):
                原始的字段列表.append(key)
            elif "网络等待" not in key:
                原始的字段列表.append(key)
        # 等第一个字段出现,防止提前进入逻辑:
        if isinstance(原始的字段列表[0], Locator):
            原始的字段列表[0].filter(visible=True).wait_for()
        elif isinstance(原始的字段列表[0], str):
            self.locators.包含操作元素的最上级div(原始的字段列表[0]).filter(visible=True).last.wait_for()
        # 这里赋值是为了初始化,后面判断用
        网络等待接口关键字 = ""
        第一个元素div = None
        for 字段, 值 in default_value.items():
            self.wait_等待网络请求结束()
            字段: Union[str, Locator]
            值: str
            with allure.step(f"{字段}={值}:"):
                nth = -1
                if isinstance(字段, str):
                    if "网络等待" in 字段:
                        网络等待接口关键字 = 值
                        网络等待的key = 字段
                        continue
                # 以下是为了除去页面上没有的字段(比如选择了A后才会出现B的字段):
                if 操作块定位:
                    包含操作元素的最上级div = 操作块定位.locator(self.locators.包含操作元素的最上级div(字段))
                else:
                    包含操作元素的最上级div = self.locators.包含操作元素的最上级div(字段)
                if 包含操作元素的最上级div.count() == 1:
                    if 第一个元素div is None:
                        第一个元素div = 包含操作元素的最上级div
                else:
                    if 第一个元素div is None:
                        for key in 原始的字段列表:
                            if self.locators.包含操作元素的最上级div(key).count() == 1:
                                包含操作元素的最上级div = self.locators.包含操作元素的最上级div(key).locator(
                                    self.locators.above_元素上方所有的元素()).locator(
                                    self.locators.包含操作元素的最上级div(字段)).last
                                第一个元素div = 包含操作元素的最上级div
                                break
                        if 第一个元素div is None:
                            包含操作元素的最上级div = 包含操作元素的最上级div.last
                            第一个元素div = 包含操作元素的最上级div
                    else:
                        包含操作元素的最上级div = 第一个元素div.locator(
                            self.locators.below_元素下方所有的元素()).locator(
                            self.locators.包含操作元素的最上级div(字段)).first
                # else:
                #     for i in range(30):  # 此处循环是防止表单的第一项填写项和上一页的某一个填写项重合,或者当前表单的加载方式为分段加载造成的filter组合全无效
                #         能包含数据类所有字段的最小元素 = self.page.locator("*")
                #         for key in 原始的字段列表:
                #             temp = 能包含数据类所有字段的最小元素
                #             if isinstance(key, Locator):
                #                 能包含数据类所有字段的最小元素 = 能包含数据类所有字段的最小元素.filter(has=key)
                #             else:
                #                 能包含数据类所有字段的最小元素 = 能包含数据类所有字段的最小元素.filter(has=self.locators.包含操作元素的最上级div(key))
                #             if 能包含数据类所有字段的最小元素.count():
                #                 continue
                #             else:
                #                 能包含数据类所有字段的最小元素 = temp
                #         if str(能包含数据类所有字段的最小元素) == str(self.page.locator("*")):
                #             if i == 29:
                #                 pytest.fail("30秒内未等待到页面加载完成")
                #             self.page.wait_for_timeout(1000)
                #         else:
                #             break
                #     包含操作元素的最上级div = 能包含数据类所有字段的最小元素.last.locator(self.locators.包含操作元素的最上级div(字段))
                # else:
                #     pass

                if re.search(r"\[(-)?\d{1,3}]", 值):
                    nth = int(re.search(r"(\[)(.*)(])", 值).group(2))
                    值 = 值.replace(f"[{nth}]", "")
                结果 = self.__框内值判断(字段, 值, nth, 包含操作元素的最上级div)
                if 结果 == "finish":
                    continue
                if self.组件类型 == "OCANT":
                    if 网络等待接口关键字 and 字段 in 网络等待的key:
                        with self.page.expect_response(re.compile(网络等待接口关键字)):
                            self.__OCANT判断和填写(值, nth, 包含操作元素的最上级div)
                            网络等待接口关键字 = ""
                    else:
                        self.__OCANT判断和填写(值, nth, 包含操作元素的最上级div)
                    continue
                if self.组件类型 == "C7N":
                    if 网络等待接口关键字 and 字段 in 网络等待的key:
                        with self.page.expect_response(re.compile(网络等待接口关键字)):
                            self.__C7N判断和填写(值, nth, 包含操作元素的最上级div)
                            网络等待接口关键字 = ""
                    else:
                        self.__C7N判断和填写(值, nth, 包含操作元素的最上级div)
                    continue
        if 完成后点击:
            self.locators.button_按钮(完成后点击).click()

    @staticmethod
    def __框内值判断(字段, 值, nth, 包含操作元素的最上级div):
        with allure.step("OCANT中检查input框内值是否和预期一致,一致会直接循环下一组数据:"):
            if isinstance(字段, Locator):
                expect(字段.last).to_be_visible()
                INPUT框内值 = 字段.last.text_content()
            else:
                expect(包含操作元素的最上级div.nth(nth).filter(visible=True)).to_be_visible()
                INPUT框内值 = 包含操作元素的最上级div.nth(nth).text_content()
                if not INPUT框内值:
                    if 包含操作元素的最上级div.nth(nth).locator("input,textarea").filter(visible=True).count():
                        INPUT框内值 = 包含操作元素的最上级div.nth(nth).locator("input,textarea").locator(
                            "visible=true").last.input_value()
            if INPUT框内值 == 值:
                return "finish"
            elif 值 == "loading":
                if 包含操作元素的最上级div.nth(nth).locator.locator("input").count():
                    expect(包含操作元素的最上级div.nth(nth).locator('input')).to_have_value(
                        re.compile("^(?!-|.*?-$)[A-Za-z0-9-\u4e00-\u9fa5]+$"))
                else:
                    expect(包含操作元素的最上级div.nth(nth)).to_have_text(
                        re.compile("^(?!-|.*?-$)[A-Za-z0-9-\u4e00-\u9fa5]+$"))
                return "finish"
            else:
                return

    @staticmethod
    def __包含操作元素的最上级div自动取上级(包含操作元素的最上级div: Locator, nth=-1):
        if 包含操作元素的最上级div.nth(nth).evaluate("node => node.tagName") == "TD":
            return 包含操作元素的最上级div
        else:
            return 包含操作元素的最上级div.locator("xpath=/..")

    def __OCANT判断和填写(self, 值, nth, 包含操作元素的最上级div):
        with allure.step("OCANT中判断元素对象的操作方法并对其进行操作:"):
            start = time.time()
            while True:
                is_input = self.locators.input_表单input定位(
                    self.__包含操作元素的最上级div自动取上级(包含操作元素的最上级div), nth).count()
                if is_input:
                    操作对象 = "input"
                    break
                is_switch = self.locators.switch_表单switchbutton定位(
                    self.__包含操作元素的最上级div自动取上级(包含操作元素的最上级div), nth).count()
                if is_switch:
                    操作对象 = "switch"
                    break
                is_click_span = self.locators.click_表单可点击span定位(
                    self.__包含操作元素的最上级div自动取上级(包含操作元素的最上级div), nth).count()
                if is_click_span:
                    操作对象 = "span"
                    break
                if time.time() - start > 30:
                    pytest.fail("超过30秒未找到合适的表单或者表格填入类型,请进一步封装此处代码")
            if 操作对象 == "input":
                INPUT元素定位 = self.locators.input_表单input定位(
                    self.__包含操作元素的最上级div自动取上级(包含操作元素的最上级div), nth)
                INPUT元素最上级DIV = self.__包含操作元素的最上级div自动取上级(包含操作元素的最上级div).nth(nth)
                包含搜索按钮 = INPUT元素最上级DIV.locator("xpath=/..").locator(
                    '//div[contains(@class,"select-suffix")]').or_(
                    INPUT元素最上级DIV.locator('//*[@data-icon="plus"]')).count()
                INPUT元素Type = INPUT元素定位.filter(visible=True).get_attribute("type")
                相对方主体名称 = INPUT元素最上级DIV.locator('//*[@id="mainPartyName"]').count()
                if (
                        INPUT元素Type == "text" or INPUT元素Type is None or INPUT元素Type == "textarea" or 相对方主体名称 or INPUT元素最上级DIV.locator(
                    '//input[contains(@class,"input-number-input")]').count()) and not 包含搜索按钮:
                    with allure.step("可直接填写的操作:"):
                        self.__OCANT_input_直接填写(值, nth, 包含操作元素的最上级div)
                        return

                if INPUT元素Type == "radio":
                    with allure.step("可单选(radio)的操作:"):
                        self.__OCANT_input_radio(值, nth, 包含操作元素的最上级div)
                        return

                if INPUT元素Type == "checkbox":
                    with allure.step("可复选(checkbox)的操作:"):
                        self.__OCANT_input_checkbox(值, nth, 包含操作元素的最上级div)
                        return

                if 包含搜索按钮 or "搜索按钮" in 值:
                    with allure.step("点击+号进行弹窗搜索的操作:"):
                        if "搜索按钮" in 值:
                            值 = 值.replace("搜索按钮", "")
                        self.__OCANT_input_搜索(值, nth, 包含操作元素的最上级div)
                        return

                包含下拉框属性 = INPUT元素最上级DIV.locator('//*[contains(@class,"select-selector")]').count()
                确认下拉框属性 = INPUT元素最上级DIV.locator('//*[contains(@class,"select-show-search")]').count()
                if 包含下拉框属性 and 确认下拉框属性:
                    with allure.step("下拉框进行选择的操作:"):
                        self.__OCANT_input_下拉框(值, nth, 包含操作元素的最上级div)
                        return

                if 包含下拉框属性 and not 确认下拉框属性:
                    with allure.step("点击输入框进行弹窗搜索的操作:"):
                        self.__OCANT_input_搜索(值, nth, 包含操作元素的最上级div, 按钮搜索=False)
                        return

            elif 操作对象 == "switch":
                with allure.step("对switch_button的操作:"):
                    self.__OCANT_switch_button(值, nth, 包含操作元素的最上级div)
                    return
            elif 操作对象 == "span":
                with allure.step("对可点击的span的操作:"):
                    self.__OCANT_click_span(值, nth, 包含操作元素的最上级div)
                    return

    def __OCANT_input_直接填写(self, 值, nth, 包含操作元素的最上级div):
        INPUT元素定位 = self.locators.input_表单input定位(
            self.__包含操作元素的最上级div自动取上级(包含操作元素的最上级div), nth)
        INPUT元素最上级DIV = self.__包含操作元素的最上级div自动取上级(包含操作元素的最上级div).nth(nth)
        INPUT元素上级DIV是时间日期控件 = INPUT元素最上级DIV.filter(visible=True).locator(
            '//div[contains(@class,"picker-input")]').count()
        if INPUT元素上级DIV是时间日期控件 == 1:
            INPUT元素定位.click()
            try:
                int(值.split(",")[0])
                值 = 返回当前时间xxxx_xx_xx加N天(int(值.split(",")[0]))
            except:
                值 = 值.split(",")[0]
            INPUT元素定位.fill(值)
            self.page.keyboard.press("Enter")
        elif INPUT元素上级DIV是时间日期控件 == 2:
            try:
                int(值.split(",")[0])
                值0 = 返回当前时间xxxx_xx_xx加N天(int(值.split(",")[0]))
            except:
                值0 = 值.split(",")[0]
            INPUT元素最上级DIV.locator("//input").nth(0).click()
            INPUT元素最上级DIV.locator("//input").nth(0).fill(值0)
            try:
                int(值.split(",")[1])
                值1 = 返回当前时间xxxx_xx_xx加N天(int(值.split(",")[1]))
            except:
                值1 = 值.split(",")[1]
            INPUT元素最上级DIV.locator("//input").nth(1).click()
            INPUT元素最上级DIV.locator("//input").nth(1).fill(值1)
            self.page.keyboard.press("Enter")
        else:
            INPUT元素定位.click()
            INPUT元素定位.fill(值)

    def __OCANT_input_搜索(self, 值, nth, 包含操作元素的最上级div, 按钮搜索=True):
        INPUT元素最上级DIV = 包含操作元素的最上级div.nth(nth)
        当前modal元素数量 = self.locators.modal_弹窗().count()
        点击LOV搜索按钮后modal数量 = 当前modal元素数量
        LOV弹窗元素定位 = self.locators.modal_弹窗().nth(点击LOV搜索按钮后modal数量)
        modal元素位置信息列表 = []
        if 当前modal元素数量:
            modal元素信息列表 = self.locators.modal_弹窗().all()
            for element in modal元素信息列表:
                modal元素位置信息列表.append(element.bounding_box())
        if 按钮搜索:
            INPUT元素最上级DIV.locator('//div[contains(@class,"select-suffix")]').or_(
                INPUT元素最上级DIV.locator('//*[@data-icon="plus"]')).click()
        else:
            INPUT元素最上级DIV.click()
        LOV弹窗元素定位.wait_for(state="visible")
        # 获取LOV窗口数量，通过窗口大小判断是否为新弹出LOV，如果新弹出的LOV大小与之前有重合，则使用最后一个LOV元素定位
        点击操作后modal元素 = self.locators.modal_弹窗().all()
        for element in 点击操作后modal元素:
            元素位置信息 = element.bounding_box()
            if 元素位置信息 not in modal元素位置信息列表:
                LOV弹窗元素定位 = element
        self.page.wait_for_timeout(1_000)
        try:
            self.page.locator("*").filter(visible=True).first.click(trial=True, timeout=10_000)
            self.page.wait_for_load_state(state="networkidle", timeout=10_000)
        except:
            pass
        LOV内checkbox = LOV弹窗元素定位.locator("input[type='checkbox']").count()
        if "nth(" in 值:
            self.wait_等待网络请求结束()
            for _ in range(5):
                try:
                    if "nth(r)" in 值:
                        if LOV内checkbox:
                            random.choice(self.locators.modal_弹窗().locator('input[type="checkbox"]').all()).click(
                                timeout=5_000)
                        else:
                            random.choice(self.locators.modal_弹窗().locator('input[type="radio"]').all()).click(
                                timeout=5_000)
                    else:
                        序列 = int(值.replace("nth(", "").replace(")", ""))
                        if LOV内checkbox:
                            self.locators.modal_弹窗().locator('input[type="checkbox"]').nth(序列).click(timeout=5_000)
                        else:
                            self.locators.modal_弹窗().locator('input[type="radio"]').nth(序列).click(timeout=5_000)
                    break
                except:
                    if _ == 4:
                        pytest.fail("随机选择失败")
        else:
            try:
                self.search_填写搜索框(值, LOV内搜索=True)
            except:
                pass
            if LOV内checkbox:
                self.min_找出locator中最短的元素定位(
                    self.locators.modal_弹窗().locator("td").filter(has_text=值)).locator("//ancestor::tr").locator(
                    'input[type="checkbox"]').last.click()
            else:
                self.min_找出locator中最短的元素定位(
                    self.locators.modal_弹窗().locator("td").filter(has_text=值)).locator("//ancestor::tr").locator(
                    'input[type="radio"]').last.click()
        有确定或确认按钮 = LOV弹窗元素定位.filter(has=self.locators.button_按钮("确")).count()
        if 有确定或确认按钮:
            LOV弹窗元素定位.locator(self.locators.button_按钮("确")).click()
        # 等待LOV弹窗关闭
        for counter in range(0, 300):
            modal元素数量 = self.locators.modal_弹窗().filter(visible=True).count()
            if modal元素数量 == 当前modal元素数量:
                break
            self.page.wait_for_timeout(100)

    def __OCANT_input_下拉框(self, 值, nth, 包含操作元素的最上级div):
        INPUT元素定位 = self.locators.input_表单input定位(包含操作元素的最上级div, nth)
        # 下拉值集元素定位 = self.page.locator(
        #     "//div[contains(@class,'select-dropdown') and not (contains(@class,'dropdown-hidden'))]")
        expect(INPUT元素定位).to_be_enabled()
        with allure.step("已经判断为下拉框选择:"):
            for i in range(7):
                try:
                    self.page.set_default_timeout(5_000)
                    INPUT元素定位 = self.locators.input_表单input定位(包含操作元素的最上级div, nth)
                    下拉值集元素定位 = self.page.locator(
                        "//div[contains(@class,'select-dropdown') and not (contains(@class,'dropdown-hidden'))]")
                    expect(INPUT元素定位).to_be_enabled()
                    with allure.step("已经判断为下拉框选择:"):
                        if "nth(" in 值:
                            self.wait_等待网络请求结束()
                            if "nth(r)" in 值:
                                包含操作元素的最上级div.click()
                                for _ in range(100):
                                    if 下拉值集元素定位.count() == 1:
                                        break
                                    else:
                                        self.page.wait_for_timeout(100)
                                下拉值集元素定位.locator("//*[@title]").filter(visible=True).last.wait_for()
                                random.choice(
                                    下拉值集元素定位.locator("//*[@title]").filter(visible=True).all()).click()
                            else:
                                序列 = int(值.replace("nth(", "").replace(")", ""))
                                包含操作元素的最上级div.click()
                                下拉值集元素定位.locator("//*[@title]").nth(序列).click()
                        elif "/" in 值:
                            层级值列表 = 值.split("/")
                            选项定位 = self.page.locator(f"//*[@title='{层级值列表[0]}']")  # 抽出第一个层级作为最终元素定位生成的起始
                            for 值 in 层级值列表[1:]:
                                选项定位 = 选项定位.locator(f"xpath=/following::*[@title='{值}']")
                            包含操作元素的最上级div.click()
                            input元素states = INPUT元素定位.filter(visible=True).last.is_editable(timeout=0)
                            if input元素states:
                                搜索填写值 = 层级值列表[-1]
                                INPUT元素定位.fill(搜索填写值)
                            else:
                                包含操作元素的最上级div.click()
                            选项定位.click()
                        elif "&&" in 值:
                            多选值列表 = 值.split("&&")
                            包含操作元素的最上级div.click()
                            for 多选值 in 多选值列表:
                                INPUT元素定位 = self.locators.input_表单input定位(包含操作元素的最上级div, nth)
                                input元素states = INPUT元素定位.filter(visible=True).last.is_editable(timeout=0)
                                if input元素states:
                                    INPUT元素定位.fill(多选值)
                                else:
                                    包含操作元素的最上级div.click()
                                选项定位 = self.page.get_by_title(多选值)
                                # 选项定位 = self.page.locator(f"/following::*[@title='{多选值}']")
                                选项定位.click()
                        else:
                            搜索填写值 = 值
                            包含操作元素的最上级div.click()
                            input元素states = INPUT元素定位.filter(visible=True).last.is_editable(timeout=0)
                            if input元素states:
                                INPUT元素定位.fill(搜索填写值)
                            else:
                                包含操作元素的最上级div.click()
                            选项定位 = self.min_找出locator中最短的元素定位(下拉值集元素定位.locator(
                                f'//*[contains(@title,"{值}")][not(contains(@class,"hidden"))]'))
                            if 选项定位.count() > 1:
                                x = 10000
                                for 定位 in 选项定位.all():
                                    定位_位置 = 定位.bounding_box()["x"]
                                    if 定位_位置 < x:
                                        x = 定位_位置
                                        选项定位 = 定位
                            选项定位.click()
                        self.page.keyboard.press("Tab")
                        break
                except:
                    if i == 6:
                        pytest.fail("x下拉框重试3次失败")
                finally:
                    self.page.set_default_timeout(30_000)

    def __OCANT_switch_button(self, 值, nth, 包含操作元素的最上级div):
        switch_button元素定位 = self.locators.switch_表单switchbutton定位(
            self.__包含操作元素的最上级div自动取上级(包含操作元素的最上级div), nth)
        if 值 == "开" or 值 == "是":
            switch_button元素定位.check()
        elif 值 == "关" or 值 == "否":
            switch_button元素定位.uncheck()

    @staticmethod
    def __OCANT_click_span(值, nth, 包含操作元素的最上级div):
        if "antBase-tag-checkable-checked" not in 包含操作元素的最上级div.nth(nth).get_by_text(值,
                                                                                               exact=True).get_attribute(
                "class"):  # 合同创建选择甲方乙方,如果已经选中则不操作
            包含操作元素的最上级div.nth(nth).get_by_text(值, exact=True).click()

    def __OCANT_input_radio(self, 值, nth, 包含操作元素的最上级div):
        包含操作元素的最上级div.nth(nth).locator('label,span,button').filter(
            has=self.page.get_by_text(值, exact=True)).locator("input").check()

    def __OCANT_input_checkbox(self, 值, nth, 包含操作元素的最上级div):
        包含操作元素的最上级div.nth(nth).locator('label,span,button').filter(
            has=self.page.get_by_text(值, exact=True)).locator("input").check()

    def __C7N判断和填写(self, 值, nth, 包含操作元素的最上级div):
        with allure.step("OCANT中判断元素对象的操作方法并对其进行操作:"):
            start = time.time()
            while True:
                if time.time() - start > 30:
                    break
                is_input = self.locators.input_表单input定位(
                    self.__包含操作元素的最上级div自动取上级(包含操作元素的最上级div), nth).count()
                if is_input:
                    操作对象 = "input"
                    break
                is_switch = self.locators.switch_表单switchbutton定位(
                    self.__包含操作元素的最上级div自动取上级(包含操作元素的最上级div), nth).count()
                if is_switch:
                    操作对象 = "switch"
                    break
                is_click_span = self.locators.click_表单可点击span定位(
                    self.__包含操作元素的最上级div自动取上级(包含操作元素的最上级div), nth).count()
                if is_click_span:
                    操作对象 = "span"
                    break
            if 操作对象 == "input":
                INPUT元素定位 = self.locators.input_表单input定位(包含操作元素的最上级div, nth)
                INPUT元素最上级DIV = 包含操作元素的最上级div.nth(nth)
                包含搜索按钮 = INPUT元素最上级DIV.locator(".anticon-search").count()
                if 包含搜索按钮 or "搜索按钮" in 值:
                    with allure.step("点击放大镜进行弹窗搜索的操作:"):
                        if "搜索按钮" in 值:
                            值 = 值.replace("搜索按钮", "")
                        self.__C7N_input_搜索(值, nth, 包含操作元素的最上级div)
                        return

                包含下拉框属性 = INPUT元素最上级DIV.locator('.c7n-pro-tree-select').or_(
                    INPUT元素最上级DIV.locator('.c7n-pro-select')).or_(INPUT元素最上级DIV.locator('.c7n-select')).or_(
                    INPUT元素最上级DIV.locator('.ant-select-search__field')).count()
                if 包含下拉框属性:
                    with allure.step("下拉框进行选择的操作:"):
                        self.__C7N_input_下拉框(值, nth, 包含操作元素的最上级div)
                        return

                INPUT元素Type = INPUT元素定位.filter(visible=True).get_attribute("type")
                if (INPUT元素Type == "text" or INPUT元素Type is None or INPUT元素最上级DIV.locator(
                        "textarea").count() or INPUT元素最上级DIV.locator(
                    'input.c7n-pro-input').count() or INPUT元素最上级DIV.locator(
                    '.c7n-pro-calendar-picker').count()) and not INPUT元素定位.and_(
                    self.page.locator(".ant-select-search__field")).count():
                    with allure.step("可直接填写的操作:"):
                        self.__C7N_input_直接填写(值, nth, 包含操作元素的最上级div)
                        return

                if INPUT元素Type == "radio":
                    with allure.step("可单选(radio)的操作:"):
                        self.__C7N_input_radio(值, nth, 包含操作元素的最上级div)
                        return

            elif 操作对象 == "switch":
                with allure.step("对switch_button的操作:"):
                    self.__C7N_switch_button(值, nth, 包含操作元素的最上级div)
                    return
            elif 操作对象 == "span":
                with allure.step("对可点击的span的操作:"):
                    if 包含操作元素的最上级div.locator('.c7n-select').count():
                        self.__C7N_input_下拉框(值, nth, 包含操作元素的最上级div)
                    else:
                        self.__C7N_click_span(值, nth, 包含操作元素的最上级div)
                    return

    def __C7N_input_直接填写(self, 值, nth, 包含操作元素的最上级div):
        INPUT元素定位 = self.locators.input_表单input定位(包含操作元素的最上级div, nth)
        INPUT元素最上级DIV = 包含操作元素的最上级div.nth(nth)
        INPUT元素上级DIV是时间日期控件 = INPUT元素最上级DIV.filter(visible=True).locator(
            '.c7n-pro-calendar-picker').count()
        if INPUT元素上级DIV是时间日期控件 == 1:
            INPUT元素定位.click()
            try:
                int(值.split(",")[0])
                值 = 返回当前时间xxxx_xx_xx加N天(int(值.split(",")[0]))
            except:
                值 = 值.split(",")[0]
            INPUT元素定位.fill(值)
            self.page.keyboard.press("Enter")
        elif INPUT元素上级DIV是时间日期控件 == 2:
            try:
                int(值.split(",")[0])
                值0 = 返回当前时间xxxx_xx_xx加N天(int(值.split(",")[0]))
            except:
                值0 = 值.split(",")[0]
            INPUT元素最上级DIV.locator("//input").nth(0).click()
            INPUT元素最上级DIV.locator("//input").nth(0).fill(值0)
            try:
                int(值.split(",")[1])
                值1 = 返回当前时间xxxx_xx_xx加N天(int(值.split(",")[1]))
            except:
                值1 = 值.split(",")[1]
            INPUT元素最上级DIV.locator("//input").nth(1).click()
            INPUT元素最上级DIV.locator("//input").nth(1).fill(值1)
            self.page.keyboard.press("Enter")
        else:
            INPUT元素定位.fill(值)

    def __C7N_input_搜索(self, 值, nth, 包含操作元素的最上级div, 按钮搜索=True):
        INPUT元素最上级DIV = 包含操作元素的最上级div.nth(nth)
        当前modal元素数量 = self.locators.modal_弹窗().count()
        点击LOV搜索按钮后modal数量 = 当前modal元素数量 + 1
        LOV弹窗元素定位 = f'(//div[contains(@class,"modal-content")])[{点击LOV搜索按钮后modal数量}]'
        modal元素位置信息列表 = []
        if 当前modal元素数量:
            modal元素信息列表 = self.locators.modal_弹窗().all()
            for element in modal元素信息列表:
                modal元素位置信息列表.append(element.bounding_box())
        if 按钮搜索:
            INPUT元素最上级DIV.locator(".anticon-search").click()
        else:
            INPUT元素最上级DIV.click()
        self.page.locator(LOV弹窗元素定位).wait_for(state="visible")
        # 获取LOV窗口数量，通过窗口大小判断是否为新弹出LOV，如果新弹出的LOV大小与之前有重合，则使用最后一个LOV元素定位
        点击操作后modal元素 = self.locators.modal_弹窗().all()
        LOV内checkbox = None
        for element in 点击操作后modal元素:
            元素位置信息 = element.bounding_box()
            if 元素位置信息 not in modal元素位置信息列表:
                LOV弹窗元素定位 = element
        if not isinstance(LOV弹窗元素定位, str):
            LOV内checkbox = LOV弹窗元素定位.locator("input[type='checkbox']").count()

        if "nth(" in 值:
            self.wait_等待网络请求结束()
            序列 = int(值.replace("nth(", "").replace(")", ""))
            if LOV内checkbox:
                self.page.locator('//*[contains(@class, "-modal-content")] >> input[type="checkbox"]').nth(序列).click()
            else:
                self.page.locator('//*[contains(@class, "-modal-content")] >> input[type="radio"]').nth(序列).click()
        else:
            try:
                self.search_填写搜索框(值, LOV内搜索=True)
            except:
                pass
            if LOV内checkbox:
                self.page.locator(f'[class*="modal-content"] tr:has-text("{值}") >> input[type="checkbox"]').nth(
                    1).click()
            else:
                self.page.locator(f'[class*="modal-content"] tr:has-text("{值}") >> input[type="radio"]').nth(0).click()
        if isinstance(LOV弹窗元素定位, str):
            LOV弹窗元素定位 = self.page.locator(LOV弹窗元素定位)
        有确定或确认按钮 = LOV弹窗元素定位.filter(has=self.locators.button_按钮("确")).count()
        if 有确定或确认按钮:
            LOV弹窗元素定位.locator(self.locators.button_按钮("确")).click()
        # 等待LOV弹窗关闭
        for counter in range(0, 300):
            modal元素数量 = self.page.locator('//div[contains(@class,"modal-content")] >> visible=true').count()
            if modal元素数量 == 当前modal元素数量:
                break
            self.page.wait_for_timeout(100)

    def __C7N_input_下拉框(self, 值, nth, 包含操作元素的最上级div: Locator):
        INPUT元素定位 = self.locators.input_表单input定位(包含操作元素的最上级div, nth)
        下拉值集元素定位 = self.page.locator('.c7n-pro-popup').filter(visible=True).or_(
            self.page.locator(".c7n-select-tree-list")).or_(self.page.locator(".ant-select-dropdown")).locator(
            "visible=true").last
        with allure.step("已经判断为下拉框选择:"):
            start = time.time()
            while True:
                if time.time() - start > 30:
                    pytest.fail("30秒未能点开下拉框")
                try:
                    下拉值集元素定位.wait_for(state="hidden", timeout=1000)
                    包含操作元素的最上级div.click()
                    下拉值集元素定位.wait_for(timeout=2000)
                    break
                except:
                    pass

            if "nth(" in 值:
                self.wait_等待网络请求结束()
                if "nth(r)" in 值:
                    #  通过重试来兼容上一个下拉列表为完全消失,随机列表获取不正确的问题
                    start = time.time()
                    while True:
                        if time.time() - start > 30:
                            pytest.fail("30秒未能选择到下拉框随机内容")
                        try:
                            random.choice(下拉值集元素定位.locator("//li").filter(visible=True).or_(
                                下拉值集元素定位.locator("*[title]").filter(visible=True)).all()).click(timeout=1000)
                            break
                        except:
                            pass
                else:
                    序列 = int(值.replace("nth(", "").replace(")", ""))
                    下拉值集元素定位.locator("//li").filter(visible=True).or_(
                        下拉值集元素定位.locator("*[title]").filter(visible=True)).nth(序列).click()
            else:
                选项定位 = 下拉值集元素定位.locator(
                    f'//li[text()="{值}"][not(contains(@class,"hidden"))]|//*[@title="{值}"][not(contains(@class,"hidden"))]')
                填写值 = 值
                input元素states = INPUT元素定位.filter(visible=True).last.is_editable(timeout=0)
                if "/" in 值:
                    层级值列表 = 值.split("/")
                    选项定位 = self.page.locator(f"//*[@title='{层级值列表[0]}']")  # 抽出第一个层级作为最终元素定位生成的起始
                    for 值 in 层级值列表[1:]:
                        选项定位 = 选项定位.locator(f"/following::*[@title='{值}']")
                    包含操作元素的最上级div.click()
                    input元素states = INPUT元素定位.filter(visible=True).last.is_editable(timeout=0)
                    if input元素states:
                        搜索填写值 = 层级值列表[-1]
                        INPUT元素定位.fill(搜索填写值)
                    else:
                        包含操作元素的最上级div.click()
                    选项定位.click()
                elif "&&" in 值:
                    多选值列表 = 值.split("&&")
                    包含操作元素的最上级div.click()
                    for 多选值 in 多选值列表:
                        INPUT元素定位 = self.locators.input_表单input定位(包含操作元素的最上级div, nth)
                        input元素states = INPUT元素定位.filter(visible=True).last.is_editable(timeout=0)
                        if input元素states:
                            INPUT元素定位.fill(多选值)
                        else:
                            包含操作元素的最上级div.click()
                        选项定位 = self.page.get_by_title(多选值)
                        # 选项定位 = self.page.locator(f"/following::*[@title='{多选值}']")
                        选项定位.click()
                elif input元素states:
                    INPUT元素定位.fill(填写值)
                else:
                    选项定位.click()
            包含操作元素的最上级div.locator(self.locators.above_元素上方紧邻的元素()).click()

    def __C7N_switch_button(self, 值, nth, 包含操作元素的最上级div):
        switch_button元素定位 = self.locators.switch_表单switchbutton定位(包含操作元素的最上级div, nth)
        if 值 == "开" or 值 == "是":
            switch_button元素定位.check()
        elif 值 == "关" or 值 == "否":
            switch_button元素定位.uncheck()
        else:
            pass

    @staticmethod
    def __C7N_click_span(值, nth, 包含操作元素的最上级div):
        包含操作元素的最上级div.nth(nth).get_by_text(值).click()

    @staticmethod
    def __C7N_input_radio(值, nth, 包含操作元素的最上级div):
        包含操作元素的最上级div.nth(nth).locator('//label').filter(has_text=值).locator("input").check()

    def switch_切换页内标签(self, 标签名称: str):
        self.page.locator('//div[@role="tab"]').filter(has_text=标签名称).click()
        self.page.locator('//div[@role="tab"]').filter(has_text=标签名称).focus()

    def wait_等待元素对象稳定(self, locator: Locator, timeout=30_000):
        old_box = locator.bounding_box()
        count = 20
        for i in range(int(timeout / 50)):
            self.page.wait_for_timeout(50)
            new_box = locator.bounding_box()
            if old_box == new_box:
                count = count - 1
                if not count:
                    break
            else:
                old_box = new_box
                count = 20
                continue

    def get_获取文字的链接地址(self, 文字: str):
        return self.page.get_by_role("link").filter(has_text=文字).get_attribute("href")

    def check_勾选当前所有checkbox(self, start=0, stop=None, step=1):
        self.page.get_by_role("checkbox").last.filter(visible=True).wait_for()
        self.wait_等待网络请求结束()
        all_viewed_checkbox = self.page.get_by_role("checkbox").filter(visible=True).all()
        for checkbox in all_viewed_checkbox[start:stop:step]:
            checkbox.check()
        return len(all_viewed_checkbox)

    def check_去勾选当前所有checkbox(self):
        self.page.get_by_role("checkbox").last.filter(visible=True).wait_for()
        self.page.locator("#apiCounter").wait_for(state="detached")
        all_viewed_checkbox = self.page.get_by_role("checkbox").filter(visible=True).all()
        for checkbox in all_viewed_checkbox:
            checkbox.uncheck()
        return len(all_viewed_checkbox)

    def get_获取字段的可用值(self, 字段, 字段页面排序=-1):
        start = time.time()
        while True:
            if time.time() - start > 30:
                break
            try:
                text_value = self.locators.包含操作元素的最上级div(字段).nth(字段页面排序).text_content(timeout=1000)
                if text_value != "-" and text_value:
                    return text_value
            except:
                pass
            try:
                input_value = self.locators.包含操作元素的最上级div(字段).nth(字段页面排序).locator(
                    "input").input_value(timeout=1000)
                if input_value != "-" and input_value:
                    return input_value
            except:
                pass

    def tab_页签操作(self, 操作页签名称: str, 动作: str):
        self.page.locator(f'//div[@role="tab"]//span[contains(text(),"{操作页签名称}")]').locator(
            "visible=true").last.click(button="right")
        self.page.locator(f'//span[text()="{动作}"]').click()

    def fill_填写输入框(self, 字段名称: str, 要填写的文字: str, 索引: int = -1):
        self.page.locator(f"//*[contains(text(),'{字段名称}')]/following::*[position()=1]//input").nth(索引).fill(
            要填写的文字)

    def select_选择输入框(self, 字段名称: str, 要选择的项: str, 索引: int = -1):
        self.page.locator(f"//*[text()='{字段名称}']/following::*[position()=1]").nth(索引).click()
        self.page.get_by_text(要选择的项, exact=True).filter(visible=True).last.click()

    def assert_检查页面是否包含一组文字(self, *args, timeout: float = None):
        for arg in args:
            expect(self.page.get_by_text(str(arg)).filter(visible=True).last).to_be_visible(timeout=timeout)

    def assert_检查表单页面是否包含键值对(self, **kwargs):
        原始的字段列表 = []
        for key, value in kwargs.items():
            if isinstance(key, Locator):
                原始的字段列表.append(key)
            elif "__" not in key:
                原始的字段列表.append(key)
            elif "nth(" in value:
                原始的字段列表.append(key)
        # 等第一个字段出现,防止提前进入逻辑:
        if isinstance(原始的字段列表[0], Locator):
            原始的字段列表[0].wait_for()
        elif isinstance(原始的字段列表[0], str):
            self.page.get_by_text(原始的字段列表[0]).last.wait_for()

        # for index, (字段, 值) in enumerate(kwargs.items()):
        #     字段: Union[str, Locator]
        #     值: str
        #     with allure.step(f"{字段}={值}:"):
        #         nth = -1
        #         # 以下是为了除去页面上没有的字段(比如选择了A后才会出现B的字段):
        #         包含操作元素的最上级div = self.locators.包含操作元素的最上级div(字段)
        #         if 包含操作元素的最上级div.count() == 1:
        #             if index == 0:
        #                 第一个元素div = 包含操作元素的最上级div
        #         else:
        #             if index == 0:
        #                 for key in 原始的字段列表:
        #                     if self.locators.包含操作元素的最上级div(key).count() == 1:
        #                         包含操作元素的最上级div = self.locators.包含操作元素的最上级div(key).locator(self.locators.above_元素上方所有的元素()).locator(self.locators.包含操作元素的最上级div(字段)).last
        #                         第一个元素div = 包含操作元素的最上级div
        #                         break
        #             else:
        #                 包含操作元素的最上级div = 第一个元素div.locator(self.locators.below_元素下方所有的元素()).locator(self.locators.包含操作元素的最上级div(字段)).first

        第一个元素div = None
        for 字段, 值 in kwargs.items():
            # 以下是为了除去页面上没有的字段(比如选择了A后才会出现B的字段):
            包含操作元素的最上级div = self.locators.包含操作元素的最上级div(字段)
            if 包含操作元素的最上级div.count() == 1:
                if 第一个元素div is None:
                    第一个元素div = 包含操作元素的最上级div
            else:
                if 第一个元素div is None:
                    for key in 原始的字段列表:
                        if self.locators.包含操作元素的最上级div(key).count() == 1:
                            包含操作元素的最上级div = self.locators.包含操作元素的最上级div(key).locator(
                                self.locators.above_元素上方所有的元素()).locator(
                                self.locators.包含操作元素的最上级div(字段)).last
                            第一个元素div = 包含操作元素的最上级div
                            break
                    if 第一个元素div is None:
                        包含操作元素的最上级div = 包含操作元素的最上级div.last
                        第一个元素div = 包含操作元素的最上级div
                else:
                    包含操作元素的最上级div = 第一个元素div.locator(self.locators.below_元素下方所有的元素()).locator(
                        self.locators.包含操作元素的最上级div(字段)).first

            # 这里是删除[12]这种标注页面序列:
            if re.search(r"\[(-)?\d{1,3}]", 值):
                nth = int(re.search(r"(\[)(.*)(])", 值).group(2))
                值 = 值.replace(f"[{nth}]", "")
            else:
                nth = -1
            for value in 值.split(","):
                包含操作元素的最上级div.nth(nth).wait_for()
                text = 包含操作元素的最上级div.nth(nth).text_content()
                if not text:
                    if 包含操作元素的最上级div.nth(nth).locator("input,textarea").filter(visible=True).count():
                        text = 包含操作元素的最上级div.nth(nth).locator("input,textarea").locator(
                            "visible=true").last.input_value()
                with allure.step(f"比对字段{字段}的页面值:{text}和预计值:{value}"):
                    for i in range(5):
                        try:
                            assert value in text
                            break
                        except:
                            self.page.wait_for_timeout(1000)

    def upload_模板导入(self, file_path):
        with self.page.expect_file_chooser() as file_chooser:
            self.click_button("上传数据")
        file_chooser.value.set_files(file_path)
        # self.page.get_by_text("上传数据中").wait_for()
        # self.page.get_by_text("上传数据中").wait_for(state="hidden")
        self.page.locator('span.c7n-upload').filter(has_text='重新上传').wait_for()
        self.click_button("下一步")
        self.click_button("校验数据")
        self.page.get_by_text("导出全部数据").filter(visible=True).last.wait_for()
        self.page.get_by_text("验证成功").last.wait_for()
        self.click_button("下一步")
        self.click_button("导入数据")
        self.page.get_by_text("导入成功").last.wait_for(state="attached")

    def ocant_datetime_填写日期控件(self, datatime_value, nth=-1):
        # 年份填写
        if nth != -1:
            self.page.wait_for_timeout(1000)
        self.page.locator("button[class$=picker-year-btn]").filter(visible=True).nth(nth).click()
        try:
            self.page.locator(f"div[class$=picker-cell-inner]:has-text('{datatime_value.year}')").locator(
                "visible=true").nth(nth).click(timeout=1000)
        except:
            if datetime.datetime.now().year > datatime_value.year:
                年份翻页 = self.page.locator("button[class$=picker-header-super-prev-btn]").locator(
                    "visible=true")  # 年份减小
            else:
                年份翻页 = self.page.locator("button[class$=picker-header-super-next-btn]").locator(
                    "visible=true")  # 年份增加
            for i in range(10):
                年份翻页.click()
                try:
                    self.page.locator(f"div[class$=picker-cell-inner]:has-text('{datatime_value.year}')").locator(
                        "visible=true").click(timeout=1000)
                    break
                except:
                    pass
        # 月份填写
        try:
            self.page.locator("button[class$=picker-month-btn]").filter(visible=True).nth(nth).click(timeout=1000)
        except:
            pass
        self.page.locator(f"div[class$=picker-cell-inner]:text-is('{datatime_value.month}月'):visible").click()
        # 日期填写
        self.page.locator(
            f"td[class*=picker-cell-in-view] div[class$=picker-cell-inner]:text-is('{datatime_value.day}')").locator(
            "visible=true").nth(nth).click()

    def get_获取tagName(self, locator: Locator | str):
        """
        获取元素tagName的方法,比如div,span
        :param locator: 可以传入locator对象或者selector的字符串
        :return: tagName
        """
        return self.page.locator(locator).evaluate("node => node.tagName")

    def hover_加重试的hover(self, hover对象: Locator, 下一步点击对象: Locator, 第一步动作="hover", 第二步动作="click",
                            timeout=30_000):
        start = time.time()
        while True:
            if time.time() - start > timeout / 1000:
                pytest.fail("加重试的hover超时失败")
            try:
                if 第一步动作 == "hover":
                    hover对象.last.hover(timeout=3_000)
                else:
                    hover对象.last.click(timeout=3_000)
            except:
                self.click_模拟点击空白()  # 这里点击是重置页面逻辑,极少数情况下,需要通过点击空白处来重置hover逻辑
                continue
            self.page.wait_for_timeout(1_000)
            try:
                if 第二步动作 == "click":
                    下一步点击对象.last.click(timeout=3000)
                else:
                    下一步点击对象.last.wait_for(state="visible", timeout=3000)
            except:
                self.click_模拟点击空白()  # 这里点击是重置页面逻辑,极少数情况下,需要通过点击空白处来重置hover逻辑
                continue
            break

    def assert_提示词断言(self, 提示词: str, 策略: Optional[Literal["可见", "消失"]] = "可见", timeout=None):
        if 策略 == "可见":
            expect(self.page.get_by_text(提示词).filter(visible=True).last).to_be_visible(timeout=timeout)
        if 策略 == "消失":
            expect(self.page.get_by_text(提示词).filter(visible=True).last).to_be_hidden(timeout=timeout)

    def check_随机选择页面上一个radio(self):
        self.page.locator('//input[@type="radio"]').filter(visible=True).last.wait_for()
        random.choice(self.page.locator('//input[@type="radio"]').all()).click()

    def wait_等待网络请求结束(self, timeout=None):
        """
        和页面的apiCount的区别为:本条会判断当前是否有新的网络请求,如果有新的网络请求
        :param timeout:
        :return:
        """
        try:
            self.page.locator("*").filter(visible=True).first.click(trial=True, timeout=timeout)
        except:
            pass
        # if not timeout:
        #     timeout = 30_000
        # start = time.time()
        # self.page.wait_for_timeout(500)
        # while time.time() - start < timeout / 1000:
        #     with allure.step("等待时间"):
        #         apiCounter = self.page.evaluate("window.apiCounter")
        #         lastResponseEndTime = self.page.evaluate("window.lastResponseEndTime")
        #         domStatus = self.page.evaluate("window.domStatus")
        #         if not apiCounter and time.time() * 1000 - lastResponseEndTime >= 500 and not self.locators.loading_页面四瓣加载().count() and not domStatus:
        #             return
        #         self.page.wait_for_timeout(500)
        # self.page.wait_for_load_state("networkidle")
        # self.page.wait_for_timeout(1_000)
        # self.page.wait_for_load_state("networkidle")
        # self.page.wait_for_timeout(1_000)
        # self.page.wait_for_load_state("networkidle")
        # self.page.wait_for_timeout(1_000)
        # self.page.wait_for_load_state("networkidle")
        # self.page.wait_for_timeout(1_000)
        # try:
        #     self.page.wait_for_timeout(200)
        #     self.page.wait_for_load_state("networkidle", timeout=10_000)
        #     self.locators.loading_页面四瓣加载().wait_for(state="hidden", timeout=10_000)
        # except:
        pass

    def max_更改当前页显示为最大值(self):
        self.page.get_by_title("条/页").filter(visible=True).click()
        max(self.page.get_by_text("条/页").filter(visible=True).all(), key=lambda locator: str(locator)).click()
        try:
            # self.page.wait_for_load_state("networkidle")
            self.page.locator("*").filter(visible=True).first.click(trial=True)
        except:
            pass
        # self.page.locator("#apiCounter").wait_for(state="detached")

    def 选择审批人(self, 名称或编码, 类型="员工"):
        if 类型 == "员工" and self.loc_tab指定审批人员工.get_attribute("aria-selected") == "false":
            self.loc_tab指定审批人员工.click()
        elif 类型 == "用户" and self.loc_tab指定审批人用户.get_attribute("aria-selected") == "false":
            self.loc_tab指定审批人用户.click()
        self.search_填写搜索框(名称或编码)
        result = self.table(名称或编码)
        cell_1_1 = result.get_cell(0, 1)
        if cell_1_1.locator("input").count():
            for _ in range(5):
                try:
                    cell_1_1.locator("input").set_checked(True, timeout=6_000)
                    break
                except:
                    pass

    def expect_notice(self, *args, 点击弹窗内链接=False):
        """
        :param 点击弹窗内链接: True为点击
        :param args: str
        :return: None
        """
        expect(self.locators.notice(*args)).to_be_attached()
        if 点击弹窗内链接:
            self.click_js点击隐藏的元素(self.locators.notice(*args).locator("a"))

    @staticmethod
    def 转换数据类为字典(数据):
        if isinstance(数据, list):
            数据类列表 = []
            for 单数据 in 数据:
                数据类列表.append(单数据.as_dict())
            return 数据类列表
        else:
            try:
                return 数据.as_dict()
            except:
                return 数据

    @allure.step("重试")
    def 重试(self, *args, 重试次数=10):
        """
        重试一系列步骤
        @param args:子步骤的指针,比如locator.click, locator.hover
        @param 重试次数:
        @return:
        """
        with apiCount(self.page):
            for _ in range(重试次数):
                try:
                    for arg in args:
                        if isinstance(arg, tuple):
                            with allure.step(f"{arg[0].__name__} 参数:{arg[1:]}"):
                                f = arg[0]
                                param = arg[1:]
                                f(*param)
                        else:
                            with allure.step(arg.__name__):
                                arg(timeout=3000)
                    break
                except Exception as e:
                    if _ == 重试次数 - 1:
                        print(f"已经重试{重试次数}次，但仍然失败，错误信息：", e)
                        raise e

    def 获取粘贴板的内容(self) -> str:
        self.page.context.grant_permissions(["clipboard-read"])
        return self.page.evaluate(
            """
            () => {
                return navigator.clipboard.readText();
            }
            """
        )

    @staticmethod
    def max_找出locator中最长的元素定位(locator: Locator):
        expect(locator.last).to_be_attached()
        return max(locator.all(), key=lambda loc: len(loc.text_content()))

    @staticmethod
    def min_找出locator中最短的元素定位(locator: Locator):
        expect(locator.last).to_be_attached()
        min_loc = min(locator.all(), key=lambda loc: len(loc.text_content()))
        if locator.all_text_contents().count(min_loc.text_content()) > 1:
            return locator
        else:
            return min_loc

    def blur_使当前元素失焦(self):
        self.page.evaluate('document.activeElement.blur()')
        self.page.mouse.move(10, 10)

    @staticmethod
    def check_file_exists(file_path):
        # 检查文件是否存在
        if os.path.exists(file_path):
            # 检查文件是否为普通文件
            if os.path.isfile(file_path):
                # 获取文件大小
                file_size = os.path.getsize(file_path)
                if file_size > 0:
                    return True
        return False

    def copy_image_to_clipboard(self, filepath: str):
        import base64
        self.page.context.grant_permissions(["clipboard-read", "clipboard-write"])
        with open(filepath, "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode("utf-8")

        # 通过浏览器上下文写入剪贴板
        self.page.evaluate(
            """([base64Data]) => {
                const byteCharacters = atob(base64Data);
                const byteNumbers = new Array(byteCharacters.length);
                for (let i = 0; i < byteCharacters.length; i++) {
                    byteNumbers[i] = byteCharacters.charCodeAt(i);
                }
                const byteArray = new Uint8Array(byteNumbers);
                const blob = new Blob([byteArray], {type: 'image/png'});

                return navigator.clipboard.write([
                    new ClipboardItem({'image/png': blob})
                ]);
            }""",
            [img_base64]
        )

    def set_text_to_clipboard(self, text: str):
        self.page.context.grant_permissions(["clipboard-read", "clipboard-write"])
        self.page.evaluate(
            """(text) => {
                // 浏览器环境下操作剪贴板
                return navigator.clipboard.writeText(text);
            }""",
            text  # 传参给 JS
        )

    def click_模拟点击空白(self):
        self.page.locator("body").click()
        self.page.mouse.click(0, 0)

    @staticmethod
    def modify_docx(input_file, output_file, old_text=None, new_text=None, add_timestamp=False):
        from docx import Document
        from datetime import datetime

        # 打开文档
        doc = Document(input_file)

        # 替换文本（如果提供了old_text和new_text）
        if old_text and new_text:
            # 遍历文档中的每个段落
            for para in doc.paragraphs:
                if old_text in para.text:
                    para.text = para.text.replace(old_text, new_text)

            # 遍历文档中的每个表格
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for para in cell.paragraphs:
                            if old_text in para.text:
                                para.text = para.text.replace(old_text, new_text)

        # 添加时间戳（如果add_timestamp为True）
        if add_timestamp:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            doc.add_paragraph(f"文档处理时间：{current_time}")

        # 另存为新的文档
        doc.save(output_file)
        return output_file

