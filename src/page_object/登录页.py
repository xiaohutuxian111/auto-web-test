from src.page_object import *
from src.core.base_page import PageObject


class 登录页(PageObject):
    def __init__(self, page):
        """
        初始化登录页面
        """
        super().__init__(page)
        self.url = "login"
        # 页面元素定位
        self.department_input = self.page.get_by_placeholder("请输入租户标识")
        self.username_input = self.page.get_by_placeholder("请输入用户名")
        self.password_input = self.page.get_by_placeholder("请输入密码")
        self.帮助中心 = self.page.get_by_text('帮助中心')
        self.login_button = self.locators.button_按钮('登录')
        self.error_message = self.page.locator(".ant-form-item-explain-error")

    def navigate(self):
        self.page.goto(self.url)

    def login_页面登录(self, department: str, username: str, password: str, expect_success: bool = True) -> bool:
        self.navigate()
        self.department_input.fill(department)
        self.username_input.fill(username)
        self.password_input.fill(str(password))
        self.login_button.click()

        if expect_success:
            # 等待登录成功，检查是否跳转到工作台页面
            self.page.wait_for_url("**/root/index", timeout=30_000)
            return True
        else:
            # 等待错误信息出现
            self.error_message.wait_for(timeout=5_000)
            return False


