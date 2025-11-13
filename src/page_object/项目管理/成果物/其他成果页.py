from src.page_object import *
from src.core.base_page import PageObject


class 其他成果页(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.url = "achievements/otherResults"

    def navigate(self):
        self.page.goto(self.url)

    @property
    def 主表格(self):
        return self.table('成果登记号')

    def search_其他成果(self, 查询信息: str):
        self.search_填写搜索框(placeholder='成果名称/成果登记号', 关键字=查询信息)
        info = self.主表格.get_row_dict(0)
        return info

    def fill_其他成果(self, 其他信息: Dict[str, Any], temp_path: str):
        self.fill_快捷操作_填写表单(**其他信息)
        file_path = os.path.join(temp_path, f'test_upload.pdf')
        generate_formatted_file(file_type='pdf', file_path=file_path)
        upload_input = self.page.locator("input[type='file']")
        upload_input.last.set_input_files(file_path)
