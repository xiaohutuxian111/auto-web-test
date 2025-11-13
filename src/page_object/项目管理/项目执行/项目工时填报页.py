from src.core import *
from src.core.table import Table
from src.core.base_page import PageObject


class 项目工时填报页(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.url = "projectImplement/workHoursStatistics"
        self.日历视图_tab = self.page.get_by_role("tab", name="日历视图")
        self.原型视图_tab = self.page.get_by_role("tab", name="原型视图")

    def navigate(self):
        self.page.goto(self.url)

    @property
    def 主表格(self):
        return self.table("工作开始时间")

    def search_条件查询(self, 日期: str, 项目类型: str, 项目名称: str):
        self.search_填写搜索框(placeholder="项目名称", 关键字=项目名称)

    def select_calendar_day(self, day: int):
        """
        :param day: 日期数字 (int)
        """
        locator = self.page.locator(f".el-calendar-table td.current:has(.day-number:text('{day}')) >> .add-button")
        locator.first.click()

    def _click_日期(self, 日期: str):
        self.page.get_by_placeholder("结束日期").click()
        self.page.locator(f".el-date-table-cell:has(.el-date-table-cell__text:text('{日期}'))").filter(
            visible=True
        ).first.click()

    def fill_工时填报(self, 项目名称, 当前日期: str, 执行进度填写info: Dict[str, Any]):

        # 特殊处理结束日期
        self._click_日期(当前日期)
        # 特数处理项目名称 ！！ 前端未非点击框
        self.page.get_by_placeholder("请选择项目名称").click()
        self.page.get_by_placeholder("项目编码/名称").fill(项目名称)
        self.page.get_by_placeholder("项目编码/名称").press("Enter")
        table = Table(self.page, "项目编码")
        table.get_cell("单选", 0).locator(".el-radio__inner").click()
        self.click_button("确定")
        self.fill_快捷操作_填写表单(**执行进度填写info)

        self.click_button("送审")
