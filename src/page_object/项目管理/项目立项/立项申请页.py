from src.page_object import *
from src.page_object.项目管理.项目立项 import Base项目立项


class 立项申请页(Base项目立项):
    def __init__(self, page):
        super().__init__(page)
        self.url = "projectInitiation/reqInit"
        self.需求立项_按钮 = self.locators.button_按钮('需求立项')
        self.直接立项_按钮 = self.locators.button_按钮('直接立项')

    def navigate(self) -> None:
        """导航到绩效指标库页面"""
        self.page.goto(self.url)

    @property
    def 主表格(self) -> Table:
        """获取主表格对象"""
        return self.table("项目编码")

    def search_立项信息(self, 项目立项信息: str):
        self.search_填写搜索框(placeholder='关键词搜索', 关键字=项目立项信息)
        row = self.主表格.get_row_dict(0)
        return row


