from src.test_cases import *
from src.data_models.项目信息数据 import 其他成果_基本信息Data


@用例名称("新建其他成果")
@用例描述("""
测试新建其他成果
测试步骤:
1. 创建项目立项并审批通过
2. 新增其他成果,并审批通过
5. 验证审批结果
""")
@用例级别(普通)
def test_新增其他成果(oc_page, oc_page_backup, 成果物_项目立项):
    with  测试步骤('创建初始化数据'):
        项目名称 = 成果物_项目立项
        其他成果info = 其他成果_基本信息Data(
            关联项目=项目名称,
            成果所有人='一级部门A_负责人'
        ).as_dict()
        论文名称 = 其他成果info.get('成果名称')
    with 测试步骤("项目管理人员登录并进入立项申请页"):
        oc_page.其他成果页.set_设置当前用户为("superAdmin")
        oc_page.其他成果页.navigate()

    with 测试步骤("填写立项论证并提交"):
        oc_page.其他成果页.click_button('新增')
        oc_page.其他成果页.fill_其他成果(其他成果info, oc_page.log_dir)
        oc_page.其他成果页.click_button('提交')
        oc_page.其他成果页.confirm_弹框()
        info = oc_page.其他成果页.search_其他成果(论文名称)
        assert '待审批' in info.get('审批状态')

    with 测试步骤("审批通过"):
        oc_page_backup.我的待办.set_设置当前用户为("testUser")
        oc_page_backup.我的待办.navigate()
        oc_page_backup.我的待办.审批同意('其他成果流程审批')
        info = oc_page.其他成果页.search_其他成果(论文名称)
        assert '已审批' in info.get('审批状态')


