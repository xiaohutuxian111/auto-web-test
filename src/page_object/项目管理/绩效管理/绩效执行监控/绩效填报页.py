from src.page_object import *
from src.core.base_page import PageObject


class 绩效填报页(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.url = "performance/monitoring/fill/manage"

    def navigate(self) -> None:
        """导航到绩效指标库页面"""
        self.page.goto(self.url)

    def select_财政项目(self, 项目名称: str) -> None:
        """选择财政项目"""
        self.page.get_by_placeholder('项目名称').fill(项目名称)
        self.page.locator(f".tree-node:has-text('{项目名称}')").filter(visible=True).first.click()

    def 获取卡片定位(self, 查询关键字: str = None,
                     卡片状态: Literal['未开始', '待提交', '审批中', '已审批'] = '待提交') -> List[
        Locator]:
        if 查询关键字:
            self.search_填写搜索框(placeholder='项目编码', 关键字=查询关键字)
        cards_loc = self.page.locator('.el-card .is-always-shadow').filter(visible=True).all()
        ans_loc = []
        for card in cards_loc:
            status = card.locator('.card-status').inner_text(),
            if 卡片状态 in status:
                ans_loc.append(card)
        return ans_loc

    def fill_绩效填报(self, card_loc: Locator, 绩效填报: Dict[str, Any], tmp_path: str):
        资金到位情况, 资金支付进度, 绩效运行监控结论与建议 = 绩效填报.get('资金到位情况', {}), 绩效填报.get(
            '资金支付进度', {}), 绩效填报.get(
            '绩效运行监控结论与建议', {})
        card_loc.locator(".el-dropdown").click()
        self.page.get_by_role('menuitem', name='填报', exact=True).filter(visible=True).click()
        self.fill_快捷操作_填写表单(**资金到位情况)
        # self.fill_快捷操作_填写表单(**资金支付进度)
        # 佐证材料上传
        self.upload_random_file(tmp_path, locator_index=0)
        # 绩效目标完成情况
        self.fill_绩效目标表格()
        # 绩效运行监控结论与建议
        self.fill_快捷操作_填写表单(**绩效运行监控结论与建议)
        self.upload_random_file(tmp_path, locator_index=-1)
        self.click_button('提交')
        self.confirm_弹框()

    # def _勾选复选框(self, 文本列表: list):
    #     for 文本 in 文本列表:
    #         label = self.page.locator(f"label:has-text('{文本}')")
    #         if label.count() > 0:
    #             checkbox_input = label.locator("input[type=checkbox]")
    #             if not checkbox_input.is_checked():
    #                 label.click()

    def fill_绩效目标表格(self):
        table = Table(self.page, 唯一文字='完成目标可能性')
        rows = len(table.get_col_list('完成目标可能性'))
        for i in range(rows):
            row_info = {'监控期间执行情况': faker_text(50),
                        '全年预计完成情况': faker_text(50),
                        '完成目标可能性': random.choice(['确定能', '有可能', '不可能']),
                        '偏差分析原因': faker_text(30)}
            self.fill_快捷操作_填写表格(table=table, 行定位或行号=i, **row_info)

    def get_card_by_field(self, 字段: str, 值: str, first_only: bool = True) -> list[Locator]:
        """根据字段和值查找卡片"""
        result = []
        cards_loc = self.page.locator('.el-card .is-always-shadow').filter(visible=True).all()
        for card in cards_loc:
            if 字段 == "名称":
                field_value = card.locator('.card-title').inner_text()
            elif 字段 == "状态":
                field_value = card.locator('.card-status').inner_text()
            else:
                field_value = card.locator(
                    f'xpath=.//span[@class="label" and contains(text(), "{字段}")]/following-sibling::span').text_content()
            if field_value and 值 in field_value:
                result.append(card)
                if first_only:
                    break
        return result
