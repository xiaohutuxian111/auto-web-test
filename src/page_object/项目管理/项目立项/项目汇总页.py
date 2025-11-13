from src.page_object import *
from src.core.base_page import PageObject


class 项目汇总页(PageObject):

    def __init__(self, page):
        super().__init__(page)
        self.url = "projectInitiation/projectSummary"
        self.一键催办_按钮 = self.locators.button_按钮('一键催办')

    def navigate(self) -> None:
        """导航到绩效指标库页面"""
        self.page.goto(self.url)

    @property
    def 主表格(self) -> Table:
        """获取主表格对象"""
        return self.table("汇总人")

    def search_汇总项目(self, 关键字: str):
        pass

    def fill_项目汇总(self, 汇总信息: Dict[str, Any]):
        pass
