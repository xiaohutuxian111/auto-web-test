from src.core import *
from src.core.base_page import PageObject


class 资产巡检结果页(PageObject):
    def __init__(self, page):
        super().__init__(page)

        self.url = "maintenance/inspectionResultsList"

    def navigate(self):
        self.page.goto(self.url)

    @property
    def 主表格(self):
        return self.table('资产编号')

    def search_项目可行性研究报告(self, 查询信息: str):
        self.search_填写搜索框(placeholder='资产编号/资产名称', 关键字=查询信息)
        info = self.主表格.get_row_dict(0)
        return info

    def fill_资产登记(self, 资产登记信息: Dict[str, Any]):
        pass
