from src.test_cases import *


@用例名称("新建项目概算")
@用例描述("""
测试步骤:
1. 创建项目立项审批通过(是否政府投资类='是',项目前期文档="项目概算")
2. 新增项目概算
3. 验证结果
""")
@用例级别(严重)
def test_新建项目概算(oc_page, oc_page_backup, 项目概算_项目立项):
    with 测试步骤("初始化数据"):
        项目名称 = 项目概算_项目立项
        项目概算 = {
            '基本信息': 项目概算_基本信息(项目名称=项目名称).as_dict(),
            '批文信息': 项目概算_批文信息().as_dict()
        }

    with 测试步骤("项目管理人员登录并进入项目概算页"):
        oc_page.项目概算页.set_设置当前用户为("superAdmin")
        oc_page.项目概算页.navigate()

    with 测试步骤("新增项目概算"):
        oc_page.项目概算页.新增_按钮.click()
        oc_page.项目概算页.fill_项目概算(项目概算, oc_page.log_dir)
        info = oc_page.项目概算页.search_项目概算(项目名称)
        assert '审批中' in info.get('审批状态')

    with 测试步骤("审批且验证通过"):
        oc_page_backup.我的待办.set_设置当前用户为('testUser')
        oc_page_backup.我的待办.navigate()
        oc_page_backup.我的待办.审批同意('项目概算', 项目名称)
        info = oc_page.项目概算页.search_项目概算(项目名称)
        assert '已审批' in info.get('审批状态')
