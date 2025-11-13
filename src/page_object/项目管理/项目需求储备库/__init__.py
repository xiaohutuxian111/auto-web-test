from src.page_object import *
from src.core.base_page import PageObject


class Base需求页(PageObject):
    """需求相关页面基类，封装通用的表单/表格/附件操作"""

    def __init__(self, page):
        super().__init__(page)
        self.需求详情_tab = self.page.get_by_role("tab", name='需求详情', exact=True)
        self.采购类专项信息_tab = self.page.get_by_role("tab", name='采购类专项信息', exact=True)
        self.建设工程类专项信息_tab = self.page.get_by_role("tab", name='建设工程类专项信息', exact=True)
        self.教学管理类专项信息_tab = self.page.get_by_role("tab", name='教学管理类专项信息', exact=True)
        self.科研项目类专项信息_tab = self.page.get_by_role("tab", name='科研项目类专项信息', exact=True)
        self.预算明细_tab = self.page.get_by_role("tab", name='预算明细', exact=True)
        self.需求附件_tab = self.page.get_by_role("tab", name='需求附件', exact=True)


    def fill_基本信息(self, 基本信息: Dict[str, str]):
        self.fill_快捷操作_填写表单(**基本信息)

    def fill_需求详情(self, 需求详情: Dict[str, str]):
        if 需求详情:
            logger.info(f"填写需求详情:{需求详情}")
            self.需求详情_tab.click()
            self.fill_快捷操作_填写表单(**需求详情)

    def fill_采购类专项信息(self, 采购类专项信息: Dict[str, Any]):
        if 采购类专项信息:
            logger.info(f"填写采购类专项信息:{采购类专项信息}")
            self.采购类专项信息_tab.click()
            采购信息, 采购明细 = 采购类专项信息['采购信息'], 采购类专项信息['采购明细']
            self.fill_快捷操作_填写表单(**采购信息)
            # TODO 后续将层级选择封装
            self.page.locator('//button[@type="button"]//span[contains(text(),"新增")]').click()
            table = Table(self.page, '资产字典编码', 表格序号=0)
            for index, code in enumerate(采购明细):
                self.search_填写搜索框(placeholder='项目编码/名称', 关键字=code)
                self.page.wait_for_timeout(5_00)
                loc = table.get_cell(0, 0).first.locator('.el-checkbox__inner')
                if loc.is_checked():
                    continue
                loc.click()
            self.click_button('确定')
            #  填充表格其他信息
            table_main = Table(self.page, '采购品目名称')
            rows = len(table_main.get_col_list('采购品目名称'))
            for i in range(rows):
                info = {
                    '规格型号':faker_产品型号(),
                    '计量单位': faker_单位(),
                    '采购数量': str(random.randint(1, 100)),
                    '预算单价': str(random.randint(1, 50)),
                    '备注': faker_text(50)
                }
                self.fill_快捷操作_填写表格(table_main, i, **info)

    def fill_建设工程类专项信息(self, 建设工程类专项信息: Dict[str, Any]):
        if 建设工程类专项信息:
            logger.info(f"填写建设工程类专项信息:{建设工程类专项信息}")
            self.建设工程类专项信息_tab.click()
            self.fill_快捷操作_填写表单(**建设工程类专项信息)

    def fill_教学管理类专项信息(self, 教学管理类专项信息: Dict[str, Any]):
        if 教学管理类专项信息:
            logger.info(f"填写教学管理类专项信息:{教学管理类专项信息}")
            self.教学管理类专项信息_tab.click()
            self.fill_快捷操作_填写表单(**教学管理类专项信息)

    def fill_科研项目类专项信息(self, 科研项目类专项信息: Dict[str, Any]):
        if 科研项目类专项信息:
            logger.info(f"填写科研项目类专项信息:{科研项目类专项信息}")
            self.科研项目类专项信息_tab.click()
            self.fill_快捷操作_填写表单(**科研项目类专项信息)

    def fill_预算明细(self, 资金来源: Dict[str, str]):
        if 资金来源:
            logger.info(f"填写预算明细:{资金来源}")
            self.预算明细_tab.click()

            self.fill_快捷操作_填写表单(**资金来源)
            table = Table(self.page, '支出事项')
            标题事项 = 资金来源['资金来源'].split('&&')
            rows = len(table.get_col_list('支出事项'))
            for i in range(rows):
                info = {}
                for 事项 in 标题事项:
                    info[事项] = str(faker_随机数生成(3))
                info['测算依据'] = faker_text(20)
                self.fill_快捷操作_填写表格(table, 行定位或行号=i, **info)

    def fill_需求附件(self, temp_path=None):
        if temp_path:
            logger.info("上传需求附件")
            self.需求附件_tab.click()
            file_path = os.path.join(temp_path, f'test_upload_{faker_随机数生成(3)}.pdf')
            generate_formatted_file(file_type='pdf', file_path=file_path)
            upload_input = self.page.locator("input[type='file']")
            upload_input.last.set_input_files(file_path)

    def fill_整体填报(self, 需求表单信息: Dict[str, any], temp_path: str = None):
        基本信息 = 需求表单信息.get('基本信息', {})
        需求详情 = 需求表单信息.get('需求详情', {})
        采购类专项信息 = 需求表单信息.get('采购类专项信息', {})
        建设工程类专项信息 = 需求表单信息.get('建设工程类专项信息', {})
        教学管理类专项信息 = 需求表单信息.get('教学管理类专项信息', {})
        科研项目类专项信息 = 需求表单信息.get('科研项目类专项信息', {})
        预算明细 = 需求表单信息.get('预算明细', {})
        self.fill_基本信息(基本信息)
        self.fill_需求详情(需求详情)
        self.fill_采购类专项信息(采购类专项信息)
        self.fill_建设工程类专项信息(建设工程类专项信息)
        self.fill_教学管理类专项信息(教学管理类专项信息)
        self.fill_科研项目类专项信息(科研项目类专项信息)
        self.fill_预算明细(预算明细)
        self.fill_需求附件(temp_path)
