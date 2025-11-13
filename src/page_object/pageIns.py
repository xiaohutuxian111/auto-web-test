from src.page_object import *

from src.core.base_page import PageObject
from src.page_object.登录页 import 登录页
from src.page_object.我的待办 import 我的待办
from src.page_object.审批中心 import 审批中心
from src.page_object.审批中心 import 审批详情

from src.page_object.项目管理.基础配置.专项项目层级配置页 import 专项项目层级配置页
from src.page_object.项目管理.基础配置.绩效体系模板页 import 绩效体系模板页
from src.page_object.项目管理.基础配置.绩效填报频率配置页 import 绩效填报频率配置页
from src.page_object.项目管理.基础配置.绩效指标库页 import 绩效指标库页
from src.page_object.项目管理.基础配置.采购品目配置页 import 采购品目配置页

# 基础配置
from src.page_object.项目管理.基础配置.需求类型配置页 import 需求类型配置页
from src.page_object.项目管理.基础配置.项目类型配置 import 项目类型配置页

# 成果物
from src.page_object.项目管理.成果物.专著编书页 import 专著编书页
from src.page_object.项目管理.成果物.奖励证书页 import 奖励证书页
from src.page_object.项目管理.成果物.专利成果页 import 专利成果页
from src.page_object.项目管理.成果物.论文成果页 import 论文成果页
from src.page_object.项目管理.成果物.其他成果页 import 其他成果页

from src.page_object.项目管理.绩效管理.绩效执行监控.绩效填报页 import 绩效填报页
from src.page_object.项目管理.绩效管理.绩效执行监控.绩效汇总页 import 绩效汇总页
from src.page_object.项目管理.绩效管理.绩效执行评价.绩效自评页 import 绩效自评页
from src.page_object.项目管理.绩效管理.绩效执行评价.自评汇总页 import 自评汇总页
from src.page_object.项目管理.绩效管理.绩效整改管理.整改下发页 import 整改下发页
from src.page_object.项目管理.绩效管理.绩效整改管理.整改反馈页 import 整改反馈页

# 绩效管理模块
from src.page_object.项目管理.绩效管理.项目绩效申报页 import 项目绩效申报页
from src.page_object.项目管理.项目前期文档.项目可行性性研究报告页 import 项目可行性性研究报告页

# 项目前期文档
from src.page_object.项目管理.项目前期文档.项目建议书页 import 项目建议书页
from src.page_object.项目管理.项目前期文档.项目概算页 import 项目概算页

#  项目库管理工作台
from src.page_object.项目管理.项目库管理工作台.领导工作台页 import 领导工作台页
from src.page_object.项目管理.项目执行.重大项目进展填报页 import 重大项目进展填报页

# 项目执行
from src.page_object.项目管理.项目执行.项目任务分解页 import 项目任务分解页
from src.page_object.项目管理.项目执行.我的任务页 import 我的任务页
from src.page_object.项目管理.项目执行.项目变更页 import 项目变更页
from src.page_object.项目管理.项目执行.项目工时填报页 import 项目工时填报页
from src.page_object.项目管理.项目执行.项目工时统计页 import 项目工时统计页
from src.page_object.项目管理.项目执行.项目整体进度填报页 import 项目整体进度填报页
from src.page_object.项目管理.项目执行.项目月度用款页 import 项目月度用款页

# 项目立项
from src.page_object.项目管理.项目立项.备选库管理页 import 备选库管理页
from src.page_object.项目管理.项目立项.立项申请页 import 立项申请页
from src.page_object.项目管理.项目立项.立项论证页 import 立项论证页
from src.page_object.项目管理.项目立项.项目汇总页 import 项目汇总页
from src.page_object.项目管理.项目立项.项目变更页 import 项目变更页

# 项目结项
from src.page_object.项目管理.项目结项.项目验收页 import 项目验收页
from src.page_object.项目管理.项目结项.结项申报页 import 结项申报页

# 项目需求储备库
from src.page_object.项目管理.项目需求储备库.需求申报页 import 需求申报页
from src.page_object.项目管理.项目需求储备库.需求储备库页 import 需求储备库页


from src.page_object.资产管理.资产使用.资产登记页 import 资产登记页
from src.page_object.资产管理.资产使用.资产领用页 import 资产领用页
from src.page_object.资产管理.资产使用.资产出租页 import 资产出租页
from src.page_object.资产管理.资产使用.资产出借页 import 资产出借页
from src.page_object.资产管理.资产使用.资产归还页 import 资产归还页
from src.page_object.资产管理.资产使用.资产调拨页 import 资产调拨页


from src.page_object.资产管理.资产维护.资产报修页 import 资产报修页
from src.page_object.资产管理.资产维护.资产巡检计划页 import 资产巡检计划页
from src.page_object.资产管理.资产维护.资产巡检结果页 import 资产巡检结果页


class PageInstance:
    登录页: 登录页 = 登录页
    我的待办: 我的待办 = 我的待办
    审批详情页: 审批详情 = 审批详情
    审批中心: 审批中心 = 审批中心

    # === 基础配置 ===
    需求类型配置页: 需求类型配置页 = 需求类型配置页
    项目类型配置页: 项目类型配置页 = 项目类型配置页
    专项项目层级配置页: 专项项目层级配置页 = 专项项目层级配置页
    采购品目配置页: 采购品目配置页 = 采购品目配置页
    绩效指标库页: 绩效指标库页 = 绩效指标库页
    绩效体系模板页: 绩效体系模板页 = 绩效体系模板页
    绩效填报频率配置页: 绩效填报频率配置页 = 绩效填报频率配置页

    # === 绩效管理 ===
    项目绩效申报页: 项目绩效申报页 = 项目绩效申报页
    绩效填报页: 绩效填报页 = 绩效填报页
    绩效汇总页: 绩效汇总页 = 绩效汇总页
    整改下发页: 整改下发页 = 整改下发页
    整改反馈页: 整改反馈页 = 整改反馈页
    绩效自评页: 绩效自评页 = 绩效自评页
    自评汇总页: 自评汇总页 = 自评汇总页

    # === 项目立项 ===
    立项申请页: 立项申请页 = 立项申请页
    立项论证页: 立项论证页 = 立项论证页
    备选库管理页: 备选库管理页 = 备选库管理页
    项目汇总页: 项目汇总页 = 项目汇总页
    项目变更页: 项目变更页 = 项目变更页

    # === 项目库管理工作台 ===
    领导工作台页: 领导工作台页 = 领导工作台页

    # === 项目需求储备库 ===
    需求申报页: 需求申报页 = 需求申报页
    需求储备库页: 需求储备库页 = 需求储备库页

    # === 项目前期文档 ===
    项目建议书页: 项目建议书页 = 项目建议书页
    项目可行性性研究报告页: 项目可行性性研究报告页 = 项目可行性性研究报告页
    项目概算页: 项目概算页 = 项目概算页

    # === 项目执行 ===
    项目任务分解页: 项目任务分解页 = 项目任务分解页
    我的任务页: 我的任务页 = 我的任务页
    项目工时填报页: 项目工时填报页 = 项目工时填报页
    项目整体进度填报页: 项目整体进度填报页 = 项目整体进度填报页
    重大项目进展填报页: 重大项目进展填报页 = 重大项目进展填报页
    项目月度用款页: 项目月度用款页 = 项目月度用款页
    项目变更页: 项目变更页 = 项目变更页
    项目工时统计页: 项目工时统计页 = 项目工时统计页

    # === 项目结项 ===
    项目验收页: 项目验收页 = 项目验收页
    结项申报页: 结项申报页 = 结项申报页

    # === 成果物 ===
    奖励证书页: 奖励证书页 = 奖励证书页
    专著编书页: 专著编书页 = 专著编书页
    专利成果页: 专利成果页 = 专利成果页
    论文成果页: 论文成果页 = 论文成果页
    其他成果页: 其他成果页 = 其他成果页

    # +++++++++++++资产管理+++++++++++++++++++
    资产登记页: 资产登记页 = 资产登记页
    资产领用页: 资产领用页 = 资产领用页
    资产出租页: 资产出租页 = 资产出租页
    资产出借页: 资产出借页 = 资产出借页
    资产归还页: 资产归还页 = 资产归还页
    资产调拨页: 资产调拨页 = 资产调拨页

    资产报修页: 资产报修页 = 资产报修页
    资产巡检结果页: 资产巡检结果页 = 资产巡检结果页
    资产巡检计划页: 资产巡检计划页 = 资产巡检计划页

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
