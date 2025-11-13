from src.test_cases import *
from src.data_models.绩效管理数据 import *


@用例名称("绩效填报审批")
@用例描述("""
1. 绩效管理员登录系统
2. 点击申报按钮
3. 引入绩效指标
4. 在线添加绩效指标
5. 审批通过
""")
@用例级别(严重)
def test_绩效填报(oc_page, oc_page_backup, 绩效填报):
    with  测试步骤('数据初始化'):
        绩效填报info = {
            '资金到位情况': 资金到位情况Data().as_dict(),
            '资金支付进度': 资金支付进度Data().as_dict(),
            '绩效运行监控结论与建议': 绩效运行监控结论与建议Data().as_dict()
        }
        logger.info(f'绩效申报信息: {绩效填报info}')
    with 测试步骤("绩效管理员登录"):
        oc_page.绩效填报页.set_设置当前用户为("liyuxia")
        oc_page.绩效填报页.navigate()

    with 测试步骤("获取数据，并点击申报"):
        oc_page.绩效填报页.select_财政项目(绩效填报)
        未提交卡片_loc = oc_page.绩效填报页.获取卡片定位()
        assert len(未提交卡片_loc) > 0, '当前无可以填写的绩效数据'
        oc_page.绩效填报页.fill_绩效填报(未提交卡片_loc[0], 绩效填报info, oc_page.log_dir)

    with 测试步骤("审批提交"):
        oc_page_backup.我的待办.set_设置当前用户为('testUser')
        oc_page_backup.我的待办.navigate()
        oc_page_backup.我的待办.审批同意("绩效填报")

    with 测试步骤("验证状态"):
        已审批申请 = oc_page.绩效填报页.获取卡片定位(卡片状态='已审批')
        assert len(已审批申请) > 0, '审批状态失效'
