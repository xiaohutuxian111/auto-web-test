from src.test_cases import *


class 项目立项数据生成:

    @staticmethod
    def 创建项目基本信息(项目类型=None, 关联需求=None) -> Dict[str, Any]:
        基本信息 = 项目立项基本信息Data(
            项目类型=项目类型,
            实施部门="一级部门",
            经费类型="创收经费",
            项目层级="【全部】",
            是否政府投资类="是",
            项目前期文档="项目建议书&&项目可行性报告&&项目概算",
            项目负责人="一级部门A_负责人",
        ).格式化()

        if 关联需求:
            基本信息["关联需求"] = 关联需求
            基本信息["实施部门"] = "一级部门"
            基本信息["项目负责人"] = "一级部门A_负责人"
        logger.info(f"创建项目基本信息:{基本信息}")
        return 基本信息

    @staticmethod
    def 创建立项信息() -> Dict[str, str]:

        res = {
            "项目立项依据": f"项目立项依据_{faker_text(20)}",
            "项目概况": f"项目概况_{faker_text(20)}",
            "是否立项论证": "是",
        }
        立项信息Data()
        return res

    @staticmethod
    def 创建采购专项信息() -> Tuple[Dict[str, str], List[Dict[str, str]]]:

        采购信息 = {
            "采购类别": "自动化品目父级&&货物类&&采购品目新增123&&演示设备&&服务类&&工程类&&电子设备&&通用设备",
            "采购组织方式": random.choice(["非政府集中采购", "政府集中采购", "不限"]),
            "是否一次性采购": random.choice(["是", "否"]),
        }

        购置明细导入信息 = []
        导入采购物品信息 = [
            {"项采购品目名称": "工程类\构筑物施工\桥梁工程施工\铁路桥梁工程施工", "采购品目编码": "B020701"},
            {"项采购品目名称": "工程类\构筑物施工\桥梁工程施工\公路桥梁工程施工", "采购品目编码": "B020702"},
            {"项采购品目名称": "工程类\构筑物施工\桥梁工程施工\城市道路桥梁工程施工", "采购品目编码": "B020703"},
        ]

        for ele in 导入采购物品信息:
            info = {
                "*采购品目名称": ele.get("项采购品目名称"),
                "采购品目编码": ele.get("采购品目编码"),
                "规格型号": faker_产品型号(),
                "计量单位": faker_单位(),
                "*采购数量": str(random.randint(0, 1000)),
                "*预算单价（元）": str(random.randint(0, 1000)),
                "备注": faker_text(50),
            }
            购置明细导入信息.append(info)

        logger.info(f"创建采购专项信息:{采购信息},{购置明细导入信息}")
        return 采购信息, 购置明细导入信息

    @staticmethod
    def 创建建设项目专项信息() -> Tuple[Dict[str, str], List[Dict[str, str]]]:

        工程建设信息 = {
            "计划开工时间": 返回当前时间xxxx_xx_xx加N天(-30),
            "计划完工时间": 返回当前时间xxxx_xx_xx加N天(30),
            "项目建设必要性": faker_text(50),
            "项目建设可行性": faker_text(50),
            "现场条件与措施": faker_text(50),
        }

        施工区域及位置 = [{"区域": faker_城市(), "具体位置": faker_地址()} for _ in range(3)]

        logger.info(f"创建建设项目专项信息:{工程建设信息},{施工区域及位置}")
        return 工程建设信息, 施工区域及位置

    @staticmethod
    def 创建科研项目专项信息() -> Tuple[Dict[str, str], Dict[str, str], List[Dict[str, str]]]:
        科研项目信息 = {
            "课题类型": random.choice(["纵向课题", "横向课题"]),
            "项目来源": random.choice(["其他来源", "科技部(厅)其他项目", "国家自然科学基金项目"]),
            "研究类型": random.choice(list(InvestigateType)).value,
            "预计项目周期": "-30,30",
        }

        项目负责人信息 = {
            "负责人": "审批领导",
            "职称": random.choice(list(Title)).value,
            "学历": random.choice(list(Qualifications)).value,
            "学位": random.choice(list(Degree)).value,
            "联系电话": faker_移动电话(),
            "邮箱": faker_邮箱(),
        }

        项目组成员信息 = [
            {
                "姓名": "审批领导",
                "所属部门": "福建省妇幼保健院",
                "性别": random.choice(["男", "女"]),
                "出生日期": 返回当前时间xxxx_xx_xx加N天(-3000),
                "职称": random.choice(list(Title)).value,
                "联系电话": faker_移动电话(),
                "邮箱": faker_邮箱(),
                "学历": random.choice(list(Qualifications)).value,
                "学位": random.choice(list(Degree)).value,
                "分工说明": faker_text(50),
            }
        ]

        logger.info(f"创建科研项目专项信息:{科研项目信息},{项目负责人信息},{项目组成员信息}")
        return 科研项目信息, 项目负责人信息, 项目组成员信息

    @staticmethod
    def 创建教学管理项目专项信息() -> Tuple[Dict[str, str], List[Dict[str, str]], Dict[str, str]]:

        主导人信息 = {
            "主导人": "审批领导",
            "性别": random.choice(["女", "男"]),
            "出生日期": 返回当前时间xxxx_xx_xx加N天(-4000),
            "专业技术职务": faker_text(10),
            "职位": faker_职业(),
            "邮箱": faker_邮箱(),
            "最终学历": random.choice(list(Qualifications)).value,
            "学位": random.choice(list(Degree)).value,
            "教学技术与专长": faker_text(20),
            "成果与业绩": faker_text(50),
        }

        项目组成员信息 = [
            {
                "姓名": "审批领导",
                "所属部门": "福建省妇幼保健院",
                "性别": random.choice(["男", "女"]),
                "出生日期": 返回当前时间xxxx_xx_xx加N天(-4000),
                "职称": random.choice(list(Title)).value,
                "联系电话": faker_移动电话(),
                "邮箱": faker_邮箱(),
                "学历": random.choice(list(Qualifications)).value,
                "学位": random.choice(list(Degree)).value,
                "分工说明": faker_text(50),
            }
        ]

        立项依据和目标 = {"课题类别": random.choice(["一般", "重要", "重大"]), "立项依据和目标": faker_text(100)}

        logger.info(f"创建教学管理项目专项信息:{主导人信息},{项目组成员信息},{立项依据和目标}")
        return 主导人信息, 项目组成员信息, 立项依据和目标

    @staticmethod
    def 创建项目专项信息():
        主导人信息 = {
            "主导人": "审批领导",
            "性别": random.choice(["女", "男"]),
            "出生日期": 返回当前时间xxxx_xx_xx加N天(-4000),
            "专业技术职务": faker_text(10),
            "职位": faker_职业(),
            "邮箱": faker_邮箱(),
            "最终学历": random.choice(list(Qualifications)).value,
            "学位": random.choice(list(Degree)).value,
            "教学技术与专长": faker_text(20),
            "成果与业绩": faker_text(50),
        }

        项目组成员信息 = [
            {
                "姓名": "审批领导",
                "性别": random.choice(["男", "女"]),
                "出生日期": 返回当前时间xxxx_xx_xx加N天(-4000),
                "职务": random.choice(list(Title)).value,
                "专业技术职称": faker_职业(),
                "项目分工": faker_职业(),
                "备注": faker_text(50),
            }
        ]

        立项依据和目标 = {"课题类别": random.choice(["一般", "重要", "重大"]), "立项依据和目标": faker_text(100)}

        logger.info(f"创建项目专项信息:{主导人信息},{项目组成员信息},{立项依据和目标}")
        return 主导人信息, 项目组成员信息, 立项依据和目标

    @staticmethod
    def 创建绩效目标信息(绩效指标: Dict[str, List[Dict[str, str]]]) -> List[str]:
        """
        指标必须包含产出和效益指标
        """
        产出指标, 效益指标, 满意度指标 = 绩效指标["产出指标"], 绩效指标["效益指标"], 绩效指标["满意度指标"]
        产出指标 = [info["三级指标"] for info in 产出指标[:3]]
        效益指标 = [info["三级指标"] for info in 效益指标[:3]]
        满意度指标 = [info["三级指标"] for info in 满意度指标[:3]]

        指标 = [*产出指标, *效益指标, *满意度指标]
        logger.info(f"创建绩效目标信息:{指标}")
        return 指标

    @staticmethod
    def 创建预算明细信息(years: int) -> Tuple[List[str], Dict[str, str], Dict[str, str]]:

        指标编码 = ["YSBM0055", "YSBM0043", "YSBM0044"]
        资金来源 = {"资金来源": "财政&&非财政&&科研&&人力"}
        年度用款计划 = {
            "第一季度用款计划": str(random.randint(1, 10000)),
            "第二季度用款计划": str(random.randint(1, 10000)),
            "第三季度用款计划": str(random.randint(1, 10000)),
            "第四季度用款计划": str(random.randint(1, 10000)),
        }
        logger.info(f"创建预算明细信息:{指标编码},{资金来源},{年度用款计划}")
        return 指标编码, 资金来源, 年度用款计划

    @staticmethod
    def 创建验收标准信息() -> Tuple[Dict[str, str], List[Dict[str, str]]]:

        验收标准说明 = {"验收标准说明": faker_text(50)}
        验收信息 = [{"验收项": faker_text(50), "验收标准": faker_text(100)} for _ in range(3)]
        logger.info("创建验收标准信息:{验收标准说明},{验收信息}")
        return 验收标准说明, 验收信息

    @staticmethod
    def 创建成果物信息() -> List[Dict[str, str]]:
        res = [
            {
                "成果物名称": faker_text(20),
                "成果物类型": random.choice(list(DeliverableType)).value,
                "负责人": "审批领导",
                "说明": faker_text(50),
            }
            for _ in range(3)
        ]
        logger.info(f"创建成果物信息:{res}")
        return res


def fill_项目立项审批(oc_page, oc_page_backup, 基础配置, 项目基本信息: Dict[str, Any], 是否需求立项: bool = False):
    """
    填写项目立项表单的公共方法
    """
    助手 = 项目立项数据生成
    years = int(项目基本信息.get("项目周期"))

    # 填写立项信息
    with 测试步骤("填写立项信息"):
        oc_page.立项申请页.立项信息_tab.click()
        立项信息 = 助手.创建立项信息()
        oc_page.立项申请页.fill_立项信息(立项信息)

    # 填写采购专项信息
    with 测试步骤("填写采购专项信息"):
        oc_page.立项申请页.采购项目专项_tab.click()
        采购信息, 购置明细导入信息 = 助手.创建采购专项信息()
        oc_page.立项申请页.fill_采购项目专项(
            采购信息=采购信息, temp_path=oc_page.log_dir, 导入采购物品信息=购置明细导入信息
        )

    # 填写建设项目专项信息
    with 测试步骤("填写建设项目专项信息"):
        oc_page.立项申请页.建设项目专项信息_tab.click()
        工程建设信息, 施工区域及位置 = 助手.创建建设项目专项信息()
        oc_page.立项申请页.fill_建设项目专信息(工程建设信息, 施工区域及位置)

    # 填写科研项目专项信息
    with 测试步骤("填写科研项目专项信息"):
        oc_page.立项申请页.科研项目专项信息_tab.click()
        科研项目信息, 项目负责人信息, 项目组成员信息 = 助手.创建科研项目专项信息()
        oc_page.立项申请页.fill_科研项目专项信息(科研项目信息, 项目负责人信息, 项目组成员信息)

    # 填写教学管理项目专项信息
    with 测试步骤("填写教学管理项目专项信息"):
        oc_page.立项申请页.教学管理项目专项信息_tab.click()
        主导人信息, 项目组成员信息, 立项依据和目标 = 助手.创建教学管理项目专项信息()
        oc_page.立项申请页.fill_填写教学管理项目专项(主导人信息, 项目组成员信息, 立项依据和目标)

    # 填写项目专项信息
    with 测试步骤("项目专项信息"):
        oc_page.立项申请页.项目专项信息_tab.click()
        主导人信息, 项目组成员信息, 立项依据和目标 = 助手.创建项目专项信息()
        oc_page.立项申请页.fill_项目专项信息(主导人信息, 项目组成员信息, 立项依据和目标)

    # 填写绩效目标
    with 测试步骤("填写绩效目标"):
        oc_page.立项申请页.绩效目标_tab.click()
        绩效指标 = 基础配置["绩效指标库"]
        指标库编码 = 助手.创建绩效目标信息(绩效指标)
        oc_page.立项申请页.fill_绩效目标(指标库编码, years)

    # 填写预算明细
    with 测试步骤("填写预算明细"):
        oc_page.立项申请页.预算明细_tab.click()
        指标编码, 资金来源, 年度用款计划 = 助手.创建预算明细信息(years)
        oc_page.立项申请页.fill_预算明细(
            立项方式=项目基本信息.get("立项方式"),
            预算指标编码=指标编码,
            资金来源=资金来源,
            years=years,
            年度用款计划=年度用款计划,
            是否需求立项=是否需求立项,
        )

    # 填写执行任务
    with 测试步骤("填写执行任务"):
        oc_page.立项申请页.执行任务_tab.click()
        oc_page.立项申请页.fill_执行任务()

    # 填写验收标准
    with 测试步骤("填写验收标准"):
        oc_page.立项申请页.验收标准_tab.click()
        验收标准说明, 验收信息 = 助手.创建验收标准信息()
        oc_page.立项申请页.fill_快捷操作_填写表单(**验收标准说明)
        oc_page.立项申请页.fill_验收标准(验收信息=验收信息)

    # 填写成果物
    with 测试步骤("成果物"):
        oc_page.立项申请页.成果物_tab.click()
        成果物 = 助手.创建成果物信息()
        oc_page.立项申请页.fill_成果物(成果物)

    # 填写附件材料
    with 测试步骤("附件材料"):
        oc_page.立项申请页.附件材料_tab.click()
        oc_page.立项申请页.fill_附件材料(temp_path=oc_page.log_dir)

    with 测试步骤("验证提交结果"):
        oc_page.立项申请页.click_button("提交")
        oc_page.立项申请页.confirm_弹框()
        error_message = oc_page.立项申请页.wait_for_error_message()
        if error_message:
            logger.warning(f"立项提交报错信息: {error_message}")

        验证项目立项结果(oc_page, 项目基本信息, "审批中")

    with 测试步骤("审批通过"):
        oc_page.切换页面(oc_page_backup)

        oc_page_backup.我的待办.set_设置当前用户为("testUser")
        oc_page_backup.我的待办.navigate()
        oc_page_backup.我的待办.审批同意("立项申请")

    with 测试步骤("验证审批状态"):
        oc_page_backup.切换页面(oc_page)
        验证项目立项结果(oc_page, 项目基本信息, "已审批")


def 验证项目立项结果(cur_page, 项目基本信息: Dict[str, Any], 期望状态: str = None):
    """
    验证项目立项结果的公共方法
    """
    cur_page.立项申请页.search_填写搜索框(placeholder="关键词搜索", 关键字=项目基本信息.get("项目名称"))
    项目信息 = cur_page.立项申请页.主表格.get_row_dict(0)

    项目基本信息 = get_dict_info(项目基本信息)
    assert compare_dicts(项目基本信息, 项目信息, keys=["项目名称", "项目类型"]), "项目基本信息验证失败"

    if 期望状态:
        assert 期望状态 in 项目信息.get("审批状态"), f"期望状态: {期望状态}, 实际状态: {项目信息.get('审批状态')}"
