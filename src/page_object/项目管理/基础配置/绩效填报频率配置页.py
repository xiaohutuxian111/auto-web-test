from src.core.base_page import PageObject


class 绩效填报频率配置页(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.url = "basicConfiguration/submission"
        self.填报频率 = self.locators.表单项中包含操作元素的最上级div("填报频率")
        self.消息通知 = self.locators.表单项中包含操作元素的最上级div("消息通知")
        self.修改按钮 = (
            self.page.locator(".el-card__body").locator("button").get_by_text("修改")
        )
        self.保存按钮 = (
            self.page.locator(".el-card__body").locator("button").get_by_text("保存")
        )

    def navigate(self):
        """导航到绩效指标库页面"""
        self.page.goto(self.url)

    def 修改绩效填报频率配置(self, info_dict: dict):
        self.修改按钮.click()
        self.填报频率.click()
        self.page.get_by_role("option").locator("span").locator(
            "visible=true"
        ).get_by_text(info_dict["填报频率"], exact=True).click()
        self.消息通知.click()
        self.page.get_by_role("option").locator("span").locator(
            "visible=true"
        ).get_by_text(info_dict["消息通知"], exact=True).click()
        self.保存按钮.click()
        self.confirm_弹框()

    def get_配置信息(self):
        form_info = {}
        items = self.page.locator(".el-form-item").filter(visible=True)
        count = items.count()
        for i in range(count):
            label = (
                items.nth(i).locator(".el-form-item__label").inner_text().strip(" :")
            )
            value = items.nth(i).locator(".el-form-item__content").inner_text().strip()
            form_info[label] = value
        return form_info
