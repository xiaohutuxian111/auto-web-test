from src.test_cases import *
from src.data_models.采购信息数据 import 采购品目配置新增Data


@用例名称("采购品目配置新增")
@用例描述(
    """
1. 采购人员角色登录
2. 新增采购品目配置
3. 校验并删除新增配置
"""
)
@用例级别(严重)
def test_采购品目配置新增(oc_page, test_name, 删除采购品目配置):
    with 测试步骤("初始化数据"):
        采购品目数据info = 采购品目配置新增Data(
            采购品目名称=f"自动化创建_采购品目_{faker_随机数生成(4)}",
            上级目录="采购品目",
            是否末级目录="是",
            归口部门="福建省妇幼保健院",
            资产字典="",  # TODO: 资产字典字段待补充
            是否启用="启用",
            品目说明=f"品目说明_{faker_text(50)}",
        ).as_dict()
        采购品目名称 = 采购品目数据info["采购品目名称"]
    with 测试步骤("采购相关角色登录,并跳采购品目配置页面"):
        oc_page.采购品目配置页.set_设置当前用户为("superAdmin")
        oc_page.采购品目配置页.navigate()

    with 测试步骤("新建采购品目配置"):
        oc_page.采购品目配置页.fill_新增采购品配置(采购品目数据info)

    with 测试步骤("验证新增结果并清理数据"):
        oc_page.采购品目配置页.search_填写搜索框(
            placeholder="采购品目编码/名称", 关键字=采购品目名称
        )
        table_info = oc_page.采购品目配置页.主表格.get_row_dict(0)
        logger.info(f"页面数据: {table_info}, 期望数据: {采购品目数据info}")

        assert compare_dicts(
            dict1=采购品目数据info,
            dict2=table_info,
            keys=["采购品目名称", "是否末级目录", "归口部门", "是否启用/启用状态"],
        ), "新增采购品目配置校验未通过"

        删除采购品目配置(采购品目名称)


@用例名称("采购品目配置导入")
@用例描述(
    """
1. 采购人员角色登录
2. 导入采购品目配置
3. 校验并删除导入配置
"""
)
@用例级别(严重)
def test_采购品目配置导入(oc_page, test_name, 删除采购品目配置):
    with 测试步骤("初始化数据"):
        prefix_key = f"自动化创建_导入_{faker_随机数生成(3)}"
        采购品目导入info = [
            {
                "政府采购类别": "工程类",
                "上级采购品目编码": "CGPL-000015",
                "采购品目编码": f"ZDH_{faker_随机数生成(10)}",
                "采购品目名称": f"{prefix_key}_{faker_随机数生成(3)}",
                "部门编码": "fjsfybjy",
                "归口部门": "福建省妇幼保健院",
                "采购品目说明": f"自动化创建_{faker_text(50)}",
            }
            for _ in range(3)
        ]
        delete_code = [item["采购品目编码"] for item in 采购品目导入info]

    with 测试步骤("采购相关角色登录"):
        oc_page.采购品目配置页.set_设置当前用户为("superAdmin")
        oc_page.采购品目配置页.navigate()

    with 测试步骤("导入采购品目配置"):
        oc_page.采购品目配置页.导入按钮.click()
        import_file_path = oc_page.采购品目配置页.upload_模板(
            采购品目导入info, oc_page.log_dir
        )

    with 测试步骤("检验导入结果并清理数据"):
        oc_page.采购品目配置页.search_填写搜索框(
            placeholder="采购品目编码/名称", 关键字=prefix_key
        )
        assert oc_page.采购品目配置页.主表格.excel和页面table比对(
            excel_path=import_file_path,
            sheet_name="导入模板",
            要检查的列名=["采购品目名称/*采购品目名称", "归口部门/*归口部门"],
        ), "导入数据与页面不一致"

        删除采购品目配置(delete_code)
