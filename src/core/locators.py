"""
页面元素定位器模块

该模块提供了统一的页面元素定位功能，包括：
- 通用元素定位（按钮、输入框、弹窗等）
- 表单元素定位
- 动态元素定位
- 断言循环检查

基于Playwright的Locator API，提供了更高级的定位功能。
"""

import time
import inspect
import re
from typing import Union, List, Optional

from src.core import Page, Locator


def assert_with_loop(statement: str, timeout: int = 30) -> None:
    """
    带循环的断言检查
    
    Args:
        statement: 断言语句
        timeout: 超时时间（秒），默认为30秒
        
    Raises:
        AssertionError: 超时后断言仍未成功
    """
    start_time = time.time()
    frame = inspect.currentframe().f_back
    global_vars = frame.f_globals
    local_vars = frame.f_locals
    
    while True:
        try:
            exec(f"assert {statement}", global_vars, local_vars)
            return
        except AssertionError:
            if time.time() - start_time > timeout:
                raise AssertionError(f"{timeout} 秒内 assert 没有成功: {statement}")


class Locators:
    """
    页面元素定位器类
    
    提供了各种页面元素的定位方法，支持复杂的定位逻辑和动态元素查找。
    """
    
    def __init__(self, page: Page):
        """
        初始化定位器
        
        Args:
            page: Playwright页面对象
        """
        self.page = page

    def loading_页面按钮加载(self) -> Locator:
        """
        定位页面按钮加载动画
        
        Returns:
            Locator: 加载动画元素定位器
        """
        return self.page.locator("//*[contains(@class, 'btn-loading-icon')]").filter(visible=True).last

    def loading_加载动画(self) -> Locator:
        """
        定位页面加载动画
        
        Returns:
            Locator: 加载动画元素定位器
        """
        return self.page.locator("//*[contains(@class, 'app-loading-item')]").filter(visible=True).last

    def modal_弹窗(self) -> Locator:
        """
        定位模态弹窗
        
        Returns:
            Locator: 弹窗元素定位器
        """
        return self.page.locator('//div[contains(@class,"modal-content")]').filter(visible=True)

    def text_唯一文字(self, text: str) -> Locator:
        """
        定位包含指定文字的元素
        
        Args:
            text: 要查找的文字
            
        Returns:
            Locator: 文字元素定位器
        """
        return self.page.get_by_text(text).filter(visible=True)

    def button_按钮(self, text: str, nth: int = -1, exact: bool = False) -> Locator:
        """
        定位按钮元素
        
        Args:
            text: 按钮文字
            nth: 第几个按钮，默认为-1（最后一个）
            exact: 是否精确匹配，默认为False
            
        Returns:
            Locator: 按钮元素定位器
        """
        button = self.page.locator("button")
        if exact:
            button = button.filter(has_text=rf'^{text}$')
        else:
            for word in text:
                button = button.filter(has_text=word)
        return button.filter(visible=True).nth(nth)

    def close_右上角关闭(self, nth: int = -1) -> Locator:
        """
        定位右上角关闭按钮
        
        Args:
            nth: 第几个关闭按钮，默认为-1（最后一个）
            
        Returns:
            Locator: 关闭按钮定位器
        """
        return self.page.locator('//span[@class="antBase-modal-close-x"]').filter(visible=True).nth(nth)

    def more_三点(self, 包含三点上层定位: Optional[Locator] = None, nth: int = -1) -> Locator:
        """
        定位三点菜单
        
        Args:
            包含三点上层定位: 上层定位器，默认为None
            nth: 第几个三点菜单，默认为-1（最后一个）
            
        Returns:
            Locator: 三点菜单定位器
        """
        if 包含三点上层定位 is None:
            return self.page.locator('//*[@*="#oc_base-more"]').locator("visible=true").nth(nth)
        else:
            # TODO: 实现上层定位器的三点菜单定位
            return 包含三点上层定位.locator('')

    def 包含操作元素的最上级div(self, 字段名: Union[str, Locator]) -> Locator:
        """
        定位包含操作元素的最上级div
        
        Args:
            字段名: 字段名称或定位器
            
        Returns:
            Locator: 最上级div定位器
        """
        最终上级元素locator = None
        if isinstance(字段名, Locator):
            return 字段名
        else:
            字段名列表 = 字段名.split("OR")
            for index, 字段 in enumerate(字段名列表):
                # 构建字段正则表达式，支持必填标记
                字段正则 = re.compile(rf"^\s*\**{re.escape(字段.replace('__', '.'))}([（(][^）)]*[）)])?[:：]*\s*$")
                if index == 0:
                    最终上级元素locator = self.page.locator("label").or_(self.page.locator(".form-label")).or_(self.page.locator('.el-form-item__label')).or_(self.page.locator('.required-label')).filter(
                        visible=True).filter(
                        has=self.page.get_by_text(字段正则)).locator(self.below_元素下方紧邻的元素())
                else:
                    最终上级元素locator = 最终上级元素locator.or_(
                        self.page.locator("label").or_(self.page.locator(".form-label")).or_(self.page.locator('.el-form-item__label')).or_(self.page.locator('.required-label')).filter(
                            has=self.page.get_by_text(字段正则)).locator(self.below_元素下方紧邻的元素()))
            return 最终上级元素locator

    def input_表单input定位(self, 包含操作元素的最上级div: Locator, 字段页面排序: int = -1) -> Locator:
        """
        定位表单输入框
        
        Args:
            包含操作元素的最上级div: 上级div定位器
            字段页面排序: 字段页面排序，默认为-1（最后一个）
            
        Returns:
            Locator: 输入框定位器
        """
        return 包含操作元素的最上级div.nth(字段页面排序).locator(
            self.page.locator('input,textarea').filter(visible=True).last)

    def switch_表单switchButton定位(self, 包含操作元素的最上级div: Locator, 字段页面排序: int = -1) -> Locator:
        """
        定位表单开关按钮
        
        Args:
            包含操作元素的最上级div: 上级div定位器
            字段页面排序: 字段页面排序，默认为-1（最后一个）
            
        Returns:
            Locator: 开关按钮定位器
        """
        return 包含操作元素的最上级div.nth(字段页面排序).locator(
            self.page.locator('//div[contains(@class,"el-switch")]').filter(visible=True).last)

    def click_表单可点击span定位(self, 包含操作元素的最上级div: Locator, 字段页面排序: int = -1) -> Locator:
        """
        定位表单可点击的span元素
        
        Args:
            包含操作元素的最上级div: 上级div定位器
            字段页面排序: 字段页面排序，默认为-1（最后一个）
            
        Returns:
            Locator: span元素定位器
        """
        return 包含操作元素的最上级div.nth(字段页面排序).locator(
            self.page.locator('span').filter(visible=True).last)

    def click_从详情返回列表箭头(self, 字段页面排序: int = -1) -> Locator:
        """
        定位从详情返回列表的箭头
        
        Args:
            字段页面排序: 字段页面排序，默认为-1（最后一个）
            
        Returns:
            Locator: 返回箭头定位器
        """
        return self.page.locator(".back-btn").filter(visible=True).nth(字段页面排序)

    def below_元素下方紧邻的元素(self, 要找的元素类型: str = "*") -> Locator:
        """
        定位元素下方紧邻的元素
        
        Args:
            要找的元素类型: 元素类型，默认为"*"（任意类型）
            
        Returns:
            Locator: 下方元素定位器
        """
        return self.page.locator(f"xpath=/following::{要找的元素类型}[position()=1]")

    def above_元素上方紧邻的元素(self, 要找的元素类型: str = "*") -> Locator:
        """
        定位元素上方紧邻的元素
        
        Args:
            要找的元素类型: 元素类型，默认为"*"（任意类型）
            
        Returns:
            Locator: 上方元素定位器
        """
        return self.page.locator(f"xpath=/preceding::{要找的元素类型}[position()=1]")

    def below_元素下方所有的元素(self, 要找的元素类型: str = "*") -> Locator:
        """
        定位元素下方所有的元素
        
        Args:
            要找的元素类型: 元素类型，默认为"*"（任意类型）
            
        Returns:
            Locator: 下方所有元素定位器
        """
        return self.page.locator(f"xpath=/following::{要找的元素类型}")

    def above_元素上方所有的元素(self, 要找的元素类型: str = "*") -> Locator:
        """
        定位元素上方所有的元素
        
        Args:
            要找的元素类型: 元素类型，默认为"*"（任意类型）
            
        Returns:
            Locator: 上方所有元素定位器
        """
        return self.page.locator(f"xpath=/preceding::{要找的元素类型}")

    def list_下拉项的定位(self, 下拉项名称: str) -> Locator:
        """
        定位下拉项
        
        Args:
            下拉项名称: 下拉项的名称
            
        Returns:
            Locator: 下拉项定位器
        """
        return self.page.get_by_title(下拉项名称).filter(visible=True)

    def notice(self, text: Union[List[str], str]) -> Locator:
        """
        定位通知消息
        
        Args:
            text: 通知文字，可以是字符串或字符串列表
            
        Returns:
            Locator: 通知消息定位器
        """
        notice_locator = self.page.locator(".c7n-notification-notice")
        if isinstance(text, str):
            return notice_locator.filter(has_text=text).last
        elif isinstance(text, list):
            for _ in text:
                notice_locator = notice_locator.filter(has_text=_)
            return notice_locator.last
        else:
            raise ValueError("text参数必须是字符串或字符串列表")

    def use_locator(self, use_text: str, nth: int = -1) -> Locator:
        """
        使用属性包含指定文字的元素定位器
        
        Args:
            use_text: 要查找的文字
            nth: 第几个元素，默认为-1（最后一个）
            
        Returns:
            Locator: 元素定位器
        """
        return self.page.locator(f"//*[contains(@*,'{use_text}')]").filter(visible=True).nth(nth)

    def 表单项中包含操作元素的最上级div(self, 字段名: str) -> Locator:
        """
        定位表单项中包含操作元素的最上级div
        
        Args:
            字段名: 字段名称
            
        Returns:
            Locator: 最上级div定位器
        """
        最终上级元素locator = self.page.locator("label,.el-form-item__label").filter(visible=True).filter(
            has=self.page.get_by_text(字段名)).locator(self.below_元素下方紧邻的元素())
        return 最终上级元素locator

    def 表单包含操作元素的最上级div(self, 字段名: str) -> Locator:
        """
        定位表单包含操作元素的最上级div
        
        Args:
            字段名: 字段名称
            
        Returns:
            Locator: 最上级div定位器
        """
        最终表单上级元素locator = self.page.locator(".card-title").filter(visible=True).filter(
            has=self.page.get_by_text(字段名)).locator(self.below_元素下方紧邻的元素())
        return 最终表单上级元素locator

    def model_弹窗(self) -> Locator:
        """
        定位模型弹窗
        
        Returns:
            Locator: 弹窗定位器
        """
        return self.page.locator("//div[contains(@class,'model-content')]").locator("visible=true")

    def 包含操作元素最上级div(self, 字段名: Union[str, Locator]) -> Locator:
        """
        定位包含操作元素的最上级div（简化版）
        
        Args:
            字段名: 字段名称或定位器
            
        Returns:
            Locator: 最上级div定位器
        """
        if isinstance(字段名, Locator):
            return 字段名
        else:
            if "__" in 字段名:
                字段名列表 = 字段名.split("__")
                label初定位 = '//label'
                for i, name in enumerate(字段名列表):
                    label初定位 = label初定位 + f'[contains(test(),f"{name}")]'
                label定位 = self.page.locator(label初定位)
            else:
                label定位 = self.page.locator('//label').filter(
                    has=self.page.get_by_text(re.compile(f"^\\s*{字段名}\\s*$"), exact=True)).locator("visible=true")
            return label定位.locator("xpath=/following::*[position()=1]")

    def switch_表单可点击span定位(self, 包含操作元素的最上级div: Locator, 字段页面排序: int = -1) -> Locator:
        """
        定位表单可点击的span元素（开关类型）
        
        Args:
            包含操作元素的最上级div: 上级div定位器
            字段页面排序: 字段页面排序，默认为-1（最后一个）
            
        Returns:
            Locator: span元素定位器
        """
        return 包含操作元素的最上级div.nth(字段页面排序).locator(self.page.locator("span").locator("visible=true").last)
