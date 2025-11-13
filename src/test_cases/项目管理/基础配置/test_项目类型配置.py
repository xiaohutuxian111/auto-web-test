from src.test_cases import *
from src.data_models.项目信息数据 import 项目类型配置Data


@用例名称("项目类型配置导入新增")
@用例描述(
    """
测试项目类型配置的导入新增功能
测试步骤:
1. 导入一个项目类型
2. 对比导入是否正常
3. 删除导入的项目
"""
)
@用例级别(严重)
def test_项目类型配置_导入(oc_page, test_name, 基础配置, 关联预算事项, 删除项目配置):
    """
    测试项目类型配置导入新增功能
    """
    with 测试步骤("初始化测试数据"):
        项目类型info = [
            项目类型配置Data(
                上级类型编码="XMLX101014",
                上级类型="职工薪酬4",
                项目类型编码=f"XMLX0001{faker_随机数生成(4)}",
                项目类型=f"自动化创建_项目类型_{faker_随机数生成(4)}",
                部门编码="fjsfybjy",
                归口部门="福建省妇幼保健院",
                立项填报表单="立项信息,项目专项信息,附件材料",
                绩效目标触发阈值=str(random.randint(10000, 20000)),
                立项专项信息表单="建设工程类专项信息,科研类专项信息",
                关联预算事项编码=关联预算事项.get("事项编码"),
                关联预算事项名称=关联预算事项.get("事项名称"),
            ).as_dict()
        ]
        项目类型编码 = 项目类型info[0].get("项目类型编码")
        项目类型 = 项目类型info[0].get("项目类型")
        delete_project_type = [项目类型编码]
        logger.info(f"项目类型信息:{项目类型info}")
    with 测试步骤("切换到用户项目管理人员并跳转项目管理页面"):
        oc_page.项目类型配置页.set_设置当前用户为("superAdmin")
        oc_page.项目类型配置页.navigate()

    with 测试步骤("页面新增需求类型配置"):
        oc_page.项目类型配置页.click_button("导入")
        import_file_path = oc_page.项目类型配置页.upload_模板(
            项目类型info, oc_page.log_dir, sheet_name="项目类型配置", skip_row=1
        )
        oc_page.项目类型配置页.page.wait_for_timeout(1_000)

    with 测试步骤("对比导入是否正常"):
        # 选中上级节点,与数据的上级类型一致
        oc_page.项目类型配置页.选中左侧树节点(节点名称="职工薪酬4")
        oc_page.项目类型配置页.search_填写搜索框(
            placeholder="项目类型编码/项目类型", 关键字=项目类型
        )

        assert oc_page.项目类型配置页.主表格.excel和页面table比对(
            excel_path=import_file_path,
            要检查的列名=[
                "项目类型编码/*项目类型编码",
                "归口部门/*归口部门",
                "立项专项信息表单/*立项专项信息表单",
                "是否分层级项目/*是否分层级项目",
            ],
            sheet_name="项目类型配置",
        ), "导入项目类型校验失败"

        删除项目配置(delete_project_type)


@用例名称("项目类型配置页面新增(全)")
@用例描述(
    """
测试项目类型配置的页面新增功能

测试步骤:
1. 新建项目子级
2. 新增项目类型
3. 删除项目类型并验证
"""
)
@用例级别(严重)
def test_项目类型配置_页面新增(
    oc_page, test_name, 基础配置, 关联预算事项, 删除项目配置
):
    with 测试步骤("初始化数据"):
        项目类型配置info = {
            "基本信息": 项目类型配置Data(
                项目类型编码=f"AUTOTEST{faker_随机数生成(7)}",
                项目类型=f"自动化创建_ALL_项目类型_{faker_随机数生成(3)}",
                归口部门="一级部门&&测试机构(勿删)",
                立项填报表单="项目专项信息&&绩效目标&&预算明细&&执行计划&&验收标准&&成果物",
                绩效目标触发阈值=str(random.randint(10000, 20000)),
                立项专项信息表单="采购类专项信息&&建设工程类专项信息&&教学管理类专项信息&&科研类专项信息",
                是否分层级项目="是",
                关联预算事项=关联预算事项.get("事项编码"),
                是否启用="是",
                是否末级="是",
            ).格式化(),
            "附件类型配置": [
                {
                    "附件类型名称": f"附件类型名称_{faker_随机数生成(3)}",
                    "表名": faker_text(10),
                    "支持格式": random.choice(list(FileType)).value,
                    "大小限制": str(random.randint(10, 100)),
                    "允许上传附件数": str(random.randint(2, 10)),
                    "附件提示": f"附件提示_{faker_随机数生成(7)}",
                    "说明": faker_text(50),
                    "是否必填": random.choice(["否", "是"]),
                }
                for _ in range(2)
            ],
            "项目管理流程": [
                {
                    "项目总预算下限金额（万元）": str(random.randint(10000, 20000)),
                    "项目总预算上限金额（万元）": str(random.randint(20000, 50000)),
                    "项目管理流程": "项目可行性研究报告&&项目概算",
                }
            ],
            "项目任务阶段创建": [{"任务阶段名称": f"第{i}阶段"} for i in range(1, 4)],
            "附件类型": [
                {
                    "附件类型名称": f"附件类型名称_{faker_随机数生成(3)}",
                    "表名": f"自动化创建_表名_{faker_随机数生成(3)}",
                    "支持格式": random.choice(list(FileType)).value,
                    "大小限制": str(random.randint(10, 100)),
                    "允许上传附件数": str(random.randint(2, 10)),
                    "附件提示": f"附件提示_{faker_随机数生成(7)}",
                    "说明": faker_text(50),
                    "是否必填": random.choice(["否", "是"]),
                }
                for _ in range(3)
            ],
        }
        基本信息, 项目管理流程, 项目任务阶段创建, 附件类型配置 = (
            项目类型配置info.get("基本信息", {}),
            项目类型配置info.get("项目管理流程", []),
            项目类型配置info.get("项目任务阶段创建", []),
            项目类型配置info.get("附件类型", []),
        )
        项目类型编码 = 基本信息.get("项目类型编码")
        delete_project_type = [项目类型编码]

    with 测试步骤("切换到用户项目管理人员并跳转项目管理页面"):
        oc_page.项目类型配置页.set_设置当前用户为("superAdmin")
        oc_page.项目类型配置页.navigate()

    with 测试步骤("新增"):
        oc_page.项目类型配置页.add_添加子级()
        # 基本信息
        oc_page.项目类型配置页.fill_基本信息(基本信息)
        # 填写项目管理流程
        oc_page.项目类型配置页.fill_项目管理流程(项目管理流程)
        # 填写项目任务阶段创建
        oc_page.项目类型配置页.fill_项目任务阶段创建(项目任务阶段创建)
        # 附件
        oc_page.项目类型配置页.fill_附件类型配置(附件类型配置)
        oc_page.项目类型配置页.click_button("保存")
        oc_page.项目类型配置页.confirm_弹框()

    with 测试步骤("验证结果并删除"):
        #  选中上级节点,与数据的上级类型一致
        oc_page.项目类型配置页.search_填写搜索框(
            placeholder="项目类型编码/项目类型", 关键字=项目类型编码
        )
        table = oc_page.项目类型配置页.主表格
        table_info = table.get_row_dict(0)
        # 整理多余的字符
        基本信息_info = get_dict_info(table_info)
        基本信息_info["立项专项信息表单"] = 基本信息_info["立项专项信息表单"].replace(
            "&&", ","
        )
        assert compare_dicts(
            table_info,
            基本信息_info,
            keys=[
                "项目类型编码",
                "项目类型",
                "归口部门",
                "立项专项信息表单",
                "是否分层级项目",
                "启用状态",
            ],
        ), "页面新增项目类型校验失败"
        删除项目配置(delete_project_type)
