from src.test_cases import *


@用例名称("绩效自评审批")
@用例描述("""
1. 创建绩效申报数据
2. 填写绩效自评
3. 审批通过
""")
@用例级别(严重)
def test_绩效自评(oc_page, test_name, 绩效申报):
    with 测试步骤("绩效管理员登录"):
        oc_page.绩效自评页.set_设置当前用户为("Bfzr")
        oc_page.绩效自评页.navigate()
        项目名称 = 绩效申报

    with 测试步骤("填写绩效自评"):
        oc_page.绩效自评页.search_填写搜索框(placeholder="项目名称", 关键字=项目名称)
        待填报_loc = oc_page.绩效填报页.获取卡片定位()
        assert len(待填报_loc) > 0, '当前无可以填写的绩效数据'
        oc_page.绩效自评页.fill_绩效自评(待填报_loc[0], oc_page.log_dir)

    with 测试步骤("审批提交"):
        oc_page.我的待办.set_设置当前用户为('testUser')
        oc_page.我的待办.navigate()
        oc_page.我的待办.审批同意('绩效自评流程')
    with 测试步骤('验证自评'):
        pass
