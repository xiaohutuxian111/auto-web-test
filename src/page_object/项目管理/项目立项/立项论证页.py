from src.page_object import *
from src.core.base_page import PageObject


class 立项论证页(PageObject):

    def __init__(self, page):
        super().__init__(page)
        self.url = "projectInitiation/argumentationProjectList"
        self.新增_按钮 = self.locators.button_按钮('新增')

    def navigate(self) -> None:
        self.page.goto(self.url)

    @property
    def 主表格(self) -> Table:
        return self.table("立项论证周期")

    def fill_立项论证(self, 立项论证: Dict[str, Any]):
        立项论证信息, 论证项目明细 = 立项论证.get('立项论证信息', {}), 立项论证.get('论证项目明细', [])
        self.fill_快捷操作_填写表单(**立项论证信息)
        table = Table(self.page, '项目编码')
        for i, info in enumerate(论证项目明细):
            self.page.locator('#button').click()
            self.fill_快捷操作_填写表格(table=table, 行定位或行号=i, **info)

    def search_项目论证(self, 查询信息: str):
        self.search_填写搜索框(placeholder='立项论证登记单号/经办人', 关键字=查询信息)
        info = self.主表格.get_row_dict(0)
        return info
