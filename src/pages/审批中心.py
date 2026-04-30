from src.pages import *
from src.core.base_page import PageObject


class 审批中心(PageObject):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.page = page
        self.url = 'workflow/task/audit?activeTab=todo&sign=workflow'
        self.待办任务_tab = self.page.get_by_role('tab', name='待办任务')
        self.已办任务_tab = self.page.get_by_role('tab', name='已办任务')
        self.我创建的_tab = self.page.get_by_role('tab', name='我创建的')
        self.待办任务_search = self.page.get_by_placeholder('流程名称/任务名称')
        self.我创建的_search = self.page.get_by_placeholder('请输入流程名称')
        self.待办任务_批量审批_按钮 = self.locators.button_按钮('批量审批')

    def navigate(self):
        self.page.goto(self.url)

    def get_待办任务(self, 单据: str, 关键字: str = None):
        """
        当前关键字为用户名来区分流程
        """
        self.待办任务_tab.click()
        待办任务_table = Table(self.page, 唯一文字='流程名称')
        self.search_填写搜索框(placeholder='流程名称/任务名称', 关键字=单据)

        with self.page.expect_popup() as popup_info:
            待办任务_table.get_cell('操作', 关键字).get_by_text('办理').click()
        return 审批详情(popup_info.value)

    def get_已办任务(self, 单据: str):
        pass

    def get_我创建的(self, 单据: str):
        pass


class 审批详情(PageObject):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.page = page
        self.审批意见输入框 = self.page.get_by_placeholder('请输入审批意见')

    @allure.step("执行审批操作")
    def 执行审批操作(self, 审批意见: str, 按钮名称: str):
        self.审批意见输入框.fill(审批意见)
        self.page.evaluate("document.body.style.zoom = '80%'")
        self.click_button(按钮名称)
        self.confirm_弹框()

    @allure.step("执行驳回操作")
    def 执行驳回(self, 节点名称: str, 审批意见: str):
        self.审批意见输入框.fill(审批意见)
        self.locators.button_按钮('驳回').click()
        self.page.get_by_role("dialog").get_by_text(节点名称).click()
        self.locators.button_按钮('确定').click()

    @allure.step("执行转交操作")
    def 执行转交(self, 转交人: str, 转交人类型: str, 审批意见: str):
        self.审批意见输入框.fill(审批意见)
        self.locators.button_按钮('转交').click()
        self.page.get_by_role("dialog").get_by_placeholder(f"请输入{转交人类型}").fill(转交人)
        self.locators.button_按钮('确定').click()

    @allure.step("执行加签/加审/抄送操作")
    def 执行加签加审抄送(self, 类型: str, 人员, 审批意见: str):
        self.审批意见输入框.fill(审批意见)
        self.locators.button_按钮(类型).click()
        # TODO: 根据你的 UI 选择人员，这里略
        self.locators.button_按钮('确定').click()

    @allure.step("执行指定下一审批人操作")
    def 执行指定下一审批人(self, 下一节点审批人: str, 审批任务来源: str, 意见: str):
        self.审批意见输入框.fill(意见)
        self.locators.button_按钮('指定下一审批人').click()
        # TODO: 根据 UI 选择人/来源
        self.locators.button_按钮('确定').click()
