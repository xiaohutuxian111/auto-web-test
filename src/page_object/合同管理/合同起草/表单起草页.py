from src.core.base_page import PageObject
from src.core.table import Table


class 表单起草_类(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.合同管理_URL = 'home/dashboard?sign=contract'
        self.url = 'drafting/form'

        self.请选择合同起草的类型_输入框 = self.page.get_by_placeholder('类型名称')
        self.合同起草类型树根节点 = self.page.get_by_role('tree')
        self.上传文件框 = self.page.get_by_text('点击或将文件拖拽到这里上传')
        self.我的合同起草按钮 = self.locators.button_按钮('我的合同起草')
        self.手动填写表单发起 = self.page.get_by_text('手动填写表单发起')

    def navigate(self):
        """导航到绩效指标库页面"""
        self.page.goto(self.合同管理_URL)
        self.page.goto(self.url)
        self.page.wait_for_load_state("networkidle")

    def 选择合同起草类型(self, 合同类型: str):
        self.请选择合同起草的类型_输入框.fill(合同类型)
        self.合同起草类型树根节点.locator(f".node-label:has-text('{合同类型}'):visible").click()
        self.page.wait_for_load_state("networkidle")

    def 填写基本信息(self, base_info: dict, executive_department_info: str):
        基本信息表单定位 = self.page.locator(".card-title:has-text('基本信息') + .el-form")
        self.快捷操作_填写表单_增加根据数据类确定唯一表单(基本信息表单定位, **base_info)
        #  点击执行部门输入框
        self.page.locator("label:has-text('执行部门') + div").click()
        self.page.wait_for_load_state("networkidle")
        self.__填写执行部门(executive_department_info)

    def 关联前置信息(self, purchase_order: str):
        # 采购订单定位 = self.page.locator()
        # 采购订单定位.fill(purchase_order)
        pass

    def 关联预算信息(self, budget_info: dict):
        pass

    def 填写合同清单信息(self, contracts_list_info: dict):
        pass

    def 签约主体信息(self, subject_info: dict):
        pass

    def 填写合同阶段信息(self, contracts_stage_info):
        table = Table(self.page, 唯一文字='合同约定任务')

    def 上传文件(self, 文件路径: str):
        with self.page.expect_file_chooser() as fc_info:
            self.上传文件框.click()
        file_chooser = fc_info.value
        file_chooser.set_files(文件路径)

    def __填写执行部门(self, executive_department_info: str):
        # TODO 后续是否要添加通过机构部门类型 查询部门
        self.机构部门类型_类型名称查询框 = self.page.get_by_placeholder('类型名称')

        self.机构部门类型_根节点 = self.page.get_by_role('tree')
        self.部门名称_查询框 = self.page.get_by_placeholder('部门名称')

        self.部门名称_查询框.fill(executive_department_info)
        self.部门名称_查询框.press('Enter')

        部门table = Table(self.page, 唯一文字='筛选')
        # 选中部门
        depart_lis = 部门table.get_col_list('部门编号')
        if len(depart_lis) == 0:
            raise f"查询部门{executive_department_info}不存在,请检查"
        部门table.get_cell('筛选', 0).locator('.el-radio__inner').click()
        self.locators.button_按钮('确认').click()
