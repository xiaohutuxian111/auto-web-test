from src.data_models.绩效管理数据 import 整改下发Data
from src.test_cases import *


@用例名称("整改下发新增审批")
@用例描述("""
1. 绩效管理员登录
2. 填写整改下发信息
3. 审批
""")
@用例级别(普通)
def test_整改下发新增(oc_page, oc_page_backup, 整改项目):
    with  测试步骤('初始化数据'):
        项目名称 = 整改项目.get('项目名称')
        整改下发info = 整改下发Data(整改项目=项目名称).as_dict()
    with 测试步骤("绩效管理员登录"):
        oc_page.整改下发页.set_设置当前用户为("Afzr")
        oc_page.整改下发页.navigate()
    with 测试步骤("新增整改下发"):
        oc_page.整改下发页.新增_按钮.click()
        oc_page.整改下发页.fill_整改下发(temp_path=oc_page.log_dir, 整改信息=整改下发info)
    with 测试步骤('绩效管理员审批通过'):
        oc_page_backup.我的待办.set_设置当前用户为('Afzr')
        oc_page_backup.我的待办.navigate()
        oc_page_backup.我的待办.审批同意('整改下发流程')
    with  测试步骤('验证整改信息'):
        pass


@pytest.fixture
def 整改项目(oc_page, oc_page_back_up):
    return {'项目名称': 'aaa', '项目编码': 'bbb'}
