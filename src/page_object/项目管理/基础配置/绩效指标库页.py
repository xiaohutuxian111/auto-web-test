from src.page_object import *
from src.core.base_page import PageObject


class 绩效指标库页(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.url = "basicConfiguration/performanceIndexConfig"
        self.导入按钮 = self.locators.button_按钮('导入')
        self.导出按钮 = self.locators.button_按钮('导出')
        self.新增按钮 = self.locators.button_按钮('新增')
        self.指标类型查询输入框 = self.page.get_by_placeholder('输入类型')
        self.分页总数 = self.page.locator('span.el-pagination__total.is-first')
        self.编辑页面 = self.page.get_by_text("编辑绩效指标")

    def navigate(self):
        """导航到绩效指标库页面"""
        self.page.goto(self.url)

    @property
    def 主表格(self):
        return self.table("指标库编码")

    def fill_新增绩效指标(self, 绩效指标信息: Dict[str, str]):
        self.fill_快捷操作_填写表单(**绩效指标信息)
        self.click_button("保存")
        self.confirm_弹框()
