from src.core import *
from src.core.base_page import PageObject


class 项目建议书页(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.url = "projectEarlyDoc/projectProposalList"
        self.新增_按钮 = self.locators.button_按钮('新增')

    def navigate(self):
        self.page.goto(self.url)

    @property
    def 主表格(self):
        return self.table('审批状态')

    def search_项目建议书(self, 查询信息: str):
        self.search_填写搜索框(placeholder='项目编码/项目名称', 关键字=查询信息)
        info = self.主表格.get_row_dict(0)
        return info

    def fill_项目建议书(self, 建议书信息: Dict[str, Any], temp_path: str):
        基本信息, 批文信息 = 建议书信息.get('基本信息'),建议书信息.get('批文信息')
        self.fill_快捷操作_填写表单(**基本信息)
        self.fill_快捷操作_填写表单(**批文信息)
        # 上传附件
        file_path = os.path.join(temp_path, f'test_upload.pdf')
        generate_formatted_file(file_type='pdf', file_path=file_path)
        upload_input = self.page.locator("input[type='file']")
        upload_input.last.set_input_files(file_path)
        self.click_button('提交')
        self.confirm_弹框()
