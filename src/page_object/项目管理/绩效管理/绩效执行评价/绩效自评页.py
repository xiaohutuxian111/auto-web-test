from src.page_object import *
from src.core.base_page import PageObject
from src.test_cases.项目管理.绩效管理.conftest import split_score_integer


class 绩效自评页(PageObject):
    """绩效自评"""

    def __init__(self, page):
        super().__init__(page)
        self.url = "performance/selfEval/projectPerformanceSelfEval"

    def navigate(self) -> None:
        self.page.goto(self.url)

    def fill_绩效自评(self, loc: Locator, temp_path: str):

        loc.click()
        # 填报数据
        table = Table(self.page, '实际完成情况')
        table.get_cell('实际完成情况', 0).fill(faker_text(50))

        指标_table = Table(self.page, '偏差分析原因')
        rows = 指标_table.get_col_list('指标单位')
        scores = split_score_integer(len(rows))
        for index in range(len(rows)):
            info = {
                '实际完成值': faker_随机数生成(2),
                '指标总分': scores[index],
                '得分': str(int(scores[index] * 0.8)),
                '偏差分析原因': faker_text(50),
            }
            self.fill_快捷操作_填写表格(table=指标_table, 行定位或行号=index, **info)
            上传按钮 = 指标_table.get_cell('佐证材料', index).get_by_role('button', name='上传')
            上传按钮.click()
            self.upload_random_file(temp_path)
        self.click_button('提交')

    def 获取卡片定位(self, 查询关键字: str = None,
                     卡片状态: Literal['未开始', '待填报', '审批中', '已审批'] = '待填报') -> List[
        Locator]:
        if 查询关键字:
            self.search_填写搜索框(placeholder='项目名称', 关键字=查询关键字)
        cards_loc = self.page.locator('.el-card .is-always-shadow').filter(visible=True).all()
        ans_loc = []
        for card in cards_loc:
            status = card.locator('.card-status').inner_text(),
            if 卡片状态 in status:
                ans_loc.append(card)
        return ans_loc
