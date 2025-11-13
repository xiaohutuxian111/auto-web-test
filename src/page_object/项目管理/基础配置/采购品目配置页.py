from src.test_cases import *
from src.core.base_page import PageObject


class 采购品目配置页(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.url = "basicConfiguration/procurementItemConfig"
        self.新增按钮 = self.locators.button_按钮('新增')
        self.导入按钮 = self.locators.button_按钮('导入')
        self.查询输入框 = self.page.get_by_placeholder('采购品目编码/名称')
        self.左侧查询框 = self.page.get_by_placeholder('请输入关键字过滤')

    def navigate(self):
        self.page.goto(self.url)

    @property
    def 主表格(self):
        return self.table("是否末级目录")

    def main_search(self, 搜索信息: str = None):
        self.查询输入框.fill(搜索信息)
        self.查询输入框.press('Enter')

    def fill_新增采购品配置(self, procurement_info: dict[str, str]):
        self.新增按钮.click()
        self.fill_快捷操作_填写表单(default_value=None, 操作块定位=None, **procurement_info)
        self.click_button('保存')

    def get_采购品目_一级(self) -> List[str]:
        self.page.wait_for_timeout(1000)
        node_names = []
        groups = self.page.locator('//div[@role="tree"]/div[@role="treeitem"]/div[@role="group"]')
        child_nodes = groups.locator('xpath=/div[@role="treeitem"]')
        count = child_nodes.count()
        for i in range(count):
            title = child_nodes.nth(i).locator(
                'xpath=/div[@class="el-tree-node__content"]/div[@class="custom-tree-node"]').inner_text()
            node_names.append(title)
        return node_names

    from typing import Literal

    def get_采购品目_一级_采购品目编码(
            self,
            mode: Literal['All', 'Effective'] = "Effective",
            numbers: int = 5
    ) -> Dict[str, List[str]]:
        """
        获取一级采购品目对应的采购品目编码
        """
        self.page.wait_for_timeout(1000)
        采购品目 = self.get_采购品目_一级()
        table = self.主表格
        search_box = self.page.get_by_placeholder('请输入关键字过滤').first
        info: Dict[str, List[str]] = {}

        for 品目 in 采购品目:
            search_box.fill(品目)
            search_box.press('Enter')
            self.page.locator(f"//div/span[text()='{品目}']").first.click()

            self.page.wait_for_timeout(1000)
            编码列表 = table.get_col_list('采购品目编码')[:numbers]

            if mode == 'Effective' and not 编码列表:
                continue
            info[品目] = 编码列表
        return info
