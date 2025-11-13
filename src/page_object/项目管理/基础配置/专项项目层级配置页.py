from src.page_object import *
from src.core.base_page import PageObject


class 专项项目层级配置页(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.url = "basicConfiguration/specialProjectLevel"
        self.查询输入框 = self.page.get_by_placeholder("层级名称")

    def navigate(self):
        self.page.goto(self.url)

    @property
    def 主表格(self) -> Table:
        return self.table("操作")

    def search_专项层级(self, 查询信息: str):
        """搜索专项层级，返回第一条操作单元格"""
        self.search_填写搜索框(placeholder="层级名称", 关键字=查询信息)
        return self.主表格.get_cell("操作", 0)

    def fill_新增专项层级(self, 下级信息: Dict[str, Any]) -> Dict[str, Any]:
        """新增一个下级层级"""
        self.fill_快捷操作_填写表单(**下级信息)
        self.click_button("保存")
        self.confirm_弹框()
        return 下级信息

    def click_处理定位(self, 项目类型名称: str):
        """点击某个项目类型的 新增下级 按钮"""
        self.search_填写搜索框(关键字=项目类型名称, placeholder='层级名称')
        操作定位 = self.主表格.get_cell('操作', 0)
        操作定位.get_by_text('新增下级').click()

    def search_下级信息(self, 项目类型名称: str, 层级名称: str) -> Dict[str, Any]:
        """搜索某个项目类型下的下级层级信息"""
        self.search_填写搜索框(placeholder="层级名称", 关键字=项目类型名称)
        self.max_更改当前页显示为最大值()
        self.主表格.get_cell(0, 0).locator(".corner-arrow").click()

        下级信息_list = self.主表格.get_col_list("层级名称")
        index = next((i for i, name in enumerate(下级信息_list) if 层级名称 in name), None)
        if index is None:
            raise ValueError(f"未找到层级名称: {层级名称}")

        return self.主表格.get_row_dict(index)

    def delete_专项层级_项目类型(self, 项目类型编码: str):
        pass
