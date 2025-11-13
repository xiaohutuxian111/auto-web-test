from src.core.base_page import PageObject


class 项目详情页(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.项目管理_URL = 'projectPortal/leaderShow?sign=project'
        self.url = "projectImplement/projectDetail"


    def navigate(self):
        self.page.goto(self.项目管理_URL)
        self.page.goto(self.url)
        self.page.wait_for_load_state("networkidle")

