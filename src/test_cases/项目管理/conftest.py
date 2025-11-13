from src.test_cases.项目管理 import *


@pytest.fixture(scope="function", autouse=True)
def 基础配置(oc_page, 关联预算事项) -> Dict[str, Any]:
    cache = JsonCache(get_path(".temp/ProjectInitialization.json"))
    print("\033[32m====初始化项目配置信息公用数据===\033[0m")
    return {
        "需求类型": cache.get_or_init("需求类型", lambda: init_需求类型配置(oc_page)),
        "项目类型": cache.get_or_init("项目类型", lambda: init_项目类型配置(oc_page, 关联预算事项)),
        "专项项目": cache.get_or_init("专项项目", lambda: init_专项项目层级配置(oc_page, 关联预算事项)),
        "采购品目": cache.get_or_init("采购品目", lambda: init_采购品目配置(oc_page)),
        "绩效指标库": cache.get_or_init("绩效指标库", lambda: init_绩效指标库(oc_page)),
        "绩效体系模板": cache.get_or_init("绩效体系模板", lambda: init_绩效体系模板(oc_page, 关联预算事项)),
        "绩效指标填报频率": cache.get_or_init("绩效指标填报频率", lambda: init_绩效指标填报频率配置(oc_page)),
    }


@pytest.fixture
def 删除绩效指标(oc_page):
    def _delete(project_code: List[str] | str):
        if isinstance(project_code, str):
            project_code = [project_code]
        for code in project_code:
            delete_config(
                page=oc_page.绩效指标库页,
                search_placeholder="资金用途",
                code=code,
                table_name="绩效指标库",
            )

    yield _delete


@pytest.fixture
def 删除采购品目配置(oc_page):
    def _delete(project_code: List[str] | str):
        if isinstance(project_code, str):
            project_code = [project_code]
        oc_page.采购品目配置页.navigate()
        for code in project_code:
            delete_config(
                page=oc_page.采购品目配置页,
                search_placeholder="采购品目编码/名称",
                code=code,
                table_name="采购品目配置",
            )

    yield _delete


@pytest.fixture
def 删除需求类型配置(oc_page):
    def _delete(project_code: List[str] | str):
        if isinstance(project_code, str):
            project_code = [project_code]
        oc_page.需求类型配置页.navigate()
        for code in project_code:
            delete_config(
                page=oc_page.需求类型配置页,
                search_placeholder="需求类型编码/需求类型",
                code=code,
                table_name="需求类型配置",
            )

    yield _delete


@pytest.fixture
def 删除项目配置(oc_page):
    def _delete(project_code: List[str] | str):
        if isinstance(project_code, str):
            project_code = [project_code]
        for code in project_code:
            delete_config(
                page=oc_page.项目类型配置页,
                search_placeholder="项目类型编码/项目类型",
                code=code,
                table_name="项目类型配置",
                db_fallback=delete_database_项目类型,
            )

    yield _delete


@pytest.fixture
def 关联需求(oc_page, oc_page_backup, 基础配置):
    """
    创建多个需求
    """

    # 为解决审批并发无法处理问题,传入用户名
    def _create_demand(用户名: str):
        demand_name = 创建关联需求(oc_page, oc_page_backup, 基础配置, 用户名)
        return demand_name

    return _create_demand


@pytest.fixture
def 关联预算事项(oc_page):
    return {
        "事项编码": "ZCSX-0125",
        "事项名称": "ferry_支出预算事项名称_开支标准是选填",
    }
