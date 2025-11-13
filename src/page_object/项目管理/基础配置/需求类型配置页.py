from src.page_object import *
from src.core.base_page import PageObject


class 需求类型配置页(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.url = "basicConfiguration/index"
        self.新增按钮 = self.locators.button_按钮('新增')
        self.查询输入框 = self.page.get_by_placeholder('需求类型编码/需求类型')

    def navigate(self):
        """导航到绩效指标库页面"""
        self.page.goto(self.url)

    @property
    def 主表格(self):
        return self.table("操作")

    def fill_基本信息(self, base_info: dict[str, str]):
        self.fill_快捷操作_填写表单(default_value=None, 操作块定位=None, **base_info)

    def fill_附件类型配置(self, table_info: List[dict[str, str]]):

        table = Table(self.page, '附件类型名称')
        n = len(table_info)
        for index, line_info in enumerate(table_info):
            self.fill_快捷操作_填写表格(table=table, 行定位或行号=index, **line_info)
            if index < n - 1:
                self.locators.button_按钮('新增').click()
        self.click_button('保存')
        self.confirm_弹框()
