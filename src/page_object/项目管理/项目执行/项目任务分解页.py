from src.core import *

from src.core.base_page import PageObject
from src.core.components.table import Table
from src.utils import faker_随机数生成


class 项目任务分解页(PageObject):
    def __init__(self, page):
        super().__init__(page)

        self.url = "projectImplement/taskBreakdown"

    def navigate(self):
        self.page.goto(self.url)

    def click_任务分解(self, 项目名称: str):

        self.page.locator(".project-item").first.locator(".more-icon").click()
        self.page.locator(".menu-button").get_by_text("编辑").filter(visible=True).click()

    def _fix_项目任务列表(self, 项目任务列表: List[str]):
        self.click_button("修改")
        项目任务阶段修改_table = self.table("任务阶段名称", 表格序号=-1)
        for i, info in enumerate(项目任务列表):
            self.page.locator(".add-step").get_by_text("新增").click()
            self.fill_快捷操作_填写表格(table=项目任务阶段修改_table, 行定位或行号=i, **{"任务阶段名称": info})
        # 删除多余行
        num = len(项目任务列表)
        操作_list = 项目任务阶段修改_table.get_col_list("操作", text=False)[num:]
        if len(操作_list) > 0:
            for _ in range(len(操作_list)):
                项目任务阶段修改_table.get_cell("操作", num).get_by_role("button", name="删除").click()
        self.locators.button_按钮("保存", nth=0).click()

    def fill_项目任务分解(self, 项目计划分解: Dict[str, Any]):
        项目任务列表, 项目计划分解 = 项目计划分解.get("项目任务列表", []), 项目计划分解.get("项目计划分解", [])
        self._fix_项目任务列表(项目任务列表)
        table = Table(self.page, "任务阶段")
        for i, info in enumerate(项目计划分解):
            self.fill_快捷操作_填写表格(table, 行定位或行号=i, **info)
            if i < len(项目计划分解) - 1:
                self.page.locator(".add").get_by_text("新增").click()

    def upload_附件(self, temp_path: str):
        file_path = os.path.join(temp_path, f"test_upload_{faker_随机数生成(4)}.pdf")
        generate_formatted_file(file_type="pdf", file_path=file_path)
        upload_input = self.page.locator("input[type='file']")
        upload_input.last.set_input_files(file_path)
