from src.test_cases import *


@用例名称("自评汇总")
@用例描述("""
1. 创建绩效填报
2. 选择项目汇总
3. 汇总列表审批
""")
@用例级别(严重)
def test_绩效汇总(oc_page, oc_page_backup, 绩效自评):
    with 测试步骤("绩效管理员登录，并切换到自评汇总页面"):
        oc_page.自评汇总页.set_设置当前用户为("Bfzr")
        oc_page.自评汇总页.navigate()
        已填绩效自评 = 绩效自评
    with 测试步骤("选中多个项目实现绩效汇总"):
        oc_page.自评汇总页.fill_自评汇总(已填绩效自评)
    with 测试步骤('汇总审批'):
        oc_page_backup.我的待办.set_设置当前用户为('testUser')
        oc_page_backup.我的待办.navigate()
        oc_page_backup.我的待办.审批同意('自评汇总流程')
    with 测试步骤('汇总列表检验'):
        oc_page.自评汇总页.汇总列表_tab.click()
        oc_page.自评汇总页.search_填写搜索框(placeholder='自评编码/项目编码', 关键字=已填绩效自评[0]['项目编码'])
        oc_page.自评汇总页.click_button('导出')
        #  页面数据与导出文件比对


@pytest.fixture
def 绩效自评(oc_page, oc_page_backup):
    return {'项目名称': 'aaa', '项目编码': 'bbb'}
