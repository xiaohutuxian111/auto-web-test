from src.pages import *
from src.pages.审批中心 import 审批中心


class 我的待办(审批中心):

    @allure.step("审批同意")
    def 审批同意(self, 单据: str, 关键字: str = None, 审批意见: str = "同意"):
        审批页 = self.get_待办任务(单据, 关键字)
        # 审批页.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        审批页.执行审批操作(审批意见, 按钮名称='通过')

    @allure.step("审批驳回")
    def 审批驳回(self, 单据: str, 关键字: str = None, 审批意见: str = "驳回"):
        审批页 = self.get_待办任务(单据)
        审批页.执行审批操作(审批意见, 按钮名称='驳回')

    @allure.step("审批驳回至指定节点")
    def 审批驳回至节点(self, 单据: str, 节点名称: str, 审批意见: str = "驳回"):
        审批页 = self.get_待办任务(单据)
        审批页.执行驳回(节点名称, 审批意见)

    @allure.step("审批转交")
    def 审批转交(self, 单据: str, 转交人: str, 转交人类型: str = "员工", 审批意见: str = "转交"):
        审批页 = self.get_待办任务(单据)
        审批页.执行转交(转交人, 转交人类型, 审批意见)

    @allure.step("审批加签")
    def 审批加签(self, 单据: str, 加签人, 审批意见: str = "加签"):
        审批页 = self.get_待办任务(单据)
        审批页.执行加签加审抄送('加签', 加签人, 审批意见)

    @allure.step("审批加审")
    def 审批加审(self, 单据: str, 加审人, 审批意见: str = "加审"):
        审批页 = self.get_待办任务(单据)
        审批页.执行加签加审抄送('加审', 加审人, 审批意见)

    @allure.step("审批抄送")
    def 审批抄送(self, 单据: str, 抄送人, 审批意见: str = "抄送"):
        审批页 = self.get_待办任务(单据)
        审批页.执行加签加审抄送('抄送', 抄送人, 审批意见)

    @allure.step("指定下一审批人")
    def 指定下一审批人(self, 单据: str, 下一节点审批人: str,
                       审批任务来源: Optional[Literal["任意审批人", "节点默认审批人"]] = "任意审批人",
                       意见: str = "自动化指定审批人"):
        审批页 = self.get_待办任务(单据)
        审批页.执行指定下一审批人(下一节点审批人, 审批任务来源, 意见)
