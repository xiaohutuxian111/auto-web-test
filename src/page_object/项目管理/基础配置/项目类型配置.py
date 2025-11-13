from src.page_object import *
from src.core.base_page import PageObject


class 项目类型配置页(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.url = "basicConfiguration/projectType"
        self.导入按钮 = self.locators.button_按钮('导入')
        self.项目类型_新增 = self.page.locator(
            "//div[@class='custom-tree-node'][.//span[text()='项目类型']]//div[@class='more-icon']")

    def navigate(self):
        """导航到绩效指标库页面"""
        self.page.goto(self.url)

    @property
    def 主表格(self):
        return self.table("是否分层级项目")

    def 选中左侧树节点(self, 节点名称: str):
        节点定位 = self.page.locator('.tree-scroll-container').get_by_text(节点名称)
        if 节点定位.count() == 1:
            节点定位.click()

    def add_添加子级(self):
        self.项目类型_新增.click()
        self.page.locator("div.context-menu-content >> div.menu-item", has_text="添加子级").click()

    def fill_基本信息(self, 基本信息: Dict[str, str]):
        self.fill_快捷操作_填写表单(**基本信息)

    def fill_项目管理流程(self, 项目管理流程_info: List[Dict[str, str]]):
        管理流程_table = Table(self.page, '项目总预算下限金额（万元）')
        for index, info in enumerate(项目管理流程_info):
            self.fill_快捷操作_填写表格(table=管理流程_table, 行定位或行号=index, **info)

    def fill_项目任务阶段创建(self, 项目任务阶段创建_info: List[Dict[str, str]]):
        项目任务阶段创建_table = Table(self.page, '务阶段名称')
        for index, info in enumerate(项目任务阶段创建_info):
            self.fill_快捷操作_填写表格(table=项目任务阶段创建_table, 行定位或行号=index, **info)
            # 点击新增,最后一行不用新增
            if index < len(项目任务阶段创建_info) - 1:
                self.page.locator("div.el-card__body", has_text='项目任务阶段创建').get_by_role('button',
                                                                                                name='新增').click()

    def fill_附件类型配置(self, 附件类型配置_info: List[Dict[str, str]]):
        附件类型配置_tabel = Table(self.page, '附件类型名称')
        for index, info in enumerate(附件类型配置_info):
            self.fill_快捷操作_填写表格(table=附件类型配置_tabel, 行定位或行号=index, **info)
            # 点击新增
            if index < len(附件类型配置_info) - 1:
                self.page.locator("div.el-card__body", has_text='附件类型配置').get_by_role('button',
                                                                                            name='新增').click()

