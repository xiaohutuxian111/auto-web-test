import sys
import re
import time
import allure
from playwright.sync_api import Page, Locator

if sys.version_info >= (3, 8):
    from typing import Literal, Union, List
else:
    from typing_extensions import Literal

import inspect
import time


def assert_with_loop(statement):
    start_time = time.time()
    frame = inspect.currentframe().f_back
    global_vars = frame.f_globals
    local_vars = frame.f_locals
    while True:
        try:
            exec(f"assert {statement}", global_vars, local_vars)
            return
        except AssertionError:
            if time.time() - start_time > 30:
                raise AssertionError(f"30 秒内 assert 没有成功: {statement}")


class Locators:
    def __init__(self, page: Page):
        self.page = page

    def loading_页面按钮加载(self):
        return self.page.locator("//*[contains(@class, 'btn-loading-icon')]").filter(visible=True).last

    def loading_页面四瓣加载(self):
        return self.page.locator("//*[contains(@class, 'spin-dot-spin')]").filter(visible=True).last

    def modal_弹窗(self):
        return self.page.locator('//div[contains(@class,"modal-content")]').filter(visible=True)

    def text_唯一文字(self, text):
        return self.page.get_by_text(text).filter(visible=True)

    def button_按钮(self, text, nth=-1):
        button = self.page.locator("button")
        for word in text:
            button = button.filter(has_text=word)
        return button.filter(visible=True).nth(nth)

    def close_右上角关闭(self, nth=-1):
        return self.page.locator('//span[@class="antBase-modal-close-x"]').filter(visible=True).nth(nth)

    def more_三点(self, nth=-1):
        return self.page.locator('//*[contains(@*,"_more")]').filter(visible=True).or_(
            self.page.locator('//*[contains(@*,"-more")]')).filter(visible=True).nth(nth)

    def 包含操作元素的最上级div(self, 字段名: Union[str, Locator]):
        最终上级元素locator = None
        if isinstance(字段名, Locator):
            return 字段名
        else:
            字段名列表 = 字段名.split("OR")
            for index, 字段 in enumerate(字段名列表):
                字段正则 = re.compile(f"^\\s*\\**{字段.replace('__', '.')}[:|：]*\\s*$")
                if index == 0:
                    最终上级元素locator = self.page.locator("label").filter(visible=True).filter(
                        has=self.page.get_by_text(字段正则)).locator(self.below_元素下方紧邻的元素())
                else:
                    最终上级元素locator = 最终上级元素locator.or_(
                        self.page.locator("label").filter(visible=True).filter(
                            has=self.page.get_by_text(字段正则)).locator(self.below_元素下方紧邻的元素()))
            return 最终上级元素locator

            # else:
            #     字段名 = re.compile(f"^\\s*\\**{字段名.replace('__', '.')}[:|：]*\\s*$")
            #     return self.page.locator("label,span").filter(visible=True).filter(has=self.page.get_by_text(字段名)).locator(self.below_元素下方紧邻的元素())

    # def 包含操作元素的最上级div(self, 字段名: Union[str, Locator]):
    #     if isinstance(字段名, Locator):
    #         return 字段名
    #     else:
    #         if "__" in 字段名:
    #             字段名列表 = 字段名.split("__")
    #             label初定位 = '//label'
    #             for i in 字段名列表:
    #                 label初定位 = label初定位 + f'[contains(text(),"{i}")]'
    #             label定位 = self.page.locator(label初定位).filter(visible=True)
    #         else:
    #             label定位 = self.page.locator('//label').filter(has=self.page.get_by_text(re.compile(f"^\\s*{字段名}\\s*$"), exact=True)).filter(visible=True)
    #         return label定位.locator("xpath=/following::*[position()=1]")

    def input_表单input定位(self, 包含操作元素的最上级div: Locator, 字段页面排序=-1):
        # if 包含操作元素的最上级div.nth(字段页面排序).evaluate("node => node.tagName") in "INPUT,TEXTAREA":
        #     return 包含操作元素的最上级div.nth(字段页面排序)
        # else:
        return 包含操作元素的最上级div.nth(字段页面排序).locator(
            self.page.locator('input,textarea').filter(visible=True).last)

    def switch_表单switchbutton定位(self, 包含操作元素的最上级div: Locator, 字段页面排序=-1):
        # if "-switch" in 包含操作元素的最上级div.nth(字段页面排序).get_attribute("class"):
        #     return 包含操作元素的最上级div.nth(字段页面排序)
        # else:
        return 包含操作元素的最上级div.nth(字段页面排序).locator(
            self.page.locator('//button[contains(@class,"-switch")]').filter(visible=True).last)

    def click_表单可点击span定位(self, 包含操作元素的最上级div: Locator, 字段页面排序=-1):
        # if 包含操作元素的最上级div.nth(字段页面排序).evaluate("node => node.tagName") in "SPAN":
        #     return 包含操作元素的最上级div.nth(字段页面排序)
        # else:
        return 包含操作元素的最上级div.nth(字段页面排序).locator(
            self.page.locator('span').filter(visible=True).last)  # .antBase_proSrcTagValueList_tagList

    def click_从详情返回列表箭头(self, 字段页面排序=-1):
        return self.page.locator(".back-btn").filter(visible=True).nth(字段页面排序)

    def below_元素下方紧邻的元素(self, 要找的元素类型="*"):
        return self.page.locator(f"xpath=/following::{要找的元素类型}[position()=1]")

    def above_元素上方紧邻的元素(self, 要找的元素类型="*"):
        return self.page.locator(f"xpath=/preceding::{要找的元素类型}[position()=1]")

    def below_元素下方所有的元素(self, 要找的元素类型="*"):
        return self.page.locator(f"xpath=/following::{要找的元素类型}")

    def above_元素上方所有的元素(self, 要找的元素类型="*"):
        return self.page.locator(f"xpath=/preceding::{要找的元素类型}")

    def list_下拉项的定位(self, 下拉项名称: str):
        return self.page.get_by_title(下拉项名称).filter(visible=True)

    def notice(self, text: Union[List[str], str]):
        notice_locator = self.page.locator(".c7n-notification-notice")
        if isinstance(text, str):
            return notice_locator.filter(has_text=text).last
        elif isinstance(text, list):
            for _ in text:
                notice_locator = notice_locator.filter(has_text=_)
            return notice_locator.last

    def use_locator(self, use_text: str, nth=-1):
        return self.page.locator(f"//*[contains(@*,'{use_text}')]").filter(visible=True).nth(nth)

