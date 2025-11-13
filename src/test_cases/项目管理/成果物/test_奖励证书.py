from src.test_cases import *
from src.data_models.项目信息数据 import 奖励证书Data


@用例名称("新建奖励证书")
@用例描述("""
测试新建奖励证书

测试步骤:
1. 创建项目立项并审批通过
2. 新增奖励证书,并审批通过
5. 验证审批结果
""")
@用例级别(普通)
def test_新增奖励证书(oc_page, oc_page_backup, 成果物_项目立项):
    with  测试步骤('创建初始化数据'):
        项目名称 = 成果物_项目立项
        奖励证书info = 奖励证书Data(
            关联项目=项目名称
        ).as_dict()
        课程名称 = 奖励证书info.get('课题名称')
    with 测试步骤("项目管理人员登录并进入立项申请页"):
        oc_page.奖励证书页.set_设置当前用户为("superAdmin")
        oc_page.奖励证书页.navigate()

    with 测试步骤("填写立项论证并提交"):
        oc_page.奖励证书页.click_button('新增')
        oc_page.奖励证书页.fill_奖励证书(奖励证书info)
        oc_page.奖励证书页.click_button('提交')
        oc_page.奖励证书页.confirm_弹框()
        info = oc_page.奖励证书页.search_奖励证书(课程名称)
        assert '审批中' in info.get('审批状态')

    with 测试步骤("审批通过"):
        oc_page_backup.我的待办.set_设置当前用户为("testUser")
        oc_page_backup.我的待办.navigate()
        oc_page_backup.我的待办.审批同意('奖励证书流程审批')
        info = oc_page.奖励证书页.search_奖励证书(课程名称)
        assert '已审批' in info.get('审批状态')


