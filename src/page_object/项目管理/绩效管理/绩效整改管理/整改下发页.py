from src.page_object import *
from src.core.base_page import PageObject


class 整改下发页(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.url = "performance/performanceImproveManage/rectificationIssuanceList"
        self.新增_按钮 = self.locators.button_按钮('新增')

    def navigate(self) -> None:
        """导航到绩效指标库页面"""
        self.page.goto(self.url)

    @property
    def 主表格(self) -> Table:
        """获取主表格对象"""
        return self.table("整改截止日期")

    def fill_整改下发(self, temp_path: str, 整改信息: Dict[str, str]):
        self.fill_快捷操作_填写表单(**整改信息)
        self.upload_random_file(temp_path)
        self.click_button('提交')
        self.confirm_弹框()
