from src.test_cases import *
from src.data_models.绩效管理数据 import *
from src.data_models.需求信息数据 import *


def init_需求类型配置(oc_page) -> Dict[str, Any]:
    项目类型 = build_项目类型基本信息()
    项目类型创建(
        oc_page,
        {
            "基本信息": 项目类型,
            "项目管理流程": [
                {
                    "项目总预算下限金额（万元）": "10000",
                    "项目总预算上限金额（万元）": "30000",
                    "项目管理流程": "项目可行性研究报告&&项目概算",
                }
            ],
            "任务阶段": [{"任务阶段名称": f"第{i}阶段"} for i in range(1, 4)],
            "附件类型配置": [build_附件类型配置()],
        },
    )

    需求类型数据 = {
        "基本信息": build_需求类型基本信息(项目类型["项目类型"]),
        "附件类型配置": [build_附件类型配置()],
    }
    需求类型创建(oc_page, 需求类型数据)
    return 需求类型数据["基本信息"]["需求类型"]


def init_项目类型配置(oc_page, 关联预算事项) -> Dict[str, Any]:
    项目类型 = {
        "基本项目类型": add_基本项目类型(oc_page, 关联预算事项),
        "ALL_项目类型": add_all_项目类型(oc_page, 关联预算事项),
        "执行项目_项目类型": add_执行项目_项目类型(oc_page, 关联预算事项),
        "预算明细_项目类型": add_预算明细_项目类型(oc_page, 关联预算事项),
        "汇总项目_项目类型": add_汇总项目_项目类型(oc_page, 关联预算事项),
        "预算明细and执行_项目类型": add_预算明细and执行_项目类型(oc_page, 关联预算事项),
    }
    return 项目类型


def init_专项项目层级配置(oc_page, 关联预算事项) -> Dict[str, Any]:
    专项层级项目类型配置 = {
        "基本信息": build_项目类型基本信息(关联预算事项.get("事项编码"), 是否分层级项目="是"),
        "项目管理流程": [
            {
                "项目总预算下限金额（万元）": "10000",
                "项目总预算上限金额（万元）": "30000",
                "项目管理流程": "项目可行性研究报告&&项目概算",
            }
        ],
        "任务阶段": [{"任务阶段名称": f"第{i}阶段"} for i in range(1, 4)],
        "附件类型配置": [build_附件类型配置()],
    }
    项目类型创建(oc_page, 专项层级项目类型配置)

    专项项目层级数据 = {
        "基本信息": {
            "层级名称": f"自动化创建_一级层级_{faker_随机数生成(5)}",
            "归口部门": "一级部门",
            "责任人": "一级部门A_负责人",
            "汇总人": "一级部门A_负责人",
            "审批人": "一级部门A_负责人",
            "审批流程": "立项论证流程",
            "是否末级": "是",
        }
    }

    专项项目层级创建(oc_page, 专项层级项目类型配置["基本信息"]["项目类型"], 专项项目层级数据)

    return {"项目类型名称": 专项层级项目类型配置["基本信息"]["项目类型"]}


def init_采购品目配置(oc_page) -> Dict[str, Any]:
    with 测试步骤("采购相关角色登录,并跳采购品目配置页面"):
        oc_page.采购品目配置页.set_设置当前用户为("superAdmin")
        oc_page.采购品目配置页.navigate()
    with 测试步骤("新建采购品目配置"):
        info = oc_page.采购品目配置页.get_采购品目_一级_采购品目编码()
        return info


def init_绩效指标库(oc_page) -> Dict[str, Any]:
    指标数据 = {
        name: [
            绩效指标信息Data(
                资金用途=f"自动化创建_{faker_随机数生成(8)}",
                一级指标=name,
                三级指标=f"自动化创建_{faker_随机数生成(10)}",
                指标解释=faker_text(20),
                评分标准=faker_text(30),
                指标值=str(faker_随机数生成(2)),
            ).格式化()
            for _ in range(5)
        ]
        for name in ["产出指标", "效益指标", "满意度指标"]
    }
    绩效指标创建(oc_page, 指标数据)
    指标info = {category: [] for category in 指标数据.keys()}
    for category, indicators in 指标数据.items():
        for indicator in indicators:
            指标info[category].append(indicator["三级指标"])

    return 指标info


def init_绩效体系模板(oc_page, 关联预算事项) -> Dict[str, Any]:
    项目类型data = {
        "基本信息": build_项目类型基本信息(关联预算事项.get("事项编码")),
        "任务阶段": [{"任务阶段名称": f"第{i}阶段"} for i in range(1, 2)],
        "附件类型配置": [build_附件类型配置()],
    }
    项目类型创建(oc_page, 项目类型data)

    绩效模板数据 = {
        "基本信息": {
            "项目类型": f'{项目类型data["基本信息"]["项目类型"]}',
            "模版名称": f"自动化创建_{faker_随机数生成(6)}",
        },
        "绩效目标信息": [
            {
                "一级指标": "产出指标",
                "二级指标": "质量指标",
                "三级指标": f"自动化创建_{faker_随机数生成(10)}",
                "指标解释": f"自动化创建_{faker_随机数生成(10)}",
                "指标属性": "定性",
                "指标性质": "≥",
                "指标值": "10",
                "指标单位": "吨",
                "指标方向性": "正向指标",
                "评价标准": faker_text(30),
                "是否必填": random.choice(["否", "是"]),
                "指标汇总规则": "最大值",
            }
            for _ in range(3)
        ],
    }
    绩效模板体系创建(oc_page, 绩效模板数据)
    return 绩效模板数据["基本信息"]["模版名称"]


def init_绩效指标填报频率配置(oc_page) -> Dict[str, Any]:
    oc_page.绩效填报频率配置页.set_设置当前用户为("superAdmin")
    oc_page.绩效填报频率配置页.navigate()
    info = oc_page.绩效填报频率配置页.get_配置信息()
    return info


def add_汇总项目_项目类型(oc_page, 关联预算事项, 汇总人: str = "Atest10"):
    项目类型配置 = build_项目类型配置(
        关联预算事项,
        项目类型前缀="(汇总)",
        是否分层级="是",
        立项填报表单="绩效目标&&预算明细",
    )
    项目类型创建(oc_page, 项目类型配置)

    项目类型名称 = 项目类型配置["基本信息"]["项目类型"]
    # 添加专项汇总信息
    oc_page.专项项目层级配置页.navigate()
    oc_page.专项项目层级配置页.search_填写搜索框(关键字=项目类型名称, placeholder="层级名称")
    操作定位 = oc_page.专项项目层级配置页.主表格.get_cell("操作", 0)
    操作定位.get_by_text("新增下级").click()
    oc_page.专项项目层级配置页.fill_新增专项层级(
        专项层级Data(
            层级名称=f"自动化创建_层级名称_{faker_随机数生成(4)}", 归口部门="一级部门", 汇总人=汇总人
        ).as_dict()
    )
    return 项目类型名称


# 基本项目
def add_基本项目类型(oc_page, 关联预算事项):
    项目类型配置 = build_项目类型配置(关联预算事项, 项目类型前缀="(基本)", 是否分层级="否")
    项目类型创建(oc_page, 项目类型配置)
    return 项目类型配置["基本信息"]["项目类型"]


# ALL 项目
def add_all_项目类型(oc_page, 关联预算事项):
    extra = {
        "立项填报表单": "项目专项信息&&绩效目标&&预算明细&&执行计划&&验收标准&&成果物",
        "绩效目标触发阈值": "15000",
        "立项专项信息表单": "采购类专项信息&&建设工程类专项信息&&教学管理类专项信息&&科研类专项信息",
        "是否分层级项目": "是",
    }
    附件配置 = [
        {
            "附件类型名称": f"ZDH_{faker_随机数生成(8)}",
            "表名": f"ZDH_表名_{faker_随机数生成(5)}",
            "支持格式": ".pdf",
            "大小限制": "3",
            "允许上传附件数": "5",
            "附件提示": "ZDH_附件提示",
            "说明": "ZDH_说明",
            "是否必填": random.choice(["是", "否"]),
        }
    ]
    项目类型配置 = build_项目类型配置(
        关联预算事项,
        项目类型前缀="ALL",
        extra_basic=extra,
        附件配置=附件配置,
    )
    项目类型创建(oc_page, 项目类型配置)
    return 项目类型配置["基本信息"]["项目类型"]


# 执行项目
def add_执行项目_项目类型(oc_page, 关联预算事项):
    项目类型配置 = build_项目类型配置(
        关联预算事项,
        项目类型前缀="(执行)",
        是否分层级="否",
        立项填报表单="预算明细",
    )
    项目类型创建(oc_page, 项目类型配置)
    return 项目类型配置["基本信息"]["项目类型"]


# 预算明细
def add_预算明细_项目类型(oc_page, 关联预算事项):
    项目类型配置 = build_项目类型配置(
        关联预算事项,
        项目类型前缀="(预算)",
        是否分层级="否",
        立项填报表单="预算明细",
    )
    项目类型创建(oc_page, 项目类型配置)
    return 项目类型配置["基本信息"]["项目类型"]


# 预算明细 and 执行计划
def add_预算明细and执行_项目类型(oc_page, 关联预算事项):
    项目类型配置 = build_项目类型配置(
        关联预算事项,
        项目类型前缀="(预算and执行计划)",
        是否分层级="否",
        立项填报表单="预算明细&&执行计划",
    )
    项目类型创建(oc_page, 项目类型配置)
    return 项目类型配置["基本信息"]["项目类型"]


def build_项目类型基本信息(
    关联预算事项code: str = "ZCSX-0125", 是否分层级项目: Literal["是", "否"] = "否"
) -> Dict[str, Any]:
    return {
        "项目类型编码": f"AUTO_{faker_随机数生成(8)}",
        "项目类型": f"自动化_项目类型_{faker_随机数生成(4)}",
        "归口部门": "一级部门&&测试机构(勿删)",
        "是否分层级项目": 是否分层级项目,
        "关联预算事项": 关联预算事项code,
        "是否启用": "是",
        "是否末级": "是",
    }


def build_需求类型基本信息(项目类型名称: str) -> Dict[str, Any]:
    return 需求类型基本信息Data(
        需求类型编码=f"ZDH{faker_随机数生成(8)}",
        需求类型=f"需求类型_{faker_随机数生成(4)}",
        归口部门="一级部门",
        责任人="一级部门A_负责人",
        需求申报表单="需求详情&&专项信息&&预算明细&&需求附件",
        是否启用="是",
        申报专项信息表单="建设工程类专项信息&&教学管理类专项信息&&科研类专项信息&&采购类专项信息",
        项目类型=项目类型名称,
        说明=f"自动化_{faker_text(20)}",
    ).as_dict()


def build_附件类型配置() -> Dict[str, Any]:
    return 附件类型配置Data(
        附件类型名称=f"ZDH_{faker_随机数生成(8)}",
        表名=f"ZDH_表名_{faker_随机数生成(5)}",
        支持格式=".pdf",
        大小限制="3",
        允许上传附件数="5",
        附件提示="ZDH_附件提示",
        说明="ZDH_说明",
        是否必填="否",
    ).as_dict()


def build_项目类型配置(
    关联预算事项,
    项目类型前缀: str,
    是否分层级: str = "否",
    立项填报表单: str = "",
    立项专项信息表单: str = "",
    extra_basic: dict = None,
    附件配置=None,
):
    """
    通用的项目类型配置构造器
    """
    base_info = {
        "项目类型编码": f"AUTO_{faker_随机数生成(8)}",
        "项目类型": f"自动化_项目类型{项目类型前缀}_{faker_随机数生成(4)}",
        "归口部门": "一级部门&&测试机构(勿删)",
        "是否分层级项目": 是否分层级,
        "关联预算事项": 关联预算事项.get("事项编码"),
        "是否启用": "是",
        "是否末级": "是",
    }
    if 立项填报表单:
        base_info["立项填报表单"] = 立项填报表单
    if 立项专项信息表单:
        base_info["立项专项信息表单"] = 立项专项信息表单
    if extra_basic:
        base_info.update(extra_basic)

    项目类型配置 = {
        "基本信息": base_info,
        "项目管理流程": [
            {
                "项目总预算下限金额（万元）": "10000",
                "项目总预算上限金额（万元）": "30000",
                "项目管理流程": "项目可行性研究报告&&项目概算",
            }
        ],
        "任务阶段": [{"任务阶段名称": f"第{i}阶段"} for i in range(1, 4)],
        "附件类型配置": 附件配置 if 附件配置 else [build_附件类型配置()],
    }
    return 项目类型配置


def 需求类型创建(oc_page, 需求类型数据: Dict[str, any]):
    with 测试步骤("切换到用户管理人员,并跳转需求配置页面"):
        oc_page.需求类型配置页.set_设置当前用户为("superAdmin")
        oc_page.需求类型配置页.navigate()
        oc_page.需求类型配置页.新增按钮.click()
        基本信息, 附件类型配置 = 需求类型数据["基本信息"], 需求类型数据["附件类型配置"]
    with 测试步骤("填写基本信息"):
        oc_page.需求类型配置页.fill_基本信息(基本信息)
        oc_page.需求类型配置页.fill_附件类型配置(附件类型配置)


def 绩效模板体系创建(oc_page, 绩效模板数据: Dict[str, any]):
    with 测试步骤("绩效管理员角色登录,跳转到绩效体系模板页面"):
        oc_page.绩效体系模板页.set_设置当前用户为("superAdmin")
        oc_page.绩效体系模板页.navigate()
        基本信息, 绩效目标信息 = 绩效模板数据["基本信息"], 绩效模板数据["绩效目标信息"]

    with 测试步骤("填写绩效模板基础信息"):
        oc_page.绩效体系模板页.新增按钮.click()
        oc_page.绩效体系模板页.fill_绩效模板基础信息(基本信息)

    with 测试步骤("页面新增绩效指标"):
        oc_page.绩效体系模板页.fill_页面指标(绩效目标信息)
        oc_page.绩效体系模板页.click_button("保存")
        oc_page.绩效体系模板页.confirm_弹框()


def 专项项目层级创建(oc_page, 项目类型名称: str, 专项项目层级数据: Dict[str, Any]):
    with 测试步骤("绩效管理员角色登录,跳转到绩效体系模板页面"):
        oc_page.专项项目层级配置页.set_设置当前用户为("superAdmin")
        oc_page.专项项目层级配置页.navigate()
        项目类型名称, 基本信息 = 项目类型名称, 专项项目层级数据["基本信息"]
    with 测试步骤("新增项目层级"):
        oc_page.专项项目层级配置页.search_填写搜索框(关键字=项目类型名称, placeholder="层级名称")
        操作定位 = oc_page.专项项目层级配置页.主表格.get_cell("操作", 0)
        操作定位.get_by_text("新增下级").click()
        oc_page.专项项目层级配置页.fill_新增专项层级(基本信息)


def 绩效指标创建(oc_page, 绩效指标: Dict[str, any]):
    with 测试步骤("用户登录并跳转绩效指标创建"):
        oc_page.绩效指标库页.set_设置当前用户为("superAdmin")
        oc_page.绩效指标库页.navigate()
        产出指标, 效益指标, 满意度指标 = (
            绩效指标["产出指标"],
            绩效指标["效益指标"],
            绩效指标["满意度指标"],
        )
    with 测试步骤("新建绩效指标"):
        指标list = [*产出指标, *效益指标, *满意度指标]
        for 指标 in 指标list:
            oc_page.绩效指标库页.新增按钮.click()
            oc_page.绩效指标库页.fill_新增绩效指标(指标)
        return 绩效指标


def 项目类型创建(oc_page, 项目类型创建数据: Dict[str, Any]):
    """
    使用外部传入字典，初始化基本项目类型
    """
    with 测试步骤("切换到用户项目管理人员并跳转项目管理页面"):
        oc_page.项目类型配置页.set_设置当前用户为("superAdmin")
        oc_page.项目类型配置页.navigate()
        基本信息 = 项目类型创建数据["基本信息"]
        项目管理流程 = 项目类型创建数据.get("项目管理流程")
        任务阶段 = 项目类型创建数据.get("任务阶段")
        附件类型配置 = 项目类型创建数据.get("附件类型配置")
        oc_page.项目类型配置页.add_添加子级()

    with 测试步骤("填写基本信息"):
        oc_page.项目类型配置页.fill_基本信息(基本信息)

    with 测试步骤("填写项目管理流程"):
        if 项目管理流程:
            oc_page.项目类型配置页.fill_项目管理流程(项目管理流程)

    with 测试步骤("填写项目任务阶段创建"):
        if 任务阶段:
            oc_page.项目类型配置页.fill_项目任务阶段创建(任务阶段)

    with 测试步骤("附件类型配置"):
        if 附件类型配置:
            oc_page.项目类型配置页.fill_附件类型配置(附件类型配置)
            oc_page.项目类型配置页.click_button("保存")
            oc_page.项目类型配置页.confirm_弹框()

    with 测试步骤("验证基本项目类型"):
        oc_page.项目类型配置页.search_填写搜索框(placeholder="项目类型编码/项目类型", 关键字=基本信息.get("项目类型"))
        table = oc_page.项目类型配置页.主表格
        table_info = table.get_row_dict(0)
        assert table_info, "创建基本类型失败"


def fill_项目立项(
    oc_page,
    oc_page_backup,
    基本信息,
    基本类型立项info,
    用户名,
    是否明确资金来源: str = "否",
):
    with 测试步骤("项目管理人员登录,跳转到立项申请"):
        oc_page.立项申请页.set_设置当前用户为(用户名)
        oc_page.立项申请页.navigate()

    with 测试步骤("填写项目立项信息"):
        oc_page.立项申请页.click_button("直接立项")
        oc_page.立项申请页.fill_立项基本信息(基本信息)
        项目周期 = 基本信息["项目周期"]
        项目立项方式 = 基本信息["立项方式"]
        oc_page.立项申请页.fill_项目立项tab信息(
            tab信息=基本类型立项info,
            项目立项方式=项目立项方式,
            year=项目周期,
            是否明确资金来源=是否明确资金来源,
        )
        oc_page.立项申请页.click_button("提交")
        oc_page.立项申请页.confirm_弹框()

    with 测试步骤("审批通过"):
        oc_page_backup.我的待办.set_设置当前用户为("testUser")
        oc_page_backup.我的待办.navigate()
        oc_page_backup.我的待办.审批同意("立项申请", 用户名)

    return 基本类型立项info["基本信息"].get("项目名称")


def 创建关联需求(oc_page, oc_page_backup, 基础配置, 用户名):
    with 测试步骤("初始化数据"):
        需求类型名称, 采购类型 = 基础配置["需求类型"], 基础配置["采购品目"]
        需求表单信息 = {
            "基本信息": 基本信息Data(需求类型=需求类型名称).as_dict(),
            "需求详情": 需求详情Data().as_dict(),
            "采购类专项信息": {
                "采购信息": 采购信息Data(采购类型="&&".join(采购类型.keys())).as_dict(),
                "采购明细": 采购类型["电子设备"][:3],
            },
            "建设工程类专项信息": 建设工程类专项信息Data().as_dict(),
            "教学管理类专项信息": 教学管理类专项信息Data().as_dict(),
            "预算明细": 预算明细Data().as_dict(),
            "科研项目类专项信息": 科研项目类专项信息Data().as_dict(),
        }
        logger.info(f"填写的需求申报表单信息:{需求表单信息}")
        基本信息 = 需求表单信息.get("基本信息")

    with 测试步骤("项目管理人员登录跳转到需求创建,并创建数据"):
        oc_page.需求申报页.set_设置当前用户为(用户名)
        oc_page.需求申报页.navigate()

    with 测试步骤("填写table详情信息"):
        oc_page.需求申报页.新增_按钮.click()
        oc_page.需求申报页.fill_整体填报(需求表单信息, oc_page.log_dir)
    with 测试步骤("提交验证"):
        oc_page.需求申报页.click_button("提交")
        oc_page.需求申报页.confirm_弹框()
        info = oc_page.需求申报页.search_需求(基本信息["需求名称"])
        assert compare_dicts(info, 基本信息, keys=["需求类型", "重要程度"]), "创建需求失败"
        assert info["审批状态"].strip() == "审批中"
    with 测试步骤("审批"):
        oc_page_backup.我的待办.set_设置当前用户为("testUser")
        oc_page_backup.我的待办.navigate()
        oc_page_backup.我的待办.审批同意("需求审批", 用户名)
    with 测试步骤("验证审批状态"):
        info = oc_page.需求申报页.search_需求(基本信息["需求名称"])
        assert info["审批状态"].strip() == "已审批"

    return 基本信息["需求名称"]


def delete_database_项目类型(项目类型code: str) -> int:
    """
    删除指定项目类型及其关联的特殊项目记录。
        c_id = f"select c_id from project.t_project_type_configuration where  c_project_type_code = '{项目类型code}'"
        delete_project_sql = f"delete from project.t_project_type_configuration where  c_project_type_code = '{项目类型code}'"
        delete_special_project_sql = f"delete from project.t_special_project_level where  c_project_id = '{c_id}'"

    :param 项目类型code: 项目类型编码
    :return: 成功删除的记录总数
    """
    # Step 1: 查询 c_id
    select_c_id_sql = """
        SELECT c_id 
        FROM project.t_project_type_configuration 
        WHERE c_project_type_code = :code
    """
    result = db_util.get_one(select_c_id_sql, {"code": 项目类型code})

    if not result:
        logger.warning(f"[警告] 未找到项目类型编码为 {项目类型code} 的记录")
        return 0

    c_id = result["c_id"]

    # Step 2: 删除关联表中的记录（先删除依赖）
    delete_special_sql = """
        DELETE FROM project.t_special_project_level 
        WHERE c_project_id = :cid
    """
    count_special = db_util.delete(delete_special_sql, {"cid": c_id})

    # Step 3: 删除主表中的项目类型记录
    delete_project_sql = """
        DELETE FROM project.t_project_type_configuration 
        WHERE c_project_type_code = :code
    """
    count_project = db_util.delete(delete_project_sql, {"code": 项目类型code})

    # Step 4: 返回删除记录总数
    logger.warning(f"[成功] 删除记录：项目类型 {count_project} 条，特殊项目级别 {count_special} 条")
    return count_special + count_project


def delete_config(
    page,
    search_placeholder: str,
    code: str,
    table_name: str,
    db_fallback: callable = None,
) -> bool:
    """
    通用删除逻辑
    :param page: 页面对象（如 oc_page.绩效指标库页）
    :param search_placeholder: 搜索框 placeholder
    :param code: 待删除的编码
    :param table_name: 日志打印用的表名
    :param db_fallback: UI 删除失败时的数据库兜底删除函数
    :return: True 表示删除成功，False 表示失败
    """
    page.search_填写搜索框(placeholder=search_placeholder, 关键字=code)
    table = page.主表格
    try:
        cell_delete = table.get_cell("操作", 0)
        delete_btn = cell_delete.get_by_text("删除").filter(visible=True)
        if delete_btn.count() == 0:
            logger.warning(f"{table_name} 未找到可删除的记录: {code}")
            return False

        delete_btn.click()
        page.confirm_弹框()
        error_message = page.wait_for_error_message()

        if error_message:
            logger.warning(f"{table_name} 删除失败 {code}: {error_message}")
            if db_fallback:
                try:
                    db_fallback(code)
                    logger.info(f"{table_name} 数据库兜底删除成功: {code}")
                    return True
                except Exception as e:
                    logger.error(f"{table_name} 数据库兜底删除失败 {code}: {e}")
            return False

        logger.info(f"{table_name} 删除成功: {code}")
        return True

    except Exception as e:
        logger.error(f"{table_name} 删除异常 {code}: {e}")
        return False


def 项目立项_临时立项_项目论证(
    oc_page,
    oc_page_backup,
    基础配置,
    用户名,
    是否明确资金来源: Literal["是", "否"] = "否",
):
    """
    创建立项论证通过项目
    立项论证=否  政府投资项目=否
    """
    with 测试步骤("项目立项通过"):
        预算明细and执行_项目类型 = 基础配置["项目类型"]["预算明细and执行_项目类型"]
        项目立项info = {
            "基本信息": 项目立项基本信息Data(
                项目名称=f"自动化创建_备选库管理_{faker_随机数生成(3)}",
                项目类型=预算明细and执行_项目类型,
                实施部门="一级部门",
                经费类型="创收经费",
                项目层级="【全部】",
                立项方式="临时立项",
                是否政府投资类="否",
                项目负责人="一级部门A_负责人",
            ).as_dict(),
            "立项信息": 立项信息Data(是否立项论证="是").as_dict(),
            "预算明细": {
                "预算指标编码": ["YSBM0238", "YSBM0237", "YSBM0236"],
                "资金来源": {"资金来源": "财政&&非财政&&科研&&人力"},
                "年度用款计划": {
                    "第一季度用款计划": str(random.randint(1, 10000)),
                    "第二季度用款计划": str(random.randint(1, 10000)),
                    "第三季度用款计划": str(random.randint(1, 10000)),
                    "第四季度用款计划": str(random.randint(1, 10000)),
                },
            },
            "执行任务": {"项目计划分解": [项目计划分解Data(任务阶段=f"第{i + 1}任务阶段").as_dict() for i in range(3)]},
        }

        基本信息 = 项目立项info["基本信息"]
        logger.info(f"备选库管理_项目立项:{项目立项info}")
        备选库管理_项目立项 = fill_项目立项(
            oc_page,
            oc_page_backup,
            基本信息,
            项目立项info,
            用户名,
            是否明确资金来源=是否明确资金来源,
        )
    with 测试步骤("项目论证通过"):
        立项论证info = {
            "立项论证信息": 立项论证信息().as_dict(),
            "论证项目明细": [论证项目明细(项目编码=备选库管理_项目立项, 立项论证结果="通过").as_dict()],
        }
        print(f"项目论证信息:{立项论证info}")
        fill_项目论证(oc_page, oc_page_backup, 立项论证info, 用户名)
        return 备选库管理_项目立项


def fill_项目论证(oc_page, oc_page_backup, 立项论证info, 用户名):
    with 测试步骤("项目管理人员登录,切换到立项论证页面"):
        oc_page.立项论证页.set_设置当前用户为(用户名)
        oc_page.立项论证页.navigate()
    with 测试步骤("填写立项论证并提交"):
        oc_page.立项论证页.click_button("新增")
        oc_page.立项论证页.fill_立项论证(立项论证info)
        oc_page.立项论证页.click_button("提交")
        oc_page.立项论证页.confirm_弹框()
        info = oc_page.立项论证页.search_项目论证(用户名)
        assert "审批中" in info.get("审批状态")
    with 测试步骤("审批通过"):
        oc_page_backup.我的待办.set_设置当前用户为("testUser")
        oc_page_backup.我的待办.navigate()
        oc_page_backup.我的待办.审批同意("立项论证流程", 用户名)
        info = oc_page.立项论证页.search_项目论证(用户名)
        assert "已审批" in info.get("审批状态")
