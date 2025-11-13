from src.page_object import *
from src.core.base_page import PageObject


class 项目变更页(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.url = "projectInitiation/reqInitChange"
        self.新增_按钮 = self.locators.button_按钮('新增')

    def navigate(self) -> None:
        """导航到绩效指标库页面"""
        self.page.goto(self.url)

    @property
    def 主表格(self) -> Table:
        """获取主表格对象"""
        return self.table("变更编码")

    def fill_立项变更(self, 变更信息: Dict[str, Any]):
        self.fill_快捷操作_填写表单(**变更信息)
        self.click_button('提交')
        self.confirm_弹框()
