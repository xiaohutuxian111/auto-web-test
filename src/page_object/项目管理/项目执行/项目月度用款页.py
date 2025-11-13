import random

from src.core.base_page import PageObject
from src.core.table import Table


class 项目月度用款页(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.新增_按钮 = self.locators.button_按钮("新增")
        self.导出_按钮 = self.locators.button_按钮("导出")
        self.url = "projectImplement/budgetMonthly"

    def navigate(self):
        self.page.goto(self.url)

    @property
    def 主表格(self):
        return self.table("审批状态")

    def search_月度用款(self, 关键字: str):
        self.search_填写搜索框(placeholder="项目名称", 关键字=关键字)
        info = self.主表格.get_row_dict(0)
        return info

    def fill_月度用款(self, 项目名称: str):
        self.fill_快捷操作_填写表单(**{"项目名称": 项目名称})
        table = Table(self.page, "支出事项")
        rows = len(table.get_col_list("支出事项"))
        for i in range(rows):
            info = {
                "一月": random.randint(1, 100),
                "二月": random.randint(1, 100),
                "三月": random.randint(1, 100),
                "四月": random.randint(1, 100),
                "五月": random.randint(1, 100),
                "六月": random.randint(1, 100),
                "七月": random.randint(1, 100),
                "八月": random.randint(1, 100),
                "九月": random.randint(1, 100),
                "十月": random.randint(1, 100),
                "十一月": random.randint(1, 100),
                "十二月": random.randint(1, 100),
            }
            self.fill_快捷操作_填写表格(table=table, 行定位或行号=i, **info)
        self.click_button("提交")
        self.confirm_弹框()
