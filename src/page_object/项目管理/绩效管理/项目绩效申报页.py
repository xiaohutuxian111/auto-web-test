from src.page_object import *
from src.core.base_page import PageObject


class 项目绩效申报页(PageObject):

    def __init__(self, page):
        super().__init__(page)
        self.项目管理_URL = "performance/declaration"
        self.查询输入框 = self.page.get_by_placeholder('项目编码/项目名称')

    def navigate(self) -> None:
        self.page.goto(self.项目管理_URL)

    @property
    def 主表格(self) -> Table:
        return self.table("财政项目分类编码")

    def search_绩效申报(self, 查询关键字: str):
        self.search_填写搜索框(placeholder='项目编码/项目名称', 关键字=查询关键字)
        return self.主表格.get_row_dict(0)

    def 获取申报按钮(self, 查询关键字: str):
        self.search_填写搜索框(placeholder='项目编码/项目名称', 关键字=查询关键字)
        btn = self.主表格.get_cell('操作', 查询关键字)
        申报_btn = btn.get_by_text('申报')
        return 申报_btn

    def fill_绩效申报(self, 申报信息: Dict[str, Any]):
        绩效目标, 绩效指标 = 申报信息.get('目标信息', {}), 申报信息.get('绩效指标', [])
        self.fill_快捷操作_填写表单(**绩效目标)
        self.click_button('引入绩效指标库')
        self.fill_引入绩效指标库()
        self.click_button('提交')

    def fill_引入绩效指标库(self, 绩效指标: List[str]):
        self.click_button('引入绩效指标库')
        指标导入Table = self.table('指标库编码')
        for 指标 in 绩效指标:
            self.search_填写搜索框(placeholder='资金用途', 关键字=指标)
            指标导入Table.get_cell(0, 0).locator('//span[@class="el-checkbox__input"]').click()
        self.click_button('确认')
