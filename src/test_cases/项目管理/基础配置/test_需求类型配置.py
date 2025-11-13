from src.test_cases import *
from src.data_models.需求信息数据 import 需求类型基本信息Data, 附件类型配置Data


@用例名称("需求类型配置新增")
@用例描述(
    """
1.新增需求类配置
3.删除需求类型配置
"""
)
@用例级别(严重)
def test_需求类型配置_新增(oc_page, test_name, 删除需求类型配置):
    with 测试步骤("初始化数据"):
        delete_demand_type = []
        需求类型info = {
            "基本信息": 需求类型基本信息Data(
                需求类型编码=f"ZDH{faker_随机数生成(8)}",
                需求类型=f"自动化创建_需求类型_{faker_随机数生成(4)}",
                归口部门="一级部门",
                责任人="罗凡林3-部门负责人",
                需求申报表单="需求详情&&专项信息&&预算明细&&需求附件",
                是否启用="是",
                申报专项信息表单="建设工程类专项信息&&教学管理类专项信息&&科研类专项信息&&采购类专项信息",
                项目类型="XMLX-20250618-2b57",
                说明=f"自动化_{faker_text(50)}",
            ).as_dict(),
            "附件信息": [
                附件类型配置Data(
                    附件类型名称=f"ZDH_{faker_随机数生成(8)}",
                    表名=f"ZDH_表名_{faker_随机数生成(5)}",
                    支持格式=random.choice(list(FileType)).value,
                    大小限制="3",
                    允许上传附件数="5",
                    附件提示="ZDH_附件提示",
                    说明="ZDH_说明",
                    是否必填=random.choice(["是", "否"]),
                ).as_dict()
            ],
        }
        基本信息, 附件信息 = 需求类型info.get("基本信息", {}), 需求类型info.get(
            "附件信息", []
        )
        delete_demand_type.append(基本信息.get("需求类型编码"))

    with 测试步骤("切换到用户管理人员,并跳转需求配置页面"):
        oc_page.需求类型配置页.set_设置当前用户为("superAdmin")
        oc_page.需求类型配置页.navigate()

    with 测试步骤("填写基本信息"):
        oc_page.需求类型配置页.新增按钮.click()
        oc_page.需求类型配置页.fill_基本信息(基本信息)
        oc_page.需求类型配置页.fill_附件类型配置(附件信息)
    with 测试步骤("验证并删除"):
        oc_page.需求类型配置页.search_填写搜索框(
            placeholder="需求类型编码/需求类型", 关键字=基本信息.get("需求类型")
        )
        table_dict = oc_page.需求类型配置页.主表格.get_row_dict(0)
        info = get_dict_info(基本信息)
        assert compare_dicts(
            dict1=info,
            dict2=table_dict,
            strict=False,
            keys=["需求类型编码", "需求类型", "归口部门", "责任人"],
        )
        删除需求类型配置(delete_demand_type)
