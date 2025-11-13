from src.page_object.项目管理.项目需求储备库 import Base需求页


class 需求申报页(Base需求页):
    def __init__(self, page):
        super().__init__(page)
        self.url = "projectStore/demand"
        self.新增_按钮 = self.locators.button_按钮('新增')

    def navigate(self):
        self.page.goto(self.url)

    @property
    def 主表格(self):
        return self.table('需求编号')

    def search_需求(self, 关键字: str):
        self.search_填写搜索框(placeholder="需求编号/需求名称", 关键字=关键字)
        return self.主表格.get_row_dict(0)
