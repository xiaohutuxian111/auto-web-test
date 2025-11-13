from src.core import *
from src.core.base_page import PageObject


class 我的任务页(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.url = "projectImplement/mytask"

    def navigate(self):
        self.page.goto(self.url)

    @property
    def 主表格(self):
        return self.table("任务阶段")

    def fill_任务(self, 一级or二级任务名称: str, 执行进度填写信息: Dict[str, Any]):
        self.主表格.get_cell("操作", 一级or二级任务名称).get_by_text("编辑").click()
        self.fill_快捷操作_填写表单(**执行进度填写信息)
        # TODO 提交无反应
        self.click_button("提交")
        self.confirm_弹框()

    def get_card_info(self) -> Dict[str, int]:
        """
        获取任务统计
        """
        tasks = {}
        cards_loc = self.page.locator(".task-stats-container  .el-card__body").filter(visible=True).all()
        for card in cards_loc:
            name = card.locator(".task-name").inner_text().strip()
            value = card.locator(".task-count").inner_text().strip()
            tasks[name] = int(value) if value.isdigit() else value
        return tasks
