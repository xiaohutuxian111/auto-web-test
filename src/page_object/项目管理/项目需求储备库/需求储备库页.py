from src.page_object import *
from src.page_object.项目管理.项目需求储备库 import Base需求页


class 需求储备库页(Base需求页):
    def __init__(self, page):
        super().__init__(page)
        self.url = "projectStore/requirementRepository"
        self.新增_按钮 = self.locators.button_按钮('合并')
        self.需求储备_tab = self.page.get_by_role("tab", name='储备需求', exact=True)
        self.被合并需求_tab = self.page.get_by_role("tab", name='被合并需求', exact=True)
        self.合并按钮 = self.locators.button_按钮('合并')

    def navigate(self):
        self.page.goto(self.url)

    @property
    def 主表格(self):
        return self.table('需求编码')

    def search_需求(self, 关键字: str):
        self.search_填写搜索框(placeholder="需求编号/需求名称", 关键字=关键字)
        table = self.主表格
        info = table.get_row_dict(0)
        return info

    def set_需求主次(self, 需求编号: List[str]):
        self.合并按钮.click()
        tabel = Table(self.page, '需求名称', 表格序号=1)
        for 编号 in 需求编号:
            self.search_填写搜索框(placeholder='需求编码/名称', 关键字=编号)
            tabel.get_cell(0, 0).locator('.el-checkbox__input').first.click()
        tabel1 = Table(self.page, '操作')
        # 设为主要
        tabel1.get_cell('操作', 需求编号[0]).get_by_role('button', name='设为主要').click()

        self.click_button('确定')

    def fill_合并_采购类专项信息(self, 采购类专项信息: Dict[str, Any]):
        """
         这个页面元素与其他不重用！！！！
        """

        self.采购类专项信息_tab.click()
        # TDOO 单独定位
        采购组织方式_loc = self.page.locator("label,.required-label").filter(visible=True).filter(
            has=self.page.get_by_text('采购组织方式')).locator(
            self.page.locator(f"xpath=/following::*[position()=1]")).first
        采购组织方式_loc.click()
        start = time.time()
        while time.time() - start < 2:
            loc = self.page.locator('.el-select-dropdown__item').filter(visible=True).get_by_text('不限')
            if loc.count() > 0:
                loc.click()
                return
            time.sleep(0.2)

        pass
        # 采购信息, 采购明细 = 采购类专项信息['采购信息'], 采购类专项信息['采购明细']
        # self.fill_快捷操作_填写表单(**采购信息)
        # # 添加采购数目
        # table = Table(self.page, '采购品目编码')
        # rows = len(table.get_col_list('采购品目编码'))
        # for i in range(rows):
        #     info = {
        #         '规格型号': faker_产品型号(),
        #         '计量单位': faker_单位(),
        #         '采购数量': str(faker_随机数生成(2)),
        #         '预算单价': str(faker_随机数生成(2)),
        #         '备注': faker_text(10)
        #     }
        #     self.fill_快捷操作_填写表格(table=table, 行定位或行号=i, **info)

    def fill_合并_建设工程类专项信息(self):
        self.建设工程类专项信息_tab.click()
        # self.fill_快捷操作_填写表单(**建设工程类专项信息)
        pass

    def fill_合并_教学管理类专项信息(self):
        self.教学管理类专项信息_tab.click()
        # self.fill_快捷操作_填写表单(**教学管理类专项信息)
        pass

    def fill_合并_科研项目类专项信息(self):
        self.科研项目类专项信息_tab.click()
        # self.fill_快捷操作_填写表单(**科研项目类专项信息)
        pass

    def fill_合并_预算明细(self):
        self.预算明细_tab.click()

        # self.fill_快捷操作_填写表单(**资金来源)
        # table = Table(self.page, '支出事项')
        # 标题事项 = 资金来源['资金来源'].split('&&')
        # rows = len(table.get_col_list('支出事项'))
        # for i in range(rows):
        #     info = {}
        #     for 事项 in 标题事项:
        #         info[事项] = str(faker_随机数生成(3))
        #     info['测算依据'] = faker_text(20)
        #     self.fill_快捷操作_填写表格(table, 行定位或行号=i, **info)
        pass
