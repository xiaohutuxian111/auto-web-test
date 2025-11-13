from src.core import *
from src.core.base_page import PageObject


class Base项目立项(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.立项信息_tab = self.page.get_by_role("tab", name='立项信息', exact=True)
        self.采购项目专项_tab = self.page.get_by_role("tab", name='采购项目专项', exact=True)
        self.建设项目专项信息_tab = self.page.get_by_role("tab", name='建设项目专项信息', exact=True)
        self.科研项目专项信息_tab = self.page.get_by_role("tab", name='科研项目专项信息', exact=True)
        self.教学管理项目专项信息_tab = self.page.get_by_role("tab", name='教学管理项目专项信息', exact=True)
        self.项目专项信息_tab = self.page.get_by_role("tab", name='项目专项信息', exact=True)
        self.绩效目标_tab = self.page.get_by_role("tab", name='绩效目标', exact=True)
        self.预算明细_tab = self.page.get_by_role("tab", name='预算明细', exact=True)
        self.执行任务_tab = self.page.get_by_role("tab", name='执行任务', exact=True)
        self.验收标准_tab = self.page.get_by_role("tab", name='验收标准', exact=True)
        self.成果物_tab = self.page.get_by_role("tab", name='成果物', exact=True)
        self.附件材料_tab = self.page.get_by_role("tab", name='附件材料', exact=True)

    def fill_立项基本信息(self, 立项基本信息: Dict[str, str]):
        self.fill_快捷操作_填写表单(**立项基本信息)

    def fill_立项信息(self, 立项信息: Dict[str, str]):
        self.立项信息_tab.click()
        self.fill_快捷操作_填写表单(**立项信息)

    def fill_采购项目专项(self, temp_path, 采购项目专项: Dict[str, any]):
        if 采购项目专项:
            采购信息 = 采购项目专项.get('采购信息', {})
            购置明细 = 采购项目专项.get('购置明细', [])
            self.采购项目专项_tab.click()
            self.fill_快捷操作_填写表单(**采购信息)
            self.click_button('导入')
            with self.page.expect_download() as 购置明细导入模板:
                self.click_button("点击下载")
            购置明细导入模板.value.save_as(os.path.join(temp_path, 购置明细导入模板.value.suggested_filename))
            excel = ExcelUtil(os.path.join(temp_path, 购置明细导入模板.value.suggested_filename))

            excel.write_excel(sheet_name="导入模板", info_data=购置明细, skip_row=1)
            self.upload_file(os.path.join(temp_path, 购置明细导入模板.value.suggested_filename))

    def fill_建设项目专项信息(self, 建设项目专项信息: Dict[str, any]):
        if 建设项目专项信息:
            工程建设信息 = 建设项目专项信息.get('工程建设信息', {})
            施工区域及位置 = 建设项目专项信息.get('施工区域及位置', [])
            self.建设项目专项信息_tab.click()

            self.fill_快捷操作_填写表单(**工程建设信息)
            施工区域及位置_table = self.table('具体位置')
            for index, info in enumerate(施工区域及位置):
                self.page.locator("div[role='tabpanel'][aria-hidden='false']").get_by_text('新增').click()
                self.fill_快捷操作_填写表格(table=施工区域及位置_table, 行定位或行号=index,
                                            **info)

    def fill_科研项目专项信息(self, 科研项目专项信息: Dict[str, any]):
        if 科研项目专项信息:
            科研项目信息 = 科研项目专项信息.get('科研项目信息', {})
            项目负责人信息 = 科研项目专项信息.get('项目负责人信息', {})
            项目组成员 = 科研项目专项信息.get('项目组成员', [])
            self.科研项目专项信息_tab.click()
            self.fill_快捷操作_填写表单(**科研项目信息)
            self.fill_快捷操作_填写表单(**项目负责人信息)
            项目组成员信息_table = self.table('姓名')
            for index, info in enumerate(项目组成员):
                self.page.locator("div[role='tabpanel'][aria-hidden='false']").get_by_text('新增').click()
                self.fill_快捷操作_填写表格(table=项目组成员信息_table, 行定位或行号=index,
                                            **info)

    def fill_教学管理项目专项(self, 教学管理项目专项信息: Dict[str, any]):
        if 教学管理项目专项信息:
            主导人信息 = 教学管理项目专项信息.get('主导人信息', {})
            项目组成员信息 = 教学管理项目专项信息.get('项目组成员信息', [])
            立项依据和目标 = 教学管理项目专项信息.get('立项依据和目标', {})
            self.教学管理项目专项信息_tab.click()
            self.fill_快捷操作_填写表单(**主导人信息)
            项目组成员信息_table = self.table('姓名')
            for index, info in enumerate(项目组成员信息):
                self.page.locator("div[role='tabpanel'][aria-hidden='false']").get_by_text('新增').click()
                self.fill_快捷操作_填写表格(table=项目组成员信息_table, 行定位或行号=index,
                                            **info)
            self.fill_快捷操作_填写表单(**立项依据和目标)

    def fill_项目专项信息(self, 项目专项信息: Dict[str, Any]):
        if 项目专项信息:

            主导人信息 = 项目专项信息.get('主导人信息', {})
            项目组成员 = 项目专项信息.get('项目组成员', [])
            立项依据和目标 = 项目专项信息.get('立项依据和目标', {})

            self.项目专项信息_tab.click()
            self.fill_快捷操作_填写表单(**主导人信息)
            项目组成员_table = self.table('姓名')
            for index, info in enumerate(项目组成员):
                self.page.locator("div[role='tabpanel'][aria-hidden='false']").get_by_text('新增').click()
                self.fill_快捷操作_填写表格(table=项目组成员_table, 行定位或行号=index,
                                            **info)
            self.fill_快捷操作_填写表单(**立项依据和目标)

    def fill_绩效目标(self, 绩效目标: Dict[str, Any], years: int):
        if 绩效目标:
            本年度绩效目标 = 绩效目标.get('本年度绩效目标', {})
            长期绩效目标 = 绩效目标.get('长期绩效目标', {})
            产出指标 = 绩效目标.get('产出指标', [])
            效益指标 = 绩效目标.get('效益指标', [])
            满意度指标 = 绩效目标.get('满意度指标', [])
            指标库编码 = [*产出指标[:3], *效益指标[:3], *满意度指标[:3]]
            self.绩效目标_tab.click()
            self.fill_快捷操作_填写表单(**{'本年度绩效目标': 本年度绩效目标})
            self.locators.button_按钮('引入绩效指标', nth=-1).click()
            绩效指标选中_table = self.table('指标库编码')
            for code in 指标库编码:
                self.search_填写搜索框(placeholder='指标库编码/名称', 关键字=code)
                绩效指标选中_table.get_cell(0, 0).click()
            self.click_button('确定')
            if int(years) > 1:
                self.fill_快捷操作_填写表单(**{'长期绩效目标': 长期绩效目标})
                self.locators.button_按钮('引入绩效指标', nth=0).click()
                绩效指标选中_table = self.table('指标库编码')
                for code in 指标库编码:
                    self.search_填写搜索框(placeholder='指标库编码/名称', 关键字=code)
                    绩效指标选中_table.get_cell(0, 0).click()
                self.click_button('确定')

    def fill_预算明细(self, 项目立项方式: Literal['临时立项', '年度统一立项'], 预算明细: Dict[str, Any], years: int,
                      是否明确资金来源: str = '是'):
        if 预算明细:
            预算指标编码 = 预算明细.get('预算指标编码', [])
            资金来源 = 预算明细.get('资金来源', {})
            年度用款计划 = 预算明细.get('年度用款计划', {})

            self.预算明细_tab.click()
            if 项目立项方式 == '临时立项':
                资金来源info = {'是否明确资金来源': 是否明确资金来源}
                self.fill_快捷操作_填写表单(**资金来源info)
                if 是否明确资金来源 == '是':
                    关联指标_table = self.table('指标名称')
                    self.page.locator("div[role='tabpanel'][aria-hidden='false']").get_by_text('新增').click()
                    for index, code in enumerate(预算指标编码):
                        预算指标选择_table = self.table('预算事项名称')
                        self.search_填写搜索框(placeholder='预算指标编码/名称', 关键字=code)
                        预算指标选择_table.get_cell(0, 0).click()
                    self.click_button('确定')
                    row = 关联指标_table.get_col_list('指标名称')
                    for i in range(len(row)):
                        self.fill_快捷操作_填写表格(table=关联指标_table, 行定位或行号=i,
                                                    **{'申请金额（元）': str(random.randint(1, 10000))})
            self.fill_快捷操作_填写表单(**资金来源)

            for i in range(1, int(years) + 1):
                tab_name = f'第{i}年'
                self.page.get_by_role('tab', name=tab_name).click()
                项目预算明细_table = self.table('支出事项')
                rows = 项目预算明细_table.get_col_list('支出事项')
                for j in range(len(rows)):
                    info = {
                        '测算依据': faker_text(50),
                        '财政': str(random.randint(1, 100)),
                        '非财政': str(random.randint(1, 100)),
                        '科研': str(random.randint(1, 100)),
                        '人力': str(random.randint(1, 100)),
                    }
                    self.fill_快捷操作_填写表格(table=项目预算明细_table, 行定位或行号=j, **info)

            年度用款计划_table = self.table('第一季度用款计划')
            self.fill_快捷操作_填写表格(table=年度用款计划_table, 行定位或行号=0, **年度用款计划)

    def fill_执行任务(self, 执行任务: Dict[str, Any]):
        if 执行任务:
            项目计划分解 = 执行任务.get('项目计划分解', [])
            self.执行任务_tab.click()

            #  新增修改里程碑
            self.click_button('修改')
            项目任务阶段修改_table = self.table('任务阶段名称')
            任务阶段修改list = [计划['任务阶段'] for 计划 in 项目计划分解]
            for i, info in enumerate(任务阶段修改list):
                self.page.locator('.addBtn').get_by_text('新增').click()
                self.fill_快捷操作_填写表格(table=项目任务阶段修改_table, 行定位或行号=i, **{'任务阶段名称': info})
            # 删除多余行
            num = len(任务阶段修改list)
            操作_list = 项目任务阶段修改_table.get_col_list('操作', text=False)[num:]
            if len(操作_list) > 0:
                for _ in range(len(操作_list)):
                    项目任务阶段修改_table.get_cell('操作', num).get_by_role('button', name='删除').click()
                    self.confirm_弹框()
            self.page.locator('.el-dialog__footer').filter(visible=True).get_by_role('button',
                                                                                     name='保存').click()
            任务阶段_table = self.table('任务阶段')
            self.page.wait_for_timeout(500)
            for i, info in enumerate(项目计划分解):
                self.page.locator("div[role='tabpanel'][aria-hidden='false']").get_by_text('新增').filter(
                    visible=True).click()
                # todo 后续解决多层级table填充
                表格cell_td_任务名称 = 任务阶段_table.get_cell('任务名称', i)
                self.fill_快捷操作_填写表单(
                    default_value={表格cell_td_任务名称: info.get('任务阶段')})

                表格cell_td_任务内容 = 任务阶段_table.get_cell('任务内容', i)
                self.fill_快捷操作_填写表单(
                    default_value={表格cell_td_任务内容: info.get('任务名称')})

                表格cell_td_任务时间 = 任务阶段_table.get_cell('任务时间', i)
                self.fill_快捷操作_填写表单(
                    default_value={表格cell_td_任务时间: info.get('任务内容')})

                表格cell_td_任务工时 = 任务阶段_table.get_cell('任务工时', i)
                self.fill_快捷操作_填写表单(
                    default_value={表格cell_td_任务工时: info.get('任务时间')})

                表格cell_td_输出成果 = 任务阶段_table.get_cell('输出成果', i)
                self.fill_快捷操作_填写表单(
                    default_value={表格cell_td_输出成果: info.get('里程碑要求')})

    def fill_验收标准(self, 验收标准: Dict[str, Any]):
        if 验收标准:
            验收标准说明 = 验收标准.get('验收标准说明', {})
            验收信息 = 验收标准.get('验收信息', [])
            self.验收标准_tab.click()
            self.fill_快捷操作_填写表单(**验收标准说明)
            验收标准_table = self.table('验收项')
            for i, info in enumerate(验收信息):
                self.page.locator("div[role='tabpanel'][aria-hidden='false']").get_by_text('新增').filter(
                    visible=True).click()
                self.fill_快捷操作_填写表格(table=验收标准_table, 行定位或行号=i, **info)

    def fill_成果物(self, 成果物: Dict[str, Any]):
        if 成果物:
            self.成果物_tab.click()
            成果物说明, 成果物详情 = 成果物.get('成果物说明'), 成果物.get('成果物详情')

            self.fill_快捷操作_填写表单(**成果物说明)
            成果物_table = self.table('成果物名称')
            for i, info in enumerate(成果物详情):
                self.page.locator("div[role='tabpanel'][aria-hidden='false']").get_by_text('新增').click()
                self.fill_快捷操作_填写表格(table=成果物_table, 行定位或行号=i, **info)

    def fill_附件材料(self, temp_path: str = None):
        if temp_path:
            self.附件材料_tab.click()
            附件材料_table = self.table('附件类型名称')
            # file_types = 附件材料_table.get_cell('支持格式', 0).text_content().split(', ')
            # file_type = random.choice(file_types)
            # if file_type =='excel':
            #     file_type = 'xlsx'
            # 修改默认为pdf
            file_path = os.path.join(temp_path, f'test_upload.pdf')
            generate_formatted_file(file_type='pdf', file_path=file_path)
            upload_input = self.page.locator("input[type='file']")
            upload_input.last.set_input_files(file_path)

    def fill_项目立项tab信息(self, tab信息: Dict[str, any], year: int = None,
                             项目立项方式: Literal['临时立项', '年度统一立项'] = '年度统一立项', temp_path: str = None,
                             是否明确资金来源: str = '否'):
        立项信息 = tab信息.get('立项信息')
        self.fill_立项信息(立项信息)
        # 采购项目专项
        采购项目专项 = tab信息.get('采购项目专项')
        self.fill_采购项目专项(temp_path, 采购项目专项)

        # 建设项目专项信息
        建设项目专项信息 = tab信息.get('建设项目专项信息')
        self.fill_建设项目专项信息(建设项目专项信息)

        # 科研项目专项信息
        科研项目专项信息 = tab信息.get('科研项目专项信息')
        self.fill_科研项目专项信息(科研项目专项信息)

        # 教学管理项目专项信息
        教学管理项目专项信息 = tab信息.get('教学管理项目专项信息')
        self.fill_教学管理项目专项(教学管理项目专项信息)

        # 项目专项信息
        项目专项信息 = tab信息.get('项目专项信息')
        self.fill_项目专项信息(项目专项信息)

        # 绩效目标
        绩效目标 = tab信息.get('绩效目标')
        self.fill_绩效目标(绩效目标, year)

        # 预算明细
        预算明细 = tab信息.get('预算明细')
        self.fill_预算明细(项目立项方式, 预算明细, year, 是否明确资金来源)

        # 执行任务
        执行任务 = tab信息.get('执行任务')
        self.fill_执行任务(执行任务)

        # 验收标准
        验收标准 = tab信息.get('验收标准')
        self.fill_验收标准(验收标准)

        # 成果物
        成果物 = tab信息.get('成果物')
        self.fill_成果物(成果物)

        # 附件材料
        self.fill_附件材料(temp_path)
