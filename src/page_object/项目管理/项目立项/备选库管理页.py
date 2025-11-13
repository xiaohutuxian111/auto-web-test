from src.page_object import *
from src.core.base_page import PageObject


class 备选库管理页(PageObject):

    def __init__(self, page):
        super().__init__(page)
        self.url = "projectInitiation/alternativeLibrary"
        self.清空排序分组_按钮 = self.locators.button_按钮('清空排序分组')
        self.批量排序_按钮 = self.locators.button_按钮('批量排序')

    def navigate(self) -> None:
        self.page.goto(self.url)

    @property
    def 主表格(self) -> Table:
        """获取主表格对象"""
        return self.table("项目编码")

    def search_备选库(self, 查询信息: str):
        self.search_填写搜索框(placeholder='关键词搜索', 关键字=查询信息)
        info = self.主表格.get_row_dict(0)
        return info

    def 备选库处置(self, 查询信息: str, 项目处置: Dict[str, str]):
        self.search_填写搜索框(placeholder='关键词搜索', 关键字=查询信息)
        btn = self.主表格.get_cell('操作', 0)
        if not btn:
            raise '不存在处置的项目'
        处置_按钮 = btn.get_by_text('处置').first
        处置_按钮.click()
        self.fill_快捷操作_填写表单(**项目处置)
        self.click_button('确认')
