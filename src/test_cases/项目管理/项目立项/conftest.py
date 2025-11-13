from src.test_cases import *
from src.data_models.项目信息数据 import *
from src.test_cases.项目管理.conftest import fill_项目立项

"""
论证通过
    临时立项（c_initiation_method=2）
    明确资金来源，关联预算指标：项目状态=执行（c_project_status=10）
    未明确资金来源：项目状态=备选（c_project_status=5）
    年度统一立项（c_initiation_method=1）
    项目状态=备选（c_project_status=5）
"""


@pytest.fixture
def 基本项目立项(oc_page, oc_page_backup, 基础配置, global_map):
    """
    新增简要的项目立项，后续调用
    """
    基础项目立项 = global_map.get("基础项目立项")
    if 基础项目立项 is None:
        with 测试步骤("初始化立项数据"):
            基本项目类型 = 基础配置["项目类型"]["基本项目类型"]
            基本类型立项info = {
                "基本信息": 项目立项基本信息Data(
                    项目类型=基本项目类型,
                    实施部门="测试部门222",
                    经费类型="创收经费",
                    立项方式="年度统一立项",
                    项目层级="【全部】",
                    是否政府投资类="否",
                    项目前期文档="",
                    项目负责人="liyuxia2",
                ).as_dict(),
                "立项信息": 立项信息Data(是否立项论证="是").as_dict(),
            }
            基本信息 = 基本类型立项info["基本信息"]
            logger.info(f"创建项目立项数据:{基本类型立项info}")
        with 测试步骤("项目立项"):
            基础项目立项 = fill_项目立项(oc_page, oc_page_backup, 基本信息, 基本类型立项info, "")
            global_map.set("基础项目立项", 基本类型立项info["基本信息"].get("项目名称"))
    return 基础项目立项


def fill_备选库(oc_page, 项目名称, 项目处置信息, 用户名):
    with 测试步骤("切换页面处置项目"):
        oc_page.备选库管理页.set_设置当前用户为(用户名)
        oc_page.备选库管理页.navigate()
        oc_page.备选库管理页.备选库处置(项目名称, 项目处置信息)

    with 测试步骤("备选库处理结果验证"):
        处置方式 = 项目处置信息.get("处置方式")
        if 处置方式 == "清理库":
            info = oc_page.备选库管理页.search_备选库(项目名称)
            assert info.get("审批状态") is None, f"项目 {项目名称} 在清理库后仍然存在"
        if 处置方式 == "立项退回":
            oc_page.立项申请页.navigate()
            info = oc_page.立项申请页.search_立项信息(项目名称)
            assert "备选驳回" in info.get(
                "审批状态"
            ), f"项目 {项目名称} 审批状态应为 '备选驳回'，实际为 {info.get('审批状态')}"


@pytest.fixture
def 删除项目立项(oc_page):
    def _delete_project(project_code: List[str] | str):
        oc_page.立项申请页.navigate()
        if isinstance(project_code, str):
            project_code = [project_code]

        for code in project_code:
            try:
                oc_page.立项申请页.search_填写搜索框(placeholder="关键词搜索", 关键字=code)
                table = oc_page.立项申请页.主表格
                cell_delete = table.get_cell("操作", 0)
                delete_btn = cell_delete.get_by_text("删除").filter(visible=True)
                if delete_btn.count() == 0:
                    break
                delete_btn.click()
                oc_page.立项申请页.confirm_弹框()
                error_message = oc_page.立项申请页.wait_for_error_message()
                if error_message:
                    logger.warning(f"删除失败: {error_message}")
            except Exception as e:
                logger.error(f"删除项目失败: {e}")
                raise ValueError(f"删除失败：{e}")

    yield _delete_project


def delete_database_项目立项(项目立项code: str):
    pass
