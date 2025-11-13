from src.core.base_page import PageObject
from src.page_object.我的待办 import 我的待办


class 领导工作台页(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.url = 'projectPortal/leaderShow'
        self.待办事项_更多 = self.page.get_by_role('button', name='更多').filter(visible=True)
        self.我的待办 = 我的待办(self.page)

    def navigate(self):
        self.page.goto(self.url)







