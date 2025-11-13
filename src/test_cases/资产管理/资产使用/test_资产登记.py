from src.data_models.资产信息数据 import 资产登记_基本信息Data, 资产登记_财务信息Data, 资产登记_其他信息Data
from src.test_cases import *


@用例名称("新增资产登记")
@用例描述("""
测试步骤:

""")
@用例级别(严重)
def test_新增资产登记(oc_page, oc_page_backup):
    with 测试步骤("初始化数据"):
        资产登记info = {
            '基本信息': 资产登记_基本信息Data().as_dict(),
            '财务信息': 资产登记_财务信息Data().as_dict(),
            '其他信息': 资产登记_其他信息Data().as_dict()

        }
        logger.info(f'资产登记信息:{资产登记info}')
        资产名称=资产登记info['基本信息']['资产名称']

    with 测试步骤("项目管理人员登录并进入立项申请页"):
        oc_page.资产登记页.set_设置当前用户为("testUser")
        oc_page.资产登记页.navigate()
        oc_page.资产登记页.表格_图标.click()

    with 测试步骤("新增项目可行性研究报告"):
        oc_page.资产登记页.资产登记.click()
        oc_page.资产登记页.fill_资产登记(资产登记info)
        info = oc_page.资产登记页.search_资产(资产名称)
        assert '审批中' in info.get('审批状态')

    # with 测试步骤("审批且验证通过"):
    #     oc_page_backup.我的待办.set_设置当前用户为('testUser')
    #     oc_page_backup.我的待办.navigate()
    #     oc_page_backup.我的待办.审批同意('项目可行性研究报告',项目名称)
    #     info = oc_page.资产登记页.search_项目可行性研究报告(项目名称)
    #     assert '已审批' in info.get('审批状态')
