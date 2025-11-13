from src.test_cases import *
from src.data_models.绩效管理数据 import 绩效指标信息Data


@用例名称("绩效指标_导入导出")
@用例描述(
    """
    1. 导入三个项目
    2. 对比导入是否正常
    3. 删除导入的项目
    4. 导出并校验导出结果
"""
)
@用例级别(严重)
def test_绩效指标_导入导出(oc_page, test_name, 删除绩效指标):
    with 测试步骤("初始化数据"):
        绩效指标导入info = [
            绩效指标信息Data(
                资金用途=f"自动化创建_导入_资金用途_{faker_text(20)}",
                三级指标=f"自动化创建_三级指标_{faker_随机数生成(10)}",
                指标解释=f"{faker_text(30)}",
                评分标准=f"评分标准_{faker_text(40)}",
                指标值=str(faker_随机数生成(2)),
            ).格式化()
            for _ in range(3)
        ]
        delete_code = [item["资金用途"] for item in 绩效指标导入info]

    with 测试步骤("切换到用户'绩效管理员'并跳转绩效指标库页面"):
        oc_page.绩效指标库页.set_设置当前用户为("superAdmin")
        oc_page.绩效指标库页.navigate()

    with 测试步骤("导入三个绩效指标"):
        oc_page.绩效指标库页.导入按钮.click()
        import_file_path = oc_page.绩效指标库页.upload_模板(绩效指标导入info, oc_page.log_dir)

    with 测试步骤("对比导入是否正常"):
        oc_page.绩效指标库页.navigate()
        oc_page.绩效指标库页.search_填写搜索框(关键字="自动化创建_导入_资金用途_", placeholder="资金用途")
        assert oc_page.绩效指标库页.主表格.excel和页面table比对(
            excel_path=import_file_path,
            要检查的列名=[
                "资金用途/资金用途*",
                "三级指标/三级指标*",
                "指标属性/指标属性*",
                "评分标准/评价标准*",
            ],
            sheet_name="导入模板",
            skip_rows=0,
        ), "绩效指标导入数据与页面不一致"

    with 测试步骤("导出项目并校验结果"):
        oc_page.绩效指标库页.navigate()
        oc_page.绩效指标库页.search_填写搜索框(关键字="自动化创建_导入_资金用途_", placeholder="资金用途")
        oc_page.绩效指标库页.导出按钮.click()

        with oc_page.page.expect_download() as 绩效指标导出:
            oc_page.绩效指标库页.confirm_弹框()

        export_file_path = os.path.join(oc_page.log_dir, 绩效指标导出.value.suggested_filename)
        绩效指标导出.value.save_as(export_file_path)

        assert oc_page.绩效指标库页.主表格.excel和页面table比对(
            excel_path=export_file_path,
            要检查的列名=["资金用途", "三级指标", "指标属性", "评分标准/评价标准"],
            sheet_name="Sheet0",
            skip_rows=0,
        ), "绩效指标导出数据与页面不一致"

    with 测试步骤("清理测试数据"):
        删除绩效指标(delete_code)


@用例名称("绩效指标_新增")
@用例描述(
    """
    1. 新增绩效指标
    2. 对比新增指标是否正常
    3. 删除新增的指标
"""
)
@用例级别(严重)
def test_绩效指标_新增(oc_page, test_name, 删除绩效指标):
    with 测试步骤("切换到用户'绩效管理员'并跳转绩效指标库页面"):
        oc_page.绩效指标库页.set_设置当前用户为("superAdmin")
        oc_page.绩效指标库页.navigate()

    with 测试步骤("新建绩效指标"):
        oc_page.绩效指标库页.新增按钮.click()
        绩效指标info = 绩效指标信息Data(
            资金用途=f"自动化创建_页面新增_{faker_text(20)}",
            三级指标=f"自动化创建_{faker_随机数生成(10)}",
            指标解释=f"{faker_text(30)}",
            评分标准=f"{faker_text(40)}",
            指标值=str(faker_随机数生成(2)),
        ).格式化()

        delete_code = [绩效指标info["资金用途"]]

        oc_page.绩效指标库页.fill_新增绩效指标(绩效指标info)

    with 测试步骤("对比新增是否正常"):
        oc_page.绩效指标库页.search_填写搜索框(placeholder="资金用途", 关键字=绩效指标info["资金用途"])
        info_dict = oc_page.绩效指标库页.主表格.get_row_dict(0)

        assert compare_dicts(
            dict1=info_dict,
            dict2=绩效指标info,
            keys=["资金用途", "三级指标", "指标属性", "评分标准"],
        ), "页面新增绩效指标校验未通过"

    with 测试步骤("清理测试数据"):
        删除绩效指标(delete_code)
