from src.test_cases import *
from src.data_models.绩效管理数据 import 绩效指标信息Data


@用例名称("绩效体系模板新增")
@用例描述(
    """
1.绩效角色人员登录
2.填写基本信息
3.引入绩效指标库
4.导入绩效指标
5.手动页面新增
6.保存
"""
)
@用例级别(严重)
def test_绩效体系模板新增(oc_page, 基础配置, 删除绩效体系模板):
    with 测试步骤("初始化数据"):
        项目类型信息, 绩效指标信息 = (
            基础配置["项目类型"]["基本项目类型"],
            基础配置["绩效指标库"],
        )
        引入绩效指标 = [
            绩效指标信息["产出指标"][0],
            绩效指标信息["效益指标"][0],
            绩效指标信息["满意度指标"][0],
        ]
        绩效体系模板info = {
            "基本信息": {
                "项目类型": f"{项目类型信息}",
                "模版名称": f"自动化创建_模板名称_{faker_随机数生成(4)}",
            },
            "绩效导入数据": [
                绩效指标信息Data(
                    三级指标=f"自动化创建_{faker_随机数生成(10)}",
                    指标类型="",
                    指标解释=faker_text(30),
                    评分标准=faker_text(40),
                    指标值=str(faker_随机数生成(2)),
                    是否必填=random.choice(["是", "否"]),
                ).格式化()
                for _ in range(3)
            ],
            "绩效页面数据": [
                绩效指标信息Data(
                    一级指标="产出指标",
                    二级指标="质量指标",
                    三级指标=f"自动化创建_{faker_随机数生成(10)}",
                    指标值="20",
                    指标解释=f"自动化创建_指标解释_{faker_随机数生成(4)}",
                    指标类型="",
                    评价标准=faker_text(40),
                ).as_dict()
            ],
        }
        基本信息, 绩效导入数据, 绩效页面数据 = (
            绩效体系模板info["基本信息"],
            绩效体系模板info["绩效导入数据"],
            绩效体系模板info["绩效页面数据"],
        )
        logger.info(f"新增绩效模板信息: {绩效体系模板info}")

    with 测试步骤("绩效管理员角色登录,跳转到绩效体系模板页面"):
        oc_page.绩效体系模板页.set_设置当前用户为("superAdmin")
        oc_page.绩效体系模板页.navigate()

    with 测试步骤("新增绩效模板"):
        oc_page.绩效体系模板页.新增按钮.click()
        # 填写模板的基础信息（名称、编码、类型等）
        oc_page.绩效体系模板页.fill_绩效模板基础信息(基本信息)
        # 上传绩效模板 Excel（先下载导入模板 → 写入测试数据 → 再上传）
        oc_page.绩效体系模板页.click_button("导入")
        oc_page.绩效体系模板页.upload_模板(绩效导入数据, oc_page.log_dir)
        # 映入绩效指标
        oc_page.绩效体系模板页.click_button("引入绩效指标库")
        oc_page.绩效体系模板页.fill_引入绩效指标(引入绩效指标)
        # 在页面的指标表格中，补充填写每一行的指标信息（含是否必填）
        oc_page.绩效体系模板页.fill_页面指标table信息(绩效页面数据)
        oc_page.绩效体系模板页.click_button("保存")
        oc_page.绩效体系模板页.confirm_弹框()

    with 测试步骤("验证并删除模板"):
        oc_page.绩效体系模板页.search_填写搜索框(
            placeholder="模版名称", 关键字=基本信息["模版名称"]
        )
        cards = oc_page.绩效体系模板页.获取卡片模板信息()
        cards = [c for c in cards if 基本信息["模版名称"] in c["名称"]]
        assert len(cards) == 1, f"预期找到 1 个模板，实际找到 {len(cards)}"
        oc_page.绩效体系模板页.assert_card_status(cards, "未启用")
        删除绩效体系模板(基本信息["模版名称"])


@用例名称("绩效体系模板启用与禁用")
@用例描述(
    """
1.创建一个绩效模板
2.启用绩效体系模板
3.禁用体系模板
验证:一个项目只有一个启用状态
"""
)
@用例级别(普通)
def test_绩效体系模板启用与禁用(oc_page, 新增绩效模板, 删除绩效体系模板):
    with 测试步骤("绩效相关角色登录"):
        oc_page.绩效体系模板页.set_设置当前用户为("superAdmin")
        oc_page.绩效体系模板页.navigate()
        mode_name = 新增绩效模板

    with 测试步骤("绩效体系模板启用"):
        oc_page.绩效体系模板页.开启or禁用_绩效模板(项目名=mode_name, status="启用")
        oc_page.绩效体系模板页.search_填写搜索框(
            placeholder="模版名称", 关键字=mode_name
        )
        cards = oc_page.绩效体系模板页.获取卡片模板信息(mode_name)
        oc_page.绩效体系模板页.assert_card_status(cards, "已启用")

    with 测试步骤("禁用模板"):
        oc_page.绩效体系模板页.开启or禁用_绩效模板(项目名=mode_name, status="禁用")
        oc_page.绩效体系模板页.search_填写搜索框(
            placeholder="模版名称", 关键字=mode_name
        )
        cards = oc_page.绩效体系模板页.获取卡片模板信息()
        oc_page.绩效体系模板页.assert_card_status(cards, "未启用")
        删除绩效体系模板(mode_name)


@pytest.fixture
def 新增绩效模板(oc_page, 基础配置):
    with 测试步骤("初始化数据"):
        项目类型信息, 绩效指标信息 = (
            基础配置["项目类型"]["基本项目类型"],
            基础配置["绩效指标库"],
        )
        绩效体系模板info = {
            "基本信息": {
                "项目类型": f"{项目类型信息}",
                "模版名称": f"自动化创建_模板名称_{faker_随机数生成(4)}",
            },
            "绩效导入数据": [
                绩效指标信息Data(
                    三级指标=f"自动化创建_{faker_随机数生成(10)}",
                    指标类型="",
                    指标解释=faker_text(30),
                    评分标准=faker_text(40),
                    指标值=str(faker_随机数生成(2)),
                    是否必填=random.choice(["是", "否"]),
                ).格式化()
                for _ in range(3)
            ],
        }
        基本信息, 绩效导入数据 = (
            绩效体系模板info["基本信息"],
            绩效体系模板info["绩效导入数据"],
        )
        logger.info(f"新增绩效模板信息: {绩效体系模板info}")

    with 测试步骤("绩效管理员角色登录,跳转到绩效体系模板页面"):
        oc_page.绩效体系模板页.set_设置当前用户为("superAdmin")
        oc_page.绩效体系模板页.navigate()

    with 测试步骤("新增绩效模板"):
        oc_page.绩效体系模板页.新增按钮.click()
        oc_page.绩效体系模板页.fill_绩效模板基础信息(基本信息)
        oc_page.绩效体系模板页.click_button("导入")
        oc_page.绩效体系模板页.upload_模板(绩效导入数据, oc_page.log_dir)
        # 删除最后一行空行
        oc_page.绩效体系模板页.delete_table_last()
        oc_page.绩效体系模板页.click_button("保存")
        oc_page.绩效体系模板页.confirm_弹框()

    yield 基本信息["模版名称"]


@pytest.fixture
def 删除绩效体系模板(oc_page):
    def _delete(project_code: List[str] | str):
        """根据模板名称删除指定模板"""
        if isinstance(project_code, str):
            project_code = [project_code]

        for code in project_code:
            oc_page.绩效体系模板页.search_填写搜索框(
                placeholder="模版名称", 关键字=code
            )
            cards = oc_page.绩效体系模板页.page.locator("div.el-card.box-card")
            for i in range(cards.count()):
                card = cards.nth(i)
                if code in card.inner_text():
                    card.get_by_role("button").click()
                    del_btn = oc_page.绩效体系模板页.page.get_by_role(
                        "menuitem", name="删除"
                    )
                    del_btn.click()
                    oc_page.绩效体系模板页.confirm_弹框()
                    break

    return _delete
