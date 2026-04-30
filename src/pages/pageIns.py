from src.pages import *

from src.core.base_page import PageObject
from src.pages.登录页 import 登录页
from src.pages.我的待办 import 我的待办
from src.pages.审批中心 import 审批中心
from src.pages.审批中心 import 审批详情


class PageInstance:
    登录页: 登录页 = 登录页
    我的待办: 我的待办 = 我的待办
    审批详情页: 审批详情 = 审批详情
    审批中心: 审批中心 = 审批中心

    def __init__(self, context: BrowserContext, log_dir=None, test_name=None):
        self.context = context
        self.log_dir = log_dir
        self.test_name = test_name
        self.previousPage = None

    def __getattribute__(self, item):
        # 通过obj的魔术方法获取attr
        attr = object.__getattribute__(self, item)

        # 如果页面没有实例化且attr是PageObject(basepage)的子类:
        if isinstance(attr, type) and issubclass(attr, PageObject):
            # 如果实例化对象没有page,则需要增加新的page,并且在持久化中会多出来一个未被实例化的page,需要关掉
            if not hasattr(self, "page"):
                if len(self.context.pages):
                    self.page = self.context.new_page()
                    self.context.pages[0].close()
                else:
                    self.page = self.context.new_page()
                # 这里是为了后面切换页面,保存一个初始值
                self.defaultPage = self.page
            # 通过attr对self.page进行实例化
            instance = attr(self.page)
            # 把实例化结果写入类属性,之后再进这里,会标记为已class,即isinstance(attr, type)的结果为False
            setattr(self, item, instance)
            # 返回instance是因为这次要使用
            return instance
        # 如果attr的type中包含po类的路径,并且当前调用方的page不是类中原来的page,说明我们要做切换:
        elif "class 'models." in str(type(attr)) and attr.page is not self.page:
            # 使用attr里已经有的__class__来调用实例化方法,对新的page进行相应的实例化:
            instance = attr.__class__(self.page)
            # 由于用不到attr了,删除节省内存
            del attr
            # 把实例化结果写入类属性
            setattr(self, item, instance)
            # 返回instance是因为这次要使用
            return instance
        # 如果上面条件都不满足,即判断已被实例化过且没有切换页面的操作,可直接使用
        return attr

    def 切换页面(
            self,
            page: Page = None,
            切换到上个页面: bool = False,
            要跳转的页面的title: str = None,
            关闭其它页面=False,
            关闭切换前页面=False,
    ):
        """
        共有四种用法:
        1. 不写入参,会切换到第一个打开的页面
        2. 填写目标page对象,会切换到目标页面
        3. 填写"切换到上个页面"为True时,会切换到上次切换的页面
        4. 填写"要跳转的页面的title",会切换到对应的页面
        :param page:
        :param 切换到上个页面:
        :param 要跳转的页面的title:
        :param 关闭其它页面:
        :param 关闭切换前页面:
        :return:
        """
        try:
            切换前页面title = self.page.title()
        except:
            切换前页面title = "哈哈哈哈哈都是假的"
        if page:
            # 兼容传入的是 PageInstance 的情况，解包为其内部的 Playwright Page
            self.previousPage = self.page
            self.page = page
        elif 切换到上个页面:
            current_page = self.page
            self.page = self.previousPage
            self.previousPage = current_page
        elif 要跳转的页面的title:
            pages = self.page.context.pages
            for page in pages:
                if page.title() == 要跳转的页面的title:
                    self.previousPage = self.page
                    self.page = page
                    break
        else:
            self.page = self.defaultPage
        if 关闭其它页面:
            self.page.wait_for_timeout(5_000)
            for page in self.page.context.pages.copy():
                if page != self.page:
                    page.close()
        if 关闭切换前页面:
            self.page.wait_for_timeout(5_000)
            for page in self.page.context.pages.copy():
                if page.title() == 切换前页面title:
                    page.close()
        try:
            self.page.bring_to_front()
        except:
            pass
