from src.core.base_page import PageObject


class 结项申报页(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.项目管理_URL = 'projectPortal/leaderShow?sign=project'
        self.url = "projectCompletion/finalDeclarationList"
        self.新增_按钮 = self.locators.button_按钮('新增')

    def navigate(self):
        self.page.goto(self.项目管理_URL)
        self.page.goto(self.url)
        self.page.wait_for_load_state("networkidle")

    @property
    def 主表格(self):
        return self.table('审批状态')