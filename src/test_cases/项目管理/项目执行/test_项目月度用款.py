from src.test_cases import *


@用例名称("项目月度用款的新增导出")
@用例描述(
    """
    项目月度用款的新增导出
测试步骤:
    1. 项目月度用款前置步骤
    2. 新增月度用款
    3. 审批验证
    4. 导出
"""
)
@用例级别(严重)
def test_项目月度用款新增导出(oc_page, oc_page_backup, 月度用款_前置):

    用户名 = "testUser"
    项目名称 = 月度用款_前置

    with 测试步骤("新增月度用款"):
        oc_page.项目月度用款页.set_设置当前用户为(用户名)
        oc_page.项目月度用款页.navigate()
        oc_page.项目月度用款页.新增_按钮.click()
        oc_page.项目月度用款页.fill_月度用款(项目名称)

    with 测试步骤("审批与验证"):
        oc_page_backup.我的待办.set_设置当前用户为("testUser")
        oc_page_backup.我的待办.navigate()
        oc_page_backup.我的待办.审批同意("项目月度计划用款", 用户名)

        info = oc_page.项目月度用款页.search_月度用款(项目名称)
        assert "已审批" in info["审批状态"]

    with 测试步骤("导出并验证"):
        oc_page.项目月度用款页.主表格.除了all的checkbox()
        oc_page.项目月度用款页.导出_按钮.click()
        with oc_page.page.expect_download() as 项目月度用款导出:
            oc_page.项目月度用款页.confirm_弹框()

        export_file_path = os.path.join(oc_page.log_dir, 项目月度用款导出.value.suggested_filename)
        项目月度用款导出.value.save_as(export_file_path)

        assert os.path.exists(export_file_path), f"导出文件不存在: {export_file_path}"

        assert oc_page.项目月度用款页.主表格.excel和页面table比对(
            excel_path=export_file_path,
            要检查的列名=["项目名称", "项目金额", "审批状态"],
            sheet_name="Sheet0",
            skip_rows=0,
        ), "项目月度用款导出数据与页面不一致"
