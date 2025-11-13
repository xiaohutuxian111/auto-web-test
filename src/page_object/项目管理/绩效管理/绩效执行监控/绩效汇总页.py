from typing import Dict, List

from src.core.base_page import PageObject


class 绩效汇总页(PageObject):

    def __init__(self, page):
        super().__init__(page)
        self.url = "performance/monitoring/fill/summary"
        self.汇总_按钮 = self.locators.button_按钮('汇总')
        self.填报汇总_tab = self.page.get_by_role('tab', name='填报汇总')
        self.汇总列表_tab = self.page.get_by_role('tab', name='汇总列表')

    def navigate(self) -> None:
        """导航到绩效指标库页面"""
        self.page.goto(self.url)

    @property
    def 主表格(self):
        return self.table("绩效监控时间")

    def select_财政项目(self, 项目名称: str) -> None:
        """选择财政项目"""
        self.page.get_by_placeholder('项目名称').fill(项目名称)
        self.page.locator(f".tree-node:has-text('{项目名称}')").filter(visible=True).first.click()

    def search_绩效项目(self, 搜索关键字):
        self.search_填写搜索框(placeholder='填报编码/项目编码', 关键字=搜索关键字)
        tabel = self.主表格
        return tabel.get_row_dict(0)

    def fill_绩效汇总(self, 已填报绩效项目: List[Dict[str, str]]):
        for 项目信息 in 已填报绩效项目:
            self.select_财政项目(项目信息['项目名称'])
            self.search_绩效项目(项目信息['项目编码'])
            self.主表格.除了all的checkbox()
        self.汇总_按钮.click()
        self.confirm_弹框()
