from src.core.base_page import PageObject


class 项目验收页(PageObject):
    def __init__(self, page):
        super().__init__(page)

        self.url = "projectCompletion/projectAcceptance"
        self.新增_按钮 = self.locators.button_按钮('新增')

    def navigate(self):
        self.page.goto(self.url)

    @property
    def 主表格(self):
        return self.table('审批状态')
