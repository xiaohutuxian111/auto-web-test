from src.page_object import *
from src.core.base_page import PageObject


class 奖励证书页(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.url = "achievements/awardCertificateList"
        self.新增_按钮 = self.locators.button_按钮('新增')

    def navigate(self):
        self.page.goto(self.url)

    @property
    def 主表格(self):
        return self.table('课题名称')

    def search_奖励证书(self, 查询信息: str):
        self.search_填写搜索框(placeholder='项目名称/课程名称', 关键字=查询信息)
        info = self.主表格.get_row_dict(0)
        return info

    def fill_奖励证书(self, 奖励证书: Dict[str, str]):
        self.fill_快捷操作_填写表单(**奖励证书)
