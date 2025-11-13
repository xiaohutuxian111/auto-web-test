from src.test_cases import *
from src.test_cases.项目管理.conftest import fill_项目立项, 项目立项_临时立项_项目论证

"""
 两种生成立项的方式
    1、备选库中 的项目关联预算走指标-生成指标结束后流转为执行
    2、临时立项-明确资金来源项目审批通过后，并且走完项目前期和立项论证阶段，直接变更为执行阶段
"""


@pytest.fixture
def 项目执行_前置(oc_page, oc_page_backup, 基础配置):
    # 为解决审批并发无法处理问题,传入用户名
    def _create_demand(用户名: str):
        demand_name = 项目立项_临时立项_项目论证(oc_page, oc_page_backup, 基础配置, 用户名, 是否明确资金来源="是")
        return demand_name

    return _create_demand


@pytest.fixture
def 我的任务_前置(oc_page, oc_page_backup, 基础配置):
    return "24年预算-执行计划项目"


@pytest.fixture
def 工时填报_前置(oc_page, oc_page_backup, 基础配置):
    return "临时立项-明确资金来源845"


@pytest.fixture
def 项目变更_前置(oc_page, oc_page_backup, 基础配置):
    return "直接立项+明确资金来源1"
