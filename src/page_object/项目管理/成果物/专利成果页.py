from src.page_object import *
from src.core.base_page import PageObject


class 专利成果页(PageObject):
    def __init__(self, page):
        super().__init__(page)

        self.url = "achievements/patent"
        self.新增_按钮 = self.locators.button_按钮('新增')

    def navigate(self):
        self.page.goto(self.url)

    @property
    def 主表格(self):
        return self.table('专利所有权人')

    def search_专利成果(self, 查询信息: str):
        self.search_填写搜索框(placeholder='专利名称/项目名称', 关键字=查询信息)
        info = self.主表格.get_row_dict(0)
        return info

    def fill_专利成果(self, 专利信息: Dict[str, Any]):
        基本信息 = 专利信息.get('基本信息', {})
        self.fill_快捷操作_填写表单(**基本信息)
