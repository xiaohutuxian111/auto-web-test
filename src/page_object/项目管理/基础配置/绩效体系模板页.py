from src.page_object import *
from src.core.base_page import PageObject


class 绩效体系模板页(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.项目管理_URL = 'projectPortal/leaderShow?sign=project'
        self.url = "basicConfiguration/performanceTemplates"

        # 常用按钮
        self.导入按钮 = self.locators.button_按钮('导入')
        self.导出按钮 = self.locators.button_按钮('导出')
        self.新增按钮 = self.locators.button_按钮('新增')
        self.引入绩效指标库 = self.locators.button_按钮('引入绩效指标库')

        # 输入框
        self.查询输入框 = self.page.get_by_placeholder('模版名称')

        # 分页信息
        self.分页总数 = self.page.locator('span.el-pagination__total.is-first')

    @property
    def 主表格(self):
        return self.table("指标库编码")

    def navigate(self):
        """进入绩效体系模板页"""
        self.page.goto(self.url)

    def fill_绩效模板基础信息(self, 基本信息: Dict[str, str]):
        """填写绩效模板基础信息表单"""
        self.fill_快捷操作_填写表单(**基本信息)


    def fill_引入绩效指标(self, 绩效指标info: List[str]):
        """引入绩效指标库中的指标"""
        指标导入Table = Table(self.page, '指标库编码')
        for 指标 in 绩效指标info:
            self.search_填写搜索框(placeholder='资金用途', 关键字=指标)
            指标导入Table.get_cell(0, 0).locator('//span[@class="el-checkbox__input"]').click()
        self.click_button('确认')

    def fill_页面指标table信息(self, 页面新增绩效指标: Dict[str, str]):
        """在页面指标表格中填写数据"""
        table = Table(self.page, '是否必填')
        rows = len(table.get_col_list('是否必填'))

        if rows == 0:
            raise ValueError("页面指标表格为空，无法填写数据")

        # 填充最后一行
        self.fill_快捷操作_填写表格(table=table, 行定位或行号=rows - 1, **页面新增绩效指标)

        # 填充是否必填
        for i in range(rows):
            self.fill_快捷操作_填写表格(table=table, 行定位或行号=i, **{'是否必填': random.choice(['是', '否'])})

    def fill_页面指标(self ,指标信息: List[Dict[str, str]]):
        table = Table(self.page, '是否必填')
        for i,info  in enumerate(指标信息):
            self.fill_快捷操作_填写表格(table=table, 行定位或行号=i ,**info)
            if  i < len(指标信息)-1:
                self.click_button('新增')



    def 开启or禁用_绩效模板(self, 项目名: str, status: Literal['禁用', '启用']):
        """启用或禁用指定绩效模板"""
        self.search_填写搜索框(placeholder='模版名称', 关键字=项目名)
        cards = self.page.locator("div.el-card.box-card")

        if cards.count() == 0:
            raise ValueError(f"未找到模板：{项目名}")

        # 点击操作按钮
        cards.nth(0).get_by_role('button').click()
        self.page.get_by_role('menuitem', name=status).click()
        self.confirm_弹框()

    def delete_table_last(self):
        """删除表格最后一行"""
        self.page.wait_for_timeout(1_000)
        table = Table(self.page, '是否必填')
        rows = len(table.get_col_list('是否必填'))
        loc = table.get_cell('操作', rows-1)
        loc.get_by_text('删除').click()
        self.confirm_弹框()

    def 项目类型_树形查询(self, 节点名称: str, timeout: int = 5000):
        """选择树形结构中的节点"""
        self.page.locator(".el-tree-node__label").get_by_text(节点名称, exact=True).click(timeout=timeout)

    def 获取卡片模板信息(self, card_name: str = None, status: str = None):
        """获取页面卡片信息，可按名称和状态过滤"""
        template_list = []
        cards = self.page.locator("div.el-card.box-card")

        for i in range(cards.count()):
            card = cards.nth(i)

            # 名称
            name = card.locator(".el-card__header .node-label").inner_text()

            # 数据项
            cells = card.locator(".el-card__body .el-descriptions__cell.is-bordered")
            cell_texts = [cells.nth(j).inner_text().strip() for j in range(cells.count())]

            data = {
                "名称": name,
                "编码": cell_texts[0] if len(cell_texts) > 0 else "",
                "项目类型": cell_texts[1] if len(cell_texts) > 1 else "",
                "申报人": cell_texts[2] if len(cell_texts) > 2 else "",
                "申报部门": cell_texts[3] if len(cell_texts) > 3 else "",
                "更新时间": cell_texts[4] if len(cell_texts) > 4 else "",
                "状态": card.locator(".el-tag").inner_text().strip()
            }
            template_list.append(data)

        if card_name:
            template_list = [card for card in template_list if card_name in card['名称']]
        if status:
            template_list = [card for card in template_list if card['状态'] == status]

        return template_list

    @staticmethod
    def assert_card_status(cards: list, expected_status: str):
        """
        校验卡片状态并提供更直观的断言信息
        """
        assert cards, "没有找到任何模板卡片"
        actual_status = cards[0].get('状态')
        assert actual_status == expected_status, f"预期状态 {expected_status}，实际为 {actual_status}"
