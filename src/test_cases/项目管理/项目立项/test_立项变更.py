from src.test_cases import *
from src.test_cases.项目管理.conftest import fill_项目立项


@用例名称("新增项目变更")
@用例描述(
    """
测试步骤:
1. 创建项目立项并审批通过
2. 立项变更
"""
)
@用例级别(严重)
def test_立项变更(oc_page, oc_page_backup, 基础配置):
    with 测试步骤("项目立项并审批通过"):
        用户名 = "Atest11"
        基本项目类型 = 基础配置["项目类型"]["基本项目类型"]
        基本类型立项info = {
            "基本信息": 项目立项基本信息Data(
                项目类型=基本项目类型,
                实施部门="一级部门",
                经费类型="创收经费",
                项目层级="【全部】",
                立项方式="年度统一立项",
                是否政府投资类="否",
            ).as_dict(),
            "立项信息": 立项信息Data(是否立项论证="是").as_dict(),
        }
        基本信息 = 基本类型立项info["基本信息"]
        logger.info(f"项目立项开启论证:{基本类型立项info}")
    #     项目立项 = fill_项目立项(oc_page, oc_page_backup, 基本信息, 基本类型立项info, 用户名)
    # with  测试步骤('切换到立项变更'):
    #     oc_page.项目变更页.set_设置当前用户为(用户名)
    #     oc_page.项目变更页.navigate()
    #     oc_page.项目变更页.新增_按钮.click()
    #     项目变更info = {
    #     }
    #     oc_page.项目变更页.fill_立项变更(项目变更info)
    # with 测试步骤('验证结果'):
    #     oc_page_backup.我的待办.set_设置当前用户为("testUser")
    #     oc_page_backup.我的待办.navigate()
    #     oc_page_backup.我的待办.审批同意('立项论证流程', 用户名)
