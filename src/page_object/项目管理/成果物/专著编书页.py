from src.page_object import *
from src.core.base_page import PageObject


class 专著编书页(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.url = "achievements/compilationMonographsList"
        self.新增_按钮 = self.locators.button_按钮('新增')

    def navigate(self):
        self.page.goto(self.url)

    @property
    def 主表格(self):
        return self.table('专著名称')

    def search_专著编书(self, 查询信息: str):
        self.search_填写搜索框(placeholder='项目名称/课程名称', 关键字=查询信息)
        info = self.主表格.get_row_dict(0)
        return info

    def fill_专著编书(self, 专著编书: Dict[str, Any]):
        基本信息, 参与作者 = 专著编书.get('基本信息', {}), 专著编书.get('参与作者', [])
        self.fill_快捷操作_填写表单(**基本信息)
        table = Table(self.page, '担任职责')
        for i, info in enumerate(参与作者):
            self.click_button('新增')
            self.fill_快捷操作_填写表格(table, 行定位或行号=i, **info)
