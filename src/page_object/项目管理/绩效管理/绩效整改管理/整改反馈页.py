from src.page_object import *
from src.core.base_page import PageObject


class 整改反馈页(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.url = "performance/performanceImproveManage/rectificationFeedbackList"

    def navigate(self) -> None:
        self.page.goto(self.url)

    @property
    def 主表格(self) -> Table:
        return self.table("整改反馈编码")

    def fill_整改反馈(self, temp_path: str, 反馈信息: Dict[str, str]):
        self.fill_快捷操作_填写表单(**反馈信息)
        self.upload_random_file(temp_path)
        self.click_button('提交')
        self.confirm_弹框()

    def get_状态定位(self, 项目名称: str, 状态: str = '编辑') -> Locator:
        self.max_更改当前页显示为最大值()
        loc = self.主表格.get_cell('操作', 项目名称)
        编辑_btn = loc.get_by_text('编辑')

        return 编辑_btn
