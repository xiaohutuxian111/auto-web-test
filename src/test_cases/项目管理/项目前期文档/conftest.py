from  src.test_cases import *
from src.test_cases.项目管理.conftest import fill_项目立项


def 构造项目立项(oc_page, oc_page_backup, 基础配置, 项目前期文档: str, 名称前缀: str):
    """统一生成项目立项数据并执行填报"""
    基本项目类型 = 基础配置['项目类型']['基本项目类型']
    项目名称 = f'自动化创建_{名称前缀}_{faker_随机数生成(3)}'

    立项info = {
        '基本信息': 项目立项基本信息Data(
            项目名称=项目名称,
            项目类型=基本项目类型,
            实施部门='一级部门',
            经费类型='创收经费',
            项目层级='【全部】',
            立项方式='年度统一立项',
            是否政府投资类='是',
            项目前期文档=项目前期文档,
            项目负责人='一级部门A_负责人'
        ).as_dict(),
        '立项信息': 立项信息Data().as_dict()
    }
    logger.info(f"{项目前期文档}_项目立项: {立项info}")

    return fill_项目立项(oc_page, oc_page_backup, 立项info['基本信息'], 立项info)


@pytest.fixture
def 可行性研究报告项目_项目立项(oc_page, oc_page_backup, 基础配置):
    return 构造项目立项(oc_page, oc_page_backup, 基础配置, "项目可行性报告", "开启可行性研究报告")


@pytest.fixture
def 项目建议书_项目立项(oc_page, oc_page_backup, 基础配置):
    return 构造项目立项(oc_page, oc_page_backup, 基础配置, "项目建议书", "开启项目建议书")


@pytest.fixture
def 项目概算_项目立项(oc_page, oc_page_backup, 基础配置):
    return 构造项目立项(oc_page, oc_page_backup, 基础配置, "项目概算", "项目概算")