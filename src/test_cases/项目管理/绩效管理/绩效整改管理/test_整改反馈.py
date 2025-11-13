from src.data_models.绩效管理数据 import 整改反馈Data
from src.test_cases import *


@用例名称("整改反馈新增审批")
@用例描述("""
1. 新增整改下发审批通过
2. 编辑整改反馈
3. 整改反馈审批
""")
@用例级别(严重)
def test_整改反馈(oc_page, oc_page_backup, 整改下发):
    with  测试步骤('初始化数据'):
        整改反馈info = 整改反馈Data().as_dict()
        项目名称 = 整改下发
        logger.info(f"整改下发信息: {整改反馈info}")
    with 测试步骤("绩效管理员登录,并切换到绩效反馈"):
        oc_page.整改反馈页.set_设置当前用户为("Afzr")
        oc_page.整改反馈页.navigate()

    with 测试步骤("编辑整改反馈"):
        oc_page.整改反馈页.get_状态定位(项目名称).click()
        oc_page.整改反馈页.fill_整改反馈(temp_path=oc_page.log_dir, 反馈信息=整改反馈info)

    with 测试步骤('绩效管理员审批通过'):
        oc_page.我的待办.set_设置当前用户为('Afzr')
        oc_page.我的待办.navigate()
        oc_page.我的待办.审批同意('整改反馈流程')
    with 测试步骤('验证绩效反馈'):
        pass


@pytest.fixture
def 整改下发():
    return '项目名称'
