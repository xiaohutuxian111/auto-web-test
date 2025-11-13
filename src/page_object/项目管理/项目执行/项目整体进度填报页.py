from src.core.base_page import PageObject


class 项目整体进度填报页(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.项目管理_URL = 'projectPortal/leaderShow?sign=project'
        self.url = "projectImplement/majorProjectReport"

    def navigate(self):
        self.page.goto(self.项目管理_URL)
        self.page.goto(self.url)
        self.page.wait_for_load_state("networkidle")

    @property
    def 主表格(self):
        return self.table('操作列')