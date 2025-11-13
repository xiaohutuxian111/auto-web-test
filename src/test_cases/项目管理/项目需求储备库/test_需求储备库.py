from src.test_cases import *
from src.data_models.需求信息数据 import *


@用例名称("编辑需求储备库审批通过")
@用例描述(
    """
    需求储备库修改提交审批功能
    测试步骤:
    1. 创建需求并审批通过
    2. 编辑需求申报
    3. 审批通过
    4. 验证审批结果
"""
)
@用例级别(普通)
def test_编辑需求储备库审批(oc_page, oc_page_backup, 基础配置, 关联需求):
    with 测试步骤("数据初始化"):
        需求类型名称 = 基础配置["需求类型"]
        采购类型 = 基础配置["采购品目"]
        需求表单info = {
            "基本信息": 基本信息Data(需求类型=需求类型名称).as_dict(),
            "需求详情": 需求详情Data().as_dict(),
            "采购类专项信息": {
                "采购信息": {
                    "采购类型": "&&".join(采购类型.keys()),
                    "采购组织方式": random.choice(["政府集中采购", "不限", "非政府集中采购"]),
                    "是否一次性采购": random.choice(["是", "否"]),
                },
                "采购明细": 采购类型["电子设备"][:3],
            },
            "建设工程类专项信息": 建设工程类专项信息Data().as_dict(),
            "教学管理类专项信息": 教学管理类专项信息Data().as_dict(),
            "预算明细": {"资金来源": "财政&&非财政&&科研&&人力"},
            "科研项目类专项信息": 科研项目类专项信息Data().as_dict(),
        }
        已创建需求名称 = 关联需求("Atest1")
        logger.info(f"需求初始化: {需求表单info}")

    with 测试步骤("进入需求储备库并选择已有需求编辑"):
        oc_page.需求储备库页.set_设置当前用户为("Atest1")
        oc_page.需求储备库页.navigate()
        oc_page.需求储备库页.需求储备_tab.click()
        tabel = oc_page.需求储备库页.主表格
        oc_page.需求储备库页.search_填写搜索框(placeholder="需求编号/需求名称", 关键字=已创建需求名称)
        需求编码 = tabel.get_cell("需求编码", 0).inner_text()
        tabel.get_cell("操作", 0).get_by_text("编辑").click()

    with 测试步骤("填写需求储备表单"):
        oc_page.需求储备库页.fill_整体填报(需求表单info, oc_page.log_dir)
        oc_page.需求储备库页.click_button("提交")
        oc_page.需求储备库页.confirm_弹框()
        提交并审批(oc_page, oc_page_backup, 需求编码, 用户名="Atest1")


@用例名称("需求储备库需求合并审批通过")
@用例描述(
    """
需求储备库需求合并
测试步骤:
1. 创建两个需求并审批通过
2. 填写需求合并信息
3. 提交审批
4. 验证审批结果
"""
)
@用例级别(普通)
def test_需求储备库合并审批(oc_page, oc_page_backup, 基础配置, 关联需求):
    with 测试步骤("数据初始化"):
        需求类型名称 = 基础配置["需求类型"]
        采购类型 = 基础配置["采购品目"]
        需求表单信息 = {"基本信息": 基本信息Data(需求类型=需求类型名称).as_dict()}
        采购类专项信息 = {
            "采购信息": {
                "采购类型": "&&".join(采购类型.keys()),
                "采购组织方式": random.choice(["政府集中采购", "不限", "非政府集中采购"]),
            },
            "采购明细": 采购类型["电子设备"][:3],
        }
        基本信息 = 需求表单信息["基本信息"]
        关联需求01 = 关联需求("Atest2")
        关联需求02 = 关联需求("Atest2")
        已创建需求list = [关联需求01, 关联需求02]

        logger.info(f"需求合并初始化: {采购类专项信息}")

    with 测试步骤("进入需求合并页面并选择需求"):
        oc_page.需求储备库页.set_设置当前用户为("Atest2")
        oc_page.需求储备库页.navigate()
        oc_page.需求储备库页.被合并需求_tab.click()
        oc_page.需求储备库页.set_需求主次(已创建需求list)

    with 测试步骤("填写合并表单数据"):
        oc_page.需求储备库页.fill_整体填报(需求表单信息)
        oc_page.需求储备库页.fill_合并_采购类专项信息(采购类专项信息)
        oc_page.需求储备库页.fill_合并_建设工程类专项信息()
        oc_page.需求储备库页.fill_合并_教学管理类专项信息()
        oc_page.需求储备库页.fill_合并_科研项目类专项信息()
        oc_page.需求储备库页.fill_合并_预算明细()

    with 测试步骤("提交并校验审批"):
        oc_page.需求储备库页.click_button("提交")
        oc_page.需求储备库页.search_填写搜索框(placeholder="需求编号/需求名称", 关键字=基本信息["需求名称"])
        table = oc_page.需求储备库页.主表格
        需求编码 = table.get_cell("需求编码", 0).inner_text()
        提交并审批(oc_page, oc_page_backup, 需求编码, 待办类型="需求合并审批", 用户名="Atest2")


def 提交并审批(oc_page, oc_page_backup, 需求编码: str, 待办类型: str = "需求补充审批", 用户名: str = None):
    """通用的提交审批并校验"""
    with 测试步骤("提交并验证审批中状态"):
        info = oc_page.需求储备库页.search_需求(需求编码)
        assert info["审批状态"].strip() == "审批中", f"需求 {需求编码} 未进入审批中"

    with 测试步骤("审批通过"):
        oc_page_backup.我的待办.set_设置当前用户为("testUser")
        oc_page_backup.我的待办.navigate()
        oc_page_backup.我的待办.审批同意(待办类型, 用户名)

    with 测试步骤("验证审批通过状态"):
        info = oc_page.需求储备库页.search_需求(需求编码)
        assert info["审批状态"].strip() in ["-", "审批通过"], f"需求 {需求编码} 审批未通过"
