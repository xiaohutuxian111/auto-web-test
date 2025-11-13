from src.core.base_page import PageObject


class 自评汇总页(PageObject):

    def __init__(self, page):
        super().__init__(page)
        self.url = "performance/selfEval/projectPerformanceSelfEvalSummary"
        self.填报汇总_tab = self.page.get_by_role('tab', name='填报汇总')
        self.汇总列表_tab = self.page.get_by_role('tab', name='汇总列表')

    def navigate(self) -> None:
        self.page.goto(self.url)

    @property
    def 主表格(self):
        return self.table('自评编码')

    def select_财政项目(self, 项目名称: str) -> None:
        """选择财政项目"""
        self.page.get_by_placeholder('项目名称').fill(项目名称)
        self.page.locator(f".tree-node:has-text('{项目名称}')").filter(visible=True).first.click()
